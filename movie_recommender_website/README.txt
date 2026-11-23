# CineMatch — Movie Recommendation Website

This project wraps your movie recommendation model in a Flask website.

## 1. Put the files together
Keep this folder structure:

```
movie_recommender_website/
├── app.py
├── movie_dataset.csv
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## 2. Open the folder in VS Code

Open a terminal in this folder. (On Windows, use Terminal > New Terminal.)

## 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If `python` does not work, try `py -m pip install -r requirements.txt`.

## 4. Run the website

```bash
python app.py
```

If needed, try `py app.py`.

## 5. Open it in your browser

Visit:

http://127.0.0.1:5000

Type a movie title (for example, Avatar) and click **Find movies**.

## How it works

- `app.py` loads the CSV and builds a CountVectorizer matrix when the server starts.
- Flask serves the website and receives the movie title from the search form.
- The recommender calculates cosine similarity for the selected movie and returns the closest matches.
- `templates/index.html` displays the selected movie and recommendations.
- `static/style.css` controls the appearance.

## Notes

- The recommendation method stays aligned with your original project: keywords + cast + genres + director, CountVectorizer, and cosine similarity.
- Your uploaded dataset does not include movie poster image URLs, so this first version uses designed poster-style cards rather than real movie posters.
- The app is intended for local learning/testing. Before deploying publicly, turn off Flask debug mode and add production hosting/security configuration.
