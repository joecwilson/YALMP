import json
import os

from yalmp_scripts.constants import MUSIC_FOLDER
from yalmp_scripts.utils import get_all_tracks


def main():
    tracks = get_all_tracks()
    unrated_tracks = []
    for track in tracks:
        with open(track) as f:
            track_dict = json.load(f)
            if "rating" not in track_dict:
                unrated_tracks.append(track_dict["path"] + "\n")
    with open(os.path.join(MUSIC_FOLDER, "unratedsongs.m3u8"), "w") as f:
        for track in unrated_tracks:
            f.write(track)


if __name__ == "__main__":
    main()
