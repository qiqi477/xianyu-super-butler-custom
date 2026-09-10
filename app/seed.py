import sqlite3

# Seed script to create example accounts, products, and materials for demo

def seed(db_path='./data/app.db'):
    import os
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cookie TEXT, enabled INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, description TEXT, price REAL, original_price REAL, images TEXT, spec TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS materials (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, images TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS publish_records (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, product_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    # sample accounts
    cur.execute("INSERT INTO accounts (name, cookie, enabled) VALUES (?,?,?)", ('demo_shop_1','',1))
    cur.execute("INSERT INTO accounts (name, cookie, enabled) VALUES (?,?,?)", ('demo_shop_2','',1))

    # sample product
    cur.execute("INSERT INTO products (title,category,description,price,original_price,images,spec) VALUES (?,?,?,?,?,?,?)",
                ('日语N1 N2 N3考级学习资料合集','图书','包含练习题与解析。','9.9', '19.9', '', '电子书'))

    # sample material
    cur.execute("INSERT INTO materials (title,description,images) VALUES (?,?,?)", ('日语学习资料','备用素材',''))

    conn.commit()
    conn.close()
    print('Seed data created at', db_path)

if __name__ == '__main__':
    seed()
