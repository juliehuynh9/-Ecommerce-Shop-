import sqlite3
conn = sqlite3.connect('ecommerce.db')
c = conn.cursor()

#CREATE THE TABLE ACCOUNTS TABLE, NEED TO RUN ONCE ONLY
# c.execute("""CREATE TABLE accounts(
#     username VARCHAR PRIMARY KEY, 
#     password VARCHAR NOT NULL, 
#     address VARCHAR NOT NULL, 
#     cart VARCHAR)""")
# c.execute("INSERT INTO accounts VALUES('kelly','123kelly','8934 N. Wakehurst Ave Winchester, VA 22601','1 4')")
# c.execute("INSERT INTO accounts VALUES('john','123john','392 Studebaker St La Vergne, TN 37086','2 3')")
# c.execute("INSERT INTO accounts VALUES('tom','123tom','521 Euclid Ave Mcallen, TX 78501','2 4')")


#CREATE THE TABLE ITEMS TABLE, NEED TO RUN ONCE ONLY
c.execute("""CREATE TABLE items(
    id VARCHAR PRIMARY KEY, 
    product VARCHAR NOT NULL, 
    description VARCHAR NOT NULL, 
    img VARCHAR NOT NULL,
    price INTEGER,
    count INTEGER)""")
c.execute("INSERT INTO accounts VALUES('lipstick','Peach color, long-wear, matt finish','', '20','0')")
c.execute("INSERT INTO accounts VALUES('brush','','392 Studebaker St La Vergne, TN 37086','2 3')")
c.execute("INSERT INTO accounts VALUES('tom','123tom','521 Euclid Ave Mcallen, TX 78501','2 4')")

#EXTRACT ROWS FROM DATABASE
# c.execute("SELECT * FROM accounts WHERE username LIKE 'kefdflly'")

#PRINT ALL AVAILABLE ACCOUNTS
print(c.fetchall())

#SAVE TO DB
conn.commit()

#CLOSE
conn.close()