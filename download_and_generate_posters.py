"""
Download authentic poster images for movies from Wikipedia and generate
individualized cinematic SVG poster fallbacks for all 50 movies in static/images/.
"""

import os
import sys
import re
import json
import urllib.request
import urllib.parse
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")
CSV_PATH = os.path.join(BASE_DIR, "movies.csv")

os.makedirs(STATIC_IMG_DIR, exist_ok=True)
df = pd.read_csv(CSV_PATH)

HEADERS = {'User-Agent': 'CineIR-Tollywood/2.0 (academic IRS project; contact@cineir.edu)'}

# Genre theme colors for SVG generation
GENRE_THEMES = {
    "action": {"primary": "#e50914", "secondary": "#1a0507", "accent": "#ff5252", "icon": "sword"},
    "fantasy": {"primary": "#d4af37", "secondary": "#1c1405", "accent": "#ffd700", "icon": "crown"},
    "mythology": {"primary": "#ff9800", "secondary": "#1c0d02", "accent": "#ffb74d", "icon": "temple"},
    "historical": {"primary": "#c59b27", "secondary": "#191408", "accent": "#ffe082", "icon": "shield"},
    "crime": {"primary": "#00e676", "secondary": "#061a0f", "accent": "#69f0ae", "icon": "gun"},
    "thriller": {"primary": "#00b0ff", "secondary": "#051624", "accent": "#80d8ff", "icon": "radar"},
    "mystery": {"primary": "#7c4dff", "secondary": "#120a26", "accent": "#b388ff", "icon": "eye"},
    "horror": {"primary": "#9c27b0", "secondary": "#18051f", "accent": "#e040fb", "icon": "skull"},
    "romance": {"primary": "#ff4081", "secondary": "#210511", "accent": "#ff80ab", "icon": "heart"},
    "comedy": {"primary": "#ffeb3b", "secondary": "#211f05", "accent": "#fff59d", "icon": "smile"},
    "drama": {"primary": "#00e5ff", "secondary": "#041b21", "accent": "#84ffff", "icon": "theater"},
    "sport": {"primary": "#00e676", "secondary": "#061a0e", "accent": "#b9f6ca", "icon": "trophy"},
    "sci-fi": {"primary": "#00e5ff", "secondary": "#021a24", "accent": "#18ffff", "icon": "rocket"},
    "adventure": {"primary": "#ff9100", "secondary": "#241202", "accent": "#ffd180", "icon": "compass"}
}

def get_theme(genres_str):
    g_lower = genres_str.lower()
    for key, theme in GENRE_THEMES.items():
        if key in g_lower:
            return theme
    return {"primary": "#00e676", "secondary": "#0a1410", "accent": "#69f0ae", "icon": "film"}

def generate_svg_poster(row, target_path):
    title = str(row["title"])
    year = str(row["release_year"])
    rating = str(row["rating"])
    director = str(row["director"])
    cast = str(row["cast"])
    genre = str(row["genre"])
    category = str(row["category"])
    
    theme = get_theme(genre)
    p_color = theme["primary"]
    bg_color = theme["secondary"]
    acc_color = theme["accent"]

    # Wrap title into 2-3 lines
    words = title.split()
    lines = []
    curr = []
    for w in words:
        if len(" ".join(curr + [w])) <= 16:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    lines = lines[:3]

    title_svg_lines = ""
    y_start = 420 - (len(lines) * 20)
    for i, line in enumerate(lines):
        title_svg_lines += f'<text x="250" y="{y_start + (i * 44)}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1">{line.upper()}</text>\n'

    # Clean director & cast for safe SVG XML
    safe_director = director.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_cast = ", ".join(cast.split(",")[:3]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_genre = genre.split(",")[0].strip()

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 750" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}"/>
      <stop offset="60%" stop-color="#0a0f16"/>
      <stop offset="100%" stop-color="#05080c"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{p_color}"/>
      <stop offset="100%" stop-color="{acc_color}"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="500" height="750" fill="url(#bgGrad)"/>
  
  <!-- Subtle Cinematic Atmospheric Elements -->
  <circle cx="250" cy="220" r="160" fill="{p_color}" opacity="0.12" filter="url(#glow)"/>
  <circle cx="250" cy="220" r="120" fill="none" stroke="{p_color}" stroke-width="2" stroke-dasharray="8 6" opacity="0.35"/>
  <circle cx="250" cy="220" r="95" fill="none" stroke="{acc_color}" stroke-width="1" opacity="0.25"/>

  <!-- Center Decorative Emblem -->
  <g transform="translate(250, 220)">
    <!-- Outer Shield/Badge -->
    <polygon points="0,-60 52,-25 52,35 0,65 -52,35 -52,-25" fill="{bg_color}" stroke="{p_color}" stroke-width="3" opacity="0.9"/>
    <!-- Inner Icon -->
    <circle cx="0" cy="0" r="32" fill="{p_color}" opacity="0.15"/>
    <text x="0" y="8" font-family="-apple-system, sans-serif" font-size="28" font-weight="900" fill="{acc_color}" text-anchor="middle">&#9733;</text>
  </g>

  <!-- Top Category Banner -->
  <rect x="30" y="30" width="130" height="28" rx="6" fill="{p_color}" opacity="0.9"/>
  <text x="95" y="49" font-family="-apple-system, sans-serif" font-size="12" font-weight="800" fill="#05080c" text-anchor="middle" letter-spacing="1">{category.upper()}</text>

  <!-- Top Right Rating Badge -->
  <rect x="370" y="30" width="100" height="28" rx="6" fill="#131c26" stroke="#ffc107" stroke-width="1.5"/>
  <text x="420" y="49" font-family="-apple-system, sans-serif" font-size="12" font-weight="800" fill="#ffc107" text-anchor="middle">&#9733; {rating} IMDb</text>

  <!-- Middle Divider Glow -->
  <line x1="80" y1="340" x2="420" y2="340" stroke="{p_color}" stroke-width="1.5" opacity="0.4"/>

  <!-- Movie Title Lines -->
  {title_svg_lines}

  <!-- Year and Primary Genre -->
  <text x="250" y="{y_start + (len(lines) * 44) + 12}" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="{acc_color}" text-anchor="middle" letter-spacing="2">
    {year} &bull; {safe_genre.upper()}
  </text>

  <!-- Director & Cast Panel -->
  <rect x="40" y="580" width="420" height="110" rx="10" fill="#0d141d" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="250" y="612" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" fill="#8b949e" text-anchor="middle" letter-spacing="1">DIRECTED BY</text>
  <text x="250" y="632" font-family="-apple-system, sans-serif" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">{safe_director.upper()}</text>
  <text x="250" y="658" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" fill="#8b949e" text-anchor="middle" letter-spacing="1">STARRING</text>
  <text x="250" y="676" font-family="-apple-system, sans-serif" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">{safe_cast}</text>

  <!-- Bottom Accent Line -->
  <rect x="0" y="744" width="500" height="6" fill="url(#accentGrad)"/>
  
  <!-- Outer Glow Border -->
  <rect x="10" y="10" width="480" height="730" rx="14" fill="none" stroke="{p_color}" stroke-width="1.5" opacity="0.3"/>
</svg>'''

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

def search_wikipedia_image_url(film_title):
    try:
        query = f"{film_title} film"
        s_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
        req = urllib.request.Request(s_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as r:
            res = json.loads(r.read().decode('utf-8'))
        
        search_results = res.get('query', {}).get('search', [])
        if not search_results:
            return None
        page_title = search_results[0]['title']
        
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=images&format=json"
        req2 = urllib.request.Request(img_url, headers=HEADERS)
        with urllib.request.urlopen(req2, timeout=5) as r2:
            res2 = json.loads(r2.read().decode('utf-8'))
        
        pages = res2.get('query', {}).get('pages', {})
        target_image_title = None
        for pid, pdata in pages.items():
            for img in pdata.get('images', []):
                iname = img.get('title', '')
                if any(x in iname.lower() for x in ['poster', 'theatrical', 'release', 'cover', 'soundtrack', film_title.lower()[:5]]):
                    target_image_title = iname
                    break
            if not target_image_title and pdata.get('images'):
                target_image_title = pdata['images'][0].get('title')

        if not target_image_title:
            return None

        info_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(target_image_title)}&prop=imageinfo&iiprop=url&format=json"
        req3 = urllib.request.Request(info_url, headers=HEADERS)
        with urllib.request.urlopen(req3, timeout=5) as r3:
            res3 = json.loads(r3.read().decode('utf-8'))
        
        ipages = res3.get('query', {}).get('pages', {})
        for pid, pdata in ipages.items():
            if 'imageinfo' in pdata and len(pdata['imageinfo']) > 0:
                raw_url = pdata['imageinfo'][0].get('url')
                return raw_url
    except Exception as e:
        pass
    return None

def download_image(url, target_path):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            if len(data) > 3000:  # Valid image size
                with open(target_path, "wb") as f:
                    f.write(data)
                return True
    except Exception as e:
        pass
    return False

print("Processing posters for all 50 movies...")

updated_poster_urls = []

for idx, row in df.iterrows():
    movie_id = int(row["id"])
    title = row["title"]
    
    jpg_filename = f"poster_{movie_id}.jpg"
    svg_filename = f"poster_{movie_id}.svg"
    
    jpg_path = os.path.join(STATIC_IMG_DIR, jpg_filename)
    svg_path = os.path.join(STATIC_IMG_DIR, svg_filename)
    
    # 1. Always generate the individualized, bespoke SVG poster
    generate_svg_poster(row, svg_path)
    
    # 2. Try fetching and downloading the authentic photo/poster from Wikipedia
    downloaded = False
    if not os.path.exists(jpg_path) or os.path.getsize(jpg_path) < 3000:
        wiki_img_url = search_wikipedia_image_url(title)
        if wiki_img_url:
            downloaded = download_image(wiki_img_url, jpg_path)
    else:
        downloaded = True

    if downloaded and os.path.exists(jpg_path) and os.path.getsize(jpg_path) > 3000:
        print(f"[{movie_id}/50] {title}: Downloaded authentic poster -> {jpg_filename}")
        updated_poster_urls.append(f"/static/images/{jpg_filename}")
    else:
        print(f"[{movie_id}/50] {title}: Generated bespoke cinematic poster -> {svg_filename}")
        updated_poster_urls.append(f"/static/images/{svg_filename}")

# Update movies.csv with local guaranteed URLs
df["poster_url"] = updated_poster_urls
df.to_csv(CSV_PATH, index=False)
print("\nSuccessfully updated movies.csv with local guaranteed posters!")
