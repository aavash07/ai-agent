import React, { useState, useEffect } from "react";
import MovieList from "./components/MovieList";
import ChatDialog from "./components/ChatDialog";
import {
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";
import { FaComments } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [genres, setGenres] = useState([]);
  const [genre, setGenre] = useState("");
  const [actor, setActor] = useState("");
  const [year, setYear] = useState("");
  const [recommendations, setRecommendations] = useState("");
  const [typedRecommendations, setTypedRecommendations] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);

  // List of emojis
  const emojiList = ["🎬", "🍿", "🎥", "📽️", "🎞️", "⭐", "🥳", "🎤", "👓"];

  // Get a random emoji
  const getRandomEmoji = () => {
    return emojiList[Math.floor(Math.random() * emojiList.length)];
  };

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

  const handleChatMessage = async (query) => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setRecommendations(data.recommendations || "No recommendations found.");
      setMovies(data.movies || []);
      return data.recommendations || "No recommendations found.";
    } catch (error) {
      console.error("Error processing chat query:", error);
      return "Sorry, something went wrong. Please try again.";
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

  const sanitizedRecommendations = typedRecommendations.replace(
    /\n{2,}/g,
    "\n"
  );

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
              <InputLabel style={{ color: "black" }}>Genre</InputLabel>
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

            <div
              style={{
                display: "flex",
                gap: "10px",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Button
                variant="contained"
                type="submit"
                style={{
                  background:
                    "linear-gradient(90deg, rgba(0,36,36,1) 0%, rgba(9,121,113,1) 35%, rgba(2,88,122,1) 100%)",
                  color: "white",
                  fontWeight: "bold",
                  height: "50px",
                  width: "235px",
                  borderRadius: "5px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                GET RECOMMENDATIONS
              </Button>
              <span>or</span>
              <div
                className="chat-button"
                onClick={() => setChatOpen(true)}
                style={{
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  height: "50px",
                  width: "50px",
                  borderRadius: "5px",
                  background:
                    "linear-gradient(90deg, rgba(0,36,36,1) 0%, rgba(9,121,113,1) 35%, rgba(2,88,122,1) 100%)",
                  color: "white",
                  fontSize: "1.2rem",
                }}
              >
                <FaComments size={20} className="bouncy-chat-icon" />
              </div>
            </div>
          </form>

          <h2 style={{ marginTop: "30px" }}>Movies</h2>
          <MovieList movies={movies.length > 0 ? movies : []} />
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
          <div
            style={{
              whiteSpace: "pre-wrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
              fontSize: "0.9rem",
              lineHeight: "1.6",
              width: "100%",
              maxWidth: "100%",
              minHeight: "80vh",
            }}
          >
            <ReactMarkdown
              components={{
                strong: ({ children }) => (
                  <strong
                    style={{
                      fontSize: "1.2rem",
                      color: "white",
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    {children}
                    <span
                      style={{
                        marginLeft: "5px",
                        fontSize: "1rem",
                      }}
                    >
                      {getRandomEmoji()}
                    </span>
                  </strong>
                ),
                p: ({ children }) => (
                  <p style={{ margin: "0", color: "white" , marginBottom:"-40px"}}>{children}</p>
                ),
                li: ({ children }) => (
                  <li style={{ marginBottom: "5px", color: "white" }}>
                    {children}
                  </li>
                ),
                ol: ({ children }) => (
                  <ol
                    style={{
                      margin: "0",
                      paddingInlineStart: "20px",
                    }}
                  >
                    {children}
                  </ol>
                ),
              }}
            >
              {sanitizedRecommendations}
            </ReactMarkdown>
          </div>
        </div>
      </div>

      <ChatDialog
        open={chatOpen}
        onClose={() => setChatOpen(false)}
        onSendMessage={handleChatMessage}
        movies={movies}
      />
    </div>
  );
}

export default App;
