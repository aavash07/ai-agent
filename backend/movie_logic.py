import openai
import requests
from dotenv import load_dotenv
import os

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

def fetch_genres():
    """
    Fetches available genres from TMDB API.
    """
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"]: genre["id"] for genre in genres}
    return {}

def fetch_movies(genre_id=None, actor_name=None, release_year=None):
    """
    Fetches movies from TMDB API based on filters.
    """
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False,
        "include_video": False,
        "page": 1,
        "with_genres": genre_id,
        "primary_release_year": release_year,
    }

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
    return []

def generate_ai_recommendations(user_input, movie_list):
    """
    Uses Azure OpenAI GPT to generate reasoning-based recommendations.
    """
    movie_titles = [movie["title"] for movie in movie_list]
    prompt = f"""
    Based on the user's input: {user_input},
    and the following movies: {movie_titles},
    suggest other similar movies and explain why they might be a good fit.
    """
    try:
        # Ensure both "messages" and "engine" are passed
        response = openai.chat.completions.create(
            model=AZURE_OPENAI_MODEL,  # Azure-specific field for the deployed model
            messages=[
                {"role": "system", "content": "You are a helpful movie recommendation assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        # Access the response correctly as a Pydantic model
        choices = response.choices  # This is a list of choices
        if choices and len(choices) > 0:
            reply = choices[0].message.content.strip()
            return reply
        return "No response received from the AI model."
    except openai.OpenAIError as e:
        return f"Error generating AI recommendations: {e}"

