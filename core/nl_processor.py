"""
NL Processor — integrates with Google Gemini API to convert natural language
to SQL queries, classify intent, and generate human-readable explanations.
Uses the modern google.genai SDK.
"""

import json
import re
from google import genai
from config import Config


class NLProcessor:
    """Processes natural language requests into SQL using Google Gemini."""

    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "Gemini API key not configured. "
                "Set GEMINI_API_KEY in your .env file. "
                "Get a free key at: https://aistudio.google.com/apikey"
            )
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL

    def process(self, user_input, schema_text, conversation_history=""):
        """
        Process a natural language request and generate SQL.

        Args:
            user_input: The user's natural language request
            schema_text: Text representation of the database schema
            conversation_history: Previous conversation context

        Returns:
            dict with:
                - intent: SELECT, INSERT, UPDATE, DELETE, or CLARIFICATION
                - sql: Generated SQL query (empty for CLARIFICATION)
                - explanation: Human-readable explanation
                - affected_description: Description of what will be affected
                - confidence: Confidence score 0.0-1.0
                - error: Error message if processing failed
        """
        prompt = self._build_prompt(user_input, schema_text, conversation_history)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            result = self._parse_response(response.text)
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract info from raw text
            return self._fallback_parse(response.text)
        except Exception as e:
            return {
                "intent": "ERROR",
                "sql": "",
                "explanation": f"I had trouble understanding your request. Could you try rephrasing it? (Error: {str(e)})",
                "affected_description": "",
                "confidence": 0.0,
                "error": str(e),
            }

    def explain_error(self, error_message, sql, schema_text):
        """
        Generate a user-friendly explanation for a SQL error.

        Args:
            error_message: The technical error message
            sql: The SQL that caused the error
            schema_text: The database schema context

        Returns:
            str: User-friendly error explanation with suggestions
        """
        prompt = f"""You are a helpful database assistant. A SQL query failed with an error.
Explain the error in simple, non-technical language and suggest how the user can fix their request.

Database Schema:
{schema_text}

Failed SQL Query:
{sql}

Error Message:
{error_message}

Respond with a friendly, helpful explanation in 2-3 sentences. Do not include any SQL code.
Start with "I couldn't complete this request because..." and then explain what went wrong
and suggest what the user could try instead."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text.strip()
        except Exception:
            return (
                f"I couldn't complete this request due to a database error. "
                f"The issue might be related to incorrect table or column names. "
                f"Could you try rephrasing your request?"
            )

    def explain_operation(self, sql, query_type, affected_rows, schema_text):
        """
        Generate a human-readable explanation of what a SQL operation will do.

        Args:
            sql: The SQL query
            query_type: SELECT, INSERT, UPDATE, DELETE
            affected_rows: Number of rows affected
            schema_text: The database schema

        Returns:
            str: Human-readable explanation
        """
        prompt = f"""You are a helpful database assistant. Explain the following SQL operation
in simple, non-technical language. Be specific about what will happen.

SQL: {sql}
Operation Type: {query_type}
Records Affected: {affected_rows}

Respond with a single clear sentence starting with "I will..." that explains what this
operation does in plain English. Be specific about the table, conditions, and values involved.
Do not include any SQL code in your response."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text.strip()
        except Exception:
            return f"This {query_type} operation will affect {affected_rows} record(s)."

    def generate_initial_insights(self, db, schema_text):
        """
        Analyze the schema, generate exploratory queries, execute them, and summarize results.
        """
        # Step 1: Generate exploratory queries
        prompt1 = f"""You are an expert Data Analyst exploring a new database.
Review the following database schema and generate exactly 3 analytical SQL queries that would reveal interesting trends, warnings, or opportunities (e.g., top performers, anomalies, missing data, aggregates).

Database Schema:
{schema_text}

Rules:
1. Return exactly 3 SQL queries.
2. Format the response as a valid JSON array of strings.
3. DO NOT include markdown formatting like ```json.
4. Ensure the queries are safe READ-ONLY (SELECT) operations.
5. Add LIMIT 5 to each query to keep results small.
"""
        try:
            resp1 = self.client.models.generate_content(model=self.model, contents=prompt1)
            queries = self._parse_json_array(resp1.text)
            
            # Step 2: Execute queries
            results_context = ""
            for i, sql in enumerate(queries):
                if not isinstance(sql, str): continue
                res = db.execute_query(sql)
                print(f"DEBUG Initial Insight Query {i+1}: {sql}")
                print(f"DEBUG Result: {res.get('success')}")
                if res.get("success") and res.get("rows"):
                    results_context += f"Query {i+1}: {sql}\nResults: {json.dumps(res['rows'][:5])}\n\n"
                else:
                    print(f"DEBUG Error: {res.get('error')}")
                    
            if not results_context:
                print("DEBUG: All queries failed or returned empty results.")
                return self._fallback_insights()

            # Step 3: Summarize into insights
            prompt2 = f"""You are an expert Data Analyst. I ran some exploratory queries on my database and got the following results.

{results_context}

Based on these results, generate exactly 3 punchy, 1-sentence data-backed insights.
Format each insight to start with one of these exact labels: "Trend: ", "Warning: ", or "Opportunity: ".
Make them sound like a smart business analyst reporting a factual finding.

Rules:
1. Return exactly 3 insights.
2. Format the response as a valid JSON array of strings.
3. DO NOT include markdown formatting like ```json.
4. Example: ["Warning: 3 products account for 85% of all refund requests.", "Trend: Customer signups grew by 40% this quarter."]
"""
            resp2 = self.client.models.generate_content(model=self.model, contents=prompt2)
            insights = self._parse_json_array(resp2.text)
            
            if len(insights) >= 3:
                return insights[:3]
            return self._fallback_insights()

        except Exception as e:
            print("ERROR IN generate_initial_insights:", str(e))
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                return [
                    "Trend: Database successfully connected.",
                    "Warning: The AI API hit a rate limit (too many requests).",
                    "Opportunity: Please wait a minute before querying again to let the API cool down."
                ]
            import traceback
            traceback.print_exc()
            return self._fallback_insights()

    def _fallback_insights(self):
        return [
            "Trend: Database successfully connected and is ready for analysis.",
            "Opportunity: Ask me to find your top performing items.",
            "Warning: No deep insights could be automatically generated right now."
        ]

    def generate_post_execution_insights(self, user_request, sql, rows):
        """
        Generate an 'Explain Like I'm 5' TL;DR and 3 follow-up questions based on query results.
        """
        prompt = f"""You are an expert Data Analyst assisting a non-technical executive. 
The executive asked: "{user_request}"
We ran this SQL query: {sql}
The first few rows of the result are:
{json.dumps(rows[:10])}

Your task is to provide:
1. An "Explain Like I'm 5" executive summary (TL;DR) of what these results actually mean for the business. 
   - Write 1-2 clear, punchy sentences.
   - Do NOT use database jargon (no mentions of "rows", "columns", "SQL", or "tables").
   - Focus on the actual business insight or takeaway.
2. 3 smart, natural-language follow-up questions the executive might want to ask next to drill down into this data.

Return ONLY a valid JSON object matching this exact structure:
{{
    "tldr": "The executive summary here.",
    "follow_ups": [
        "Follow up question 1?",
        "Follow up question 2?",
        "Follow up question 3?"
    ]
}}
Do NOT include markdown formatting like ```json.
"""
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:]
            if text.startswith("```"): text = text[3:]
            if text.endswith("```"): text = text[:-3]
            
            result = json.loads(text.strip())
            return {
                "tldr": result.get("tldr", "Here is your requested data."),
                "follow_ups": result.get("follow_ups", [])[:3]
            }
        except Exception as e:
            return {
                "tldr": "Here is the data you requested.",
                "follow_ups": []
            }
        
    def _parse_json_array(self, text):
        text = text.strip()
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        text = text.strip()
        try:
            arr = json.loads(text)
            if isinstance(arr, list): return arr
        except:
            pass
        # regex fallback
        import re
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                arr = json.loads(match.group(0))
                if isinstance(arr, list): return arr
            except:
                pass
        return []

    # --- Private helpers ---

    def _build_prompt(self, user_input, schema_text, conversation_history):
        """Build the full prompt for the Gemini model."""
        return f"""You are an expert database assistant that converts natural language requests into SQL queries.
You must respond ONLY with a valid JSON object. Do not include any text before or after the JSON.

DATABASE SCHEMA:
{schema_text}

CONVERSATION HISTORY:
{conversation_history if conversation_history else "No previous conversation."}

RULES:
1. Analyze the user's request and determine the intent (SELECT, INSERT, UPDATE, DELETE, or CLARIFICATION).
2. Generate a valid SQL query for the connected database.
3. If the request is a follow-up to the previous conversation, use the context to understand what the user means.
4. If the request is ambiguous or you need more information, set intent to "CLARIFICATION".
5. For SELECT queries, always include meaningful column selections (avoid SELECT * when possible).
6. For INSERT, make sure to include all required (NOT NULL) columns.
7. For UPDATE and DELETE, always include a WHERE clause unless the user explicitly says "all".
8. Use the actual table and column names from the schema above.
9. For date/time operations, use appropriate SQL functions for the database type.
10. If the user asks about the database structure (tables, columns), generate a query to show that information.
11. DATA WARNING: Uploaded datasets often contain summary or "Total" rows. When querying for top items, rankings, or aggregates, explicitly filter out rows where the primary identifier or category column contains words like 'Total' or 'Summary' (e.g., WHERE name NOT LIKE '%Total%') unless the user explicitly asks for totals.

USER REQUEST: {user_input}

Respond with this exact JSON structure:
{{
    "intent": "SELECT or INSERT or UPDATE or DELETE or CLARIFICATION",
    "sql": "the SQL query here (empty string for CLARIFICATION)",
    "explanation": "A clear, friendly explanation of what this query does or what clarification is needed",
    "affected_description": "Description of which records will be affected (for modifications)",
    "confidence": 0.85
}}"""

    def _parse_response(self, response_text):
        """Parse the JSON response from Gemini."""
        # Try to extract JSON from the response
        text = response_text.strip()

        # Remove markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        # Try direct JSON parse
        try:
            result = json.loads(text)
            return self._validate_result(result)
        except json.JSONDecodeError:
            pass

        # Try to find JSON in the text
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return self._validate_result(result)
            except json.JSONDecodeError:
                pass

        # Try a more aggressive JSON extraction
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return self._validate_result(result)
            except json.JSONDecodeError:
                pass

        raise json.JSONDecodeError("Could not parse response as JSON", text, 0)

    def _fallback_parse(self, response_text):
        """Fallback parsing when JSON extraction fails."""
        text = response_text.strip()

        # Try to detect if it looks like a SQL query
        sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE"]
        for kw in sql_keywords:
            if text.upper().startswith(kw):
                return {
                    "intent": kw,
                    "sql": text.split("\n")[0].strip(),
                    "explanation": f"Generated a {kw} query based on your request.",
                    "affected_description": "",
                    "confidence": 0.5,
                    "error": None,
                }

        # Treat as clarification
        return {
            "intent": "CLARIFICATION",
            "sql": "",
            "explanation": text[:500] if text else "I need more information to help you. Could you please rephrase your request?",
            "affected_description": "",
            "confidence": 0.3,
            "error": None,
        }

    def _validate_result(self, result):
        """Validate and normalize the parsed result."""
        valid_intents = ["SELECT", "INSERT", "UPDATE", "DELETE", "CLARIFICATION"]

        intent = result.get("intent", "CLARIFICATION").upper()
        if intent not in valid_intents:
            intent = "CLARIFICATION"

        return {
            "intent": intent,
            "sql": result.get("sql", "").strip(),
            "explanation": result.get("explanation", "Processing your request."),
            "affected_description": result.get("affected_description", ""),
            "confidence": min(max(float(result.get("confidence", 0.5)), 0.0), 1.0),
            "error": None,
        }
