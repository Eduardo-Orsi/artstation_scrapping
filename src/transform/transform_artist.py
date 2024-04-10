from bs4 import BeautifulSoup


class TransformArtist:

    def __init__(self) -> None:
        self.__artist_json = {}

    def transform(self, extracted_data : dict) -> dict:
        self.__get_json_data(extracted_data.get("json", None))
        self.__get_artist_email(extracted_data.get("html", None))
        return self.__artist_json

    def __get_artist_email(self, html_content: str) -> None:
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            self.__artist_json["email"] = soup.find("div", "about-email").find("a").text
        except AttributeError:
            print(f"NO EMAIL IN HTML")

    def __get_json_data(self, artist: dict) -> None:
        self.__artist_json = {}
        self.__artist_json["id"] = artist.get("id", None)
        self.__artist_json["username"] = artist.get("username", None)
        self.__artist_json["email"] = None
        self.__artist_json["full_name"] = artist.get("full_name", None)
        self.__artist_json["first_name"] = artist.get("first_name", None)
        self.__artist_json["last_name"] = artist.get("last_name", None)
        self.__artist_json["headline"] = artist.get("headline", None)
        self.__artist_json["skills"] = self.__clean_skills(artist.get("skills", None))
        self.__artist_json["skills_list"] = artist.get("skills", None)
        self.__artist_json["software_items"] = artist.get("software_items", None)
        self.__artist_json["social_profiles"] = artist.get("social_profiles", None)
        self.__artist_json["projects_count"] = artist.get("projects_count", None)
        self.__artist_json["city"] = artist.get("city", None)
        self.__artist_json["country"] = artist.get("country", None)
        self.__artist_json["resume_url"] = artist["portfolio"].get("resume_url", None)
        self.__artist_json["twitter_url"] = artist.get("twitter_url", None)
        self.__artist_json["facebook_url"] = artist.get("facebook_url", None)
        self.__artist_json["tumblr_url"] = artist.get("tumblr_url", None)
        self.__artist_json["deviantart_url"] = artist.get("deviantart_url", None)
        self.__artist_json["linkedin_url"] = artist.get("linkedin_url", None)
        self.__artist_json["instagram_url"] = artist.get("instagram_url", None)
        self.__artist_json["pinterest_url"] = artist.get("pinterest_url", None)
        self.__artist_json["youtube_url"] = artist.get("youtube_url", None)
        self.__artist_json["vimeo_url"] = artist.get("vimeo_url", None)
        self.__artist_json["behance_url"] = artist.get("behance_url", None)
        self.__artist_json["steam_url"] = artist.get("steam_url", None)
        self.__artist_json["sketchfab_url"] = artist.get("sketchfab_url", None)
        self.__artist_json["twitch_url"] = artist.get("twitch_url", None)
        self.__artist_json["imdb_url"] = artist.get("imdb_url", None)
        self.__artist_json["website_url"] = artist.get("website_url", None)

    def __clean_skills(self, skills: list[dict[str, str]]) -> str:
        skills_str = ""
        for skill in skills:
            skills_str = skills_str + f"{skill.get("name", None)} - "
        return skills_str
