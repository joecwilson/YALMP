#include "connection.h"
#include "mainwindow.h"

#include <QApplication>
#include <QSettings>
#include <QCoreApplication>
#include <QStandardPaths>

void setIfUnset(  QString key, QVariant value);
    void setDefaults();
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QCoreApplication::setOrganizationName("Joseph Wilson");
    QCoreApplication::setOrganizationName("YALMP");
    setDefaults();
    createConnection();
    MainWindow w;
    w.show();
    return a.exec();
}

void setDefaults()
{
    setIfUnset("YALMPfolder", QStandardPaths::writableLocation(QStandardPaths::MusicLocation) + "/.YALMP");

}

void setIfUnset(  QString key, QVariant value)
{
    QSettings settings;
    if (!settings.contains(key)){
        settings.setValue(key, value);
    }
}
