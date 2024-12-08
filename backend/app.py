from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import MovieRecommendationAgent
import requests
import os

app = Flask(__name__)

# Allow CORS from all origins
CORS(app, resources={r"/*": {"origins": "*"}})

TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Ensure your TMDB_API_KEY is in .env

@app.route('/genres', methods=['GET'])
def genres():
    """
    API endpoint for fetching genres from TMDB.
    """
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json()["genres"]), 200
    else:
        return jsonify({"error": "Failed to fetch genres"}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    API endpoint for generating movie recommendations.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input. Please provide genre_id, actor_name, and release_year."}), 400

    try:
        agent = MovieRecommendationAgent(data)
        result = agent.run()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
