#include "track.h"
#include "ui_track.h"
#include "mainwindow.h"
#include <QPushButton>

Track::Track(QWidget *parent) :
      QWidget(parent),
      ui(new Ui::Track)
{
    ui->setupUi(this);

    connect(ui->pushButton, &QPushButton::clicked, this, &Track::onToolButton_clicked);
    connect(this, &Track::sendRemoveItem, qobject_cast<MainWindow*>(parent), &MainWindow::removeItem);
}


QString Track::getText() {
    return ui-> label->text();
}

void Track::setText(const QString &text) {
    ui->label->setText(text);
}

void Track::onToolButton_clicked() {
    emit sendRemoveItem(ui->label->text());
}

Track::~Track()
{
    delete ui;
}
