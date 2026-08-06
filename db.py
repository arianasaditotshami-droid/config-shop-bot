import sqlite3


DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)



def create_tables():

    db = connect()
    cur = db.cursor()


    # کاربران
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        points INTEGER DEFAULT 0,
        balance INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0
    )
    """)


    # پکیج ها
    cur.execute("""
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        volume TEXT,
        duration TEXT
    )
    """)


    # سفارش ها
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        package TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)


    # کانفینگ های کاربران
    cur.execute("""
    CREATE TABLE IF NOT EXISTS configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        config TEXT
    )
    """)


    # کد هدیه
    cur.execute("""
    CREATE TABLE IF NOT EXISTS gifts (
        code TEXT PRIMARY KEY,
        points INTEGER
    )
    """)


    db.commit()
    db.close()



# ثبت کاربر

def add_user(user_id, username):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id, username) VALUES (?,?)",
        (user_id, username)
    )

    db.commit()
    db.close()



# امتیاز

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
        (amount,user_id)
    )

    db.commit()
    db.close()



# موجودی حساب

def get_balance(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()

    db.close()

    return result[0] if result else 0



def add_balance(user_id, amount):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE users SET balance = balance + ? WHERE user_id=?",
        (amount,user_id)
    )

    db.commit()
    db.close()



# پکیج ها

def add_package(name, price, volume, duration):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO packages(name,price,volume,duration) VALUES (?,?,?,?)",
        (name,price,volume,duration)
    )

    db.commit()
    db.close()



def get_packages():

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM packages"
    )

    result = cur.fetchall()

    db.close()

    return result



# سفارش

def add_order(user_id, package):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO orders(user_id,package) VALUES (?,?)",
        (user_id,package)
    )

    db.commit()
    db.close()



# کانفینگ

def add_config(user_id, config):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO configs(user_id,config) VALUES (?,?)",
        (user_id,config)
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

# =====================
# سیستم زیرمجموعه و امتیاز
# =====================

def add_referral(user_id):
    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE users 
        SET referrals = referrals + 1,
            points = points + 5
        WHERE user_id=?
        """,
        (user_id,)
    )

    db.commit()
    db.close()



def get_referrals(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT referrals FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()

    db.close()

    return result[0] if result else 0
def set_referrer(user_id, referrer_id):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT referrer FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cur.fetchone()

    if user and (user[0] is None or user[0] == 0):
        cur.execute(
            "UPDATE users SET referrer=? WHERE user_id=?",
            (referrer_id, user_id)
        )

        cur.execute(
            """
            UPDATE users
            SET points = points + 5,
                referrals = referrals + 1
            WHERE user_id=?
            """,
            (referrer_id,)
        )

    db.commit()
    db.close()
def add_points(user_id, amount):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE users SET points = points + ? WHERE user_id=?",
        (amount, user_id)
    )

    db.commit()
    db.close()



def remove_points(user_id, amount):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE users SET points = points - ? WHERE user_id=? AND points >= ?",
        (amount, user_id, amount)
    )

    db.commit()
    db.close()



def get_gift(code):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT points FROM gifts WHERE code=? AND used=0",
        (code,)
    )

    result = cur.fetchone()

    db.close()

    return result



def use_gift(code):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE gifts SET used=1 WHERE code=?",
        (code,)
    )

    db.commit()
    db.close()
