import React from "react";

function MovieCard({ movie }) {
  return (
    <div className="movie-card">
      <img src={movie.poster_url} alt={`${movie.title} Poster`} />
      <div>
        <h3>{movie.title}</h3>
        <p>
          <strong>Release Date:</strong> {movie.release_date}
        </p>
        <p>{movie.overview}</p>
        <p>
          <strong>Rating:</strong> {movie.vote_average}
        </p>
      </div>
    </div>
  );
}

export default MovieCard;
