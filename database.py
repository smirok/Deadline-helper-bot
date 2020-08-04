import sqlite3


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
    def update(cls, query: Query, old_deadline: str):
        old_query = Query(query.subject, query.task,
                          '.'.join(reversed(old_deadline.split('.'))))
        cls.delete(old_query)
        cls.add(query)

    @classmethod
    def delete(cls, query: Query):
        database_query = f"""
        DELETE FROM deadlines WHERE
        subject = '{query.subject}' AND task = '{query.task}'
        AND deadline = '{query.deadline}'
        """
        cls.cursor.execute(database_query)
        cls.conn.commit()

    @classmethod
    def show(cls) -> str:
        cls.cursor.execute("SELECT * FROM deadlines ORDER BY deadline ASC")
        message = ''
        while True:
            row = cls.cursor.fetchone()

            if row is None:
                break

            message += f'{row[0]} {row[1]} {".".join(reversed(row[2].split(".")))}\n'

        return message
