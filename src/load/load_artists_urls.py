import sqlite3 as db

from artist_repository import ArtistRepository


class LoadArtistsUrls:

    def __init__(self, repository: ArtistRepository) -> None:
        self.__repository = repository

    def load(self, artists_urls: list[tuple]) -> None:
        self.__repository.insert_artists_urls(artists_urls)
