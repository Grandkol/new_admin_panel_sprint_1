# import sqlite3
import logging
import os
import sqlite3
from dataclasses import fields, astuple

import psycopg
from dotenv import load_dotenv
from psycopg import ClientCursor, connection as _connection
from psycopg import sql
from psycopg.rows import dict_row

from tables_dataclass import (Filmwork, Genre,
                              GenreFilmWork, Person,
                              PersonFilmWork)

load_dotenv()


log = logging.getLogger(__name__)

TABLES_CLASSES = {
    "film_work": Filmwork,
    "genre": Genre,
    "person": Person,
    "genre_film_work": GenreFilmWork,
    "person_film_work": PersonFilmWork,
}


def sqlite_loader(connection, table, dataclass):

    data = []
    curs = connection.cursor()
    result = curs.execute(f"SELECT * FROM {table}")
    for row in result:
        piece = dataclass(*row)
        data.append(piece)
    return data


def postgres_saver(connection, table, data):

    curs = connection.cursor()
    curs.execute(sql.SQL(f"TRUNCATE content.{table}"))

    for piece in data:
        column_names = [field.name for field in fields(piece)]
        column_name_str = ", ".join(column_names)
        col_count = ", ".join(["%s"] * len(column_names))

        bind_values = ",".join(
            curs.mogrify(f"({col_count})", astuple(piece)) for piece in data
        )

        query = (
            f"INSERT INTO content.{table} ({column_name_str}) "
            f"VALUES {bind_values} "
            f"ON CONFLICT (id) DO NOTHING"
        )

        curs.execute(query)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    for table, dataclass in TABLES_CLASSES.items():
        try:

            data = sqlite_loader(connection, table, dataclass)
        except Exception:
            log.exception("Ошибка при чтении из SQlite")
            break
        try:
            postgres_saver(pg_conn, table, data=data)
        except Exception:
            log.exception(("Ошибка при загрузке в Postgres"))
            break


if __name__ == "__main__":
    dsl = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }

    with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
