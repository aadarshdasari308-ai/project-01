"""
Intelligent Movie Search and Recommendation System
Flask Application & Web Controller
"""

import time
from flask import Flask, render_template, request, jsonify, abort
from ir_engine import MovieIREngine

app = Flask(__name__)

# Initialize the Information Retrieval engine with the Tollywood dataset
engine = MovieIREngine("movies.csv")


@app.route("/")
def index():
    """Home page with hero search, featured blockbusters, and top-rated Telugu movies."""
    featured_movies = engine.get_featured_movies(count=8)
    top_rated_movies = engine.get_top_rated(count=8)
    genres = engine.get_all_genres()[:8]
    stats = engine.get_stats()
    return render_template(
        "index.html",
        featured_movies=featured_movies,
        top_rated_movies=top_rated_movies,
        genres=genres,
        stats=stats
    )


@app.route("/search")
def search():
    """
    Search route implementing Vector Space Model ranking and filtering.
    Accepts:
        q: query string (title, genre, keyword, storyline, director, cast)
        genre: genre filter (e.g. 'Action', 'Comedy', 'all')
        lang: language filter (e.g. 'Telugu', 'Hindi', 'all')
        sort: sorting criteria ('relevance', 'rating', 'year')
    """
    start_time = time.time()
    query = request.args.get("q", "").strip()
    genre_filter = request.args.get("genre", "all").strip()
    lang_filter = request.args.get("lang", "all").strip()
    sort_by = request.args.get("sort", "relevance").strip()

    results = engine.search(
        query=query,
        genre_filter=genre_filter,
        language_filter=lang_filter,
        sort_by=sort_by,
        top_n=30
    )

    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    genres = [g[0] for g in engine.get_all_genres()]
    fallback_recommendations = engine.get_featured_movies(count=4) if not results else []

    return render_template(
        "search_results.html",
        query=query,
        results=results,
        results_count=len(results),
        elapsed_ms=elapsed_ms,
        genre_filter=genre_filter,
        lang_filter=lang_filter,
        sort_by=sort_by,
        all_genres=genres,
        fallback_recommendations=fallback_recommendations
    )


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    """
    Movie Details Page:
    Displays full movie details and calculates at least 5 similar Tollywood recommendations
    using pairwise Cosine Similarity over the TF-IDF feature space.
    """
    movie = engine.get_movie_by_id(movie_id)
    if not movie:
        abort(404)

    # Get at least 5-6 similar Tollywood movies
    recommendations, rec_status = engine.get_recommendations(
        movie_id=movie_id,
        top_n=6,
        prioritize_tollywood=True
    )

    # Extract genre list for tags
    genre_list = [g.strip() for g in movie["genre"].split(",") if g.strip()]
    cast_list = [c.strip() for c in movie["cast"].split(",") if c.strip()]

    return render_template(
        "movie_details.html",
        movie=movie,
        genre_list=genre_list,
        cast_list=cast_list,
        recommendations=recommendations,
        rec_status=rec_status
    )


@app.route("/genres")
def genres():
    """Browse movies by categories and genres."""
    genres_data = engine.get_all_genres()
    # Also fetch sample movies for popular genres
    genre_samples = {}
    for g, count in genres_data[:6]:
        genre_samples[g] = engine.search(query="", genre_filter=g, top_n=4)

    return render_template(
        "genres.html",
        genres=genres_data,
        genre_samples=genre_samples
    )


@app.route("/recommendations")
def recommendations_hub():
    """Interactive recommendation playground to explore movie similarities."""
    movie_id = request.args.get("movie_id", type=int)
    all_movies = engine.df[["id", "title", "release_year", "category", "language"]].to_dict(orient="records")

    selected_movie = None
    recommendations = []
    rec_status = None

    if movie_id:
        selected_movie = engine.get_movie_by_id(movie_id)
        if selected_movie:
            recommendations, rec_status = engine.get_recommendations(movie_id=movie_id, top_n=6)
    else:
        # Default to Baahubali (id=1) as demonstration
        selected_movie = engine.get_movie_by_id(1)
        if selected_movie:
            recommendations, rec_status = engine.get_recommendations(movie_id=1, top_n=6)

    return render_template(
        "recommendations.html",
        all_movies=all_movies,
        selected_movie=selected_movie,
        recommendations=recommendations,
        rec_status=rec_status
    )


@app.route("/about")
def about():
    """IRS concepts, TF-IDF formulas, Cosine Similarity math, and architecture documentation."""
    stats = engine.get_stats()
    return render_template("about.html", stats=stats)


@app.route("/api/suggest")
def api_suggest():
    """Asynchronous live suggestions endpoint for responsive header search."""
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return jsonify([])

    results = engine.search(query=q, top_n=5)
    suggestions = [
        {
            "id": r["id"],
            "title": r["title"],
            "year": r["release_year"],
            "genre": r["genre"],
            "category": r["category"],
            "poster_url": r["poster_url"]
        }
        for r in results
    ]
    return jsonify(suggestions)


@app.errorhandler(404)
def not_found(e):
    return render_template("search_results.html", query="", results=[], results_count=0,
                           genre_filter="all", lang_filter="all", sort_by="relevance",
                           all_genres=[], fallback_recommendations=engine.get_featured_movies(count=4)), 404


if __name__ == "__main__":
    print("Starting Intelligent Movie Search and Recommendation System...")
    print("Serving on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
