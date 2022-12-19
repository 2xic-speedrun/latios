from urllib.parse import urlparse
import requests
from .CheckContentType import CheckContentType
from bs4 import BeautifulSoup


class GiveMeTheMetadata:
    def __init__(self):
        pass

    def get_metadata(self, url):
        skip_links = [
            "youtube.com",
            
        ]
        netloc = urlparse(url).netloc.replace("www.", "")
        if netloc in skip_links:
            return None
        elif ".pdf" in skip_links:
            return None
        elif ".zip" in skip_links:
            return None
        has_valid_header = CheckContentType().has_valid_header(url)

        if not has_valid_header:
            return None
        soup = self.give_me_soup(url)
        if soup is None:
            return None

        return {
            "text": self.give_me_the_text(soup),
            "title": self.give_me_title(soup),
            "netloc": urlparse(url).netloc.replace("www", "")
        }

    def give_me_soup(self, url):
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, features="html.parser")
            return soup
        except Exception as e:
            print(e)
            return None

    def give_me_title(self, soup):
        return " ".join(list(map(lambda x: x.text, soup.find_all("title"))))

    def give_me_the_text(self, soup):
       return "\n".join(list(map(lambda x: x.text, soup.find_all("p", text=True))))
