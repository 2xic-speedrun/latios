from urllib.parse import urlparse
from .CheckContentType import CheckContentType
import argparse
from .html.HttpHtml import HttpHtml
from .youtube.HttpYouTube import HttpYouTube

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

        if ".pdf" in skip_links:
            return None
        elif ".zip" in skip_links:
            return None

        has_valid_header = CheckContentType().has_valid_header(url)

        if not has_valid_header:
            return None
        
        return HttpHtml().fetch_text(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog = 'GiveMeTheMetadata'
    )
    parser.add_argument('-u', '--url', required=True)
    args = parser.parse_args()
    
    print(GiveMeTheMetadata().get_metadata(args.url))
