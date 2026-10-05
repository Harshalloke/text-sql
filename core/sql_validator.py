"""
SQL Validator — classifies, validates, and checks SQL queries for safety.
Prevents dangerous DDL operations and enforces row limits.
"""

import sqlparse
from config import Config


class SQLValidator:
    """Validates and classifies SQL queries for safety."""

    # Query type categories
    QUERY_TYPES = {
        "SELECT": "read",
        "WITH": "read",
        "SHOW": "read",
        "DESCRIBE": "read",
        "PRAGMA": "read",
        "INSERT": "write",
        "UPDATE": "write",
        "DELETE": "write",
        "DROP": "ddl",
        "CREATE": "ddl",
        "ALTER": "ddl",
        "TRUNCATE": "ddl",
        "RENAME": "ddl",
        "GRANT": "admin",
        "REVOKE": "admin",
        "EXEC": "admin",
        "EXECUTE": "admin",
    }

    def __init__(self):
        self.blocked_operations = [op.upper() for op in Config.BLOCKED_OPERATIONS]
        self.max_select_rows = Config.MAX_SELECT_ROWS
        self.warn_threshold = Config.WARN_AFFECTED_ROWS
        self.critical_threshold = Config.CRITICAL_AFFECTED_ROWS

    def validate(self, sql):
        """
        Validate a SQL query for safety.

        Args:
            sql: The SQL query string to validate

        Returns:
            dict with:
                - valid (bool): Whether the query is safe to execute
                - query_type (str): SELECT, INSERT, UPDATE, DELETE, etc.
                - category (str): read, write, ddl, admin
                - safety (str): SAFE, NEEDS_CONFIRMATION, BLOCKED
                - message (str): Human-readable explanation
                - cleaned_sql (str): Cleaned/formatted version of the query
        """
        if not sql or not sql.strip():
            return {
                "valid": False,
                "query_type": None,
                "category": None,
                "safety": "BLOCKED",
                "message": "Empty query provided.",
                "cleaned_sql": "",
            }

        # Clean and parse
        cleaned = self._clean_sql(sql)
        query_type = self._get_query_type(cleaned)

        if not query_type:
            return {
                "valid": False,
                "query_type": None,
                "category": None,
                "safety": "BLOCKED",
                "message": "Could not determine the type of this query.",
                "cleaned_sql": cleaned,
            }

        category = self.QUERY_TYPES.get(query_type, "unknown")

        # Check for blocked operations
        if query_type in self.blocked_operations:
            return {
                "valid": False,
                "query_type": query_type,
                "category": category,
                "safety": "BLOCKED",
                "message": f"'{query_type}' operations are not allowed for safety reasons. "
                           f"This system only supports SELECT, INSERT, UPDATE, and DELETE operations.",
                "cleaned_sql": cleaned,
            }

        # Check for multiple statements (SQL injection prevention)
        statements = [s for s in sqlparse.split(cleaned) if s.strip()]
        if len(statements) > 1:
            return {
                "valid": False,
                "query_type": query_type,
                "category": category,
                "safety": "BLOCKED",
                "message": "Multiple SQL statements are not allowed. Please make one request at a time.",
                "cleaned_sql": cleaned,
            }

        # Check for subquery-based attacks
        if self._contains_blocked_subquery(cleaned):
            return {
                "valid": False,
                "query_type": query_type,
                "category": category,
                "safety": "BLOCKED",
                "message": "This query contains operations that are not allowed for safety reasons.",
                "cleaned_sql": cleaned,
            }

        # SELECT queries and read operations are always safe
        if query_type in ["SELECT", "WITH", "SHOW", "DESCRIBE", "PRAGMA"]:
            # Add LIMIT if not present
            limited_sql = self._ensure_limit(cleaned)
            return {
                "valid": True,
                "query_type": query_type,
                "category": "read",
                "safety": "SAFE",
                "message": "This is a read-only query.",
                "cleaned_sql": limited_sql,
            }

        # Write operations need confirmation
        safety = "NEEDS_CONFIRMATION"
        if query_type == "DELETE":
            message = "This DELETE operation will permanently remove records. Please review carefully."
        elif query_type == "UPDATE":
            message = "This UPDATE operation will modify existing records."
        elif query_type == "INSERT":
            message = "This will add new records to the database."
            safety = "NEEDS_CONFIRMATION"  # Still confirm inserts
        else:
            message = f"This is a {query_type} operation."

        return {
            "valid": True,
            "query_type": query_type,
            "category": category,
            "safety": safety,
            "message": message,
            "cleaned_sql": cleaned,
        }

    def get_safety_level(self, affected_rows, query_type):
        """
        Determine the safety level based on affected row count.

        Args:
            affected_rows: Number of rows that will be affected
            query_type: Type of SQL operation

        Returns:
            dict with level (str) and warning_message (str)
        """
        if query_type in ["SELECT", "INSERT", "WITH", "SHOW", "DESCRIBE", "PRAGMA"]:
            return {"level": "info", "warning_message": ""}

        if affected_rows < 0:
            return {
                "level": "warning",
                "warning_message": "⚠️ Could not determine how many records will be affected. Proceed with caution.",
            }

        if affected_rows == 0:
            return {
                "level": "info",
                "warning_message": "No records match your criteria. Nothing will be changed.",
            }

        if affected_rows <= self.warn_threshold:
            return {
                "level": "info",
                "warning_message": f"This will affect {affected_rows} record(s).",
            }

        if affected_rows <= self.critical_threshold:
            return {
                "level": "warning",
                "warning_message": f"⚠️ This will affect {affected_rows} records. Please confirm.",
            }

        return {
            "level": "critical",
            "warning_message": f"🚨 CAUTION: This will affect {affected_rows} records! "
                               f"This is a large-scale operation. Please review carefully.",
        }

    # --- Private helpers ---

    def _clean_sql(self, sql):
        """Clean and normalize a SQL string."""
        # Remove markdown code fences if present
        sql = sql.strip()
        if sql.startswith("```"):
            lines = sql.split("\n")
            # Remove first and last line (code fences)
            lines = [l for l in lines if not l.strip().startswith("```")]
            sql = "\n".join(lines)

        # Remove trailing semicolons
        sql = sql.strip().rstrip(";").strip()

        return sql

    def _get_query_type(self, sql):
        """Extract the primary query type from a SQL statement."""
        parsed = sqlparse.parse(sql)
        if not parsed:
            return None

        first_token = None
        for token in parsed[0].tokens:
            if token.ttype is not None and not token.is_whitespace:
                first_token = token.value.upper()
                break

        return first_token if first_token in self.QUERY_TYPES else None

    def _contains_blocked_subquery(self, sql):
        """Check if a query contains blocked operations in subqueries."""
        sql_upper = sql.upper()
        for op in self.blocked_operations:
            # Check for blocked operations that aren't the main statement
            # e.g., SELECT * FROM (DROP TABLE users)
            parts = sql_upper.split()
            if len(parts) > 1 and op in parts[1:]:
                # Allow "SELECT ... FROM ... DELETE" as column/table names are unlikely
                # but block actual DDL in subqueries
                if op in ["DROP", "TRUNCATE", "ALTER", "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE"]:
                    # More strict check: look for the pattern "OP TABLE" or "OP DATABASE"
                    import re
                    pattern = rf'\b{op}\b\s+(TABLE|DATABASE|INDEX|VIEW|SCHEMA|PROCEDURE|FUNCTION)\b'
                    if re.search(pattern, sql_upper):
                        return True
        return False

    def _ensure_limit(self, sql):
        """Add LIMIT clause to SELECT queries if not already present."""
        sql_upper = sql.upper()
        if "LIMIT" not in sql_upper:
            return f"{sql} LIMIT {self.max_select_rows}"
        return sql
