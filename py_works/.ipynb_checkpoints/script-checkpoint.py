import sqlite3

con = sqlite3.connect("MenTab.sqlite3")
cur = con.cursor()

#cur.execute('''INSERT INTO elements
#VALUES (4, "Бериллий", "Be", "Beryllium", "2, 2", 9.012182, 1278, 2970, 1797, "Воклен")''')

result = cur.execute('''SELECT * FROM elements''').fetchall()
con.commit()

for x in result:
    print(x)
