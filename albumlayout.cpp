#include "albumlayout.h"

AlbumLayout::AlbumLayout(QWidget *parent, int max_column_count)
{
    m_max_column_count = max_column_count;
}

AlbumLayout::~AlbumLayout()
{
}

void AlbumLayout::add_widget(QWidget *p_widget)
{
    int row = 0;
    int col = 0;

    while (itemAtPosition(row, col) != nullptr)
    {
        if (col == (m_max_column_count - 1))
        {
            col = 0;
            row++;
        }
        else
        {
            col++;
        }
    }
    QGridLayout::addWidget(p_widget, row, col);
}
