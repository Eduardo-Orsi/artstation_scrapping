import re

import cloudscraper
from bs4 import BeautifulSoup


class ExtractArtistsUrls:

    base_sitemap_url = 'https://www.artstation.com/sitemap.xml'
    pattern = r"https://www.artstation.com/sitemap-artists-\d+\.xml"

    def __init__(self, cookie: str) -> None:
        self.__artists_sitemap_urls: list[str] = []
        self.__headers= {
            'cookie': cookie
        }

    def __get_artists_sitemaps(self) -> None:
        scraper = cloudscraper.create_scraper(delay=15, browser={'custom': 'ScraperBot/1.0'})
        sitemap_xml = scraper.get(self.base_sitemap_url, headers=self.__headers, timeout=None)
        soup = BeautifulSoup(sitemap_xml.text, 'html.parser')
        all_sitemaps = soup.find_all("loc")
        for sitemap in all_sitemaps:
            artist_sitemap = re.match(self.pattern, sitemap.text)
            if artist_sitemap:
                self.__artists_sitemap_urls.append(sitemap.text)

    def get_artists_urls(self) -> list[str]:
        self.__get_artists_sitemaps()
        scrapper = cloudscraper.create_scraper(delay=15, browser={'custom': 'ScraperBot/1.0'})
        all_artists_url = []
        for sitemap_url in self.__artists_sitemap_urls:
            sitemap = scrapper.get(sitemap_url, headers=self.__headers)
            soup = BeautifulSoup(sitemap.text, 'html.parser')
            artists_url = [url.text for url in soup.find_all("loc")]
            all_artists_url.extend(artists_url)
        return all_artists_url
