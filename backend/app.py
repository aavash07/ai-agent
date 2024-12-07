from flask import Flask, request, jsonify
from agent import MovieRecommendationAgent

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    API endpoint for generating movie recommendations.
    Accepts JSON input with user preferences.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input. Please provide genre_id, actor_name, and release_year."}), 400

    # Initialize AI agent with user input
    agent = MovieRecommendationAgent(data)
    result = agent.run()

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
