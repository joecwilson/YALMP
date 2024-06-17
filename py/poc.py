import sqlite3
import os
import json

MUSIC_FOLDER = os.path.join(os.path.expanduser("~"), "Music")
YALMP_FOLDER = os.path.join(MUSIC_FOLDER, ".YALMP")
TAGS_FOLDER = os.path.join(YALMP_FOLDER, "tags")


def create_album_table(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE  album (
                AlbumId integer PRIMARY KEY, 
                Title varchar(256), 
                AlbumArtist varchar(256)
                )""")
    
def create_disc_table(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE disc (
                DiscId INTEGER PRIMARY KEY,
                DiscNum INTEGER,
                DiscTitle varchar(256),
                Album INTEGER,
                FOREIGN KEY(Album) REFERENCES album(AlbumId)
    )""")
    
def create_track_table(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE track (
                TrackId integer PRIMARY KEY,
                Title varchar(256),
                Artist varchar(256),
                Album INTEGER,
                Disc INTEGER,
                TrackNum INTEGER,
                FOREIGN KEY(Album)  REFERENCES album(AlbumId),
                FOREIGN KEY(Disc)  REFERENCES disc(DiscId)
    )""")


def add_track_to_db(con, track, album_id, disc_id ,track_num):
    cur = con.cursor()
    track_json = {}
    with open(track) as f:
        track_json = json.load(f)
    cur.execute("""INSERT INTO track (Title, Artist, Album, Disc, TrackNum)
                VALUES (?, ?, ?, ?, ?)""", (track_json["Title"], track_json["Artist"],album_id, disc_id, track_num))


def add_disc_to_db(con, disc, album_id, disc_num ):
    cur = con.cursor()

    disc_json = {}
    with open(disc) as f:
        disc_json = json.load(f)
    disc_title = disc_json["Name"] if "Name" in disc_json else None

    cur.execute("""INSERT INTO disc (DiscNum, DiscTitle, Album)
                VALUES (?, ?, ?);""", (disc_num, disc_title, album_id))
    res = cur.execute("""SELECT DiscId FROM disc where Album = ? AND DiscNum = ?""", (album_id, disc_num))
    disc_id = res.fetchone()[0]
    track_num = 1
    for track in disc_json["Tracks"]:
        add_track_to_db(con, track, album_id, disc_id, track_num)
        track_num += 1

def add_album_to_db(con, album): 
    os.chdir(album)
    album_json = {}
    if not os.path.exists("album.json"):
        return
    with open("album.json") as f:
        album_json = json.load(f)
    cur = con.cursor()
    album_name = album_json["AlbumName"]
    album_artist = album_json["AlbumArtist"]
    cur.execute("""INSERT INTO album (Title, AlbumArtist)
                VALUES (? , ?);""",  (album_name,album_artist))
    con.commit()
    res = cur.execute("""SELECT AlbumId FROM album WHERE Title= ?""", (album_name,))
    album_id = res.fetchone()[0]
    disc_num = 1
    for disc in album_json["Discs"]:
        add_disc_to_db(con, disc, album_id, disc_num)
        disc_num += 1

def add_albums_to_db(con, base_folder):
    for folder in os.listdir(base_folder):
        subfiles = os.listdir(os.path.join(base_folder, folder))
        dir_found = False
        for subfile in subfiles:
            # print(subfile)
            if os.path.isdir(os.path.join(base_folder, folder, subfile)):
                dir_found = True
        add_album_to_db(con, os.path.join(base_folder, folder))
        if dir_found:
            add_albums_to_db(con, os.path.join(base_folder, folder))

def main():
    if (os.path.exists(os.path.join(YALMP_FOLDER, "yalmp.db"))):
        os.remove(os.path.join(YALMP_FOLDER, "yalmp.db"))
    con = sqlite3.connect(os.path.join(YALMP_FOLDER, "yalmp.db"))
    create_album_table(con)
    create_disc_table(con)
    create_track_table(con)
    add_albums_to_db(con, TAGS_FOLDER)



if __name__ == "__main__": 
    main()