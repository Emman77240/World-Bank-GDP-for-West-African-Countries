#!/usr/bin/python
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(host='localhost', user='root', password='godman', database='mywebapp')
cursor = mariadb_connection.cursor()

#insert information
#cursor.execute("CREATE TABLE clients (name VARCHAR(255), address VARCHAR(255))")

sql = "INSERT INTO clients (name, address) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]

cursor.executemany(sql, val)

mariadb_connection.commit()
print("The last inserted id was: ", cursor.lastrowid)

