"""
History Manager — tracks all database operations performed in a session.
"""

from datetime import datetime


class HistoryManager:
    """Tracks operation history for transparency and audit trail."""

    def __init__(self):
        self.operations = []

    def record(self, user_request, sql, operation_type, explanation,
               affected_rows=0, success=True, error=None):
        """
        Record a database operation.

        Args:
            user_request: The original natural language request
            sql: The SQL query that was executed
            operation_type: SELECT, INSERT, UPDATE, DELETE
            explanation: Human-readable explanation of the operation
            affected_rows: Number of rows affected
            success: Whether the operation succeeded
            error: Error message if failed
        """
        entry = {
            "id": len(self.operations) + 1,
            "timestamp": datetime.now().isoformat(),
            "user_request": user_request,
            "sql": sql,
            "operation_type": operation_type.upper() if operation_type else "UNKNOWN",
            "explanation": explanation,
            "affected_rows": affected_rows,
            "success": success,
            "error": error,
        }
        self.operations.append(entry)
        return entry

    def get_all(self):
        """Get all operation history entries, newest first."""
        return list(reversed(self.operations))

    def get_recent(self, count=20):
        """Get the most recent N operations."""
        return list(reversed(self.operations[-count:]))

    def get_by_type(self, operation_type):
        """Get operations filtered by type."""
        return [
            op for op in reversed(self.operations)
            if op["operation_type"] == operation_type.upper()
        ]

    def get_stats(self):
        """Get summary statistics of operations."""
        stats = {
            "total": len(self.operations),
            "successful": sum(1 for op in self.operations if op["success"]),
            "failed": sum(1 for op in self.operations if not op["success"]),
            "by_type": {},
        }
        for op in self.operations:
            t = op["operation_type"]
            stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
        return stats

    def clear(self):
        """Clear all history."""
        self.operations = []
