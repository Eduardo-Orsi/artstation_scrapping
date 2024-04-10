import cloudscraper

from artist_repository import ArtistRepository


class ExtractArtist:

    json_url = "https://www.artstation.com/users/{}.json"
    html_url = "https://{}.artstation.com/resume"

    def __init__(self, cookie: str) -> None:
        self.__scrapper = cloudscraper.create_scraper(delay=15, browser={'custom': 'ScraperBot/1.0'})
        self.__headers= {
            'cookie': cookie
        }

    def extract(self, artist_url: str) -> dict:
        artist_username = artist_url.split("/")[-1]
        result = {"json": None, "html": None}
        repository = ArtistRepository()

        if repository.exists(artist_username):
            print(f"EXISTS - {artist_username}")
            repository.close()
            return {}

        json_response = self.__request_json(artist_username)
        if not json_response:
            return {}

        result["json"] = json_response
        has_public_email = json_response.get("has_public_email", None)
        if not has_public_email:
            return result

        html_response = self.__request_html(artist_username)
        if not html_response:
            return result

        result["html"] = html_response
        return result

    def __request_json(self, artist_username: str) -> dict | None:
        try:
            response = self.__scrapper.get(self.json_url.format(artist_username), headers=self.__headers)
            print(f"JSON - {artist_username} - {response.status_code}")
            if response.status_code != 200:
                return

            return response.json()
        except Exception as ex:
            print(f"ERROR - {artist_username} - {ex}")
            return

    def __request_html(self, artist_username: str) -> str | None:
        try:
            response = self.__scrapper.get(self.html_url.format(artist_username), headers=self.__headers)
            print(f"HTML - {artist_username} - {response.status_code}")
            if response.status_code != 200:
                return
            return response.text
        except Exception as ex:
            print(f"ERROR - {artist_username} - {ex}")
            return
