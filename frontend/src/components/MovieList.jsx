import React from "react";

function MovieList({ movies }) {
  if (!movies || movies.length === 0) {
    return <p>No movies to display.</p>;
  }

  return (
    <div className="MovieList">
      {movies.map((movie, index) => (
        <div key={index} className="MovieCard">
          <img
            src={
              movie.poster_path
                ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
                : "https://via.placeholder.com/150x200?text=No+Image"
            }
            alt={movie.title || "No Title"}
            style={{
              width: "150px",
              height: "200px",
              borderRadius: "10px",
              objectFit: "cover",
            }}
          />
          <h3 style={{ textAlign: "center", color: "white", marginTop: "10px" }}>
            {movie.title || "No Title"}
          </h3>
          <p style={{ textAlign: "center", color: "white", fontSize: "0.9rem" }}>
            {movie.release_date || "Unknown Release Date"}
          </p>
        </div>
      ))}
    </div>
  );
}

export default MovieList;
