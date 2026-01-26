import psycopg2
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path
from typing import override


class DBConfig(BaseSettings):
    """ Database configuration loaded from environment variables.

    Environment variables are expected to use the ``DB_`` prefix and be read
    from the provided environment file.

    Attributes:
        name (str): Database name.
        user (str): Username for authentication.
        host (str): Database host address.
        password (SecretStr): Password for authentication.
        port (int): Port number used to connect to the database.
        ssl_mode (str): SSL mode used for the connection.
    """
    name: str
    user: str
    host: str
    password: SecretStr
    port: int
    ssl_mode: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file_encoding="utf-8",
        extra="ignore",  # optional but recommended
    )

    def get_conn(self) -> psycopg2.extensions.connection:
        """ Create and return a psycopg2 connection using the configured credentials.

        Returns:
            connection: psycopg2.extensions.connection

        """
        conn = psycopg2.connect(
            database=self.name,
            user=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            sslmode=self.ssl_mode
        )  # get a connection, if it cannot be made an exception will be raised here
        return conn

    def test_connection(self) -> None:
        """ Test the connection to the database.

        Raises:
            psycopg2.OperationalError: If the database connection fails.
        """
        with self.get_conn() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                print("Connection successful:", cursor.fetchone())
            except psycopg2.OperationalError as e:
                print("Connection failed:", e)
                raise

    def pretty(self, show_private: bool = False) -> str:
        """ Pretty print DBConfig attributes. Hides user password by default.

        Args:
            show_private (bool): Whether to include private attributes.

        Returns:
            str: A formatted string representation of db attributes.

        """
        password = (
            self.password.get_secret_value()
            if show_private
            else str(self.password)
        )

        return (
            "\n"
            "DB Configuration\n"
            "----------------\n"
            f"Name:       {self.name}\n"
            f"User:       {self.user}\n"
            f"Host:       {self.host}\n"
            f"Password:   {password}\n"
            f"Port:       {self.port}\n"
            f"SSL Mode:   {self.ssl_mode}"
        )