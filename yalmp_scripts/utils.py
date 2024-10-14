import json
import os

from yalmp_scripts.constants import YALMP_FOLDER


def get_albums():
    with open(os.path.join(YALMP_FOLDER, "albums.json")) as f:
        return json.load(f)


def get_all_tracks():
    albums = get_albums()
    discs = []
    for album in albums:
        discs.extend(get_discs_from_album(album))
    tracks = []
    for disc in discs:
        tracks.extend(get_tracks_from_disc(disc))
    return tracks


def get_discs_from_album(album):
    with open(album) as f:
        album_json = json.load(f)
        return album_json["discs"]


def get_tracks_from_disc(disc):
    with open(disc) as f:
        disc_json = json.load(f)
        return disc_json["tracks"]
