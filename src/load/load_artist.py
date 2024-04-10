from artist_repository import ArtistRepository

class LoadArtist:

    @staticmethod
    def load(artist_data: dict) -> None:
        artist_repository = ArtistRepository()
        return artist_repository.insert_artist(artist_data)
