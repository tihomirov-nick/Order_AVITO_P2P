import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('users.db')
    cur = base.cursor()
    if base:
        print("data base 'users.db' connected")
    base.execute('CREATE TABLE IF NOT EXISTS USERS(user_id TEXT PRIMARY KEY, status TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS ADMINS(admin_id TEXT PRIMARY KEY, status TEXT)')
    base.commit()


async def get_all_admins():
    return cur.execute('''SELECT admin_id FROM ADMINS''').fetchall()


async def get_all_users():
    return cur.execute('''SELECT user_id FROM USERS''').fetchall()


async def set_default(user_id, admin_id):
    cur.execute('''UPDATE ADMINS SET status = ? WHERE admin_id == ?''', ("None", admin_id))
    cur.execute('''UPDATE users SET status = ? WHERE user_id == ?''', ("None", user_id))
    base.commit()


async def get_admin_id(user_id):
    return cur.execute('''SELECT status FROM USERS WHERE user_id == ?''', (user_id,)).fetchall()[0][0]


async def get_user_id(admin_id):
    return cur.execute('''SELECT status FROM ADMINS WHERE admin_id == ?''', (admin_id,)).fetchall()[0][0]


async def start_dialog(user_id, admin_id):
    cur.execute('''UPDATE ADMINS SET status = ? WHERE admin_id == ?''', (user_id, admin_id))
    cur.execute('''UPDATE USERS SET status = ? WHERE user_id == ?''', (admin_id, user_id))
    base.commit()


async def check_for_free():
    return cur.execute('''SELECT * FROM USERS WHERE status == ?''', ("FREE",)).fetchall()


async def new_admin(user_id):
    if str(user_id) in str(cur.execute('''SELECT * FROM ADMINS''').fetchall()):
        cur.execute('''UPDATE ADMINS SET status = ? WHERE admin_id == ?''', ("FREE", int(user_id)))
    else:
        cur.execute('''INSERT INTO ADMINS VALUES (?, ?)''', (user_id, "FREE"))
    base.commit()


async def new_user(user_id):
    if str(user_id) in str(cur.execute('''SELECT * FROM USERS''').fetchall()):
        cur.execute('''UPDATE USERS SET status = ? WHERE user_id == ?''', ("FREE", int(user_id)))
    else:
        cur.execute('''INSERT INTO USERS VALUES (?, ?)''', (user_id, "FREE"))
    base.commit()
