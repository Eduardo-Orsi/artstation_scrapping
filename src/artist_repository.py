import sqlite3 as db

import pandas as pd


class ArtistRepository:

    def __init__(self) -> None:
        self.__conn = db.connect("data/test.db")
        self.__cursor = self.__conn.cursor()
        self.__user_id = None

    def insert_artist(self, artist: dict) -> None:
        skills_list = artist['skills_list']
        del artist['skills_list']
        software_items = artist["software_items"]
        del artist["software_items"]
        social_profiles = artist['social_profiles']
        del artist['social_profiles']
        self.__user_id = self.__insert_artist(artist)
        self.__insert_softwares_items(software_items)
        self.__insert_social_profiles(social_profiles)
        self.__insert_skills(skills_list)
        self.__conn.commit()
        self.__conn.close()

    def __insert_artist(self, artist: dict) -> int | None:
        columns = ', '.join(artist.keys())
        placeholders = ', '.join('?' * len(artist))
        values = tuple(artist.values())
        self.__cursor.execute(f"INSERT INTO users ({columns}) VALUES ({placeholders})", values)
        return self.__cursor.lastrowid

    def __insert_skills(self, skills: list[dict]) -> None:
        for skill in skills:
            self.__cursor.execute("INSERT INTO skills (user_id, name) VALUES (?, ?)", (self.__user_id, skill['name']))

    def __insert_softwares_items(self, software_items: list[dict]) -> None:
        for software_item in software_items:
            self.__cursor.execute("INSERT INTO software_items (user_id, icon_url, name) VALUES (?, ?, ?)",
                                  (self.__user_id, software_item['icon_url'], software_item['name']))

    def __insert_social_profiles(self, social_profiles: list[dict]) -> None:
        for social_profile in social_profiles:
            self.__cursor.execute("INSERT INTO social_profiles (user_id, url, social_network, position) VALUES (?, ?, ?, ?)",
                                  (self.__user_id, social_profile['url'], social_profile['social_network'], social_profile['position']))

    def insert_artists_urls(self, artists_urls: list[tuple]) -> None:
        for url in artists_urls:
            self.__cursor.execute("INSERT INTO artist_urls (url, scrapped) VALUES (?, ?)", url)
        self.__conn.commit()
        self.__conn.close()

    def exists(self, username: str) -> bool:
        row = self.__cursor.execute("SELECT username FROM users WHERE username=?", [username]).fetchall()
        if not row:
            return False
        return True

    def get_missing_urls(self) -> list[str]:
        self.__cursor.execute("SELECT url FROM artist_urls WHERE scrapped != true;")
        urls_to_scrape = self.__cursor.fetchall()
        return urls_to_scrape

    def close(self) -> None:
        self.__conn.close()
