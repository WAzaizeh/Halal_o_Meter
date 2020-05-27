# PostreSQL database for saving the scraped data

import psycopg2
from psycopg2 import sql

def append_to_businesses(name, id, url, review_count, address):
    try:
        connection, cursor = _connect_to_database()

        # insert row into table
        table = 'Google_businesses' if 'google' in url else 'Yelp_businesses'
        cursor.execute(                                                # correct
        sql.SQL("""INSERT INTO {} (Name, ID, URL, Total_review_count, Address) VALUES (%s, %s, %s, %s, %s)""").format(sql.Identifier(table)),
        (name, id, url, review_count, address))

        # # testing
        # print("Table After updating record ")
        # sql_select_query = 'SELECT * from "{}"'.format(table)
        # cursor.execute(sql_select_query)
        # record = cursor.fetchall()
        # print(record)


    finally:
        # closing database connection
        _close_connection(connection, cursor)

def _connect_to_database():
    try:
        connection = psycopg2.connect(user="wesamazaizeh",
                                      password="melad5RA",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="halal_o_meter")
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, psycopg2.Error) as error:
        print('Error in update operation\n', error)



def _close_connection(connection, cursor):
    if (connection):
        cursor.close()
        connection.close()
        print('PostgreSQL connection is closed')
