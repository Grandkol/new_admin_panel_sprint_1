import os
import sqlite3

import psycopg
from dotenv import load_dotenv
from psycopg import ClientCursor
from psycopg.rows import dict_row

from sqlite_to_postgres.tables_dataclass import (
    Filmwork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)

load_dotenv()

TABLES_CLASSES = {
    "film_work": Filmwork,
    "genre": Genre,
    "person": Person,
    "genre_film_work": GenreFilmWork,
    "person_film_work": PersonFilmWork,
}


class CheckConsistency:
    def __init__(self, connection_sl, connection_pg, table_name, dataclass):
        self.curs_sl = connection_sl.cursor()
        self.curs_pg = connection_pg.cursor()
        self.table_name = table_name
        self.dataclass = dataclass

    def tables_from_SQlite(self):
        self.curs_sl.execute("SELECT name "
                             "FROM sqlite_master "
                             "WHERE type='table'")
        tables = [table[0] for table in self.curs_sl.fetchall()]
        return tables

    def tables_from_PSG(self):
        data = []
        self.curs_pg.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'content'"
        )
        for table in self.curs_pg.fetchall():
            data.append(table["table_name"])
        return data

    def data_from_SQlite(self):
        data = []
        self.curs_sl.execute(f"SELECT COUNT(*) "
                             f"FROM {self.table_name}")
        count = self.curs_sl.fetchone()[0]

        self.curs_sl.execute(f"SELECT * FROM {self.table_name}")

        for row in self.curs_sl.fetchall():
            row = self.dataclass(*row)
            data.append(row)

        return count, data

    def data_from_PSG_id(self, id):
        self.curs_pg.execute(f"SELECT * FROM content.{self.table_name} "
                             f"WHERE id='{id}'")
        return self.curs_pg.fetchone()

    def count_from_PSG(
        self,
    ):
        self.curs_pg.execute(f"SELECT COUNT(*) "
                             f"FROM {self.table_name}")
        return self.curs_pg.fetchone()["count"]

    def check(self):

        count_sl, data = self.data_from_SQlite()
        count_pg = self.count_from_PSG()
        if count_sl == count_pg:
            print(
                f"Таблицы в БД: {self.table_name}, "
                f"имеют одинаковое количество записей"
            )

        tables_sl = self.tables_from_SQlite()
        tables_pg = self.tables_from_PSG()

        if set(tables_sl) == set(tables_pg):
            print(f"Таблицы в БД: {self.table_name}, "
                  f"соотвествуют друг другу")

        flag = True
        for row in data:
            pg_row = self.dataclass(**self.data_from_PSG_id(row.id))
            if row != pg_row:
                flag = False
        if flag is True:
            print(f"Проверка данных таблиц БД: {self.table_name}, "
                  f"завершена успешно!")
        else:
            print(f"Ошибка при проверке данных "
                  f"в таблицах {self.table_name}")


if __name__ == "__main__":
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("USER"),
        "password": os.environ.get("PASSWORD"),
        "host": os.environ.get("HOST"),
        "port": os.environ.get("PORT"),
    }

    with (sqlite3.connect("sqlite_to_postgres/db.sqlite")
          as sqlite_conn, psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn):
        for table, dataclass in TABLES_CLASSES.items():
            check = CheckConsistency(
                sqlite_conn, pg_conn, table_name=table, dataclass=dataclass
            )
            check.check()

    sqlite_conn.close()
    pg_conn.close()
