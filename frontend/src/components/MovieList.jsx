import React from "react";

function MovieList({ movies }) {
  if (!movies || movies.length === 0) {
    return <p style={{ color: "white" }}>No movies to display.</p>;
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
        gap: "20px",
        marginTop: "20px",
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
  );
}

export default MovieList;
