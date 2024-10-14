import json
import os

from yalmp_scripts.constants import TAG_FOLDER, YALMP_FOLDER


def get_an_album(tag_folder):
    tag_files = os.listdir(tag_folder)
    album_paths = []
    for file in tag_files:
        if os.path.isdir(os.path.join(tag_folder, file)):
            albums = get_an_album(
                os.path.join(tag_folder, file),
            )
            if albums:
                album_paths.extend(albums)
        elif file == "album.json":
            album_paths.append(os.path.join(tag_folder, file))
    return album_paths


def main():
    albums = get_an_album(TAG_FOLDER)
    with open(os.path.join(YALMP_FOLDER, "albums.json"), "w") as f:
        json.dump(albums, f, indent=4)


if __name__ == "__main__":
    main()
