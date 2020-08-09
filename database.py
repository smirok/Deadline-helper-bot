import sqlite3
import os.path
from typing import NamedTuple, Optional, List


class Query(NamedTuple):
    subject: str
    task: str
    deadline: str


class Database:
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    @classmethod
    def init(cls):
        cls.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'deadlines.db'))
        cls.cursor = cls.conn.cursor()

        database_query = """
        CREATE TABLE IF NOT EXISTS deadlines (
            subject TEXT,
            task TEXT,
            deadline TEXT
        )
        """
        cls.cursor.execute(database_query)
        cls.conn.commit()

    @classmethod
    def add(cls, query: Query):
        database_query = f"""
        INSERT INTO deadlines (subject , task, deadline)
        VALUES ('{query.subject}', '{query.task}', '{query.deadline}')
        """
        cls.cursor.execute(database_query)
        cls.conn.commit()

    @classmethod
    def update(cls, query: Query, old_deadline: str):
        old_query = Query(
            query.subject,
            query.task,
            '.'.join(reversed(old_deadline.split('.')))
        )
        cls.delete(old_query)
        cls.add(query)

    @classmethod
    def delete(cls, query: Query):
        database_query = f"""
        DELETE
        FROM deadlines
        WHERE subject = '{query.subject}'
            AND task = '{query.task}'
            AND deadline = '{query.deadline}'
        LIMIT 1
        """
        cls.cursor.execute(database_query)
        cls.conn.commit()

    @classmethod
    def show(cls, subject: Optional[str], task: Optional[str]) -> List[str]:
        """
        If subject and task both are None : return all records from database
        Else matching by subject and task
        """
        database_query = """
        SELECT *
        FROM deadlines
        ORDER BY deadline
        ASC
        """
        cls.cursor.execute(database_query)
        picked_deadlines = []
        while True:
            row = Database.cursor.fetchone()

            if row is None:
                break

            if row[0] == subject and row[1] == task or subject is None and task is None:
                picked_deadlines.append(f'{row[0]} {row[1]} '
                                        f'{".".join(reversed(row[2].split(".")))}')
        return picked_deadlines
