import urllib.request
import json
import urllib.parse
import re

headers = {'User-Agent': 'CineIR-Tollywood/1.0 (academic; student@project.org)'}

def fetch_wiki_poster_url(film_title):
    try:
        # Search for page
        s_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(film_title + ' film')}&format=json"
        req = urllib.request.Request(s_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as r:
            res = json.loads(r.read().decode('utf-8'))
        
        search_results = res.get('query', {}).get('search', [])
        if not search_results:
            return None
        page_title = search_results[0]['title']
        
        # Get images on this page
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=images&format=json"
        req2 = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=5) as r2:
            res2 = json.loads(r2.read().decode('utf-8'))
        
        pages = res2.get('query', {}).get('pages', {})
        target_image_title = None
        for pid, pdata in pages.items():
            for img in pdata.get('images', []):
                iname = img.get('title', '')
                if any(x in iname.lower() for x in ['poster', 'theatrical', 'release', 'cover', 'title', 'soundtrack', film_title.lower()[:5]]):
                    target_image_title = iname
                    break
            if not target_image_title and pdata.get('images'):
                target_image_title = pdata['images'][0].get('title')

        if not target_image_title:
            return None

        # Get file url for this image
        info_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(target_image_title)}&prop=imageinfo&iiprop=url&format=json"
        req3 = urllib.request.Request(info_url, headers=headers)
        with urllib.request.urlopen(req3, timeout=5) as r3:
            res3 = json.loads(r3.read().decode('utf-8'))
        
        ipages = res3.get('query', {}).get('pages', {})
        for pid, pdata in ipages.items():
            if 'imageinfo' in pdata and len(pdata['imageinfo']) > 0:
                return pdata['imageinfo'][0].get('url')
    except Exception as e:
        print(f"Error for {film_title}: {e}")
    return None

test_movies = ["Baahubali: The Beginning", "Magadheera", "Eega", "Jersey", "Mahanati", "Sita Ramam"]
for tm in test_movies:
    url = fetch_wiki_poster_url(tm)
    print(f"{tm} -> {url}")
