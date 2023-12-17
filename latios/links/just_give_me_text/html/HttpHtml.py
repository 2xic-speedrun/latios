from .Html import Html
from typing import Union
import requests
from bs4 import BeautifulSoup
from ..helpers.Metadata import Metadata
from ..helpers.get_netloc import get_netloc
from urllib.parse import urljoin
import validators


class HttpHtml(Html):
    def fetch_metadata(self, url) -> Union[Metadata, None]:
        soup = self._give_me_soup(url)
        if soup is None:
            return None

        return {
            "text": self._give_me_the_text(soup),
            "title": self._give_me_title(soup),
            "netloc": get_netloc(url),
            "links": self._get_links(soup, url)
        }

    def _give_me_soup(self, url):
        try:
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
            }, timeout=10)
            print(response.status_code)
            html = response.text
            soup = BeautifulSoup(html, features="html.parser")
            return soup
        except Exception as e:
            print(e)
            return None

    def _get_links(self, soup, url):
        return list(filter(lambda x: validators.url(x), list(map(lambda x: str(urljoin(url, x['href'])), soup.find_all("a", href=True)))))

    def _give_me_title(self, soup):
        return " ".join(list(map(lambda x: x.text, soup.find_all("title"))))

    def _give_me_the_text(self, soup):
        return "\n".join(list(map(lambda x: x.text, soup.find_all("p", text=True))))
