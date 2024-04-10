from load.load_artist import LoadArtist
from artist_repository import ArtistRepository
from extract.extract_artist import ExtractArtist
from transform.transform_artist import TransformArtist

class ArtistPipeline:

    @staticmethod
    def main(cookie: str) -> None:
        artist_repository = ArtistRepository()
        not_scrapped_urls = artist_repository.get_missing_urls()

        artist_extract = ExtractArtist(cookie=cookie)
        load_artist = LoadArtist()

        for url in not_scrapped_urls:
            scrapped_data = artist_extract.extract(url)
            transform_artist = TransformArtist()
            artist_data = transform_artist.transform(scrapped_data)
            load_artist.load(artist_data)
            del transform_artist
        print("Main Pipeline Done!")
