import logging
logger = logging.getLogger(__name__)
import os
from typing import Any, Dict
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# video_upload.py

from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore

# Restante do código

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_file: str, title: str, description: str) -> None:
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "credentials/client_secret.json", scopes
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request_body: Dict[str, Any] = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": ["automatic", "upload", "video"],
        },
        "status": {"privacyStatus": "public"},
    }

    media_file = MediaFileUpload(video_file)
    request = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media_file
    )
    response = request.execute()
    print(f"Uploaded video with ID: {response['id']}")

if __name__ == "__main__":
    upload_video("output_video.mp4", "Automated Upload", "This video was uploaded automatically.")
