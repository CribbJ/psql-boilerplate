# test_dbconfig.py
import pytest
from unittest.mock import patch

from src.db.models import DBConfig

@pytest.fixture
def valid_env_file(tmp_path):
    """Creates a valid temporary .env file."""
    env = tmp_path / ".env"
    env.write_text(
        "DB_NAME=testdb\n"
        "DB_USER=testuser\n"
        "DB_PASSWORD=testpass\n"
        "DB_HOST=localhost\n"
        "DB_PORT=5432\n"
        "DB_SSL_MODE=require\n"
    )
    return env


@pytest.fixture
def malformed_env_file(tmp_path):
    """Creates an env file missing required fields."""
    env = tmp_path / ".env"
    env.write_text(
        "DB_NAME=testdb\n"
        "DB_USER=testuser\n"
        # Missing password, host, port, ssl_mode
    )
    return env


# without env file argument
def test_db_config_without_env_file_argument():
    with pytest.raises(ValueError) as exc:
        DBConfig(env_file=None)

    assert "env_file must be provided" in str(exc.value)

# wrong env file argument
def test_db_config_with_wrong_env_file_argument():
    with pytest.raises(FileNotFoundError):
        DBConfig(env_file="does_not_exist.env")


# with env file argument
@patch("src.db.models.DBConfig.test_connection")
def test_db_config_with_env_file_argument(mock_test_conn, valid_env_file):
    """Valid env file should load successfully and call test_connection()."""
    cfg = DBConfig(env_file=valid_env_file)

    assert cfg.name == "testdb"
    assert cfg.user == "testuser"
    assert cfg.host == "localhost"
    assert cfg.port == 5432
    assert cfg.ssl_mode == "require"

    mock_test_conn.assert_called_once()


# malformed env file
def test_db_config_with_malformed_env_file(malformed_env_file):
    """Malformed env file should raise ValueError with helpful message."""
    with pytest.raises(ValueError) as exc:
        DBConfig(env_file=malformed_env_file)

    msg = str(exc.value)
    assert "missing required DB_ variables" in msg

# get connection function
def test_db_config_get_conn_function():
    pass

# pretty print without any arguments. Should default to show_private = False
def test_db_config_pretty_print_without_arguments(valid_env_file):
    """pretty() should hide password by default."""
    with patch("src.db.models.DBConfig.test_connection"):
        cfg = DBConfig(env_file=valid_env_file)

    output = cfg.pretty()

    assert "Password:   **********" in output
    assert "testpass" not in output
    assert "SecretStr" not in output

# pretty print with show_private false and true
def test_db_config_pretty_print_with_arguments(valid_env_file):
    """pretty(show_private=True) should reveal password."""
    with patch("src.db.models.DBConfig.test_connection"):
        cfg = DBConfig(env_file=valid_env_file)

    output = cfg.pretty(show_private=True)

    assert "Password:   testpass" in output
    assert "SecretStr" not in output
