import sqlite3
from itertools import count


class Query:
    subject = None
    task = None
    deadline = None

    def __init__(self, subject, task, deadline=None):
        self.subject = subject
        self.task = task
        self.deadline = deadline


class Database:
    conn = None
    cursor = None

    @classmethod
    def init(cls):
        cls.conn = sqlite3.connect("deadlines.db")  # ??? TO DO
        cls.cursor = cls.conn.cursor()

        cls.cursor.execute("""CREATE TABLE IF NOT EXISTS deadlines
                            (subject TEXT, task TEXT, deadline TEXT)
                            """)
        cls.conn.commit()

    @classmethod
    def add(cls, query: Query):
        cls.cursor.execute(f"""INSERT INTO deadlines """
                           f"""VALUES ('{query.subject}',
                           '{query.task}', '{query.deadline}')
                           """)
        cls.conn.commit()

    @classmethod
    def update(cls, query: Query):
        database_query = f"""
        UPDATE deadlines
        SET subject = '{query.subject}' AND task = '{query.task}'
        AND deadline = '{query.deadline}'
        WHERE subject = '{query.subject}' AND task = '{query.task}'
        """
        cls.cursor.execute(database_query)
        cls.conn.commit()

    @classmethod
    def delete(cls, query: Query):
        database_query = f"""
        DELETE FROM deadlines WHERE
        subject = '{query.subject}' AND task = '{query.task}'
        """
        cls.cursor.execute(database_query)
        cls.conn.commit()

    @classmethod
    def show(cls) -> str:
        cls.cursor.execute("SELECT * FROM deadlines")
        message = ''
        row_number = count(1)
        while True:
            row = cls.cursor.fetchone()

            if row is None:
                break

            message += f'{next(row_number)}) {row[0]} {row[1]} {row[2]}\n'

        return message
