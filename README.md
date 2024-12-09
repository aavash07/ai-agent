# AI-Powered Movie Recommendation Agent ( Aavash Chaudhary, Pushpa Pandey, John Moses B) Team Members

### Overview
The AI-Powered Movie Recommendation Agent is a system that provides personalized movie recommendations based on user preferences. It leverages TMDB API for movie data and Groq's large language model (LLM) for understanding natural language queries and generating relevant recommendations.


## Features
- Natural Language Query Parsing: Accepts user queries in plain language like “Action movies starring Keanu Reeves in 2021.”
- Genre and Actor Filtering: Finds movies based on specific genres, actors, and release years.
- AI Recommendations: Uses LLM to generate detailed movie suggestions.
- Feedback Loop: Ensures recommendations align with user preferences through iterative feedback validation.
- Interactive Frontend: A user-friendly Vite-based React interface to input queries and view recommendations.

## Technology Stack

- Backend: Flask (Python), TMDB API, Groq LLM API
- Frontend: React.js (Vite), Axios, Material-UI, Typewriter animation

## How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo-name/movie-recommendation-agent.git
cd movie-recommendation-agent
```

### 2. Backend Setup

#### Step 1: Install Python Dependencies
Make sure you have Python 3.7+ installed. Then install the required Python libraries:
```bash
pip install -r requirements.txt
```

#### Step 2: Set Up Environment Variables
Create a `.env` file in the root directory of the backend and add the following keys:
 # .env
TMDB_API_KEY=6c95379be6aeeb27a69402700d7e1798
AZURE_OPENAI_API_KEY=46z847AGFiOqdlWxzaYuQ0Ad9XbCwm9o6qqKXPZPvpAdoIa9tlaKJQQJ99ALACHYHv6XJ3w3AAAAACOGjxTF
AZURE_OPENAI_ENDPOINT=https://chaud-m4bwiifx-eastus2.openai.azure.com/
AZURE_OPENAI_MODEL=gpt-4
AZURE_OPENAI_API_VERSION=2024-08-01-preview
GROQ_API_KEY=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
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions

#### Step 3: Start the Backend Server
Run the backend server using the following command:
```bash
python app.py
```
The backend will run at `http://127.0.0.1:5000`.


### 3. Frontend Setup

#### Step 1: Navigate to the Frontend Folder
Move into the `frontend` directory:
```bash
cd frontend
```

#### Step 2: Install Node.js Dependencies
Ensure you have Node.js and npm installed. Then install the dependencies:
```bash
npm install
```

#### Step 3: Configure the Backend API URL
Update the `frontend/src/config.js` file with the backend server URL:
```javascript
export const API_URL = "http://127.0.0.1:5000";
```

#### Step 4: Start the Frontend Development Server
Since the frontend uses Vite, run the development server with:
```bash
npm run dev
```
The frontend will run at `http://localhost:5173` by default (or as specified in the terminal).


## API Endpoints

#### 1. GET /genres
Fetch the available genres from TMDB:
```bash
curl http://127.0.0.1:5000/genres
```

#### 2. POST /recommend
Generate movie recommendations by sending either a structured input or a query:
```bash
curl -X POST http://127.0.0.1:5000/recommend \
-H "Content-Type: application/json" \
-d '{"query": "I want action movies starring Keanu Reeves from 2021."}'
```

Example Response:
```json
{
  "recommendations": [
    {
      "title": "The Matrix Resurrections",
      "description": "Neo must once again use his abilities to free humanity from the Matrix.",
      "reason": "Keanu Reeves stars as Neo in this action-packed sci-fi sequel."
    },
    {
      "title": "John Wick: Chapter 4",
      "description": "John Wick continues his quest for revenge against the High Table.",
      "reason": "Keanu Reeves stars as the titular character in this adrenaline-fueled action film."
    },
    {
      "title": "Bill & Ted Face the Music",
      "description": "Ted declares that Bill and Ted must write a song to save the universe.",
      "reason": "Keanu Reeves stars as Ted Logan in this comedy-adventure sequel."
    }
  ]
}
```



## Workflow

### 1. Input Parsing:
- Accepts user queries in natural language or structured format.
- Extracts fields (`genre`, `actor`, `release_year`) using Groq's LLM.

### 2. Data Fetching:
- Fetches movie data from TMDB API using the parsed fields.

### 3. Recommendation Generation:
- Generates AI-based recommendations based on user preferences.
- Includes feedback validation to refine suggestions.

### 4. Output Delivery:
- Provides users with the final set of movie recommendations via the frontend.


## Key Features of the Agent

1. Feedback Mechanisms:
   - Built-in feedback loops ensure the agent refines its recommendations based on user preferences.

2. Self-Propagation:
   - The agent autonomously parses, fetches data, and generates results without manual intervention.

3. User-Friendly Frontend:
   - An interactive UI allows users to input queries and view recommendations seamlessly.



## Demo

- Backend: Accessible via API endpoints at `http://127.0.0.1:5000`.
- Frontend: Access the interactive UI at `http://localhost:5173`.


## Future Enhancements
- Add memory for user preferences to provide personalized recommendations over time.
- Implement a collaborative filtering feature to recommend movies based on other users with similar tastes.
- Enhance feedback validation by allowing users to give explicit ratings.

## Acknowledgments
- TMDB API for movie data: [TMDB Documentation](https://developers.themoviedb.org/3)
- Groq Cloud AI for natural language parsing and recommendation generation: [Groq AI](https://groq.com)

