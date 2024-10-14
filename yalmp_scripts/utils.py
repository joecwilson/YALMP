import json
import os

from yalmp_scripts.constants import YALMP_FOLDER


def get_albums():
    with open(os.path.join(YALMP_FOLDER, "albums.json")) as f:
        return json.load(f)
