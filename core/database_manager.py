"""
Database Manager — handles connections, schema inspection, and query execution.
Supports SQLite, MySQL, and PostgreSQL through SQLAlchemy.
"""

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.pool import StaticPool
import os


class DatabaseManager:
    """Manages database connections, schema introspection, and query execution."""

    def __init__(self):
        self.engine = None
        self.db_type = None
        self.db_name = None
        self._schema_cache = None

    def connect(self, db_type, **kwargs):
        """
        Connect to a database.

        Args:
            db_type: 'sqlite', 'mysql', or 'postgresql'
            **kwargs: Connection parameters (path for SQLite, host/port/user/password/database for others)

        Returns:
            dict with status and schema info

        Raises:
            ValueError: If db_type is unsupported
            ConnectionError: If connection fails
        """
        self.disconnect()

        try:
            if db_type == "sqlite":
                uri = self._build_sqlite_uri(kwargs.get("path", ""))
            elif db_type == "mysql":
                uri = self._build_mysql_uri(**kwargs)
            elif db_type == "postgresql":
                uri = self._build_postgresql_uri(**kwargs)
            else:
                raise ValueError(f"Unsupported database type: {db_type}")

            # Create engine with appropriate settings
            engine_kwargs = {}
            if db_type == "sqlite":
                engine_kwargs["connect_args"] = {"check_same_thread": False}
                engine_kwargs["poolclass"] = StaticPool
            else:
                engine_kwargs["pool_size"] = 5
                engine_kwargs["pool_timeout"] = 30
                engine_kwargs["pool_recycle"] = 1800

            self.engine = create_engine(uri, **engine_kwargs)

            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            self.db_type = db_type
            self.db_name = self._get_db_name(db_type, **kwargs)
            self._schema_cache = None  # Reset cache

            return {
                "success": True,
                "message": f"Connected to {self.db_name} ({db_type})",
                "schema": self.get_schema(),
            }

        except OperationalError as e:
            error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
            raise ConnectionError(f"Could not connect to the database: {error_msg}")
        except Exception as e:
            raise ConnectionError(f"Connection failed: {str(e)}")

    def disconnect(self):
        """Disconnect from the current database."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.db_type = None
            self.db_name = None
            self._schema_cache = None

    @property
    def is_connected(self):
        """Check if currently connected to a database."""
        return self.engine is not None

    def get_schema(self):
        """
        Inspect and return the full database schema.

        Returns:
            dict with tables, their columns, primary keys, foreign keys, and sample data
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to any database.")

        if self._schema_cache:
            return self._schema_cache

        inspector = inspect(self.engine)
        schema = {"tables": {}, "database_name": self.db_name, "database_type": self.db_type}

        for table_name in inspector.get_table_names():
            table_info = {
                "columns": [],
                "primary_keys": [],
                "foreign_keys": [],
                "row_count": 0,
                "sample_data": [],
            }

            # Columns
            for col in inspector.get_columns(table_name):
                table_info["columns"].append({
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col.get("nullable", True),
                    "default": str(col.get("default", "")) if col.get("default") else None,
                })

            # Primary keys
            pk = inspector.get_pk_constraint(table_name)
            if pk:
                table_info["primary_keys"] = pk.get("constrained_columns", [])

            # Foreign keys
            for fk in inspector.get_foreign_keys(table_name):
                table_info["foreign_keys"].append({
                    "columns": fk.get("constrained_columns", []),
                    "referred_table": fk.get("referred_table", ""),
                    "referred_columns": fk.get("referred_columns", []),
                })

            # Row count and sample data
            try:
                with self.engine.connect() as conn:
                    count_result = conn.execute(
                        text(f'SELECT COUNT(*) FROM "{table_name}"')
                    )
                    table_info["row_count"] = count_result.scalar() or 0

                    sample_result = conn.execute(
                        text(f'SELECT * FROM "{table_name}" LIMIT 3')
                    )
                    columns = list(sample_result.keys())
                    for row in sample_result:
                        table_info["sample_data"].append(
                            {col: self._serialize_value(val) for col, val in zip(columns, row)}
                        )
            except SQLAlchemyError:
                pass  # Skip if table can't be queried

            schema["tables"][table_name] = table_info

        self._schema_cache = schema
        return schema

    def get_schema_text(self):
        """
        Get a text representation of the schema for LLM context.

        Returns:
            Formatted string describing all tables, columns, types, and relationships
        """
        schema = self.get_schema()
        lines = [f"Database: {schema['database_name']} ({schema['database_type']})\n"]

        for table_name, table_info in schema["tables"].items():
            lines.append(f"Table: {table_name} ({table_info['row_count']} rows)")

            # Columns
            for col in table_info["columns"]:
                nullable = "NULL" if col["nullable"] else "NOT NULL"
                pk_marker = " [PK]" if col["name"] in table_info["primary_keys"] else ""
                lines.append(f"  - {col['name']}: {col['type']} {nullable}{pk_marker}")

            # Foreign keys
            for fk in table_info["foreign_keys"]:
                lines.append(
                    f"  FK: {', '.join(fk['columns'])} -> "
                    f"{fk['referred_table']}({', '.join(fk['referred_columns'])})"
                )

            # Sample data
            if table_info["sample_data"]:
                lines.append(f"  Sample rows:")
                for row in table_info["sample_data"][:2]:
                    row_str = ", ".join(f"{k}={v}" for k, v in row.items())
                    lines.append(f"    {row_str}")

            lines.append("")

        return "\n".join(lines)

    def execute_query(self, sql, params=None):
        """
        Execute a SQL query and return results.

        Args:
            sql: SQL query string
            params: Optional query parameters

        Returns:
            dict with columns, rows, row_count, and affected_rows
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to any database.")

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})

                if result.returns_rows:
                    columns = list(result.keys())
                    rows = []
                    for row in result:
                        rows.append(
                            {col: self._serialize_value(val) for col, val in zip(columns, row)}
                        )
                    return {
                        "success": True,
                        "type": "select",
                        "columns": columns,
                        "rows": rows,
                        "row_count": len(rows),
                    }
                else:
                    conn.commit()
                    affected = result.rowcount
                    self._schema_cache = None  # Invalidate cache after modifications
                    return {
                        "success": True,
                        "type": "modify",
                        "affected_rows": affected if affected >= 0 else 0,
                    }

        except SQLAlchemyError as e:
            error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
            return {
                "success": False,
                "error": error_msg,
            }

    def count_affected_rows(self, sql):
        """
        For UPDATE/DELETE queries, count how many rows would be affected
        by running a SELECT COUNT(*) with the same WHERE clause.

        Args:
            sql: The UPDATE or DELETE SQL statement

        Returns:
            int: Number of rows that would be affected, or -1 if unable to determine
        """
        if not self.is_connected:
            return -1

        try:
            sql_upper = sql.strip().upper()

            if sql_upper.startswith("UPDATE"):
                # Extract table name and WHERE clause
                parts = sql.split("WHERE", 1)
                if len(parts) < 2:
                    # No WHERE clause — affects all rows
                    table = sql.split("SET")[0].replace("UPDATE", "").strip()
                    count_sql = f'SELECT COUNT(*) FROM {table}'
                else:
                    table = sql.split("SET")[0].replace("UPDATE", "").strip()
                    where = parts[1].strip()
                    count_sql = f'SELECT COUNT(*) FROM {table} WHERE {where}'

            elif sql_upper.startswith("DELETE"):
                parts = sql.split("WHERE", 1)
                if len(parts) < 2:
                    table = sql_upper.replace("DELETE FROM", "").strip().split()[0]
                    count_sql = f'SELECT COUNT(*) FROM {table}'
                else:
                    table = sql.split("WHERE")[0].replace("DELETE", "").replace("FROM", "").strip()
                    where = parts[1].strip()
                    count_sql = f'SELECT COUNT(*) FROM {table} WHERE {where}'

            elif sql_upper.startswith("INSERT"):
                return 1  # INSERT always affects 1 row (for single insert)

            else:
                return -1

            with self.engine.connect() as conn:
                result = conn.execute(text(count_sql))
                return result.scalar() or 0

        except Exception:
            return -1

    # --- Private helpers ---

    def _build_sqlite_uri(self, path):
        """Build SQLite connection URI."""
        if not path:
            raise ValueError("SQLite database file path is required.")
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Database file not found: {abs_path}")
        return f"sqlite:///{abs_path}"

    def _build_mysql_uri(self, **kwargs):
        """Build MySQL connection URI."""
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 3306)
        user = kwargs.get("user", "root")
        password = kwargs.get("password", "")
        database = kwargs.get("database", "")
        if not database:
            raise ValueError("Database name is required for MySQL.")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    def _build_postgresql_uri(self, **kwargs):
        """Build PostgreSQL connection URI."""
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 5432)
        user = kwargs.get("user", "postgres")
        password = kwargs.get("password", "")
        database = kwargs.get("database", "")
        if not database:
            raise ValueError("Database name is required for PostgreSQL.")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    def _get_db_name(self, db_type, **kwargs):
        """Extract a human-readable database name."""
        if db_type == "sqlite":
            return os.path.basename(kwargs.get("path", "database"))
        return kwargs.get("database", "database")

    def _serialize_value(self, value):
        """Convert a database value to a JSON-serializable format."""
        if value is None:
            return None
        if isinstance(value, (int, float, str, bool)):
            return value
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return str(value)
