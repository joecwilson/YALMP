import json
import os

from yalmp_scripts.constants import RATINGS_ATTRIBUTE
from yalmp_scripts.utils import get_albums


def fix_album(full_path: str):
    with open(full_path) as f:
        data = json.load(f)
        discs = data["discs"]
        for disc in discs:
            fix_discs(disc)


def fix_discs(disc_path: str):
    with open(disc_path) as f:
        disc = json.load(f)
        tracks = disc["tracks"]
        for track in tracks:
            try:
                fix_track(track)
            except FileNotFoundError:
                print(f"{track} in {disc_path} not found!")


def fix_track(track_path: str):
    with open(track_path) as f:
        track = json.load(f)
        music_path = track["path"]
        music_rating = track.get("rating")
        if music_rating:
            os.setxattr(
                music_path, RATINGS_ATTRIBUTE, bytes(str(music_rating), encoding="utf8")
            )


def main():
    albums = get_albums()
    for album in albums:
        fix_album(album)


if __name__ == "__main__":
    main()
