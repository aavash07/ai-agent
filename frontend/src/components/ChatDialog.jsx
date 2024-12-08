import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextareaAutosize,
  Typography,
} from "@mui/material";

const ChatDialog = ({ open, onClose, onSendMessage, movies }) => {
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [showMovies, setShowMovies] = useState(false); // Control when to display movies

  // Add an initial greeting message when the dialog opens
  useEffect(() => {
    if (open) {
      setChatMessages([
        {
          sender: "bot",
          text: "Hi there! 👋 What kind of movies are you looking for today? 🎬✨",
        },
      ]);
      setShowMovies(false); // Hide movies when chat opens
    }
  }, [open]);

  const handleSend = async () => {
    if (!chatInput.trim()) return;

    const userMessage = { sender: "user", text: chatInput };
    setChatMessages((prev) => [...prev, userMessage]);

    try {
      const botResponse = await onSendMessage(chatInput);
      const botMessage = { sender: "bot", text: botResponse || "No recommendations found." };
      setChatMessages((prev) => [...prev, botMessage]);

      // Show movies if there are any
      if (movies.length > 0) {
        setShowMovies(true);
      }
    } catch (error) {
      setChatMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Oops! Something went wrong. Please try again. 😅" },
      ]);
    }

    setChatInput("");
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth>
      <DialogTitle>Chat with Movie Bot</DialogTitle>
      <DialogContent>
        {/* Chat Messages */}
        <div
          style={{
            height: "300px",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "10px",
          }}
        >
          {chatMessages.map((message, index) => (
            <div
              key={index}
              style={{
                alignSelf: message.sender === "user" ? "flex-end" : "flex-start",
                backgroundColor: message.sender === "user" ? "#007BFF" : "#444",
                color: "white",
                padding: "10px",
                borderRadius: "10px",
                maxWidth: "60%",
              }}
            >
              {message.text}
            </div>
          ))}
        </div>

        {/* Movies Section */}
        {showMovies && movies.length > 0 && (
          <div style={{ marginTop: "20px" }}>
            <Typography variant="h6" style={{ marginBottom: "10px" }}>
              Movies
            </Typography>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
                gap: "20px",
              }}
            >
              {movies.map((movie, index) => (
                <div
                  key={index}
                  style={{
                    backgroundColor: "#2E2E2E",
                    borderRadius: "10px",
                    padding: "10px",
                    textAlign: "center",
                    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.3)",
                  }}
                >
                  <img
                    src={
                      movie.poster_path
                        ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
                        : "https://via.placeholder.com/150x200?text=No+Image"
                    }
                    alt={movie.title || "No Title"}
                    style={{
                      width: "100%",
                      height: "200px",
                      borderRadius: "10px",
                      objectFit: "cover",
                    }}
                  />
                  <h3
                    style={{
                      color: "white",
                      fontSize: "1rem",
                      marginTop: "10px",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                    }}
                  >
                    {movie.title || "No Title"}
                  </h3>
                  <p
                    style={{
                      color: "gray",
                      fontSize: "0.8rem",
                      marginTop: "5px",
                    }}
                  >
                    {movie.release_date || "Unknown Release Date"}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </DialogContent>

      <DialogActions>
        <TextareaAutosize
          minRows={2}
          placeholder="Type your message..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "5px",
          }}
        />
        <Button
          onClick={handleSend}
          variant="contained"
          style={{
            background:
              "linear-gradient(90deg, rgba(0,36,36,1) 0%, rgba(9,121,113,1) 35%, rgba(2,88,122,1) 100%)",
            color: "white",
            fontWeight: "bold",
          }}
        >
          Send
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ChatDialog;
