import requests
import time
import argparse
from bs4 import BeautifulSoup

def check_username(username, platforms):
 
    results = []

    for platform, url_template in platforms.items():
        url = url_template.format(username=username)
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            if platform == 'Instagram':
                profile_img = soup.find('meta', property='og:image')
                profile_title = soup.find('meta', property='og:title')
                if profile_img or (profile_title and username in profile_title['content']):
                    results.append((platform, f"found: {url}"))
                else:
                    results.append((platform, 'not found'))
            elif platform == 'Twitter':
                profile_img = soup.find('meta', property='og:image')
                profile_title = soup.find('meta', property='og:title')
                if profile_img or (profile_title and username in profile_title['content']):
                    results.append((platform, f"found: {url}"))
                else:
                    results.append((platform, 'not found'))
            elif platform == 'Facebook':
                profile_img = soup.find('meta', property='og:image')
                profile_title = soup.find('meta', property='og:title')
                if profile_img or (profile_title and username in profile_title['content']):
                    results.append((platform, f"found: {url}"))
                else:
                    results.append((platform, 'not found'))
            elif platform == 'GitHub':
                profile_img = soup.find('meta', property='og:image')
                profile_title = soup.find('meta', property='og:title')
                if profile_img or (profile_title and username in profile_title['content']):
                    results.append((platform, f"found: {url}"))
                else:
                    results.append((platform, 'not found'))
            elif platform == 'Linkedin':
                profile_img = soup.find('meta', property='og:image')
                profile_title = soup.find('meta', property='og:title')
                search_results = soup.find('div', class_='search-results__list')
                if profile_img or (profile_title, search_results and username in profile_title['content']):
                    results.append((platform, f"found: {url}"))
                else:
                    results.append((platform, 'not found'))
            else:
                results.append((platform, "Platform not supported"))

        except requests.exceptions.RequestException as e:
            results.append((platform, f"Error: {e}"))

        time.sleep(2) 

    return results



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check username availability on social media platforms")
    parser.add_argument("username", help="The username to check")
    args = parser.parse_args()

    platforms = {
        "Instagram": "https://www.instagram.com/{username}/",
        "Twitter": "https://twitter.com/{username}",
        "GitHub": "https://github.com/{username}",
        "Facebook": "https://www.facebook.com/{username}",
        "Linkedin": "https://www.linkedin.com/in/{username}",
        
    }

    results = check_username(args.username, platforms)

    print("Ergebnisse:")
    for platform, result in results:
        print(f"{platform}: {result}")