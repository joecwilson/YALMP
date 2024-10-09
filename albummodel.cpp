#include "albummodel.h"
#include <QSqlQuery>

AlbumModel::AlbumModel(QObject *parent) : QAbstractItemModel(parent)
{
    QVector<int> backingVector;
    this->albums = backingVector;
}

int AlbumModel::rowCount(const QModelIndex &parent) const
{
    return (this->albums.length() + this->rowCount() - 1) / this->rowCount();
}

int AlbumModel::columnCount(const QModelIndex &parent) const
{
    return 5;
}

QModelIndex AlbumModel::index(int row, int column, const QModelIndex &parent) const
{
    int itemIndex = row * this->columnCount() + column;
    if (this->albums.length() >= itemIndex)
    {
        return QModelIndex();
    }
    return QAbstractItemModel::createIndex(row, column, &this->albums[itemIndex]);
}

QModelIndex AlbumModel::parent(const QModelIndex &index) const
{
    return QModelIndex();
}

QVariant AlbumModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
    {
        return QVariant();
    }
    int backingIndex = *(int *)index.constInternalPointer();
    int albumId = this->albums[backingIndex];

    QSqlQuery query("SELECT Title, AlbumArtist, AlbumArt FROM Albums WHERE AlbumId = ?");
    query.addBindValue(albumId);

    query.next();

    QString title = query.value(0).toString();
    QString albumArtist = query.value(1).toString();
    QString albumArtPath = query.value(2).toString();

    if (albumArtPath == "")
    {
        albumArtPath = "/home/joseph/Pictures/Album.png";
    }

    QPixmap albumArt = QPixmap(albumArtPath);

    AlbumModel::AlbumDisplay display = {title, albumArtist, albumArt};

    return QVariant::fromValue(display);
}
