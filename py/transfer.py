import os
from pathlib import Path
import shutil
import taglib
import json
from dataclasses import dataclass

MUSIC_FOLDER = os.path.join(os.path.expanduser("~"), "Music")
YALMP_FOLDER = os.path.join(MUSIC_FOLDER, ".YALMP")
TAG_FOLDER = os.path.join(YALMP_FOLDER, "tags")
LYRIC_FOLDER = os.path.join(YALMP_FOLDER, "lyrics")


@dataclass(order=True)
class AlbumInfo:
    disc_num: int
    track_num: int
    album_artist: str
    album: str
    file_name: str


def tag_folder(music_folder, tag_folder, lyric_folder):
    # print(music_folder," | " , tag_folder)
    music_files = os.listdir(music_folder)
    os.mkdir(tag_folder)
    os.mkdir(lyric_folder)
    all_info = []
    for file in music_files:
        info = tag_file(
            os.path.join(music_folder, file),
            os.path.join(tag_folder, "".join(file.split(".")[0:-1]) + ".json"),
            os.path.join(lyric_folder, "".join(file.split(".")[0:-1]) + ".txt"),
            tag_folder,
            file,
        )
        all_info.append(info)

    all_info.sort()

    create_multi_disc_album(all_info, tag_folder, "album.json")


def create_single_disc_album(
    all_info: list[AlbumInfo], tag_folder: str, json_name: str
):
    tag_to_write = {}
    tag_to_write["AlbumName"] = all_info[0].album
    tag_to_write["AlbumArtist"] = all_info[0].album_artist
    tracks = []
    for track in all_info:
        tracks.append(track.file_name)
    tag_to_write["Tracks"] = tracks
    with open(os.path.join(tag_folder, json_name), "w") as f:
        json.dump(tag_to_write, f, indent=4)


def create_multi_disc_album(all_info: list[AlbumInfo], tag_folder: str, json_name: str):
    tag_to_write = {}
    tag_to_write["AlbumName"] = all_info[0].album
    tag_to_write["AlbumArtist"] = all_info[0].album_artist
    discs = []
    cur_disc = 0
    idx = 0
    for track in all_info:
        if track.disc_num != cur_disc:
            cur_disc = track.disc_num
            json_name_disc = "disc" + str(cur_disc) + ".json"
            discs.append(os.path.join(tag_folder, json_name_disc))
            create_disc(
                all_info,
                tag_folder,
                json_name_disc,
                idx,
                os.path.join(tag_folder, json_name),
            )
        idx += 1
    tag_to_write["Discs"] = discs
    with open(os.path.join(tag_folder, json_name), "w") as f:
        json.dump(tag_to_write, f, indent=4)


def create_disc(
    all_info: list[AlbumInfo],
    tag_folder: str,
    json_name: str,
    start_idx: int,
    album_path: str,
):
    tag_to_write = {}
    tag_to_write["Album"] = album_path
    tracks = []
    disc_num = all_info[start_idx].disc_num
    for track in all_info[start_idx:]:
        if track.disc_num != disc_num:
            break
        tracks.append(track.file_name)
    tag_to_write["Tracks"] = tracks
    with open(os.path.join(tag_folder, json_name), "w") as f:
        json.dump(tag_to_write, f, indent=4)


def tag_file(
    music_file: str, tag_file: str, lyric_file: str, tag_folder: str, file_name: str
) -> AlbumInfo:
    tag = {}
    file_tags = {}
    with taglib.File(music_file) as song:
        file_tags = song.tags
    print(music_file, file_tags)
    if ("Artist" in file_tags):
        tag["Artist"] = file_tags["ARTIST"]
    else:
        tag["Artist"] = "Unknown Artist"
    tag["Title"] = file_tags["TITLE"][0]
    tag["Album"] = os.path.join(tag_folder, "album.json")
    # tag["Album"] = file_tags[]
    disc_num = 1
    if "DISCNUMBER" in file_tags:
        disc_num = int(str(file_tags["DISCNUMBER"][0]).split("/")[0])
        tag["Disc"] = os.path.join(tag_folder, "disc" + str(disc_num) + ".json")
    track_num = int(str(file_tags["TRACKNUMBER"][0]).split("/")[0])
    # print(tag, track_num)

    if "LYRICS" in file_tags:
        with open(lyric_file, "w") as f_lrc:
            f_lrc.write(file_tags["LYRICS"][0])
        tag["LyricPathRaw"] = lyric_file

    with open(tag_file, "w") as f_tag:
        # print(song.tags)\
        json.dump(tag, f_tag, indent=4)
    album_artist = "Unknown Artist"
    if ("ALBUMARTIST" in file_tags):
        album_artist = file_tags["ALBUMARTIST"][0]
    info = AlbumInfo(
        track_num=track_num,
        disc_num=disc_num,
        album_artist=album_artist,
        album=file_tags["ALBUM"][0],
        file_name=tag_file,
    )
    return info


def main():
    # print(MUSIC_FOLDER)
    # print(TAG_FOLDER)
    tag_path = Path(TAG_FOLDER)
    lyric_path = Path(LYRIC_FOLDER)
    shutil.rmtree(YALMP_FOLDER)
    # shutil.rmtree(TAG_FOLDER)
    # shutil.rmtree(LYRIC_FOLDER)
    tag_path.mkdir(parents=True, exist_ok=False)
    lyric_path.mkdir(parents=True, exist_ok=False)
    music = os.listdir(MUSIC_FOLDER)
    # print(music)
    for folder in music:
        # print(folder)
        if folder == ".YALMP":
            continue
        tag_folder(
            os.path.join(MUSIC_FOLDER, folder),
            os.path.join(TAG_FOLDER, folder),
            os.path.join(LYRIC_FOLDER, folder),
        )
    # tag_folder(
    #     os.path.join(MUSIC_FOLDER, "Factorio"),
    #     os.path.join(TAG_FOLDER, "Factorio"),
    #     os.path.join(LYRIC_FOLDER, "Factorio"),
    # )
    # tag_folder(
    #     os.path.join(MUSIC_FOLDER, "Anno 2070"),
    #     os.path.join(TAG_FOLDER, "Anno 2070"),
    #     os.path.join(LYRIC_FOLDER, "Anno 2070"),
    # )


if __name__ == "__main__":
    main()
