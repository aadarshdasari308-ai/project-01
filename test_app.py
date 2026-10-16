"""
Automated Route & IR Verification Test Suite for Flask Application
"""
from app import app

def test_routes():
    client = app.test_client()
    
    print("1. Testing GET / (Home Page)...")
    res = client.get("/")
    assert res.status_code == 200
    assert b"Discover Your Next" in res.data
    assert b"Tollywood" in res.data
    print("   -> Home page OK!")

    print("2. Testing GET /search?q=Baahubali (Search Engine)...")
    res = client.get("/search?q=Baahubali")
    assert res.status_code == 200
    assert b"Baahubali" in res.data
    assert b"Match" in res.data
    print("   -> Search results OK!")

    print("3. Testing GET /search?q=supercalifragilistic (Empty State)...")
    res = client.get("/search?q=supercalifragilistic")
    assert res.status_code == 200
    assert b"No Movies Found" in res.data
    print("   -> Empty state handled gracefully!")

    print("4. Testing GET /movie/1 (Movie Details & Similar Tollywood Movies)...")
    res = client.get("/movie/1")
    assert res.status_code == 200
    assert b"Baahubali: The Beginning" in res.data
    assert b"Recommended Tollywood Movies" in res.data
    assert b"Baahubali 2" in res.data
    print("   -> Movie details & recommendations OK!")

    print("5. Testing GET /genres (Genre Browser)...")
    res = client.get("/genres")
    assert res.status_code == 200
    assert b"Explore by" in res.data
    print("   -> Genres page OK!")

    print("6. Testing GET /recommendations (Recommendation Hub)...")
    res = client.get("/recommendations?movie_id=1")
    assert res.status_code == 200
    assert b"Recommended" in res.data
    print("   -> Recommendations hub OK!")

    print("7. Testing GET /about (IRS Academic Documentation)...")
    res = client.get("/about")
    assert res.status_code == 200
    assert b"TF-IDF" in res.data
    assert b"Cosine Similarity" in res.data
    print("   -> About page OK!")

    print("8. Testing GET /api/suggest?q=Push (Live Autocomplete API)...")
    res = client.get("/api/suggest?q=Push")
    assert res.status_code == 200
    json_data = res.get_json()
    assert len(json_data) > 0
    assert "Pushpa" in json_data[0]["title"]
    print(f"   -> Autocomplete API OK! Found: {json_data[0]['title']}")

    print("\nALL 8 FLASK SUITE TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_routes()
