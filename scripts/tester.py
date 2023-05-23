import sqlite3
from sqlite3 import Connection, Error
from hashlib import md5


# create DB and connection
def create_connection(path: str) -> Connection:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("./marktplatz.db")
cursor = connection.cursor()

# create Table
cursor.execute("CREATE TABLE if not exists Marktplatz(checksum, text)")

text = "test"
# checksum = md5(text.encode()).hexdigest()
# print(checksum,text )
# cursor.execute("INSERT INTO Marktplatz VALUES(?,?);", (checksum, text))
# cursor.execute("INSERT INTO Marktplatz VALUES(?,?);", ("Hello", "World"))
# connection.commit()
# cursor.execute("INSERT INTO Marktplatz VALUES ('2023-05-18', 'xml', 'Hello Peter')")
# cursor.execute("INSERT INTO Marktplatz VALUES ('2023-05-19', 'abc', 'Hello Danilo')")
print(cursor.execute("SELECT * FROM Marktplatz").fetchall())
