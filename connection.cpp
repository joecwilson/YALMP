#include <QDir>
#include <QMessageBox>
#include <QSqlQuery>
#include <QStandardPaths>
#include <QtDebug>
#include <QtLogging>

static bool create_tables();
static bool should_create_tables(QDir yalmpDirectory);

bool createConnection()
{
    QString musicFolder = QStandardPaths::writableLocation(QStandardPaths::MusicLocation);
    QString yalmpFolder = musicFolder + "/.YALMP";
    QDir yalmpDirectory = QDir(yalmpFolder);
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(yalmpFolder + "/yalmp.db");
    bool createTables = should_create_tables(yalmpDirectory);
    if (!db.open())
    {
        QMessageBox::critical(nullptr, "Database error", "Unable to create (or open) database", QMessageBox::Cancel);
        return false;
    }
    qDebug() << "db folder" << yalmpFolder;
    qDebug() << "db name" << db.databaseName();
    bool success = db.open();
    if (!success)
    {
        qDebug() << "Opening Faoled";
        return false;
    }
    if (createTables)
    {
        success = create_tables();
        if (!success)
        {
            qDebug() << "creating Failed";
        }
    }
    else
    {
        qDebug() << "Skipped Creation";
    }

    return success;
}

static bool should_create_tables(QDir yalmpDirectory)
{
    QStringList filters;
    filters << "yalmp.db";
    qDebug() << yalmpDirectory.entryList(filters);
    return yalmpDirectory.entryList(filters).isEmpty();
}

static bool create_tables()
{
    bool success = true;
    QSqlQuery query;
    success = query.exec("CREATE TABLE Albums ("
                         "AlbumId INTEGER PRIMARY KEY,"
                         "Title VARCHAR(256),"
                         "AlbumArtist VARCHAR(256),"
                         "AlbumArt VARCHAR(256))");
    if (!success)
    {
        qDebug() << "album failed";
        return false;
    }
    success = query.exec("CREATE TABLE Discs ("
                         "DiscId INTEGER PRIMARY KEY,"
                         "DiscNum INTEGER,"
                         "DiscTitle VARCHAR(256),"
                         "DiscArt VARCHAR(256),"
                         "Album INTEGER,"
                         "FOREIGN KEY(Album) REFERENCES Albums(AlbumId))");
    if (!success)
    {
        qDebug() << "disc failed";
        return false;
    }
    success = query.exec("CREATE TABLE Tracks ("
                         "TrackId INTEGER PRIMARY KEY,"
                         "TrackNum INTEGER,"
                         "TrackTitle VARCHAR(256),"
                         "TrackArt VARCHAR(256),"
                         "Album INTEGER,"
                         "Disc INTEGER,"
                         "FOREIGN KEY(Album) REFERENCES Albums(AlbumId),"
                         "FOREIGN KEY(Disc) REFERENCES Disc(DiscId))");
    return success;
}
