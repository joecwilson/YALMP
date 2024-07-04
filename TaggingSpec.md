# Tagging Spec

Tags in YALMP are not your traditional id3 or vorbis tags. Instead they are
stored in JSON files. The default tag location starts in ```$HOME/Music/.YALMP/tags```
tags should have the same layout as tha music itself.

## Album Spec

These will be titled as ```album.json```

* AlbumName: str
* AlbumArtist: str
* Discs: list[str]
  * In order of disc number
  * Paths to the json of the discs

### Optional Sections for Albums 

* Album Art: str
  * Path to the album art
* Copyright: str
* Comment: str
* Years: List[int]

## Multi Disc Album Spec

* AlbumName: str
* AlbumArtist: str
* Discs: List[str]
  * In order of disc number
  * Paths to the json of the tracks

### Optional Sections Multi Disc

* Album Art: str
  * Path to the album art
* Copyright: str
* Comment: str
* Years: List[int]

## Disc Spec

These will be titled as ```disc{discnumber}.json```

* Album: str
  * Path to the json of the albums
* Tracks: List[str]
  * Paths to the json of the tracks

### Optional Disc Sections

* Name: str
* Art: str
* Comment: str

## Track Spec

* Title: str
* Album: str
  * Path back to the album
* Disc: str
  * Path back to the disc (used only if album is Multi Disc)

### Optional Track Sections

* Artist: List[str]
  * If not present will assume album artist is artist
* Composer: str
* Rating: Number
  * 1 - 10
* LyricPathRaw: str
  * A path to the lyrics in their origional Language
* LyricPathTransliterated: str
  * A path to the lyrics transliterated
* LyricPathTranslated: str
  * A path to the lyrics translated