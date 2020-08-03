import os
import psycopg2
import time


def is_postgres_up():
    dbname = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST', 'postgres')
    try:
        psycopg2.connect(
            dbname=dbname, user=user, host=host, password=password)
    except psycopg2.OperationalError:
        return False
    return True


if __name__ == '__main__':
    while not is_postgres_up():
        print('Waiting for postgres')
        time.sleep(5)
