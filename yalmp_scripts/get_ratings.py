import os
import json
from yalmp_scripts.constants import RATINGS_ATTRIBUTE
from yalmp_scripts.utils import get_all_tracks 

def write_rating(track):
    with open(track) as f:
        track_json = json.load(f)
    try:
        rating = int(os.getxattr(track_json["path"], RATINGS_ATTRIBUTE))
    except OSError:
       return 
    track_json["rating"] = rating
    with open(track, "w") as f:
        json.dump(track_json,f, indent=4)


def main():
    for track in get_all_tracks():
        print(track)
        write_rating(track)

if __name__ == "__main__":
    main()