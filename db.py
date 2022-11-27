import psycopg


def connection():
    conn = psycopg.connect(
        host="172.17.0.2",
        dbname="sber",
        user="postgres",
        password="postgres",
        autocommit=True)
    return conn
