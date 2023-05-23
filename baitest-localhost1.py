import mysql.connector
import sys
import traceback

from secrets import secrets

# Hole Parameter für Connection
myhost = secrets.get("DATABASE_HOST")
myuser = secrets.get("DATABASE_USER")
mypasswd = secrets.get("DATABASE_PWD")
mydb = secrets.get("DATABASE")

try:
    connection = mysql.connector.connect(host=myhost, user=myuser, passwd=mypasswd, db=mydb)
    print("Verbindung zum Server aufgebaut")
    print()
except mysql.connector.Error:
    print("Keine Verbindung zum Server aufgebaut")
    traceback.print_exc()
    sys.exit(0)

# Lese alle Studenten von Datenbank
cursor = connection.cursor()
cursor.execute("Select * from student")
result = cursor.fetchall()
for datensatz in result:
    for feld in datensatz:
        print(f"{feld} ", end="")
    print()
print()
