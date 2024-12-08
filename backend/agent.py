import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import re
from groq import Groq

# Load environment variables
load_dotenv()

# Environment Variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class MovieRecommendationAgent:
    def __init__(self, user_input):
        self.user_input = user_input
        self.progress_log = []
        self.done = False

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

    def generate_ai_recommendations(self, movie_list):
        """
        Generate multiple recommendations using the Groq AI API and refetch movie details.
        """
        movie_titles = [movie["title"] for movie in movie_list]
        genre_name = self.user_input.get("genre_name", "not specified")
        actor_name = self.user_input.get("actor_name", "not specified")
        release_year = self.user_input.get("release_year", "not specified")

        prompt = f"""
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
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful movie recommendation assistant."},
                    {"role": "user", "content": prompt},
                ],
                model="llama3-8b-8192",
            )
            recommendation_text = chat_completion.choices[0].message.content.strip()

            # Extract movie titles from the AI response
            recommended_titles = self.extract_titles_from_text(recommendation_text)

            # Refetch movies for the recommended titles
            detailed_movies = self.refetch_movies_by_titles(recommended_titles)

            return {
                "recommendation_text": recommendation_text,
                "recommended_movies": detailed_movies,
            }
        except Exception as e:
            return {"error": f"Failed to generate recommendations: {str(e)}"}

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
        titles = re.findall(r"\*\*(.*?)\*\*", text)
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
