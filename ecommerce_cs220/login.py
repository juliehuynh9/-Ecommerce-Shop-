import sqlite3

def add_account(username, password, address):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (?,?,?,?)",(username, password, address,''))
    conn.commit()
    conn.close()

def retrieve_account(username, password):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    acc = c.execute("SELECT * FROM accounts WHERE username=(?)",(username,)).fetchall()
    print(acc)
    conn.commit()
    conn.close()
    if acc:
        return acc[0][0], acc[0][1]
    return None, None