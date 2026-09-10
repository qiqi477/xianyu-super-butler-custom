import sqlite3
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, path: str):
        self.path = path
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                cookie TEXT,
                enabled INTEGER
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                category TEXT,
                description TEXT,
                price REAL,
                original_price REAL,
                images TEXT,
                spec TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                images TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS publish_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                product_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    # Accounts
    def list_accounts(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM accounts')
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def add_account(self, name, cookie, enabled=True):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO accounts (name, cookie, enabled) VALUES (?, ?, ?)', (name, cookie, 1 if enabled else 0))
        self.conn.commit()
        return cur.lastrowid

    def delete_account(self, account_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM accounts WHERE id=?', (account_id,))
        self.conn.commit()

    # Products
    def list_products(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM products')
        rows = cur.fetchall()
        res = []
        for r in rows:
            d = dict(r)
            d['images'] = d['images'].split(';') if d['images'] else []
            res.append(d)
        return res

    def add_product(self, title, category, description, price, original_price, images, spec):
        images_str = ';'.join(images) if images else ''
        cur = self.conn.cursor()
        cur.execute('INSERT INTO products (title, category, description, price, original_price, images, spec) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (title, category, description, price, original_price, images_str, spec))
        self.conn.commit()
        return cur.lastrowid

    def update_product(self, pid, title, category, description, price, original_price, images, spec):
        images_str = ';'.join(images) if images else ''
        cur = self.conn.cursor()
        cur.execute('UPDATE products SET title=?, category=?, description=?, price=?, original_price=?, images=?, spec=? WHERE id=?',
                    (title, category, description, price, original_price, images_str, spec, pid))
        self.conn.commit()

    def add_image_to_product(self, pid, path):
        cur = self.conn.cursor()
        cur.execute('SELECT images FROM products WHERE id=?', (pid,))
        row = cur.fetchone()
        if row:
            images = row['images'] or ''
            images_list = images.split(';') if images else []
            images_list.append(path)
            images_str = ';'.join(images_list)
            cur.execute('UPDATE products SET images=? WHERE id=?', (images_str, pid))
            self.conn.commit()

    # Materials
    def list_materials(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM materials')
        rows = cur.fetchall()
        res = []
        for r in rows:
            d = dict(r)
            d['images'] = d['images'].split(';') if d['images'] else []
            res.append(d)
        return res

    def add_material(self, title, description, images):
        images_str = ';'.join(images) if images else ''
        cur = self.conn.cursor()
        cur.execute('INSERT INTO materials (title, description, images) VALUES (?, ?, ?)', (title, description, images_str))
        self.conn.commit()
        return cur.lastrowid

    def delete_material(self, mid):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM materials WHERE id=?', (mid,))
        self.conn.commit()

    def add_material_image(self, mid, path):
        cur = self.conn.cursor()
        cur.execute('SELECT images FROM materials WHERE id=?', (mid,))
        row = cur.fetchone()
        if row:
            images = row['images'] or ''
            images_list = images.split(';') if images else []
            images_list.append(path)
            images_str = ';'.join(images_list)
            cur.execute('UPDATE materials SET images=? WHERE id=?', (images_str, mid))
            self.conn.commit()

    # Publish records
    def add_publish_record(self, account_id, product_id):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO publish_records (account_id, product_id) VALUES (?, ?)', (account_id, product_id))
        self.conn.commit()
        return cur.lastrowid

    def list_publish_records(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM publish_records ORDER BY created_at DESC')
        rows = cur.fetchall()
        return [dict(r) for r in rows]
