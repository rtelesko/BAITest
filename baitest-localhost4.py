import sys

import mysql.connector
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QApplication, QTableWidgetItem

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

        # Ein vertical layout erzeugen
        layout = QVBoxLayout()

        # Einen button erzeugen
        button = QPushButton("Daten anzeigen")
        button.clicked.connect(self.displayTable)
        layout.addWidget(button)

        # Ein table widget erzeugen
        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        self.setLayout(layout)

    def displayTable(self):
        # Tabelleninhalt löschen
        self.tableWidget.clear()

        # Verbindung zur MySQL Datenbank aufbauen
        try:
            db = mysql.connector.connect(
                host=myhost,
                user=myuser,
                password=mypasswd,
                database=mydb)

        except mysql.connector.Error as e:
            print("Fehler beim Lesen der MySQL Datenbank", e)

        # Execute a query to fetch data from the table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student")
        data = cursor.fetchall()

        # Get the number of rows and columns
        num_rows = len(data)
        num_cols = len(data[0])

        # Anzahl der Zeilen / Spalten ermitteln
        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        # Tabelle mit Daten füllen
        self.tableWidget.setHorizontalHeaderLabels(["Id", "Last Name", "First Name", "Age"])
        tablerow = 0
        for row in data:
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(row[3])))
            tablerow += 1

        # Datenbank schliessen
        cursor.close()
        db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableDisplay()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec_())
