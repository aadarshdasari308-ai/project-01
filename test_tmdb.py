import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
urls = [
    "https://image.tmdb.org/t/p/w500/9BAjt85amQXzh6jh8jwTue6FsxD.jpg",
    "https://image.tmdb.org/t/p/w500/21sC2assImQIYCEDA84Qh9d1RsK.jpg",
    "https://image.tmdb.org/t/p/w500/nEufeZlyAOLqO2brrs0yeMurrgu.jpg",
]

for url in urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"Status for {url}: {resp.status}")
    except Exception as e:
        print(f"Error for {url}: {e}")
