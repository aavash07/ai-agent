import React from "react";
import { Card, CardContent, Typography, CardMedia } from "@mui/material";

function MovieCard({ movie }) {
  // Construct the full image URL using backdrop_path or poster_path
  const imageUrl = movie.backdrop_path
    ? `https://image.tmdb.org/t/p/w500${movie.backdrop_path}` // Use backdrop_path first
    : movie.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` // Fallback to poster_path
    : "https://via.placeholder.com/500x300?text=No+Image"; // Placeholder if no image is available

  return (
    <Card style={{ marginBottom: "20px", width: "300px" }}>
      <CardMedia
        component="img"
        alt={movie.title}
        height="300"
        image={imageUrl}
      />
      <CardContent>
        <Typography variant="h6">{movie.title}</Typography>
        <Typography variant="body2" color="textSecondary">
          Release Date: {movie.release_date}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Rating: {movie.vote_average}
        </Typography>
        <Typography variant="body2">{movie.overview}</Typography>
      </CardContent>
    </Card>
  );
}

export default MovieCard;
