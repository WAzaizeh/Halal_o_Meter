"""Connect to a PostgreSQL database and execute queries"""

import sys, os
import psycopg2
from dotenv import load_dotenv
import pandas as pd

class Database:
    """PostgreSQL Database class"""

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


    def select_rows(self, query, *args):
        """Run a SQL query to select rows from table"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, args)
            records = [row for row in cur.fetchall()]
        cur.close()
        return records


    def select_df(self, query, *args):
        """Run a SQL query to select rows from table and return pandas dataframe"""
        self.connect()
        dat = pd.read_sql_query(query, self.conn)
        self.conn = None
        return dat

    def insert_row(self, query, *args):
        """Run a SQL query to update rows in table"""
        try:
            self.connect()
            with self.conn.cursor() as cur:
                # cur.mogrify(query, args)
                cur.execute(query, args)
                self.conn.commit()
                cur.close()
        except Exception as e:
            self.conn.rollback()
            # get details about the exception
            e_type, e_obj, traceback = sys.exc_info()
            # get the line number when exception occured
            line_num = traceback.tb_lineno
            # print the connect() error
            print ("\npsycopg2 ERROR:", e, "on line number:", line_num)
            print ("psycopg2 traceback:", traceback, "-- type:", e_type)

    def insert_rows(self, query, *args):
        """Run a SQL query to update rows in table"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.executemany(query, args)
            self.conn.commit()
            cur.close()
