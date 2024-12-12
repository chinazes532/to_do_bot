import aiosqlite as sq

from config import DB_NAME


async def create_db():
    async with sq.connect(DB_NAME) as db:
        print("Database created!")

        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            phone TEXT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            task_title TEXT,
            task_status BOOLEAN
            )""")

        await db.commit()


async def insert_user(user_id, username, name, phone):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)", (user_id, username, name, phone))
        await db.commit()


async def get_user(user_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result


async def get_tasks_by_user_id(user_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchall()
            return result


async def insert_task(user_id, task_title, task_status):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT INTO tasks(user_id, task_title, task_status) VALUES (?, ?, ?)", (user_id, task_title, task_status))
        await db.commit()


async def get_tasks_count_by_user_id_and_status(user_id, status):
    async with sq.connect(DB_NAME) as db:
        async with db.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND task_status = ?', (user_id, status)) as cursor:
            result = await cursor.fetchone()
            return result


async def get_task(task_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,)) as cursor:
            result = await cursor.fetchone()
            return result


async def update_task_status(task_id, status):
    async with sq.connect(DB_NAME) as db:
        await db.execute('UPDATE tasks SET task_status = ? WHERE task_id = ?', (status, task_id))
        await db.commit()


async def delete_task(task_id):
    async with sq.connect(DB_NAME) as db:
        await db.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
        await db.commit()


async def get_task_ids_by_user_id_and_keywords(user_id, task_title):
    async with sq.connect(DB_NAME) as db:
        query = 'SELECT task_id FROM tasks WHERE user_id = ? AND task_title LIKE ?'
        search_pattern = f'%{task_title}%'
        async with db.execute(query, (user_id, search_pattern)) as cursor:
            results = await cursor.fetchall()
            return [row[0] for row in results]


async def get_tasks_by_ids(task_ids):
    async with sq.connect(DB_NAME) as db:
        query = 'SELECT * FROM tasks WHERE task_id IN ({})'.format(','.join('?' * len(task_ids)))
        async with db.execute(query, task_ids) as cursor:
            return await cursor.fetchall()

