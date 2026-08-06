import sqlite3


DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():

    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        points INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        package TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS gifts (
        code TEXT PRIMARY KEY,
        points INTEGER DEFAULT 0
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        config TEXT
    )
    """)


    db.commit()
    db.close()



def add_user(user_id, username):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id, username) VALUES (?,?)",
        (user_id, username)
    )

    db.commit()
    db.close()



def get_points(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()

    db.close()

    return result[0] if result else 0



def add_points(user_id, amount):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE users SET points = points + ? WHERE user_id=?",
        (amount, user_id)
    )

    db.commit()
    db.close()



def add_order(user_id, package):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO orders(user_id, package) VALUES (?,?)",
        (user_id, package)
    )

    db.commit()
    db.close()



def get_orders(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT package,status FROM orders WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchall()

    db.close()

    return result



def add_config(user_id, config):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO configs(user_id, config) VALUES (?,?)",
        (user_id, config)
    )

    db.commit()
    db.close()



def get_configs(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT config FROM configs WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchall()

    db.close()

    return result
