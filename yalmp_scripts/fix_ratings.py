import json
import os

from yalmp_scripts.constants import RATINGS_ATTRIBUTE, TAG_FOLDER


def tag_a_folder(tag_folder):
    tag_files = os.listdir(tag_folder)
    for file in tag_files:
        if os.path.isdir(os.path.join(tag_folder, file)):
            tag_a_folder(
                os.path.join(tag_folder, file),
            )
        elif file == "album.json":
            fix_album(
                os.path.join(tag_folder, file),
            )


def fix_album(full_path):
    with open(full_path) as f:
        data = json.load(f)
        discs = data["discs"]
        for disc in discs:
            fix_discs(disc)


def fix_discs(disc_path):
    with open(disc_path) as f:
        disc = json.load(f)
        tracks = disc["tracks"]
        for track in tracks:
            try:
                fix_track(track)
            except FileNotFoundError:
                print(f"{track} in {disc_path} not found!")


def fix_track(track_path):
    with open(track_path) as f:
        track = json.load(f)
        music_path = track["path"]
        music_rating = track.get("rating")
        if music_rating:
            os.setxattr(
                music_path, RATINGS_ATTRIBUTE, bytes(str(music_rating), encoding="utf8")
            )


def main():
    tag_a_folder(TAG_FOLDER)


if __name__ == "__main__":
    main()
