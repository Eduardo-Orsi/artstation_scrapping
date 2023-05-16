from bs4 import BeautifulSoup
import cloudscraper
import re

scrapper = cloudscraper.create_scraper()

res = scrapper.get("https://www.artstation.com/sitemap.xml")
soup = BeautifulSoup(res.text, 'lxml')

links = soup.find_all("loc")
artists_sitemap_urls = []
pattern = r"https://www.artstation.com/sitemap-artists-\d+\.xml"
for link in links:
    link = re.match(pattern, link.text)
    if link:
        artists_sitemap_urls.append(link.string)

for url in artists_sitemap_urls:
    res = scrapper.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    links = soup.find_all('loc')

    for link in links:
        print(link.text)
