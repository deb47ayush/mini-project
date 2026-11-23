from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "movie_dataset.csv"

app = Flask(__name__)

# Load the dataset and prepare the recommendation model once when the app starts.
df = pd.read_csv(DATASET_PATH)

required_columns = ["title", "keywords", "cast", "genres", "director"]
missing = [column for column in required_columns if column not in df.columns]
if missing:
    raise ValueError(f"The CSV is missing required columns: {', '.join(missing)}")

for column in ["keywords", "cast", "genres", "director"]:
    df[column] = df[column].fillna("").astype(str)

df["title"] = df["title"].fillna("").astype(str)
df["combined_features"] = (
    df["keywords"] + " " + df["cast"] + " " + df["genres"] + " " + df["director"]
)

# Keep the same method as your original project: CountVectorizer + cosine similarity.
vectorizer = CountVectorizer()
count_matrix = vectorizer.fit_transform(df["combined_features"])

# Map titles to row positions. If duplicate titles exist, use the first match.
title_to_position = {}
for position, title in enumerate(df["title"]):
    cleaned_title = title.strip().casefold()
    if cleaned_title and cleaned_title not in title_to_position:
        title_to_position[cleaned_title] = position

movie_titles = sorted(df["title"].dropna().unique().tolist(), key=str.casefold)


def recommend_movies(movie_title, limit=8):
    """Return up to `limit` movies most similar to the selected movie."""
    position = title_to_position.get(movie_title.strip().casefold())
    if position is None:
        return None

    # Compare the selected movie's vector with every movie vector.
    scores = cosine_similarity(count_matrix[position], count_matrix).flatten()

    # Sort highest similarity first, excluding the selected movie itself.
    ranked_positions = scores.argsort()[::-1]
    recommendations = []

    for recommended_position in ranked_positions:
        if recommended_position == position:
            continue

        row = df.iloc[recommended_position]
        recommendations.append({
            "title": row["title"],
            "genres": row.get("genres", ""),
            "director": row.get("director", ""),
            "overview": row.get("overview", ""),
            "rating": row.get("vote_average", ""),
            "year": (
                str(row.get("release_date", ""))[:4]
                if pd.notna(row.get("release_date", "")) else ""
            ),
            "score": round(float(scores[recommended_position]) * 100, 1),
        })

        if len(recommendations) >= limit:
            break

    selected = df.iloc[position]
    selected_movie = {
        "title": selected["title"],
        "genres": selected.get("genres", ""),
        "director": selected.get("director", ""),
        "overview": selected.get("overview", ""),
        "rating": selected.get("vote_average", ""),
        "year": (
            str(selected.get("release_date", ""))[:4]
            if pd.notna(selected.get("release_date", "")) else ""
        ),
    }
    return selected_movie, recommendations


@app.route("/", methods=["GET", "POST"])
def home():
    selected_movie = None
    recommendations = []
    error = None
    query = ""

    if request.method == "POST":
        query = request.form.get("movie", "").strip()
        if not query:
            error = "Please enter a movie title."
        else:
            result = recommend_movies(query)
            if result is None:
                error = f"We couldn't find “{query}” in this dataset. Try a title from the suggestions."
            else:
                selected_movie, recommendations = result

    return render_template(
        "index.html",
        movie_titles=movie_titles,
        selected_movie=selected_movie,
        recommendations=recommendations,
        error=error,
        query=query,
    )


if __name__ == "__main__":
    app.run(debug=True)
