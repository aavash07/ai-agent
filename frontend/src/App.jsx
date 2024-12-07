import React, { useState, useEffect } from "react";
import MovieList from "./components/MovieList";
import "./App.css";
import { MenuItem, Select, InputLabel, FormControl, TextField, Button } from "@mui/material";

function App() {
  const [genres, setGenres] = useState([]); // To store genre options
  const [genre, setGenre] = useState(""); // To store selected genre ID
  const [actor, setActor] = useState("");
  const [year, setYear] = useState("");
  const [recommendations, setRecommendations] = useState("");
  const [movies, setMovies] = useState([]);

  // Fetch genres from the backend on component mount
  useEffect(() => {
    async function fetchGenres() {
      try {
        const response = await fetch("http://127.0.0.1:5000/genres"); // Call the new /genres endpoint
        const data = await response.json();
        setGenres(data); // Populate genres in the dropdown
      } catch (error) {
        console.error("Error fetching genres:", error);
      }
    }
    fetchGenres();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ genre_id: genre, actor_name: actor, release_year: year }),
      });
      const data = await response.json();
      setRecommendations(data.recommendations || "No recommendations found.");
      setMovies(data.movies || []);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div className="App">
      <h1>Movie Recommendations</h1>
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth style={{ marginBottom: "20px" }}>
          <InputLabel>Genre</InputLabel>
          <Select
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
            label="Genre"
            required
          >
            {genres.map((g) => (
              <MenuItem key={g.id} value={g.id}>
                {g.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="Actor Name"
          variant="outlined"
          fullWidth
          value={actor}
          onChange={(e) => setActor(e.target.value)}
          placeholder="e.g., Keanu Reeves"
          style={{ marginBottom: "20px" }}
        />

        <TextField
          label="Release Year"
          variant="outlined"
          fullWidth
          value={year}
          onChange={(e) => setYear(e.target.value)}
          placeholder="e.g., 2021"
          style={{ marginBottom: "20px" }}
        />

        <Button variant="contained" color="primary" type="submit">
          Get Recommendations
        </Button>
      </form>

      <h2>Recommendations</h2>
      <p>{recommendations}</p>
      <MovieList movies={movies} />
    </div>
  );
}

export default App;
