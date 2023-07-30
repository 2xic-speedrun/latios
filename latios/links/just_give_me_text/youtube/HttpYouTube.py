from .Youtube import YouTube
from typing import Union
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import parse_qs
from urllib.parse import urlparse
from ..helpers.Metadata import Metadata
from ..helpers.get_netloc import get_netloc
from youtube_dl import YoutubeDL

class HttpYouTube(YouTube):
    def fetch_transcript(self, url) -> Union[Metadata, None]:
        try:
            video_id = self.get_video_id(url)
            if video_id is None:
                return None

            transcript = self._get_transcript(video_id)
            if transcript is None:
                return None

            text = transcript.fetch()
            text = " ".join(list(map(lambda x: x["text"], text)))
            title = None

            try:
                with YoutubeDL({}) as ydl:
                    obj = ydl.extract_info(url, download=False)
                    title = obj.get("title", None)    
            except Exception as e:
                print(e)

            return {
                "netloc": get_netloc(url),
                "title": title,
                "text": text,
            }
        except Exception as e:
            raise e

    def get_video_id(self, url):
        parsed_url = urlparse(url)
        video_ids = parse_qs(parsed_url.query).get("v")

        if video_ids is None or len(video_ids) == 0:
            return None

        video_id = video_ids[0]
        return video_id

    def _get_transcript(self, video_id):
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        has_manually_created = transcript_list._manually_created_transcripts.get(
            "en", None)

        if has_manually_created is not None:
            return has_manually_created

        has_automatically_created = transcript_list._generated_transcripts.get(
            "en", None)

        if has_automatically_created is not None:
            return has_automatically_created

        return None
