#ifndef ALBUMMODEL_H
#define ALBUMMODEL_H

#include <QAbstractItemModel>
#include <QPixmap>

class AlbumModel : public QAbstractItemModel
{
    Q_OBJECT
  public:
    explicit AlbumModel(QObject *parent = nullptr);

    QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override;
    QModelIndex parent(const QModelIndex &index) const override;
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    struct AlbumDisplay
    {
        QString albumTitle;
        QString albumArtist;
        QPixmap albumArt;
    };

  private:
    QVector<int> albums;
};

#endif // ALBUMMODEL_H
