import sys

import mysql.connector
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QApplication

from secrets import secrets

# Hole Parameter für Connection
myhost = secrets.get('DATABASE_HOST')
myuser = secrets.get('DATABASE_USER')
mypasswd = secrets.get('DATABASE_PWD')
mydb = secrets.get('DATABASE')


class TableDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.tableWidget = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MySQL Datenbank")

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a button
        button = QPushButton("Zeige alle Studenten")
        button.clicked.connect(self.displayTable)
        layout.addWidget(button)

        # Create a table widget
        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        self.setLayout(layout)

    def displayTable(self):
        # Clear the table
        self.tableWidget.clear()

        # Establish a connection to the MySQL database
        db = mysql.connector.connect(
            host=myhost,
            user=myuser,
            password=mypasswd,
            database=mydb
        )

        # Execute a query to fetch data from the table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student")
        data = cursor.fetchall()

        # Get the number of rows and columns
        num_rows = len(data)
        num_cols = len(data[0])

        # Set the number of rows and columns in the table
        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        # Populate the table with data
        for i in range(num_rows):
            for j in range(num_cols):
                item = QTableWidgetItem(str(data[i][j]))
                self.tableWidget.setItem(i, j, item)

        # Close the database connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableDisplay()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec_())
