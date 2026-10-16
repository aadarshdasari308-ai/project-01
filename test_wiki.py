import urllib.request
import json
import urllib.parse

def search_wiki_image(movie_name):
    headers = {'User-Agent': 'MovieIREngine/1.0 (test@cineir.edu)'}
    url = f"https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(movie_name + ' film')}&gsrlimit=1&prop=pageimages&pithumbsize=500&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, pdata in pages.items():
                print(f"Matched page: {pdata.get('title')}")
                if 'thumbnail' in pdata:
                    return pdata['thumbnail']['source']
    except Exception as e:
        print(f"Error: {e}")
    return None

print("Baahubali:", search_wiki_image("Baahubali: The Beginning"))
print("RRR:", search_wiki_image("RRR"))
print("Pushpa:", search_wiki_image("Pushpa: The Rise"))
