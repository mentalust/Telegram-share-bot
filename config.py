import sqlite3
db = sqlite3.connect('db.db', check_same_thread=False)
sql = db.cursor()

token = 'token'

admins = [our telegram id]

username_bot = 'name'

global link_channel
link_channel = 'link'