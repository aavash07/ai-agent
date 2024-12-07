import React from "react";

function MovieList({ movies }) {
  if (!movies.length) {
    return <p>No movies to display.</p>;
  }

  return (
    <div className="movie-list">
      {movies.map((movie) => (
        <div key={movie.id} className="movie-card">
          <img src={movie.poster_url} alt={`${movie.title} Poster`} />
          <h3>{movie.title}</h3>
          <p><strong>Release Date:</strong> {movie.release_date}</p>
          <p><strong>Rating:</strong> {movie.vote_average}</p>
          <p>{movie.overview}</p>
        </div>
      ))}
    </div>
  );
}

export default MovieList;
