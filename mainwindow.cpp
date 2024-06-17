#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QAudioOutput>
#include <QMediaPlayer>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QMediaPlayer *player = new QMediaPlayer;
    QAudioOutput *audioOutput = new QAudioOutput;
    player->setAudioOutput(audioOutput);
    // ...
    player->setSource(QUrl::fromLocalFile("/home/joseph/Music/Anno 1404/1-04-Pirates.mp3"));
    audioOutput->setVolume(50);
    // player->play();
}

MainWindow::~MainWindow()
{
    delete ui;
}
