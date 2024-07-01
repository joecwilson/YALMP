#include "scan.h"
#include <QDataStream>
#include <QDir>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QSettings>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QString>

bool scanFolder(QDir folder);
bool scanAlbum(QDir album);
bool scanDisc(QSqlDatabase db, QString disc, int albumId, int discNum);
bool scanTrack(QSqlDatabase db, QString track, int albumId, int discId, int trackNum);

bool scan(void)
{
    QSettings settings;
    QDir yalmpDirectory = QDir(settings.value("YALMPfolder").toString());
    return scanFolder(yalmpDirectory);
}

bool scanFolder(QDir folder)
{
    bool status = true;
    QFileInfoList entries = folder.entryInfoList(QDir::NoDotAndDotDot | QDir::Dirs | QDir::Files);
    for (int i = 0; i < entries.size(); i++)
    {
        QFileInfo fileInfo = entries.at(i);
        if (fileInfo.isDir())
        {
            status &= scanFolder(QDir(fileInfo.absoluteFilePath()));
        }
        if (fileInfo.fileName() == "album.json")
        {
            return scanAlbum(folder);
        }
    }
    return status;
}

bool scanAlbum(QDir album)
{
    QFile albumFile = album.filePath("album.json");
    if (!albumFile.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return false;
    }
    QJsonDocument albumJson = QJsonDocument::fromJson(albumFile.readAll());
    QJsonObject albumObject = albumJson.object();

    QString albumName = albumObject["AlbumName"].toString();
    QString albumArtist = albumObject["AlbumArtist"].toString();

    QSqlDatabase db = QSqlDatabase::database();

    QSqlQuery query("INSERT into Albums (Title, AlbumArtist) VALUES (?, ?)");

    query.addBindValue(albumName);
    query.addBindValue(albumArtist);

    query.exec();

    QSqlQuery getAlbumId("SELECT AlbumId FROM Albums where Title = ?");
    getAlbumId.addBindValue(albumName);
    getAlbumId.exec();
    getAlbumId.next();
    bool okay = false;
    int albumId = getAlbumId.value(0).toInt(&okay);
    if (!okay)
    {
        return false;
    }

    QJsonArray discs = albumObject["Discs"].toArray();

    for (int i = 0; i < discs.size(); i++)
    {
        QString discLocation = discs[i].toString();
        scanDisc(db, discLocation, albumId, i + 1);
    }

    return true;
}

bool scanDisc(QSqlDatabase db, QString disc, int albumId, int discNum)
{
    QFile discFile(disc);
    if (!discFile.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return false;
    }

    QJsonDocument discJson = QJsonDocument::fromJson(discFile.readAll());
    QJsonObject discObject = discJson.object();
    QString discName = discObject["Name"].toString("None");

    QSqlQuery query("INSERT into Discs (DiscNum, DiscTitle, Album) VALUES (?,?,?)");

    query.addBindValue(discNum);
    query.addBindValue(discName);
    query.addBindValue(albumId);

    query.exec();

    QSqlQuery getDiscId("SELECT DiscId from Discs WHERE Album = ? AND DiscNum = ?");
    getDiscId.addBindValue(albumId);
    getDiscId.addBindValue(discNum);
    getDiscId.exec();
    getDiscId.next();
    int discId = getDiscId.value(0).toInt();

    QJsonArray tracks = discObject["Tracks"].toArray();
    for (int i = 0; i < tracks.size(); i++)
    {
        QString trackLocation = tracks[i].toString();
        scanTrack(db, trackLocation, albumId, discId, i + 1);
    }
    return true;
}

bool scanTrack(QSqlDatabase db, QString track, int albumId, int discId, int trackNum)
{
    QFile trackFile(track);
    if (!trackFile.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return false;
    }

    QJsonDocument trackJson = QJsonDocument::fromJson(trackFile.readAll());
    QJsonObject trackObject = trackJson.object();
    QString title = trackObject["Title"].toString();
    QString artist = trackObject["Artist"].toString();

    QSqlQuery query("INSERT into Tracks (TrackNum, TrackTitle,Artist, Album, Disc ) VALUES (?,?,?,?,?)");

    query.addBindValue(trackNum);
    query.addBindValue(title);
    query.addBindValue(artist);
    query.addBindValue(albumId);
    query.addBindValue(discId);

    query.exec();

    return true;
}
