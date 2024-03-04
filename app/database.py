import sqlite3 as sq

db = sq.connect('app/clothy.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER, "
                "user_name TEXT, "
                "date_visit DATETIME DEFAULT CURRENT_TIMESTAMP, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "type TEXT, "
                "name TEXT, "
                "desc TEXT, "
                "price INTEGER, "
                "photo TEXT, "
                "brand TEXT)")
    db.commit()
    
async def cmd_start_db(user_id, user_name):
    user = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if not user:
        cur.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
        db.commit()
        
        
async def add_item_db(data):
    cur.execute('INSERT INTO items (type, name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?, ?)', 
                (data["type"], data["name"], data["desc"], data["price"], data["photo"], data["brand"]))
    db.commit()
    
    
async def get_data_by_type(type):
    data = cur.execute('SELECT i_id, type, name, brand, desc, price, photo FROM items WHERE type = ?', (type,)).fetchall()
    return data


async def get_data_by_id(id):
    data = cur.execute('SELECT i_id, type, name, brand, desc, price, photo FROM items WHERE i_id = ?', (id,)).fetchone()
    return data


async def update_item_db(data):
    cur.execute('UPDATE items SET type = ?, name = ?, desc = ?, price = ?, photo = ?, brand = ? WHERE i_id = ?', 
                (data["type"], data["name"], data["desc"], data["price"], data["photo"], data["brand"], data["id"]))
    db.commit()
    

async def delete_item_db(id):
    cur.execute('DELETE FROM items WHERE i_id = ?', (id,))
    db.commit()
    
    
async def add_item_to_cart_db(user_id, item_id):
    cur.execute('UPDATE users SET cart_id = ? WHERE user_id = ?', (item_id, user_id))
    db.commit()
    
    
async def get_user_data_by_user_id(user_id):
    data = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return data