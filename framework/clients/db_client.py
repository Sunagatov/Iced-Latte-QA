import logging

from typing import Optional, List

from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class DBClient:
    def __init__(self, dbname: str, host: str, port: str, user: str, password: str):
        """Initializing the connection

        Args:
            dbname:     name Postgres database;
            host:       URL for connecting to the Postgres database;
            port:       port for connecting to the Postgres database;
            user:       username for connecting to the Postgres database;
            password:   password for connecting to the Postgres database.
        """
        self.conn = connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        logging.info(self.conn)

    def close(self) -> None:
        if not self.conn:
            logging.info("Not connection")
            return
        if self.cur:
            logging.info("Cursor the closed")
            self.cur.close()
        logging.info("Connection the closed")
        self.conn.close()

    def execute(self, query: str) -> None:
        """Executing a query to the Postgres database without returning data

        Args:
            query: query to the Postgres database
        """
        logging.debug(query)
        self.cur.execute(str(query), None)

    def fetch_all(self, query: str) -> Optional[List[dict]]:
        """Executing a query to the Postgres database with returning data in the form of list

        Args:
            query: query to the Postgres database

        Returns:
            [{row1}, {row2}, ...]
        """
        self.execute(query)
        records = self.cur.fetchall()
        if records:
            rows = [dict(rec) for rec in records]
            return rows

        return []
