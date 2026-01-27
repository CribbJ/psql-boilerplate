# psql-boilerplate
Minimal starter template for PostgreSQL projects.

# DBConfig

`DBConfig` is a lightweight config helper for loading database credentials
from a `.env` file, validating them, and establishing a PostgreSQL connection
using `psycopg2`. It is built on top of **Pydantic BaseSettings**, 
giving you type‑safe configuration with automatic environment parsing.

---

## Installation

Make sure your environment includes:

- Python 3.13+
- `pydantic-settings`
- `psycopg2` (or `psycopg2-binary` for local development)

```bash
pip install pydantic-settings psycopg2-binary
```

## Usage

Use the `DBConfig` class with the `get_conn()` method to create a `psycopg2` cursor object. 

```python
from db.models import DBConfig

cfg = DBConfig(env_file=r'path-to-env-file.env')

with cfg.get_conn() as conn:
    cur = conn.cursor()

# Optional: To print config for logging or debugging purposes.
print(cfg.pretty(show_private=True))
```

