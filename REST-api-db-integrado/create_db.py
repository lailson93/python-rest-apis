import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS hoteis(hotel_id text PRIMARY KEY, \
  nome text, estrelas real, diaria real, cidade text)"


insert_hotel = "INSERT INTO hoteis VALUES('1','hOTEL PIrata',4.5,180.50,'Fortaleza')"

cursor.execute(create_table)

cursor.execute(insert_hotel)

connection.commit()

connection.close()
