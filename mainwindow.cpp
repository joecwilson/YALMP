#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QAudioOutput>
#include <QMediaPlayer>
#include "track.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    for (int i = 0; i < 5; i++) {
        QListWidgetItem* item = new QListWidgetItem();
        Track* track = new Track(this);
        track->setText(QString("Text %1").arg(i));
        item->setSizeHint(track->sizeHint());

        ui->listWidget->addItem(item);
        ui->listWidget->setItemWidget(item, track);
    }





    QMediaPlayer *player = new QMediaPlayer;
    QAudioOutput *audioOutput = new QAudioOutput;
    player->setAudioOutput(audioOutput);
    // ...
    player->setSource(QUrl::fromLocalFile("/home/joseph/Music/Anno 1404/1-04-Pirates.mp3"));
    audioOutput->setVolume(50);
    // player->play();
}

void MainWindow::removeItem(const QString &text) {
    for (int i = 0; i < ui->listWidget->count(); i++) {
        QListWidgetItem* item = ui->listWidget->item(i);
        Track* track = dynamic_cast<Track*>(ui->listWidget->itemWidget(item));
        if (track->getText() == text) {
            delete ui->listWidget->takeItem(i);
            break;
        }
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}
