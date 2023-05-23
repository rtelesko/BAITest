import mysql.connector
import sys
import traceback
from secrets import secrets

# Hole Parameter für Connection
host = secrets.get('DATABASE_HOST')
user = secrets.get('DATABASE_USER')
passwd = secrets.get('DATABASE_PWD')
db = secrets.get('DATABASE')

try:
    connection = mysql.connector.connect(host="localhost", user="root", passwd="rainer", db="studentdb")
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

# Eintrag neuer Studenten in Datenbank
sql = "INSERT INTO student (LastName, FirstName, Age) VALUES (%s, %s, %s)"
val = [('Harris', 'Jane', "65"), ('Pence', 'Mike', "61"), ('De Santis', 'Ron', "52")]
try:
    cursor.executemany(sql, val)
    connection.commit()
    print(cursor.rowcount, " Datensatz eingefügt")
    print()
except mysql.connector.Error:
    print("Kein Eintrag in mySQL Datenbank durchgeführt")
    traceback.print_exc()
    connection.close()
    sys.exit(0)

# Update eines Studenten in Datenbank
sql = "UPDATE STUDENT SET LastName = 'Mustermann' WHERE Id ='3'"
try:
    cursor.execute(sql)
    connection.commit()
    print(cursor.rowcount, " Datensatz geändert")
    print()
except mysql.connector.Error:
    print("Kein Update in mySQL Datenbank durchgeführt")
    traceback.print_exc()
    connection.close()
    sys.exit(0)

# Löschen eines Studenten in Datenbank
sql = "DELETE FROM STUDENT WHERE Id = '1'"
try:
    cursor.execute(sql)
    connection.commit()
    print(cursor.rowcount, " Datensatz gelöscht")
    print()
except mysql.connector.Error:
    print("Kein Update in mySQL Datenbank durchgeführt")
    traceback.print_exc()
    connection.close()
    sys.exit(0)

# Lese wieder alle Studenten von Datenbank
cursor.execute("Select * from student")
result = cursor.fetchall()
cursor.close()
connection.close()

for datensatz in result:
    for feld in datensatz:
        print(f"{feld} ", end="")
    print()
print()
