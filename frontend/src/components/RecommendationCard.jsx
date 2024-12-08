import React from "react";
import { Card, CardContent, Typography, CardMedia } from "@mui/material";

function RecommendationCard({ recommendation }) {
  return (
    <Card style={{ marginBottom: "20px", width: "300px" }}>
      <CardMedia
        component="img"
        alt={recommendation.title}
        height="150"
        image={recommendation.poster}
      />
      <CardContent>
        <Typography variant="h6">{recommendation.title}</Typography>
        <Typography variant="body2" color="textSecondary">
          Release Year: {recommendation.year}
        </Typography>
        <Typography variant="body2">{recommendation.reasoning}</Typography>
      </CardContent>
    </Card>
  );
}

export default RecommendationCard;
