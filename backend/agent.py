import openai
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Environment Variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Set up OpenAI configuration for Azure
openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = AZURE_OPENAI_API_VERSION


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
        Generate recommendations using Azure OpenAI GPT.
        """
        movie_titles = [movie["title"] for movie in movie_list]
        prompt = f"""
        Based on the user's input: {self.user_input},
        and the following movies: {movie_titles},
        suggest other similar movies and explain why they might be a good fit.
        """
        try:
            response = openai.chat.completions.create(
                model=AZURE_OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful movie recommendation assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            choices = response.choices
            if choices and len(choices) > 0:
                return choices[0].message.content.strip()
            return {"error": "No response received from the AI model."}
        except openai.OpenAIError as e:
            return {"error": str(e)}

    def record_progress(self, action, result):
        """
        Record the progress in a log.
        """
        log_entry = {
            "timestamp": datetime.now(),
            "action": action,
            "result": result,
        }
        self.progress_log.append(log_entry)

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
        while not self.done:
            actions = self.plan_actions()

            for action in actions:
                print(f"Executing action: {action['description']}")
                result = self.execute_action(action)
                self.record_progress(action, result)

                # Check if the action failed
                if isinstance(result, dict) and "error" in result:
                    print(f"Error during action: {result['error']}")
                    break

            # Check if task is completed
            self.done = all("error" not in log["result"] for log in self.progress_log)

        return {
            "recommendations": self.progress_log[-1]["result"] if self.done else "Task incomplete.",
            "progress_log": self.progress_log,
        }
