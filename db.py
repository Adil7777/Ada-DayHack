# import tools
import sqlite3


class DataBase:
    __connection = None

    def get__connection(self):
        if DataBase.__connection is None:
            DataBase.__connection = sqlite3.connect('Users.db', check_same_thread=False)
        return DataBase.__connection

    def init_db(self, force: bool = False):
        """ Проверить что нужные таблицы существуют, иначе создать их
            Важно: миграции на такие таблицы вы должны производить самостоятельно!
            :param conn: подключение к СУБД
            :param force: явно пересоздать все таблицы
        """
        conn = self.get__connection()
        c = conn.cursor()

        # Информация о пользователе
        # TODO: создать при необходимости...

        # Сообщения от пользователей
        if force:
            c.execute('DROP TABLE IF EXISTS user_message')

        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                name        TEXT NOT NULL,
                surname     TEXT NOT NULL,
                account     TEXT NOT NULL,
                email       TEXT NOT NULL,
                code        TEXT NOT NULL
            )
        ''')

        # Сохранить изменения
        conn.commit()

    def add_user(self, user_id: int, name, surname, account, email):
        # adding user to database
        conn = self.get__connection()
        c = conn.cursor()
        c.execute('INSERT INTO users (user_id, name, surname, account, email, code) VALUES (?, ?, ?, ?, ?, ?)',
                  (user_id, name, surname, account, email, 's',))
        conn.commit()

    def get_user(self, user_id):
        # get user from a database
        conn = self.get__connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE (user_id) = ?', (user_id,))

        rows = c.fetchall()
        user_ids = []
        for i in rows:
            user_ids.append(i)
        return user_ids[0]

    def subscriber_exist(self, user_id):
        # checking if user already in database
        conn = self.get__connection()
        c = conn.cursor()
        return c.execute('SELECT * FROM users WHERE (user_id) = ?', (user_id,))

    def get_users(self):
        # getting all users from database
        conn = self.get__connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        user_ids = []
        for i in rows:
            user_ids.append(i[1])
        return user_ids
