import time
import argparse
import requests
from bs4 import BeautifulSoup


class Crawly:
    def __init__(self, username):
        self.username = username
        self.results = []
        self.platforms = {
            "Instagram": {
                "url": "https://www.instagram.com/{username}/",
                "checker": self.check_profile_generic,
            },
            "X": {"url": "https://x.com/{username}", "checker": self.check_x},
            "GitHub": {
                "url": "https://github.com/{username}",
                "checker": self.check_profile_generic,
            },
            "Facebook": {
                "url": "https://www.facebook.com/{username}",
                "checker": self.check_profile_generic,
            },
            "Linkedin": {
                "url": "https://www.linkedin.com/in/{username}",
                "checker": self.check_linkedin,
            },
            "Pinterest": {
                "url": "https://www.pinterest.com/{username}/",
                "checker": self.check_profile_generic,
            },
            "Snapchat": {
                "url": "https://www.snapchat.com/add/{username}",
                "checker": self.check_profile_generic,
            },
            "Reddit": {
                "url": "https://www.reddit.com/user/{username}",
                "checker": self.check_profile_generic,
            },
            "Tumblr": {
                "url": "https://{username}.tumblr.com",
                "checker": self.check_profile_generic,
            },
            "Vimeo": {
                "url": "https://vimeo.com/{username}",
                "checker": self.check_profile_generic,
            },
            "Flickr": {
                "url": "https://www.flickr.com/photos/{username}/",
                "checker": self.check_profile_generic,
            },
            "Quora": {
                "url": "https://www.quora.com/profile/{username}",
                "checker": self.check_profile_generic,
            },
            "Steam": {
                "url": "https://steamcommunity.com/id/{username}",
                "checker": self.check_profile_generic,
            },
            "Spotify": {
                "url": "https://open.spotify.com/user/{username}",
                "checker": self.check_profile_generic,
            },
            "SoundCloud": {
                "url": "https://soundcloud.com/{username}",
                "checker": self.check_profile_generic,
            },
            "Medium": {
                "url": "https://medium.com/@{username}",
                "checker": self.check_profile_generic,
            },
            "Dribbble": {
                "url": "https://dribbble.com/{username}",
                "checker": self.check_profile_generic,
            },
        }

    def check_profile_generic(self, soup):
        profile_img = soup.find("meta", property="og:image")
        profile_title = soup.find("meta", property="og:title")
        return profile_img or (
            profile_title and self.username in profile_title["content"]
        )

    def check_linkedin(self, soup):
        profile_img = soup.find("meta", property="og:image")
        profile_title = soup.find("meta", property="og:title")
        search_results = soup.find("div", class_="search-results__list")
        return (
            profile_img
            or (profile_title and self.username in profile_title["content"])
            or search_results
        )

    def check_x(self, soup):
        title_tag = soup.find("title")
        if title_tag and self.username.lower() in title_tag.text.lower():
            return True
        error_tag = soup.find("div", {"class": "errorpage-topbar"})
        return not error_tag

    def check_username(self):
        for platform, info in self.platforms.items():
            url = info["url"].format(username=self.username)
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

                soup = BeautifulSoup(response.content, "html.parser")

                checker = info["checker"]
                if checker and checker(soup):
                    result = f"{platform}: found: {url}"
                else:
                    result = f"{platform}: not found"

            except requests.exceptions.RequestException as e:
                result = f"{platform}: Error: {e}"

            print(result)
            self.results.append((platform, result))
            time.sleep(0.2)

        return self.results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawly: Check username availability on social media platforms"
    )
    parser.add_argument("-u", "--username", help="The username to check")
    args = parser.parse_args()

    checker = Crawly(args.username)
    checker.check_username()
