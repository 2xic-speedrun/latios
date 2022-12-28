from .Html import Html
from typing import Union
import requests
from bs4 import BeautifulSoup
from ..helpers.Metadata import Metadata
from ..helpers.get_netloc import get_netloc

class HttpHtml(Html):
    def fetch_text(self, url) -> Union[Metadata, None]:
        soup = self._give_me_soup(url)
        if soup is None:
            return None
        
        return {
            "text": self._give_me_the_text(soup),
            "title": self._give_me_title(soup),
            "netloc": get_netloc(url)
        }

    def _give_me_soup(self, url):
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, features="html.parser")
            return soup
        except Exception as e:
            print(e)
            return None

    def _give_me_title(self, soup):
        return " ".join(list(map(lambda x: x.text, soup.find_all("title"))))

    def _give_me_the_text(self, soup):
       return "\n".join(list(map(lambda x: x.text, soup.find_all("p", text=True))))
