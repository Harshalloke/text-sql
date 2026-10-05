"""
Natural Language Database Assistant — Flask Application
Main entry point with REST API routes for database interaction.
"""

import os
import logging
import traceback
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_session import Session
from config import Config
from core import DatabaseManager, NLProcessor, SQLValidator, ConversationManager, HistoryManager, detect_anomalies, analyze_drivers


# ---------------------------------------------------------------------------
# App Factory
# ---------------------------------------------------------------------------

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    Session(app)
    return app


app = create_app()

# ---------------------------------------------------------------------------
# Per-session state helpers
# ---------------------------------------------------------------------------

def _get_db_manager():
    """Get or create a DatabaseManager for the current session."""
    if "db_manager" not in session:
        session["db_manager_id"] = id(session)
    key = f"db_{session.get('db_manager_id', 'default')}"
    if key not in _state:
        _state[key] = DatabaseManager()
    return _state[key]


def _get_conversation():
    """Get or create a ConversationManager for the current session."""
    key = f"conv_{session.get('db_manager_id', 'default')}"
    if key not in _state:
        _state[key] = ConversationManager()
    return _state[key]


def _get_history():
    """Get or create a HistoryManager for the current session."""
    key = f"hist_{session.get('db_manager_id', 'default')}"
    if key not in _state:
        _state[key] = HistoryManager()
    return _state[key]


# In-memory state store (keyed by session)
_state = {}

# Pending operations awaiting confirmation
_pending = {}

# Shared components
_nl_processor = None
_sql_validator = SQLValidator()


def _get_nl_processor():
    """Lazy-init the NL processor (requires API key)."""
    global _nl_processor
    if _nl_processor is None:
        _nl_processor = NLProcessor()
    return _nl_processor


# ---------------------------------------------------------------------------
# Routes — Pages
# ---------------------------------------------------------------------------

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/app")
def app_workspace():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------

@app.route("/api/status", methods=["GET"])
def api_status():
    """Check connection status and API key availability."""
    db = _get_db_manager()
    return jsonify({
        "connected": db.is_connected,
        "database_name": db.db_name,
        "database_type": db.db_type,
        "api_key_configured": bool(Config.GEMINI_API_KEY),
    })


@app.route("/api/connect", methods=["POST"])
def api_connect():
    """Connect to a database."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No connection data provided."}), 400

    db_type = data.get("db_type", "").lower()
    if db_type not in ("sqlite", "mysql", "postgresql"):
        return jsonify({
            "success": False,
            "error": "Unsupported database type. Choose sqlite, mysql, or postgresql.",
        }), 400

    db = _get_db_manager()

    try:
        # Build connection kwargs
        conn_kwargs = {}
        if db_type == "sqlite":
            conn_kwargs["path"] = data.get("path", "")
        else:
            conn_kwargs["host"] = data.get("host", "localhost")
            conn_kwargs["port"] = int(data.get("port", 3306 if db_type == "mysql" else 5432))
            conn_kwargs["user"] = data.get("user", "")
            conn_kwargs["password"] = data.get("password", "")
            conn_kwargs["database"] = data.get("database", "")

        result = db.connect(db_type, **conn_kwargs)

        # Reset conversation and pending ops on new connection
        _get_conversation().clear()
        session_id = session.get("db_manager_id", "default")
        _pending.pop(session_id, None)

        return jsonify(result)

    except (ConnectionError, ValueError, FileNotFoundError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/disconnect", methods=["POST"])
def api_disconnect():
    """Disconnect from the current database."""
    db = _get_db_manager()
    db.disconnect()
    _get_conversation().clear()
    session_id = session.get("db_manager_id", "default")
    _pending.pop(session_id, None)
    return jsonify({"success": True, "message": "Disconnected from database."})


@app.route("/api/schema", methods=["GET"])
def api_schema():
    """Get the current database schema."""
    db = _get_db_manager()
    if not db.is_connected:
        return jsonify({"success": False, "error": "Not connected to any database."}), 400
    try:
        schema = db.get_schema()
        return jsonify({"success": True, "schema": schema})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/table_data", methods=["GET"])
def api_table_data():
    """Fetch raw data for a specific table."""
    table_name = request.args.get("table")
    if not table_name:
        return jsonify({"success": False, "error": "Table name is required."}), 400

    db = _get_db_manager()
    if not db.is_connected:
        return jsonify({"success": False, "error": "Database not connected."}), 400

    try:
        # Prevent SQL injection by validating table name against schema
        schema = db.get_schema()
        if table_name not in schema.get("tables", {}):
            return jsonify({"success": False, "error": "Table not found."}), 404

        result = db.execute_query(f'SELECT * FROM "{table_name}" LIMIT 100')
        return jsonify({
            "success": True,
            "data": result,
            "table": table_name
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """Upload a CSV/Excel file, convert to SQLite, and connect."""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected."}), 400
        
    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        return jsonify({"success": False, "error": "Only CSV and Excel (.xlsx) files are supported."}), 400
        
    try:
        upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Determine table name from filename
        table_name = os.path.splitext(filename)[0]
        table_name = "".join([c if c.isalnum() else "_" for c in table_name]).strip("_")
        if not table_name:
            table_name = "data_table"
            
        # Parse into pandas
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # Create SQLite DB
        sqlite_path = os.path.join(upload_dir, f"{table_name}.db")
        
        # We need sqlalchemy to write pandas df to sqlite easily
        from sqlalchemy import create_engine
        engine = create_engine(f"sqlite:///{sqlite_path}")
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        
        # Connect DatabaseManager
        db = _get_db_manager()
        result = db.connect("sqlite", path=sqlite_path)
        
        _get_conversation().clear()
        session_id = session.get("db_manager_id", "default")
        _pending.pop(session_id, None)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Upload failed: {str(e)}"}), 500


@app.route("/api/insights", methods=["GET"])
def api_insights():
    """Generate automatic business questions based on the connected schema."""
    db = _get_db_manager()
    if not db.is_connected:
        return jsonify({"success": False, "error": "Database not connected."}), 400
        
    try:
        schema_text = db.get_schema_text()
        insights = _get_nl_processor().generate_initial_insights(db, schema_text)
        return jsonify({"success": True, "insights": insights})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/anomaly", methods=["POST"])
def api_anomaly():
    """
    ML Anomaly & Outlier Detection endpoint.
    Runs IsolationForest + LocalOutlierFactor on a given table.
    100% local — no Gemini API used.
    """
    data = request.get_json()
    if not data or not data.get("table"):
        return jsonify({"success": False, "error": "Table name is required."}), 400

    table_name = data["table"]
    contamination = float(data.get("contamination", 0.1))  # Default 10% expected anomalies
    contamination = max(0.01, min(contamination, 0.5))  # Clamp between 1% and 50%

    db = _get_db_manager()
    if not db.is_connected:
        return jsonify({"success": False, "error": "Database not connected."}), 400

    try:
        # Fetch up to 5000 rows for ML analysis
        result = db.execute_query(f'SELECT * FROM "{table_name}" LIMIT 5000')
        if not result.get("success"):
            return jsonify({"success": False, "error": result.get("error", "Query failed.")}), 500

        columns = result["columns"]
        rows = result["rows"]

        if not rows:
            return jsonify({"success": False, "error": "The table is empty — nothing to analyze."}), 400

        analysis = detect_anomalies(columns, rows, table_name=table_name, contamination=contamination)
        return jsonify(analysis)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/drivers", methods=["POST"])
def api_drivers():
    """
    ML Feature Importance & Drivers Analysis endpoint.
    Uses RandomForest to determine what drives a target column.
    100% local — no Gemini API used.
    """
    data = request.get_json()
    if not data or not data.get("table") or not data.get("target"):
        return jsonify({"success": False, "error": "Table name and Target column are required."}), 400

    table_name = data["table"]
    target_column = data["target"]

    db = _get_db_manager()
    if not db.is_connected:
        return jsonify({"success": False, "error": "Database not connected."}), 400

    try:
        # Fetch up to 5000 rows for ML analysis
        result = db.execute_query(f'SELECT * FROM "{table_name}" LIMIT 5000')
        if not result.get("success"):
            return jsonify({"success": False, "error": result.get("error", "Query failed.")}), 500

        columns = result["columns"]
        rows = result["rows"]

        if not rows:
            return jsonify({"success": False, "error": "The table is empty — nothing to analyze."}), 400

        analysis = analyze_drivers(columns, rows, target_column=target_column)
        return jsonify(analysis)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
@app.route("/api/query", methods=["POST"])
def api_query():
    """
    Process a natural language query.
    This is the main endpoint — takes user text and returns results or a confirmation prompt.
    """
    data = request.get_json()
    if not data or not data.get("query", "").strip():
        return jsonify({"success": False, "error": "Please enter a request."}), 400

    user_input = data["query"].strip()
    db = _get_db_manager()
    conversation = _get_conversation()
    history = _get_history()

    if not db.is_connected:
        return jsonify({
            "success": False,
            "error": "Please connect to a database first.",
        }), 400

    try:
        nl = _get_nl_processor()
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

    # Add user message to conversation
    conversation.add_user_message(user_input)

    try:
        # Step 1: Process natural language → SQL
        schema_text = db.get_schema_text()
        nl_result = nl.process(
            user_input=user_input,
            schema_text=schema_text,
            conversation_history=conversation.get_history_text(),
        )

        intent = nl_result["intent"]
        sql = nl_result["sql"]
        explanation = nl_result["explanation"]

        # Step 2: Handle CLARIFICATION
        if intent == "CLARIFICATION" or intent == "ERROR":
            conversation.add_assistant_message(explanation)
            return jsonify({
                "success": True,
                "type": "clarification",
                "message": explanation,
            })

        # Step 3: Validate SQL
        validation = _sql_validator.validate(sql)
        if not validation["valid"]:
            conversation.add_assistant_message(validation["message"])
            history.record(
                user_request=user_input, sql=sql,
                operation_type=intent, explanation=validation["message"],
                success=False, error=validation["message"],
            )
            return jsonify({
                "success": True,
                "type": "error",
                "message": validation["message"],
            })

        sql = validation["cleaned_sql"]
        query_type = validation["query_type"]

        # Step 4: Handle based on query type
        if query_type == "SELECT":
            return _handle_select(db, conversation, history, user_input, sql, explanation)
        else:
            return _handle_modification(
                db, nl, conversation, history,
                user_input, sql, query_type, explanation, schema_text,
            )

    except Exception as e:
        error_msg = f"Something went wrong while processing your request. Please try again. ({str(e)})"
        conversation.add_assistant_message(error_msg)
        return jsonify({"success": False, "error": error_msg}), 500


@app.route("/api/confirm", methods=["POST"])
def api_confirm():
    """Confirm and execute a pending modification operation."""
    session_id = session.get("db_manager_id", "default")
    pending = _pending.get(session_id)

    if not pending:
        return jsonify({
            "success": False,
            "error": "No pending operation to confirm.",
        }), 400

    db = _get_db_manager()
    conversation = _get_conversation()
    history = _get_history()

    sql = pending["sql"]
    query_type = pending["query_type"]
    user_request = pending["user_request"]
    explanation = pending["explanation"]

    # Execute the operation
    result = db.execute_query(sql)
    _pending.pop(session_id, None)

    if result["success"]:
        affected = result.get("affected_rows", 0)
        success_msg = f"✅ Done! {explanation} ({affected} record(s) affected.)"
        conversation.add_assistant_message(success_msg, sql=sql, result=f"{affected} rows affected")
        history.record(
            user_request=user_request, sql=sql,
            operation_type=query_type, explanation=explanation,
            affected_rows=affected, success=True,
        )
        return jsonify({
            "success": True,
            "type": "modification_result",
            "message": success_msg,
            "affected_rows": affected,
            "sql": sql,
        })
    else:
        error_explanation = _try_explain_error(result["error"], sql, db)
        conversation.add_assistant_message(error_explanation)
        history.record(
            user_request=user_request, sql=sql,
            operation_type=query_type, explanation=explanation,
            success=False, error=result["error"],
        )
        return jsonify({
            "success": True,
            "type": "error",
            "message": error_explanation,
        })


@app.route("/api/cancel", methods=["POST"])
def api_cancel():
    """Cancel a pending modification operation."""
    session_id = session.get("db_manager_id", "default")
    pending = _pending.pop(session_id, None)

    conversation = _get_conversation()
    if pending:
        conversation.add_assistant_message("Operation cancelled. No changes were made.")
        return jsonify({
            "success": True,
            "message": "Operation cancelled. No changes were made.",
        })
    else:
        return jsonify({
            "success": True,
            "message": "No pending operation to cancel.",
        })


@app.route("/api/history", methods=["GET"])
def api_history():
    """Get operation history."""
    history = _get_history()
    return jsonify({
        "success": True,
        "history": history.get_recent(50),
        "stats": history.get_stats(),
    })


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _handle_select(db, conversation, history, user_input, sql, explanation):
    """Handle a SELECT query — execute immediately and return results."""
    result = db.execute_query(sql)

    if result["success"]:
        row_count = result.get("row_count", 0)
        
        # Generate ELI5 TL;DR and follow-ups
        nl = _get_nl_processor()
        post_insights = nl.generate_post_execution_insights(user_input, sql, result.get("rows", []))
        
        conversation.add_assistant_message(
            explanation, sql=sql, result=f"{row_count} rows returned"
        )
        history.record(
            user_request=user_input, sql=sql,
            operation_type="SELECT", explanation=explanation,
            affected_rows=row_count, success=True,
        )
        return jsonify({
            "success": True,
            "type": "query_result",
            "message": explanation,
            "tldr": post_insights.get("tldr", ""),
            "follow_ups": post_insights.get("follow_ups", []),
            "data": {
                "columns": result["columns"],
                "rows": result["rows"],
                "row_count": row_count,
            },
            "sql": sql,
        })
    else:
        error_explanation = _try_explain_error(result["error"], sql, db)
        conversation.add_assistant_message(error_explanation)
        history.record(
            user_request=user_input, sql=sql,
            operation_type="SELECT", explanation=explanation,
            success=False, error=result["error"],
        )
        return jsonify({
            "success": True,
            "type": "error",
            "message": error_explanation,
        })


def _handle_modification(db, nl, conversation, history,
                         user_input, sql, query_type, explanation, schema_text):
    """Handle INSERT/UPDATE/DELETE — preview first, then await confirmation."""
    # Count affected rows
    affected_rows = db.count_affected_rows(sql)

    # Get safety level
    safety = _sql_validator.get_safety_level(affected_rows, query_type)

    # Generate detailed explanation
    try:
        detailed_explanation = nl.explain_operation(sql, query_type, affected_rows, schema_text)
    except Exception:
        detailed_explanation = explanation

    # Store pending operation
    session_id = session.get("db_manager_id", "default")
    _pending[session_id] = {
        "sql": sql,
        "query_type": query_type,
        "user_request": user_input,
        "explanation": detailed_explanation,
        "affected_rows": affected_rows,
    }

    conversation.add_assistant_message(
        f"[Pending] {detailed_explanation}", sql=sql
    )

    return jsonify({
        "success": True,
        "type": "confirmation_required",
        "message": detailed_explanation,
        "preview": {
            "operation": query_type,
            "affected_rows": affected_rows,
            "sql": sql,
            "safety_level": safety["level"],
            "warning": safety["warning_message"],
        },
    })


def _try_explain_error(error_msg, sql, db):
    """Try to explain a SQL error in user-friendly terms."""
    try:
        nl = _get_nl_processor()
        return nl.explain_error(error_msg, sql, db.get_schema_text())
    except Exception:
        return (
            f"I couldn't complete this request due to a database error. "
            f"Please try rephrasing your request or check that the data you're "
            f"referring to exists in the database."
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Ensure session directory exists
    os.makedirs(Config.SESSION_FILE_DIR, exist_ok=True)

    print("\n" + "=" * 60)
    print("  Natural Language Database Assistant")
    print("=" * 60)
    print(f"  API Key: {'[OK] Configured' if Config.GEMINI_API_KEY else '[X] Not set'}")
    print(f"  Server:  http://127.0.0.1:5000")
    print("=" * 60 + "\n")

    if not Config.GEMINI_API_KEY:
        print("[!] Warning: GEMINI_API_KEY is not set!")
        print("    Copy .env.example to .env and add your API key.")
        print("    Get a free key at: https://aistudio.google.com/apikey\n")

    app.run(debug=True, host="127.0.0.1", port=5000)
