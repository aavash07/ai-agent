import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import re
from groq import Groq
import json

# Load environment variables
load_dotenv()

# Environment Variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Groq client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class MovieRecommendationAgent:
    def __init__(self, user_input=None, query=None):
        self.user_input = user_input
        self.query = query
        self.progress_log = []
        self.done = False
        # Initialize the Groq client here
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def plan_actions(self):
        """
        Plan a sequence of actions for the agent.
        """
        return [
            {"type": "fetch_genres", "description": "Fetch available genres from TMDB."},
            {"type": "fetch_movies", "description": "Fetch movies based on user input."},
            {"type": "generate_recommendations", "description": "Generate AI-powered recommendations."},
        ]

    def fetch_genres(self):
        """
        Fetch available genres from TMDB API.
        """
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            genres = response.json().get("genres", [])
            return {genre["name"]: genre["id"] for genre in genres}
        return {"error": "Failed to fetch genres"}

    def fetch_movies(self):
        """
        Fetch movies from TMDB API based on user preferences.
        """
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "include_adult": False,
            "include_video": False,
            "page": 1,
            "with_genres": self.user_input.get("genre_id"),
            "primary_release_year": self.user_input.get("release_year"),
        }

        actor_name = self.user_input.get("actor_name")
        if actor_name:
            search_actor_url = f"https://api.themoviedb.org/3/search/person"
            search_params = {"api_key": TMDB_API_KEY, "query": actor_name}
            actor_response = requests.get(search_actor_url, params=search_params)
            if actor_response.status_code == 200:
                results = actor_response.json().get("results", [])
                if results:
                    params["with_cast"] = results[0]["id"]

        url = f"https://api.themoviedb.org/3/discover/movie"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("results", [])
        return {"error": "Failed to fetch movies"}

    def extract_json_from_response(self, response):
        """
        Extract the JSON object from the LLM's response text.
        """
        try:
            start_index = response.index("{")
            end_index = response.rindex("}") + 1
            json_str = response[start_index:end_index]
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to extract JSON from response: {str(e)}")

    def parse_query_to_fields(self):
        """
        Parse the user's natural language query into structured fields using the LLM.
        Implements a feedback loop to validate and refine parsed fields from the query.
        """
        prompt = f"""
        User Query: "{self.query}"
        Extract:
        - Genre (if mentioned)
        - Actor (if mentioned)
        - Release Year (if mentioned)

        Provide the output as a JSON object ONLY. Example:
        {{
            "genre_name": "Action",
            "actor_name": "Keanu Reeves",
            "release_year": "2021"
        }}
        """
        feedback_prompt_template = """
        The extracted fields from the user query are:
        {parsed_fields}

        Based on the user's query: "{user_query}",
        Are these fields accurate and aligned with the user's intent? If not, suggest corrections.
        Provide the response as JSON ONLY with two keys:
        - "is_valid" (true/false)
        - "suggestions" (if invalid, provide the corrected fields)
        """
        MAX_ATTEMPTS = 3  # Limit retries to avoid infinite loop
        last_valid_fields = None  # Track last valid parsed fields for fallback

        try:
            for attempt in range(MAX_ATTEMPTS):
                # Generate parsed fields from AI
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert query parser."},
                        {"role": "user", "content": prompt},
                    ],
                    model="llama3-8b-8192",
                )
                llm_response = chat_completion.choices[0].message.content.strip()
                print(f"Raw LLM response: {llm_response}")  # Debugging: Check raw response

                # Extract and parse JSON from response
                parsed_fields = self.extract_json_from_response(llm_response)
                print(f"Parsed fields: {parsed_fields}")  # Debugging: Check parsed fields

                # Validate parsed fields using feedback
                feedback_prompt = feedback_prompt_template.format(
                    parsed_fields=json.dumps(parsed_fields, indent=2),
                    user_query=self.query,
                )
                feedback_response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a feedback validator for parsed query fields."},
                        {"role": "user", "content": feedback_prompt},
                    ],
                    model="llama3-8b-8192",
                )
                feedback = json.loads(feedback_response.choices[0].message.content.strip())

                if feedback.get("is_valid", False):
                    self.user_input = parsed_fields
                    # Ensure the dictionary has all necessary keys
                    self.user_input.setdefault("genre_name", None)
                    self.user_input.setdefault("actor_name", None)
                    self.user_input.setdefault("release_year", None)
                    print("Query parsed and validated successfully.")  # Debugging
                    return  # Exit successfully if validation passes
                else:
                    print(f"Feedback suggested corrections: {feedback.get('suggestions')}")  # Debugging
                    last_valid_fields = parsed_fields  # Store current fields as fallback
                    parsed_fields = feedback.get("suggestions")  # Use suggested corrections for the next attempt

        except Exception as e:
            print(f"Error in parsing query: {str(e)}")  # Debugging
            raise ValueError(f"Failed to process query: {str(e)}")

        # If retries exhausted, fallback to last valid fields or raise an error
        if last_valid_fields:
            print("Returning last valid parsed fields after failed refinements.")
            self.user_input = last_valid_fields
            return
        raise ValueError("Failed to parse query after multiple attempts.")


    def generate_ai_recommendations(self, movie_list):
        """
        Generate multiple recommendations using the Groq AI API and refetch movie details.
        Implements a feedback loop to refine recommendations.
        """
        movie_titles = [movie["title"] for movie in movie_list]
        genre_name = self.user_input.get("genre_name", "not specified")
        actor_name = self.user_input.get("actor_name", "not specified")
        release_year = self.user_input.get("release_year", "not specified")

        base_prompt = f"""
        Based on the user's input:
        - Genre: {genre_name}
        - Actor: {actor_name}
        - Release Year: {release_year}

        Please suggest three movie recommendations that align with these preferences. For each recommendation, include:
        1. The movie title.
        2. A short description of the movie that highlights its appeal.
        3. Why this movie might interest the user based on their input.

        Make the descriptions engaging and conversational, avoiding overly technical language. Format the output as a numbered list.
        """
        feedback_prompt_template = """
        The recommendations generated are:
        {recommendation_text}

        Based on the user's input: Genre: {genre}, Actor: {actor}, Year: {year},
        Are these recommendations accurate and aligned with the input? If not, suggest corrections.
        Provide the response as JSON ONLY with two keys:
        - "is_valid" (true/false)
        - "suggestions" (if invalid, provide corrected recommendations)
        """

        MAX_ATTEMPTS = 3  # Limit retries to avoid infinite loop
        last_valid_recommendations = None  # Track last valid recommendations for fallback

        for attempt in range(MAX_ATTEMPTS):
            try:
                # Generate recommendations from AI
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful movie recommendation assistant."},
                        {"role": "user", "content": base_prompt},
                    ],
                    model="llama3-8b-8192",
                )
                recommendation_text = chat_completion.choices[0].message.content.strip()

                # Extract movie titles from the AI response
                recommended_titles = self.extract_titles_from_text(recommendation_text)

                # Refetch movies for the recommended titles
                detailed_movies = self.refetch_movies_by_titles(recommended_titles)

                # Validate recommendations using feedback
                feedback_prompt = feedback_prompt_template.format(
                    recommendation_text=recommendation_text,
                    genre=genre_name,
                    actor=actor_name,
                    year=release_year,
                )
                feedback_response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a feedback validator for recommendations."},
                        {"role": "user", "content": feedback_prompt},
                    ],
                    model="llama3-8b-8192",
                )
                feedback = json.loads(feedback_response.choices[0].message.content.strip())

                if feedback.get("is_valid", False):
                    # Valid recommendations confirmed
                    return {
                        "recommendation_text": recommendation_text,
                        "recommended_movies": detailed_movies,
                    }
                else:
                    print(f"Feedback suggested corrections: {feedback.get('suggestions')}")  # Debugging
                    base_prompt = f"""
                    User feedback indicated issues with the recommendations.
                    Based on the feedback: {feedback.get('suggestions')}, refine the recommendations.
                    """  # Update the base prompt with corrections from feedback

                    # Store the last valid recommendations for fallback
                    last_valid_recommendations = {
                        "recommendation_text": recommendation_text,
                        "recommended_movies": detailed_movies,
                    }

            except Exception as e:
                print(f"Error in generating recommendations: {str(e)}")
                return {"error": f"Failed to generate valid recommendations after multiple attempts."}

        # If retries exhausted, return the last valid recommendations or an error
        if last_valid_recommendations:
            print("Returning last valid recommendations after failed refinements.")
            return last_valid_recommendations
        return {"error": "Failed to generate valid recommendations after multiple attempts."}



    def refetch_movies_by_titles(self, titles):
        """
        Refetch detailed movie data from TMDB for the given titles.
        """
        fetched_movies = []
        for title in titles:
            try:
                search_url = f"https://api.themoviedb.org/3/search/movie"
                search_params = {
                    "api_key": TMDB_API_KEY,
                    "query": title,
                    "language": "en-US",
                }
                response = requests.get(search_url, params=search_params)
                response.raise_for_status()
                results = response.json().get("results", [])
                if results:
                    fetched_movies.append(results[0])
            except requests.RequestException as e:
                print(f"Failed to refetch movie for title '{title}': {str(e)}")
        return fetched_movies

    def extract_titles_from_text(self, text):
        """
        Extract movie titles from the AI-generated recommendation text.
        """
        titles = re.findall(r'\*\*(.*?)\*\*', text)
        return titles

    def execute_action(self, action):
        """
        Execute an action based on its type.
        """
        if action["type"] == "fetch_genres":
            return self.fetch_genres()
        elif action["type"] == "fetch_movies":
            return self.fetch_movies()
        elif action["type"] == "generate_recommendations":
            return self.generate_ai_recommendations(self.progress_log[-1]["result"])
        return {"error": "Unknown action type"}

    def run(self):
        """
        Execute the AI agent workflow with dynamic looping.
        """
        if self.query:
            self.parse_query_to_fields()

        movie_data = []
        recommendations = {}

        while not self.done:
            actions = self.plan_actions()

            for action in actions:
                print(f"Executing action: {action['description']}")
                result = self.execute_action(action)
                self.progress_log.append({"action": action, "result": result})

                if action["type"] == "fetch_movies":
                    movie_data = result
                elif action["type"] == "generate_recommendations":
                    recommendations = result

                if isinstance(result, dict) and "error" in result:
                    print(f"Error during action: {result['error']}")
                    break

            self.done = all("error" not in log["result"] for log in self.progress_log)

        return {
            "recommendations": recommendations.get("recommendation_text", ""),
            "movies": recommendations.get("recommended_movies", []),
            "progress_log": self.progress_log,
        }
