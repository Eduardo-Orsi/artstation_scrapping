

class TransformArtistsUrls:

    @staticmethod
    def transform(artist_urls: list[str]) -> list[tuple]:
        transform_result = []
        for url in artist_urls:
            transform_result.append(
                (url, False)
            )
        return transform_result
