#include "album.h"
#include "ui_album.h"

Album::Album(QWidget *parent) : QWidget(parent), ui(new Ui::Album)
{
    ui->setupUi(this);
}

Album::~Album()
{
    delete ui;
}
