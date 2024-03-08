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
                "subtype TEXT, "
                "name TEXT, "
                "desc TEXT, "
                "price INTEGER, "
                "photo TEXT, "
                "brand TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders("
                "o_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "date_order DATETIME DEFAULT CURRENT_TIMESTAMP, "
                "order_items TEXT, "
                "full_name TEXT, "
                "user_id INTEGER, "
                "adress TEXT, "
                "phone TEXT, "
                "email TEXT, "
                "total_cost INTEGER, "
                "FOREIGN KEY (user_id) REFERENCES users (id))")
    db.commit()
    
async def cmd_start_db(user_id, user_name):
    user = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if not user:
        cur.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
        db.commit()
        
        
async def get_users_db():
    data = cur.execute('SELECT * FROM users').fetchall()
    return data        
        
async def add_item_db(data):
    cur.execute('INSERT INTO items (type, subtype, name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                (data["type"], data["subtype"], data["name"], data["desc"], data["price"], data["photo"], data["brand"]))
    db.commit()
    
    
async def get_data_by_type(type):
    data = cur.execute('SELECT i_id, type, subtype, name, brand, desc, price, photo FROM items WHERE type = ?', (type,)).fetchall()
    return data


async def get_data_by_id(id):
    data = cur.execute('SELECT i_id, type, subtype, name, brand, desc, price, photo FROM items WHERE i_id = ?', (id,)).fetchone()
    return data


async def update_item_db(data):
    cur.execute('UPDATE items SET type = ?, subtype = ?, name = ?, desc = ?, price = ?, photo = ?, brand = ? WHERE i_id = ?', 
                (data["type"], data["subtype"], data["name"], data["desc"], data["price"], data["photo"], data["brand"], data["id"]))
    db.commit()
    
    
async def update_cart_id(user_id, cart):
    cur.execute('UPDATE users SET cart_id = ? WHERE user_id = ?', (cart, user_id))
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


async def add_order_db(data):
    cur.execute('INSERT INTO orders (order_items, full_name, user_id, adress, phone, email, total_cost) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                (data["order"], data["full_name"], data["user_id"], data["adress"], data["phone"], data["email"], data["total_cost"]))
    db.commit()
    
    
async def get_users_id():
    data = cur.execute('SELECT user_id FROM users').fetchall()
    return data
    
async def get_users_db_ten():
    data = cur.execute('SELECT * FROM users LIMIT 10').fetchall()
    return data    
    
async def get_orders_db():
    data = cur.execute('SELECT * FROM orders').fetchall()
    return data

async def get_items_db():
    data = cur.execute('SELECT * FROM items').fetchall()
    return data



async def get_item_by_type_subtype(type, subtype):
    data = cur.execute('SELECT i_id, type, subtype, name, brand, desc, price, photo FROM items WHERE type = ? AND subtype = ?', (type, subtype)).fetchall()
    return data