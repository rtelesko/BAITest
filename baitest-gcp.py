import sys

import mysql.connector
from PyQt5.QtGui import QColor
from mysql.connector.constants import ClientFlag

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QApplication, QTableWidgetItem, QLabel, \
    QLineEdit, QSizePolicy, QMessageBox
from translate import Translator

from secrets import secrets

# Hole Parameter für Connection
my_host = secrets.get('DATABASE_HOST')
my_user = secrets.get('DATABASE_USER')
my_passwd = secrets.get('DATABASE_PWD')
my_db = secrets.get('DATABASE')

# Config-File für den Zugriff auf die Google Cloud SQL (mit SSL-Verschlüsselung)
config = {
    'user': secrets.get('DATABASE_USER'),
    'password': secrets.get('DATABASE_PWD'),
    'host': '34.66.98.190',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

class TableDisplay(QWidget):

    def __init__(self):
        super(TableDisplay, self).__init__()
        # Logo für Anwendung
        self.setWindowIcon(QtGui.QIcon('student-logo.png'))
        # Ein LineEdit erzeugen
        self.sql_line = QLineEdit()
        self.sql_line.setText("select * from studentdb.student")
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
        button_clear.clicked.connect(self.clear_command)

        # Ein Table Widget erzeugen
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def clear_command(self):
        self.sql_line.clear()

    def display_table(self):
        # Alten Tabelleninhalt löschen
        self.table_widget.clear()
        try:
            # Verbindung zur MySQL Datenbank aufbauen
            db = mysql.connector.connect(**config)
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
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        if i % 2 == 0:
                            # Background color "hellgrau"
                            background_color = QColor(240, 240, 240)  # Light gray
                        else:
                            # Background color "weiss"
                            background_color = QColor(255, 255, 255)  # White
                        item.setBackground(background_color)
                        self.table_widget.setItem(i, j, item)
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
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setWindowTitle("Fehlermeldung")
        translator = Translator(to_lang="de-CH-1996")
        translation_de = translator.translate(str(error.msg))
        msg.setText(translation_de)
        msg.exec()


def show_program_info():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.setWindowTitle("Information")
    msg.setStyleSheet("background-color: rgb(255,255,204);")
    msg.setText("Programm zur Ausführung von SQL Kommandos")
    msg.setInformativeText("BSc BAI Projekt 1, WS 2023/24")
    msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableDisplay()
    window.resize(600, 600)
    window.show()
    show_program_info()
    sys.exit(app.exec_())
