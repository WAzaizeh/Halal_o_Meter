# PostreSQL database for saving the scraped data

import psycopg2
from psycopg2 import sql


def append_to_businesses(name, id, url, review_count, address):
    try:
        # connecto to database
        connection, cursor = _connect_to_database()

        # insert row into approproate businesses table
        cursor.execute(                                                # correct
        sql.SQL("""INSERT INTO businesses (Name, ID, URL, Total_review_count, Address) VALUES (%s, %s, %s, %s, %s)"""),
        (name, id, url, review_count, address))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print('Error in update operation\n', error)

    finally:
        # closing database connection
        _close_connection(connection, cursor)


def append_to_reviews(id, url, review_text, review_date):
    try:
        connection, cursor = _connect_to_database()

        # insert row into reviews database
        cursor.execute(                                                # correct
        sql.SQL("""INSERT INTO reviews (restaurnat_id, url, review_text, review_date) VALUES (%s, %s, %s, %s)"""),
        (id, url, review_text, review_date))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print('Error in update operation\n', error)

    finally:
        # closing database connection
        _close_connection(connection, cursor)


def fetch_urls(source):
    try:
        connection, cursor = _connect_to_database()

        # fetch list of urls for the corresponding source
        like_pattern = '%{}%'.format(source)
        cursor.execute(
        sql.SQL(""" SELECT url from businesses
            WHERE url LIKE LOWER(%s)
        """),(like_pattern,)
        )

        rows = cursor.fetchall()
        return rows

    except (Exception, psycopg2.Error) as error:
        print('Error in update operation\n', error)

    finally:
        # closing database connection
        _close_connection(connection, cursor)

def get_reviews():
    try:
        connection, cursor = _connect_to_database()

        # fetch list of urls for the corresponding source
        cursor.execute(
        sql.SQL(""" SELECT review_text from reviews"""))

        rows = cursor.fetchall()
        return rows

    except (Exception, psycopg2.Error) as error:
        print('Error in update operation\n', error)

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
