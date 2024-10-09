#ifndef ALBUMLAYOUT_H
#define ALBUMLAYOUT_H

#include <QGridLayout>
#include <QAbstractItemModel>

class AlbumLayout : public QGridLayout
{
  public:
    AlbumLayout(QWidget *parent, int max_columns);
    ~AlbumLayout();

    void add_widget(QWidget *p_widget);
    void add_item(QAbstractItemModel *p_item);

  private:
    int m_max_column_count;
};

#endif // ALBUMLAYOUT_H
