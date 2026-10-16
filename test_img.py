import urllib.request

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Baahubali_the_beginning_poster.jpg/220px-Baahubali_the_beginning_poster.jpg"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = resp.read()
        print("Success! Downloaded bytes:", len(data))
except Exception as e:
    print("Error:", e)
