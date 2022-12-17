from urllib.parse import urlparse
import requests
from .CheckContentType import CheckContentType
from bs4 import BeautifulSoup

def give_me_the_text(url):
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

    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="html.parser")
        return "\n".join(list(map(lambda x: x.text, soup.find_all("p", text=True))))
    except Exception as e:
        print(e)
        return None
