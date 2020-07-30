import sqlite3
from typing import Optional


class Query:
    subject = ''
    task = ''
    date = ''


"""  DATE format : "HH:MM:DD:MM:YY"  """


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("deadlines.db")  # ??? TO DO
        self.cursor = self.conn.cursor()

        is_db_exists = self.cursor.fetchall()
        if is_db_exists:
            return

        self.cursor.execute("""CREATE TABLE deadlines
                            (subject text, task text, date text)
                            """)
        self.conn.commit()

    def add(self, query: Query):
        self.cursor.execute(f"""INSERT INTO deadlines (subject, task, date)
                            VALUES ({query.subject},
                            {query.task}, {query.date})
                            """)
        self.conn.commit()

    def update(self, query: Query, updatable_task: Optional[str],
               updatable_date: Optional[str]):
        new_task = query.task if updatable_task is None else updatable_task
        new_date = query.date if updatable_date is None else updatable_date

        database_query = f"""
        UPDATE deadlines
        SET subject = query.subject and task = new_task and date = new_date
        WHERE subject = query.subject and task = query.task
        """
        self.cursor.execute(database_query)
        self.conn.commit()

    def delete(self, query: Query):
        database_query = f"""
        DELETE FROM deadlines WHERE
        subject = query.subject and task = query.task and date = query.date
        """
        self.cursor.execute(database_query)
        self.conn.commit()
