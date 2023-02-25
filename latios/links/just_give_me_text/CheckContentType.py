import requests


class CheckContentType:
    def has_valid_header(self, url):
        try:
            response = requests.head(url, timeout=5)
            has_valid_content_type = self.check_content_type(
                response.headers.get('Content-Type', None))
            has_valid_content_disposition = response.headers.get(
                'Content-Disposition', None) is None

            return has_valid_content_type and has_valid_content_disposition
        except Exception as e:
            print(e)
            return False

    def check_content_type(self, content_type):
        valid_types = ['text', 'html']
        for i in valid_types:
            if content_type and i in content_type:
                return True
        return False
