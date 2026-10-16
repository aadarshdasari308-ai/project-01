from ir_engine import MovieIREngine

engine = MovieIREngine('movies.csv')
print("--- DATASET STATS ---")
print(engine.get_stats())

print("\n--- SEARCH: 'Baahubali' ---")
search_results = engine.search("Baahubali")
for r in search_results[:3]:
    print(f"- {r['title']} ({r['release_year']}) | Score: {r['relevance_score']:.3f} | Match: {r['match_percent']}%")

print("\n--- SEARCH: 'investigative detective murder mystery' ---")
mystery_results = engine.search("investigative detective murder mystery")
for r in mystery_results[:3]:
    print(f"- {r['title']} ({r['release_year']}) | Genre: {r['genre']} | Match: {r['match_percent']}%")

print("\n--- RECOMMENDATIONS FOR 'Baahubali: The Beginning' (ID: 1) ---")
recs, status = engine.get_recommendations(1, top_n=5)
print("Status:", status)
for r in recs:
    print(f"- {r['title']} ({r['release_year']}) | Similarity: {r['similarity_score']:.3f} | Language: {r['language']}")
