from flask import Flask, request, jsonify
from movie_logic import fetch_genres, fetch_movies, generate_ai_recommendations

app = Flask(__name__)

@app.route('/genres', methods=['GET'])
def get_genres():
    """
    Endpoint to fetch available genres.
    """
    genres = fetch_genres()
    return jsonify(genres)

@app.route('/movies', methods=['POST'])
def get_movies():
    """
    Endpoint to fetch movies based on user input.
    """
    data = request.json
    genre_id = data.get("genre_id")
    actor_name = data.get("actor_name")
    release_year = data.get("release_year")
    
    movies = fetch_movies(genre_id=genre_id, actor_name=actor_name, release_year=release_year)
    return jsonify(movies)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """
    Endpoint to generate AI recommendations based on movies.
    """
    data = request.json
    user_input = data.get("user_input")
    movie_list = data.get("movies")
    
    recommendations = generate_ai_recommendations(user_input, movie_list)
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
