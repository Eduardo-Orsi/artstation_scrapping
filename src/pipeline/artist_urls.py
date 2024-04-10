from extract.extract_artist_urls import ExtractArtistsUrls
from transform.transform_artist_urls import TransformArtistsUrls
from load.load_artists_urls import LoadArtistsUrls
from artist_repository import ArtistRepository


class ArtistUrlPipeline:

    @staticmethod
    def main(cookie: str):
        artist_repository = ArtistRepository()
        urls_extract = ExtractArtistsUrls(cookie=cookie)
        urls_transform = TransformArtistsUrls()
        urls_load = LoadArtistsUrls(artist_repository)
        artists_urls = urls_extract.get_artists_urls()
        urls = urls_transform.transform(artists_urls)
        urls_load.load(urls)
        print("URLs Pipeline Done!")
