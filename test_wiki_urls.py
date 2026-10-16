import urllib.request

# Test known working CDN / poster URLs for major Telugu films
test_candidates = [
    ("Baahubali 1", "https://upload.wikimedia.org/wikipedia/en/7/7e/Baahubali_the_beginning_poster.jpg"),
    ("RRR", "https://upload.wikimedia.org/wikipedia/en/d/d7/RRR_Poster.jpg"),
    ("Pushpa", "https://upload.wikimedia.org/wikipedia/en/7/75/Pushpa_-_The_Rise_%282021_film%29.jpg"),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
for name, url in test_candidates:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"{name}: {resp.status}, bytes: {len(resp.read())}")
    except Exception as e:
        print(f"{name} failed: {e}")
