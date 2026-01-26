import psycopg2
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class DBConfig(BaseSettings):
    """ Database configuration loaded from environment variables.

    Attributes:
        name (str): Database name.
        user (str): Username for authentication.
        host (str): Database host address.
        password (SecretStr): Password for authentication.
        port (int): Port number used to connect to the database.
        ssl_mode (str): SSL mode used for the connection.

    Model Config:
        env_prefix (str): Prefix of environment variables (``DB_``).
        env_file_encoding (str): UTF-8 Encoding used when reading the environment file.

    """
    name: str
    user: str
    host: str
    password: SecretStr
    port: int
    ssl_mode: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file_encoding="utf-8"
    )

    def __init__(self, env_file: Path | str, **kwargs):
        """ Initialises the db instance.

        Validates that the provided environment file exists and injects it
        into the model configuration.

        Args:
            env_file (Path | str): Path to the environment file.
            **kwargs: Additional keyword arguments passed to ``BaseSettings``.

        Raises:
            ValueError: If ``env_file`` is not provided.
            FileNotFoundError: If the specified ``env_file`` does not exist.
        """
        if not env_file:
            raise ValueError("env_file must be provided")

        env_path = Path(env_file)
        if not env_path.exists():
            raise FileNotFoundError("env_file does not exist")

        # override the env_file in model_config
        self.model_config["env_file"] = env_path

        super().__init__(**kwargs)

    def get_conn(self) -> psycopg2.extensions.connection:
        """ Return a psycopg2 connection using the db database credentials.

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
            "DB Configuration\n"
            "----------------\n"
            f"Name:       {self.name}\n"
            f"User:       {self.user}\n"
            f"Host:       {self.host}\n"
            f"Password:   {password}\n"
            f"Port:       {self.port}\n"
            f"SSL Mode:   {self.ssl_mode}"
        )