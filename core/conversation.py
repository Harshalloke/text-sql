"""
Conversation Manager — maintains conversation context for follow-up queries.
"""

from config import Config


class ConversationManager:
    """Manages conversation history for contextual follow-up queries."""

    def __init__(self, max_history=None):
        self.max_history = max_history or Config.MAX_CONVERSATION_HISTORY
        self.exchanges = []  # List of {"role": "user"|"assistant", "content": str}
        self.last_query_result = None  # Store last query result for refinement
        self.last_sql = None  # Store last SQL for context

    def add_user_message(self, message):
        """Add a user message to the conversation."""
        self.exchanges.append({"role": "user", "content": message})
        self._trim()

    def add_assistant_message(self, message, sql=None, result=None):
        """
        Add an assistant response to the conversation.

        Args:
            message: The human-readable response
            sql: The SQL query that was generated (if any)
            result: The query result summary (if any)
        """
        content = message
        if sql:
            content += f"\n[SQL: {sql}]"
        if result:
            content += f"\n[Result: {result}]"

        self.exchanges.append({"role": "assistant", "content": content})
        self.last_sql = sql
        self.last_query_result = result
        self._trim()

    def get_history_text(self):
        """
        Get conversation history formatted for the LLM prompt.

        Returns:
            Formatted string of previous exchanges
        """
        if not self.exchanges:
            return "No previous conversation."

        lines = []
        for ex in self.exchanges:
            role = "User" if ex["role"] == "user" else "Assistant"
            lines.append(f"{role}: {ex['content']}")

        return "\n".join(lines)

    def get_context_summary(self):
        """
        Get a brief summary of the current conversation context.

        Returns:
            dict with context information
        """
        return {
            "exchange_count": len(self.exchanges),
            "has_previous_query": self.last_sql is not None,
            "last_sql": self.last_sql,
        }

    def clear(self):
        """Clear all conversation history."""
        self.exchanges = []
        self.last_query_result = None
        self.last_sql = None

    def _trim(self):
        """Trim conversation history to max length."""
        max_messages = self.max_history * 2  # Each exchange has 2 messages
        if len(self.exchanges) > max_messages:
            self.exchanges = self.exchanges[-max_messages:]
