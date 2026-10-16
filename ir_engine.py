"""
Information Retrieval (IR) Engine for Intelligent Movie Search and Recommendation System
Implements Vector Space Model (VSM), TF-IDF (Term Frequency-Inverse Document Frequency)
Vectorization, and Cosine Similarity for semantic search and content-based recommendation.
"""

import os
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieIREngine:
    def __init__(self, dataset_path="movies.csv"):
        self.dataset_path = dataset_path
        self.df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.feature_names = None
        self.cosine_sim_matrix = None
        self.load_and_index()

    def _clean_text(self, text):
        """Normalize text: lowercase, remove special characters, strip excess whitespace."""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def load_and_index(self):
        """Loads dataset from CSV and builds the TF-IDF Vector Space Model."""
        if not os.path.isabs(self.dataset_path):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base_dir, self.dataset_path)
        else:
            full_path = self.dataset_path

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Dataset not found at {full_path}")

        self.df = pd.read_csv(full_path)
        
        # Ensure correct column types and fill missing values
        self.df["id"] = self.df["id"].astype(int)
        self.df["title"] = self.df["title"].fillna("")
        self.df["genre"] = self.df["genre"].fillna("")
        self.df["category"] = self.df["category"].fillna("Tollywood")
        self.df["language"] = self.df["language"].fillna("Telugu")
        self.df["release_year"] = pd.to_numeric(self.df["release_year"], errors="coerce").fillna(2000).astype(int)
        self.df["rating"] = pd.to_numeric(self.df["rating"], errors="coerce").fillna(7.0)
        self.df["director"] = self.df["director"].fillna("")
        self.df["cast"] = self.df["cast"].fillna("")
        self.df["description"] = self.df["description"].fillna("")
        self.df["poster_url"] = self.df["poster_url"].fillna("")

        # Create weighted document representation for Information Retrieval:
        # We give higher frequency weight to Title, Genres, Category, Language, and Director
        # to ensure that searching for titles or genres yields powerful relevance signals.
        self.df["search_corpus"] = self.df.apply(
            lambda row: " ".join([
                (row["title"] + " ") * 3,          # 3x title weight
                (row["genre"] + " ") * 3,          # 3x genre weight
                (row["category"] + " ") * 2,       # 2x industry/category weight
                (row["language"] + " ") * 2,       # 2x language weight
                (row["director"] + " ") * 2,       # 2x director weight
                row["cast"] + " ",
                row["description"]
            ]),
            axis=1
        )
        self.df["cleaned_corpus"] = self.df["search_corpus"].apply(self._clean_text)

        # Initialize TF-IDF Vectorizer with unigrams and bigrams
        # sublinear_tf=True scales tf to 1 + log(tf), preventing dominant words from skewing results
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )

        # Build TF-IDF document matrix (N documents x V vocabulary features)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df["cleaned_corpus"])
        self.feature_names = self.tfidf_vectorizer.get_feature_names_out()

        # Compute pairwise Cosine Similarity matrix for Content-Based Recommendations
        self.cosine_sim_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def search(self, query, genre_filter="all", language_filter="all", sort_by="relevance", top_n=30):
        """
        Executes Vector Space Model query search against indexed movie documents.
        Ranks results using Cosine Similarity between query vector and document vectors,
        with partial title matching bonus to handle partial titles seamlessly.
        """
        if not query or not query.strip():
            # If no query provided, return all filtered movies
            results_df = self.df.copy()
            results_df["relevance_score"] = 0.0
            results_df["match_percent"] = 0
            results_df["matched_terms"] = [[] for _ in range(len(results_df))]
        else:
            cleaned_query = self._clean_text(query)
            query_tokens = cleaned_query.split()

            # Transform query string to TF-IDF vector
            query_vector = self.tfidf_vectorizer.transform([cleaned_query])

            # Calculate cosine similarity of query against all document vectors
            # Output shape: (1, N) -> flatten to (N,)
            cosine_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

            results_df = self.df.copy()
            final_scores = []
            matched_terms_list = []

            for idx, row in results_df.iterrows():
                base_score = float(cosine_scores[idx])
                clean_title = self._clean_text(row["title"])
                clean_desc = self._clean_text(row["description"])
                clean_genre = self._clean_text(row["genre"])

                # Find which query tokens matched in this document
                matched = [
                    token for token in query_tokens
                    if (token in clean_title or token in clean_genre or token in clean_desc or token in self._clean_text(row["director"]))
                ]
                matched_terms_list.append(matched)

                # Bonus for exact or partial title match (Information Retrieval Query Expansion / Hybrid Re-ranking)
                title_bonus = 0.0
                if cleaned_query and cleaned_query in clean_title:
                    title_bonus += 0.40  # Direct substring match in title
                elif any(tok in clean_title for tok in query_tokens if len(tok) >= 3):
                    title_bonus += 0.20

                # Genre match bonus
                if any(tok in clean_genre for tok in query_tokens if len(tok) >= 3):
                    title_bonus += 0.15

                # Category / Tollywood priority bonus
                if row["category"].strip().lower() == "tollywood" or row["language"].strip().lower() == "telugu":
                    tollywood_bonus = 0.03
                else:
                    tollywood_bonus = 0.0

                combined_score = base_score + title_bonus + tollywood_bonus
                final_scores.append(combined_score)

            results_df["relevance_score"] = final_scores
            # Convert to an intuitive 0-100% Match scale for user interface
            max_s = max(final_scores) if final_scores and max(final_scores) > 0 else 1.0
            results_df["match_percent"] = [
                int(min(99, max(15, (s / max_s) * 98))) if s > 0.05 else int(s * 100)
                for s in final_scores
            ]
            results_df["matched_terms"] = matched_terms_list

            # Filter out entries with near-zero relevance if a query was specified
            results_df = results_df[results_df["relevance_score"] > 0.04]

        # Apply genre filter if specified
        if genre_filter and genre_filter.lower() != "all":
            results_df = results_df[
                results_df["genre"].str.contains(genre_filter, case=False, na=False)
            ]

        # Apply language filter if specified
        if language_filter and language_filter.lower() != "all":
            results_df = results_df[
                results_df["language"].str.contains(language_filter, case=False, na=False)
            ]

        # Apply sorting
        if sort_by == "rating":
            results_df = results_df.sort_values(by=["rating", "release_year"], ascending=False)
        elif sort_by == "year":
            results_df = results_df.sort_values(by=["release_year", "rating"], ascending=False)
        else:  # Default: relevance
            if "relevance_score" in results_df.columns:
                results_df = results_df.sort_values(by=["relevance_score", "rating"], ascending=False)

        # Limit to top N
        return results_df.head(top_n).to_dict(orient="records")

    def get_movie_by_id(self, movie_id):
        """Retrieves a single movie record by its unique ID."""
        matches = self.df[self.df["id"] == int(movie_id)]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def get_recommendations(self, movie_id, top_n=6, prioritize_tollywood=True):
        """
        Computes Content-Based Recommendations for a given movie using Cosine Similarity.
        - Excludes the input movie from results.
        - Strictly prioritizes Tollywood (Telugu) movies.
        - Guarantees at least 5 similar Telugu movies when sufficient records exist.
        - Returns recommendations list and a status dictionary.
        """
        matches = self.df[self.df["id"] == int(movie_id)]
        if matches.empty:
            return [], {"status": "not_found", "message": "Movie not found"}

        target_idx = matches.index[0]
        target_movie = matches.iloc[0].to_dict()

        # Extract cosine similarity scores of target movie against all movies
        sim_scores = list(enumerate(self.cosine_sim_matrix[target_idx]))

        # Sort movies by similarity score in descending order
        sorted_sim = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Exclude the searched movie itself
        candidates = []
        for idx, score in sorted_sim:
            if idx == target_idx:
                continue
            rec_movie = self.df.iloc[idx].to_dict()
            rec_movie["similarity_score"] = round(float(score), 4)
            rec_movie["match_percent"] = int(min(99, max(30, score * 100)))
            candidates.append(rec_movie)

        if prioritize_tollywood:
            # Separate Tollywood/Telugu movies and other industries
            telugu_candidates = [
                m for m in candidates
                if m["category"].strip().lower() == "tollywood" or m["language"].strip().lower() == "telugu"
            ]
            other_candidates = [
                m for m in candidates
                if m not in telugu_candidates
            ]

            # Collect at least top_n recommendations prioritizing Telugu movies
            final_recs = telugu_candidates[:top_n]
            if len(final_recs) < top_n:
                # If fewer Telugu movies are available, backfill from other industries
                needed = top_n - len(final_recs)
                final_recs.extend(other_candidates[:needed])
                status = {
                    "status": "partial_telugu",
                    "telugu_count": len(telugu_candidates),
                    "message": f"Showing {len(telugu_candidates)} matching Tollywood movies and closest other industry matches."
                }
            else:
                status = {
                    "status": "success",
                    "telugu_count": len(final_recs),
                    "message": f"Displaying {len(final_recs)} highly relevant Tollywood movies based on genre and narrative cosine similarity."
                }
        else:
            final_recs = candidates[:top_n]
            status = {"status": "success", "telugu_count": len(final_recs), "message": "Success"}

        return final_recs, status

    def get_featured_movies(self, count=8):
        """Returns top Tollywood blockbusters for the homepage carousel/showcase."""
        tollywood = self.df[
            (self.df["category"].str.lower() == "tollywood") | (self.df["language"].str.lower() == "telugu")
        ]
        # Return popular blockbuster IDs or highest rated
        featured_ids = [1, 2, 3, 4, 6, 8, 12, 21, 22, 10, 16]
        featured = self.df[self.df["id"].isin(featured_ids)].copy()
        if len(featured) < count:
            featured = tollywood.sort_values(by="rating", ascending=False)
        return featured.head(count).to_dict(orient="records")

    def get_top_rated(self, count=6):
        """Returns top rated Telugu movies."""
        tollywood = self.df[
            (self.df["category"].str.lower() == "tollywood") | (self.df["language"].str.lower() == "telugu")
        ]
        return tollywood.sort_values(by="rating", ascending=False).head(count).to_dict(orient="records")

    def get_all_genres(self):
        """Returns all distinct genres with their movie counts."""
        genre_count = {}
        for genres_str in self.df["genre"].dropna():
            for g in genres_str.split(","):
                g_clean = g.strip()
                if g_clean:
                    genre_count[g_clean] = genre_count.get(g_clean, 0) + 1
        
        # Sort alphabetically or by frequency
        return sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

    def get_stats(self):
        """Returns dataset statistics for Information Retrieval project overview."""
        return {
            "total_movies": len(self.df),
            "tollywood_movies": len(
                self.df[
                    (self.df["category"].str.lower() == "tollywood") | 
                    (self.df["language"].str.lower() == "telugu")
                ]
            ),
            "vocabulary_size": len(self.feature_names) if self.feature_names is not None else 0,
            "genres_count": len(self.get_all_genres()),
            "matrix_shape": f"{self.tfidf_matrix.shape[0]} × {self.tfidf_matrix.shape[1]}" if self.tfidf_matrix is not None else "0 × 0"
        }
