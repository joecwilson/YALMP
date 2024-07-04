#ifndef TRACK_H
#define TRACK_H

#include <QWidget>

namespace Ui
{
class Track;
}

class Track : public QWidget
{
    Q_OBJECT

  public:
    explicit Track(QWidget *parent = nullptr);
    QString getText();
    void setText(const QString &text);
    ~Track();

  signals:
    void sendRemoveItem(const QString &text);

  private slots:
    void onToolButton_clicked();

  private:
    Ui::Track *ui;
};

#endif // TRACK_H
