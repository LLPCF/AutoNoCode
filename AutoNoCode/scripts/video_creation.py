import logging
logger = logging.getLogger(__name__)
import sys
import moviepy.editor as mp
import google_auth_oauthlib.flow  # type: ignore
import google_auth_oauthlib  # type: ignore
import googleapiclient.discovery  # type: ignore
import googleapiclient.errors  # type: ignore
import googleapiclient.http  # type: ignore

from moviepy.editor import *  # type: ignore

# video_creation.py

from moviepy.editor import VideoFileClip, concatenate_videoclips  # type: ignore

# Restante do código


def create_video(output_path: str) -> None:
    try:
        clip = mp.ColorClip(size=(640, 480), color=(255, 0, 0), duration=10)
        clip.write_videofile(output_path, codec="libx264")
        print(f"Video successfully created at {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    output_path = "output_video.mp4"
    create_video(output_path)
