from typing import List, Optional

from framework.clients.db_client import DBClient
from framework.tools.generators import generate_string, generate_user


class PostgresDB:
    host = None
    port = None
    dbname = None
    user = None
    password = None

    def __init__(self):
        """Initializing the connection"""

        self.db = DBClient(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
        )

    def close(self) -> None:
        """Closing the connection"""
        self.db.close()

    def get_data_by_filter(
            self, table: str, field: str, value: str
    ) -> Optional[List[dict]]:
        """Getting data from table by filter field and its value

        Args:
            table: table in database;
            field: field of table;
            value: field value.
        """
        response = self.db.fetch_all(
            f"""
                SELECT *
                FROM {table}
                WHERE {field} = '{value}';
            """
        )

        return response

    def get_random_products(self, quantity: int = 1) -> Optional[List[dict]]:
        """Getting a random product

        Args:
            quantity: number of random products
        """
        response = self.db.fetch_all(
            f"""
                SELECT *
                FROM product
                WHERE active = true
                ORDER BY RANDOM()
                LIMIT {quantity};
            """
        )
        return response

    def get_product_by_filter(
            self, field: str, ascend: bool = False, size: int = -1, page: int = -1
    ) -> Optional[List[dict]]:
        """Getting sorted products by size and page by page

        Args:
            field:  field for sorted;
            ascend: ascending sorted, True - ascending, False - descending;
            size:   the amount of data per page;
            page:   page number.
        """
        response = f"""
            SELECT *
            FROM product
            ORDER BY {field} {'ASC' if ascend else 'DESC'}
        """
        if size > 0:
            response += f" LIMIT {size}"
        if page >= 0:
            response += f" OFFSET {size * page}"
        return self.db.fetch_all(response)

    def get_random_users(self, quantity: int = 1) -> List[dict]:
        """Getting a random user

        Args:
            quantity: number of random users
        """
        response = self.db.fetch_all(
            f"""
                SELECT *
                FROM user_details
                ORDER BY RANDOM()
                LIMIT {quantity};
            """
        )
        return response

    def create_user(self, user: dict) -> None:
        """Inserting user into database

        Args:
            user: user data:
                - id - user of id;
                - first_name - first name of user;
                - last_name - last name of user;
                - email - email of user;
                - password - password for user;
                - hashed_password - hash of password for user.
        """
        self.db.execute(
            f"""
                INSERT INTO public.user_details(id
                    , first_name
                    , last_name
                    , stripe_customer_token
                    , email
                    , password
                    , address_id
                    , account_non_expired
                    , account_non_locked
                    , credentials_non_expired
                    , enabled
                )
                VALUES ('{user["id"]}'
                    , '{user["first_name"]}'
                    , '{user["last_name"]}'
                    , null, '{user["email"]}'
                    , '{user["hashed_password"]}'
                    , null
                    , true
                    , true
                    , true
                    , true
                );
            """
        )

    def create_random_users(self, quantity: int = 1) -> List[dict]:
        """Creating random user(s)

        Args:
            quantity: number of random users
        """
        users = [self.create_user(generate_user()) for _ in range(quantity)]

        return users

    def delete_user(self, user_id: str) -> None:
        """Deletes a user from the database based on user ID

        Args:
            user_id: user ID
        """
        delete_query = f"DELETE FROM public.user_details WHERE id = '{user_id}';"
        self.db.execute(delete_query)
