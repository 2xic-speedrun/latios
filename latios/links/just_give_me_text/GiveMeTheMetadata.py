from urllib.parse import urlparse
from .CheckContentType import CheckContentType
import argparse
from .html.HttpHtml import HttpHtml
from .youtube.HttpYouTube import HttpYouTube
from .documents.DocumentsParser import DocumentParser
import requests
from bs4 import BeautifulSoup
from .helpers.get_netloc import get_netloc

class GiveMeTheMetadata:
    def __init__(self):
        pass

    def get_metadata(self, url):
        skip_links = {
            "youtube.com": HttpYouTube().fetch_transcript,
            "github.com": None
        }

        netloc = urlparse(url).netloc.replace("www.", "")
        if netloc in skip_links:
            datasource = skip_links[netloc]
            if datasource is None:
                return None
            return datasource(url)

        if ".pdf" in url:
            return DocumentParser().process(url)
        elif ".zip" in url:
            return None
        elif ".tgz" in url:
            return None
        elif ".tar" in url:
            return None
        elif url.endswith("feed.xml"):
            html_page = requests.get(url, headers={
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
            })
            soup = BeautifulSoup(html_page.text, "lxml")
            links = []
            for item in soup.find_all("item"):
                link= str(item)
                i = link.find("<link/>")
                j = link.find("<guid")
                links.append( link[i+7:j] )        
            return {
                "text": None,
                "title": "feed.xml",
                "netloc": get_netloc(url),
                "links": links
            }


        has_valid_header = CheckContentType().has_valid_header(url)
        if not has_valid_header:
            return None
        
        return HttpHtml().fetch_metadata(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog = 'GiveMeTheMetadata'
    )
    parser.add_argument('-u', '--url', required=True)
    args = parser.parse_args()
    
    print(GiveMeTheMetadata().get_metadata(args.url))
