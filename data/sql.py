import sqlite3
import datetime
import config
db = sqlite3.connect('db.db', check_same_thread=False)
sql = db.cursor()

# sql.execute('INSERT INTO quests (id, first, second) VALUES (?, ?, ?);',(m.from_user.id, 0, 0,))
# sql.execute('SELECT * FROM users WHERE id = ?;', (m.from_user.id,)).fetchone()[2]
# sql.execute('UPDATE users SET nick = ? WHERE id = ?', (m.text, m.from_user.id,))
# sql.execute('DELETE FROM files WHERE link = ?;', (link,))
# db.commit()

async def add_track(title, artist, file_id, pas):
    sql.execute('INSERT INTO files (link, id, title, artist, count, type) VALUES (?, ?, ?, ?, ?, ?);',(pas, file_id, title, artist, 0, 'single',))
    db.commit()

async def check_user(m):
    if sql.execute('SELECT * FROM users WHERE id = ?;', (m.from_user.id,)).fetchone() is None:
        sql.execute('INSERT INTO users (id) VALUES (?);',(m.from_user.id,))
        db.commit()

async def add_count(pas):
    count = sql.execute('SELECT * FROM files WHERE link = ?;', (pas,)).fetchone()[4]
    sql.execute('UPDATE files SET count = ? WHERE link = ?', (count+1, pas,))
    db.commit()

async def count_all_files():
    return sql.execute('SELECT * FROM files WHERE type = ?;', ('single',)).fetchall()
async def count_all_albums():
    return sql.execute('SELECT * FROM files WHERE type = ?;', ('album',)).fetchall()