"""Connect to a PostgreSQL database and execute queries"""

import sys, os
import psycopg2
from dotenv import load_dotenv

class Database:
    """PostgreSQL Database class."""

    def __init__(self):
        load_dotenv()
        self.host = os.getenv('DATABASE_HOST')
        self.username = os.getenv('DATABASE_USERNAME')
        self.password = os.getenv('DATABASE_PASSWORD')
        self.port = os.getenv('DATABASE_PORT')
        self.dbname = os.getenv('DATABASE_NAME')
        self.conn = None


    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(host=self.host,
                                             user=self.username,
                                             password=self.password,
                                             port=self.port,
                                             dbname=self.dbname)
            except psycopg2.DatabaseError as e:
                print('Error in connecting to database ', e)
                sys.exit()
            finally:
                print('Connection opened successfully.')

    def select_rows(self, query):
        """Run a SQL query to select rows from table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
        cur.close()
        return records


    def insert_row(self, query, *args):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, args)
            self.conn.commit()
            cur.close()


    def insert_rows(self, query, *args):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.executemany(query, args)
            self.conn.commit()
            cur.close()
