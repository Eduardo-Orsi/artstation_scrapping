import re
import sqlite3
from typing import Iterable

import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup
from requests.exceptions import SSLError

from artist_repository import ArtistRepository


def get_artists_url(artists_sitemaps: list[str]) -> list[str]:
    scrapper = cloudscraper.create_scraper()
    all_artists_url = []
    for sitemap in artists_sitemaps:
        sitemap = scrapper.get(sitemap)
        soup = BeautifulSoup(sitemap.text, 'html.parser')
        artists_url = [url.text for url in soup.find_all("loc")]
        all_artists_url.extend(artists_url)
    return all_artists_url

def get_artists_sitemaps() -> list[str]:
    base_sitemap_url = 'https://www.artstation.com/sitemap.xml'
    scraper = cloudscraper.create_scraper()
    sitemap_xml = scraper.get(base_sitemap_url, timeout=None)
    soup = BeautifulSoup(sitemap_xml.text, 'html.parser')
    all_sitemaps = soup.find_all("loc")
    artists_sitemap_urls = []
    pattern = r"https://www.artstation.com/sitemap-artists-\d+\.xml"
    for sitemap in all_sitemaps:
        artist_sitemap = re.match(pattern, sitemap.text)
        if artist_sitemap:
            artists_sitemap_urls.append(sitemap.text)
    return artists_sitemap_urls

def scrappe_profile_data(artist_urls: Iterable[str]) -> None:
    scrapper = cloudscraper.create_scraper(delay=15, browser={'custom': 'ScraperBot/1.0'})
    headers= {
        'cookie': 'YOUR COOKIE GOES HERE'
    }
    for artist_url in artist_urls:
        artist_username = artist_url.split("/")[-1]
        artist_repository = ArtistRepository()
        if artist_repository.exists(artist_username):
            print(f"EXISTS - {artist_username}")
            artist_repository.close()
            continue
        artist = {}
        try:
            response = scrapper.get(f"https://www.artstation.com/users/{artist_username}.json",
                                    headers=headers)

            print(f"JSON - {artist_username} - {response.status_code}")
            if response.status_code != 200:
                continue
            response = response.json()

            artist["id"] = response.get("id", None)
            artist["username"] = response.get("username", None)
            artist["email"] = None
            artist["full_name"] = response.get("full_name", None)
            artist["first_name"] = response.get("first_name", None)
            artist["last_name"] = response.get("last_name", None)
            artist["headline"] = response.get("headline", None)
            artist["skills"] = clean_skills(response.get("skills", None))
            artist["skills_list"] = response.get("skills", None)
            artist["software_items"] = response.get("software_items", None)
            artist["social_profiles"] = response.get("social_profiles", None)
            artist["projects_count"] = response.get("projects_count", None)
            artist["city"] = response.get("city", None)
            artist["country"] = response.get("country", None)
            artist["resume_url"] = response["portfolio"].get("resume_url", None)
            artist["twitter_url"] = response.get("twitter_url", None)
            artist["facebook_url"] = response.get("facebook_url", None)
            artist["tumblr_url"] = response.get("tumblr_url", None)
            artist["deviantart_url"] = response.get("deviantart_url", None)
            artist["linkedin_url"] = response.get("linkedin_url", None)
            artist["instagram_url"] = response.get("instagram_url", None)
            artist["pinterest_url"] = response.get("pinterest_url", None)
            artist["youtube_url"] = response.get("youtube_url", None)
            artist["vimeo_url"] = response.get("vimeo_url", None)
            artist["behance_url"] = response.get("behance_url", None)
            artist["steam_url"] = response.get("steam_url", None)
            artist["sketchfab_url"] = response.get("sketchfab_url", None)
            artist["twitch_url"] = response.get("twitch_url", None)
            artist["imdb_url"] = response.get("imdb_url", None)
            artist["website_url"] = response.get("website_url", None)

            if response.get("has_public_email", None):
                try:
                    html_response = scrapper.get(f"https://{artist_username}.artstation.com/resume")
                    print(f"HTML - {artist_username} - {html_response.status_code}")
                    soup = BeautifulSoup(html_response.text, 'html.parser')
                    try:
                        artist["email"] = soup.find("div", "about-email").find("a").text
                    except AttributeError:
                        print(f"NO EMAIL - {artist_username}")
                except SSLError:
                    print("Erro SSL")
                except:
                    print("Some random error")
            artist_repository.insert_artist(artist)
            print(f"INSERTED - {artist_username}")
        except Exception as e:
            print(f"ERROR - {e}")
            return

def clean_skills(skills: list[dict[str, str]]) -> str:
    skills_str = ""
    for skill in skills:
        skills_str = skills_str + f"{skill.get("name", None)} - "
    return skills_str

def load_artists_urls_from_csv(csv_path: str) -> list[str]:
    df_urls = pd.read_csv(csv_path)
    return df_urls["artist_url"].to_list()

def get_missing_urls(db_path: str) -> set[str]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT username FROM users;")
    existing_urls = [f"https://www.artstation.com/{row[0]}" for row in c.fetchall()]
    df_urls = pd.read_csv("data/artistis_urls.csv")
    csv_urls = set(df_urls['artist_url'].dropna().tolist())
    urls_to_scrape = csv_urls - set(existing_urls)
    print(f"Scrapped: {len(existing_urls)}")
    print(f"Not Scrapped: {len(urls_to_scrape)}")
    print(f"Total of URLS: {len(csv_urls)}")
    return urls_to_scrape


if __name__ == "__main__":

    # artists_urls = load_artists_urls_from_csv("data/artistis_urls.csv")
    artists_urls = get_missing_urls('data/result.db')
    scrappe_profile_data(artists_urls)
