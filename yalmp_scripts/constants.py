import os

MUSIC_FOLDER = os.path.join(os.path.expanduser("~"), "Music")
YALMP_FOLDER = os.path.join(MUSIC_FOLDER, ".YALMP")
TAG_FOLDER = os.path.join(YALMP_FOLDER, "tags")
LYRIC_FOLDER = os.path.join(YALMP_FOLDER, "lyrics")
RATINGS_ATTRIBUTE = "user.baloo.rating"
