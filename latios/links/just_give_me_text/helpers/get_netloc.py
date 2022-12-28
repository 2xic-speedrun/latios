from urllib.parse import urlparse

def get_netloc(url):
    return urlparse(url).netloc.replace("www", "")
