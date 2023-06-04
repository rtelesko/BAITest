from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 50, 1000, 1000)

        # Add table items
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(3)
        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(f"Item {row}-{col}")
                self.table_widget.setItem(row, col, item)

        # Make the table widget invisible
        self.table_widget.setVisible(False)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
