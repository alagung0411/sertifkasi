import requests
from bs4 import BeautifulSoup

# Ganti dengan URL halaman yang berisi kumpulan lagu atau album
url = 'https://open.spotify.com/album/1hrJXgaVEGovpLl9dFdqz7'  # Ganti dengan URL lagu/album yang relevan

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# Mencari meta tag yang berisi informasi lagu/album
og_image = soup.select_one('meta[property="og:image"]')
og_title = soup.select_one('meta[property="og:title"]')
og_description = soup.select_one('meta[property="og:description"]')

if og_image:
    image = og_image['content']
    print("Image URL:", image)

if og_title:
    title = og_title['content']
    print("Title:", title)

if og_description:
    description = og_description['content']
    print("Description:", description)
