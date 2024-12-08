import React, { useState, useEffect } from "react";
// import MovieList from ".components/MovieList";
import MovieList from "./components/MovieList";
import {
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";

function App() {
  const [genres, setGenres] = useState([]);
  const [genre, setGenre] = useState("");
  const [actor, setActor] = useState("");
  const [year, setYear] = useState("");
  const [recommendations, setRecommendations] = useState("");
  const [typedRecommendations, setTypedRecommendations] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchGenres() {
      try {
        const response = await fetch("http://127.0.0.1:5000/genres");
        const data = await response.json();
        setGenres(data);
      } catch (error) {
        console.error("Error fetching genres:", error);
      }
    }
    fetchGenres();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setTypedRecommendations("");
    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          genre_id: genre,
          actor_name: actor,
          release_year: year,
        }),
      });
      const data = await response.json();
      setRecommendations(data.recommendations || "No recommendations found.");
      setMovies(data.movies || []);
      applyTypewriterEffect(data.recommendations || "No recommendations found.");
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  const applyTypewriterEffect = (text) => {
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        setTypedRecommendations((prev) => prev + text[index]);
        index++;
      } else {
        clearInterval(interval);
      }
    }, 5);
  };

  const fakeMovies = [
    {
      title: "Fake Movie 1",
      poster_path: "https://via.placeholder.com/150x200?text=Fake+Movie+1",
    },
    {
      title: "Fake Movie 2",
      poster_path: "https://via.placeholder.com/150x200?text=Fake+Movie+2",
    },
    {
      title: "Fake Movie 3",
      poster_path: "https://via.placeholder.com/150x200?text=Fake+Movie+3",
    },
  ];

  useEffect(() => {
    const carousel = document.getElementById("fakeMoviesCarousel");
    const interval = setInterval(() => {
      if (carousel) {
        carousel.scrollBy({ left: 200, behavior: "smooth" });
        if (
          carousel.scrollLeft + carousel.clientWidth >=
          carousel.scrollWidth
        ) {
          carousel.scrollTo({ left: 0, behavior: "smooth" });
        }
      }
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        background: "linear-gradient(to bottom, #1A0000, #8B0000)",
        minHeight: "100vh",
        color: "white",
        display: "flex",
        flexDirection: "column",
        padding: "20px",
        position: "relative",
      }}
    >
      {loading && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.7)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 10,
          }}
        >
          <CircularProgress style={{ color: "white", marginBottom: "10px" }} />
          <p>Loading...</p>
        </div>
      )}

      <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
        Movie Recommendations
      </h1>
      <div style={{ display: "flex", flexDirection: "row", flexGrow: 1 }}>
        <div style={{ flex: 1, marginRight: "20px" }}>
          <form onSubmit={handleSubmit}>
            <FormControl fullWidth style={{ marginBottom: "20px" }}>
              <InputLabel style={{ color: "red" }}>Genre</InputLabel>
              <Select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                style={{ backgroundColor: "white", color: "black" }}
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
              fullWidth
              value={actor}
              onChange={(e) => setActor(e.target.value)}
              placeholder="e.g., Keanu Reeves"
              style={{
                marginBottom: "20px",
                backgroundColor: "white",
                borderRadius: "4px",
              }}
              InputProps={{ style: { color: "black" } }}
            />

            <TextField
              label="Release Year"
              fullWidth
              value={year}
              onChange={(e) => setYear(e.target.value)}
              placeholder="e.g., 2021"
              style={{
                marginBottom: "20px",
                backgroundColor: "white",
                borderRadius: "4px",
              }}
              InputProps={{ style: { color: "black" } }}
            />

            <div style={{ textAlign: "center" }}>
              <Button
                variant="contained"
                type="submit"
                style={{
                  background:
                    "linear-gradient(90deg, rgba(0,36,36,1) 0%, rgba(9,121,113,1) 35%, rgba(2,88,122,1) 100%)",
                  color: "white",
                  fontWeight: "bold",
                }}
              >
                Get Recommendations
              </Button>
            </div>
          </form>

          <h2 style={{ marginTop: "30px" }}>Movies</h2>
          <MovieList movies={movies.length > 0 ? movies : fakeMovies} />
        </div>

        <div
          style={{
            flex: 1,
            marginLeft: "20px",
            borderLeft: "2px solid white",
            paddingLeft: "20px",
          }}
        >
          <h2>Recommendations</h2>
          <div style={{
    whiteSpace: "pre-wrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    fontSize: "0.9rem",
    lineHeight: "1.6",
    width: "100%",
    maxWidth: "100%", // Ensures it doesn't exceed the container
    minHeight:"80vh"
  }}>
            {typedRecommendations}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
