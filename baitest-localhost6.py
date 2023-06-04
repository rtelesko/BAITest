import sys

import mysql.connector
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QApplication, QTableWidgetItem, QLabel, \
    QLineEdit, QSizePolicy, QMessageBox

from translate import Translator
from secrets import secrets

# Hole Parameter für Connection
my_host = secrets.get('DATABASE_HOST')
my_user = secrets.get('DATABASE_USER')
my_passwd = secrets.get('DATABASE_PWD')
my_db = secrets.get('DATABASE')


class TableDisplay(QWidget):

    def __init__(self):
        super(TableDisplay, self).__init__()
        # Logo für Anwendung
        self.setWindowIcon(QtGui.QIcon('student-logo.png'))
        # Ein LineEdit erzeugen
        self.sql_line = QLineEdit()
        self.sql_line.setText("select * from student")
        self.table_widget = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MySQL Datenbank")

        # Ein Vertical Layout erzeugen
        layout = QVBoxLayout()

        # Ein Label erzeugen
        sql_label = QLabel()
        sql_label.setText('SQL Statement')
        layout.addWidget(sql_label)

        # Ein LineEdit hinzufügen
        layout.addWidget(self.sql_line)

        # Zwei Buttons erzeugen
        button_sql = QPushButton("SQL Befehl ausführen")
        button_sql.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        layout.addWidget(button_sql)
        button_sql.clicked.connect(self.display_table)

        button_clear = QPushButton("Eingabe löschen")
        button_clear.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        layout.addWidget(button_clear)
        button_clear.clicked.connect(self.clear_table)

        # Ein Table Widget erzeugen
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def clear_table(self):
        self.sql_line.clear()

    def display_table(self):
        # Tabelleninhalt löschen
        self.table_widget.clear()

        try:
            # Verbindung zur MySQL Datenbank aufbauen
            db = mysql.connector.connect(
                host=my_host,
                user=my_user,
                password=my_passwd,
                database=my_db)
            print("Verbindung zur mySQL Datenbank hergestellt")
            try:
                # SQL Befehl ausführen
                cursor = db.cursor()
                cursor.execute(self.sql_line.text())
                data = cursor.fetchall()
            except mysql.connector.Error as error:
                self.show_message(error)
                print("Fehler beim Ausführen des SQL Statements")
            # Zahl der Zeilen und Spalten ermitteln
            else:
                num_rows = len(data)
                num_cols = len(data[0])
                self.table_widget.setRowCount(num_rows)
                self.table_widget.setColumnCount(num_cols)
                # Tabelle mit Daten füllen
                table_row = 0
                for row in data:
                    self.table_widget.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
                    self.table_widget.setItem(table_row, 1, QTableWidgetItem(row[1]))
                    self.table_widget.setItem(table_row, 2, QTableWidgetItem(row[2]))
                    self.table_widget.setItem(table_row, 3, QTableWidgetItem(str(row[3])))
                    table_row += 1
                print("SQL Statement erfolgreich durchgeführt")
        except mysql.connector.Error as error:
            self.show_message(error)
            print("Fehler bei Verbindung mit SQL Datenbank")
        # Datenbank schliessen
        finally:
            cursor.close()
            db.close()

    def show_message(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setWindowTitle("Fehlermeldung")
        translator = Translator(to_lang="de-CH-1996")
        translation_de = translator.translate(str(error.msg))
        msg.setText(translation_de)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableDisplay()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec_())
