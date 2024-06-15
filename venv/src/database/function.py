# ここではdatabaseについての設定を行うが、sqlite3を使用予定。
import sqlite3



# アプリの起動時にデータベースを作成
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


# 送られてきたメッセージをデータベースに保存
def save_message(user_id, message):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))
        conn.commit()
