# -*- coding: utf-8 -*-
"""
Chapter 6: Experimental Setup Page Definitions (Pages 22 to 42)
"""
import os
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def add_ch6_experimental_setup(story, styles):
    code_style = styles['CodeBlock']
    # PAGE 22 (Internal 18): Chapter 6 Separator
    story.append(Spacer(1, 250))
    story.append(Paragraph("6. EXPERIMENTAL<br/>SETUP", styles['ChapSep']))
    story.append(PageBreak())
    
    # PAGE 23 (Internal 19): Section 6.1 Requirements Analysis (6.1.1, 6.1.2, 6.1.3 Tech 1)
    story.append(Paragraph("Page No. 19", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("6.1 Requirements Analysis:", styles['SecHead']))
    story.append(Paragraph("6.1.1 Software Requirements:", styles['SubSecHead']))
    story.append(Paragraph("<b>1. Operating System:</b> Windows 10/11 (64-bit), Ubuntu Linux 20.04 LTS or newer, or macOS Monterey 12.0 or newer.", styles['Body']))
    story.append(Paragraph("<b>2. Web Browser:</b> Modern Chromium-based or Gecko-based web browser (Google Chrome 110+, Mozilla Firefox 115+, Microsoft Edge 110+, or Safari 16+) supporting HTML5 Canvas, ECMAScript 6+ (ES6), and asynchronous Fetch APIs.", styles['Body']))
    story.append(Paragraph("<b>3. Python Runtime:</b> Python version 3.10, 3.11, or 3.12 (64-bit) with <code>pip</code> package manager and standard C-runtime libraries.", styles['Body']))
    story.append(Paragraph("<b>4. Virtual Environment:</b> Python virtual environment (<code>venv</code>) for isolated dependency sandboxing.", styles['Body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("6.1.2 Hardware Requirements:", styles['SubSecHead']))
    story.append(Paragraph("<b>1. Computing Device:</b> Personal Computer, Engineering Laptop, or Cloud Virtual Machine.", styles['Body']))
    story.append(Paragraph("<b>2. Central Processing Unit (CPU):</b> Intel Core i3 / i5 / i7 or AMD Ryzen 3 / 5 / 7 processor operating at 2.0 GHz or higher (multi-core architecture recommended for parallel tree ensembles).", styles['Body']))
    story.append(Paragraph("<b>3. System Memory (RAM):</b> 8.0 GB minimum (16.0 GB recommended for large multidimensional database table analysis and Scikit-Learn tree construction).", styles['Body']))
    story.append(Paragraph("<b>4. Storage Space:</b> 6.0 GB available storage space (Solid State Drive [SSD] recommended for low-latency SQLite reads).", styles['Body']))
    story.append(Paragraph("<b>5. Display Resolution:</b> 1280 x 720 minimum (1920 x 1080 full HD recommended for panoramic dashboard visualization).", styles['Body']))
    story.append(Paragraph("<b>6. Network Connectivity:</b> Active broadband Internet connection required exclusively for Google Gemini API model inference; all database queries and Scikit-Learn machine learning computations execute 100% locally offline.", styles['Body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("6.1.3 Technology Stack &amp; Frameworks:", styles['SubSecHead']))
    story.append(Paragraph("<b>1. Python Runtime Environment (Python 3.12):</b> Serves as the foundational programming language for the QueryMind application backend. Python provides unified access to high-performance database drivers, asynchronous web networking, string manipulation, and comprehensive scientific computing ecosystems.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 24 (Internal 20): Section 6.1.3 Technology Stack (Tech 2, 3, 4)
    story.append(Paragraph("Page No. 20", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>2. Flask Web Micro-Framework (Flask 3.0+, Flask-CORS, Flask-Session):</b><br/>"
                           "Flask provides the lightweight WSGI web application server powering QueryMind's RESTful API architecture. It manages client HTTP requests, handles JSON serialization, provisions secure server-side session persistence via <code>Flask-Session</code>, and enforces Cross-Origin Resource Sharing (CORS) security policies. Flask's decoupled routing model enables clean separation between client-facing workspace routes and backend intelligence endpoints.", styles['Body']))
    story.append(Paragraph("<b>3. SQLAlchemy Unified Database Abstraction Engine (SQLAlchemy 2.0+):</b><br/>"
                           "SQLAlchemy serves as the universal database abstraction layer across heterogeneous relational database management systems. It provides automated connection pooling, dialect-specific query compilation, transaction lifecycle management, and dynamic metadata schema introspection (reflecting table names, column specifications, primary keys, and foreign key relations across SQLite, MySQL, and PostgreSQL).", styles['Body']))
    story.append(Paragraph("<b>4. Google Gemini 2.0 Flash Generative AI Engine (google-genai SDK):</b><br/>"
                           "Google Gemini 2.0 Flash provides state-of-the-art semantic reasoning, natural language parsing, and structured code synthesis. Accessible via the official <code>google-genai</code> SDK, the model processes natural language user inquiries in conjunction with live database schema context, translating informal questions into dialect-compliant, executable SQL queries with minimal latency.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 25 (Internal 21): Section 6.1.3 Technology Stack (Tech 5, 6, 7, 8)
    story.append(Paragraph("Page No. 21", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>5. sqlparse SQL AST Parsing &amp; Security Validation Library (sqlparse 0.5+):</b><br/>"
                           "<code>sqlparse</code> is an advanced non-validating SQL parser for Python that decomposes raw query strings into Abstract Syntax Tree (AST) token hierarchies. QueryMind leverages <code>sqlparse</code> to inspect token streams, identify root statement types (DML vs. DDL), enforce strict statement boundaries, and guarantee that multi-statement SQL injection vectors and destructive commands are deterministically blocked.", styles['Body']))
    story.append(Paragraph("<b>6. Scikit-Learn Local Machine Learning Suite (Scikit-Learn 1.4+):</b><br/>"
                           "Scikit-Learn provides the local, privacy-preserving machine learning algorithms powering QueryMind's diagnostic suite. Key submodules include <code>IsolationForest</code> and <code>LocalOutlierFactor</code> for context-aware unsupervised anomaly detection, <code>RandomForestRegressor</code> and <code>RandomForestClassifier</code> for feature importance driver analysis, and <code>ColumnTransformer</code> and <code>StandardScaler</code> for preprocessing pipelines.", styles['Body']))
    story.append(Paragraph("<b>7. Pandas &amp; NumPy Scientific Data Processing Libraries (Pandas 2.2+, NumPy 1.26+):</b><br/>"
                           "Pandas and NumPy provide high-performance in-memory tabular data manipulation, numerical array transformations, date-time parsing, and automated missing-value imputation. They bridge database query result rows into structured DataFrames ready for statistical evaluation and ML training.", styles['Body']))
    story.append(Paragraph("<b>8. OpenPyXL &amp; Ingestion Engines (OpenPyXL 3.1+):</b><br/>"
                           "Enables seamless ingestion of modern Microsoft Excel workbooks (.xlsx) and delimiter-separated CSV files, dynamically parsing spreadsheet worksheets into relational database tables.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 26 (Internal 22): Section 6.1.4 Development Tools & Softwares (Tools 1, 2)
    story.append(Paragraph("Page No. 22", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("6.1.4 Development Tools &amp; Softwares:", styles['SubSecHead']))
    story.append(Paragraph("<b>1. Visual Studio Code &amp; Thonny Integrated Development Environments:</b><br/>"
                           "Visual Studio Code (VS Code) served as the primary development environment for architecting the full-stack system, featuring Python language server extensions, static type checking, automated syntax linting, and integrated terminal orchestration. Thonny IDE provided a lightweight alternative for rapid script verification, interactive step-through debugging, and localized variable state inspection during the development of local ML preprocessing algorithms.", styles['Body']))
    story.append(Paragraph("<b>2. Git &amp; GitHub Distributed Version Control:</b><br/>"
                           "Git provided distributed source code versioning, commit history tracking, and collaborative branching workflows throughout all Agile sprints. The repository hosted on GitHub facilitated safe feature experimentation, continuous milestone documentation, and reliable rollback capabilities.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 27 (Internal 23): Section 6.1.4 Development Tools & Softwares (Tools 3, 4, 5)
    story.append(Paragraph("Page No. 23", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>3. DB Browser for SQLite &amp; Database Management GUIs:</b><br/>"
                           "DB Browser for SQLite provided open-source visual database management for creating, inspecting, querying, and verifying relational schema structures, index designs, and sample e-commerce records during development and benchmark validation. Equivalent tools (MySQL Workbench and pgAdmin 4) were utilized to verify MySQL and PostgreSQL multi-dialect compatibility.", styles['Body']))
    story.append(Paragraph("<b>4. Postman API Platform:</b><br/>"
                           "Postman was employed to formulate automated test collections, validate Flask REST API endpoint contracts (<code>/api/connect</code>, <code>/api/query</code>, <code>/api/confirm</code>, <code>/api/anomalies</code>, <code>/api/drivers</code>), inspect HTTP payload schemas, and benchmark server response latencies under varied network conditions.", styles['Body']))
    story.append(Paragraph("<b>5. Chart.js &amp; Web Presentation Engines:</b><br/>"
                           "Chart.js (version 4.4+) provided responsive, HTML5 Canvas-based chart rendering in the client browser, dynamically generating bar charts, trend lines, and distribution pies based on synthesized SQL query results.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 28 (Internal 24): Section 6.2 System Architecture Diagram
    story.append(Paragraph("Page No. 24", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.2 System Architecture Diagram:", styles['SecHead']))
    story.append(Paragraph(
        "The multi-tier system architecture of QueryMind is depicted in Figure 6.1 below, illustrating the modular decoupling between the Presentation Layer, Application Routing Layer, Core Intelligence Layer, and Multi-Engine Persistence Layer.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))
    if os.path.exists("report_assets/arch_diagram.png"):
        story.append(Image("report_assets/arch_diagram.png", width=460, height=330))
    story.append(Paragraph("Fig 6.1: QueryMind Multi-Tier System Architecture", styles['FigCap']))
    story.append(Paragraph(
        "As illustrated in Figure 6.1, the Presentation Layer interacts asynchronously with the Flask Application Server via JSON REST endpoints. The Application Server delegates semantic queries to the Core Intelligence Layer, where the Google Gemini 2.0 Flash engine translates natural language into candidate SQL queries. All candidate queries must pass through the AST Security Gate before execution by SQLAlchemy against the target relational database. Local Machine Learning diagnostic requests (Anomaly Detection and Driver Analysis) are routed directly to the on-premise Scikit-Learn engine, guaranteeing complete data isolation and zero egress.",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGE 29 (Internal 25): Section 6.3 Block Diagram of System Flow
    story.append(Paragraph("Page No. 25", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.3 Block Diagram of System Flow:", styles['SecHead']))
    story.append(Paragraph(
        "A block diagram of system flow provides a high-level visual representation of the end-to-end execution pipeline, tracing data transformations and control decisions from user input to final visualization.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))
    if os.path.exists("report_assets/flow_diagram.png"):
        story.append(Image("report_assets/flow_diagram.png", width=460, height=330))
    story.append(Paragraph("Fig 6.2: QueryMind End-to-End System Flowchart", styles['FigCap']))
    story.append(Paragraph(
        "Figure 6.2 illustrates the sequential decision tree governing query and ML processing. When a user issues a natural language query, the system retrieves the active schema context and invokes Gemini 2.0 Flash. The synthesized SQL is parsed into an AST: DDL commands are immediately rejected with an error alert; DML operations trigger a transactional dry-run to preview affected row counts, prompting a user confirmation modal; and SELECT queries execute directly via SQLAlchemy. Results are formatted as JSON and visualized dynamically via tables or Chart.js graphs. Local ML diagnostic requests branch directly into Scikit-Learn pipelines, outputting explainable outlier scores and driver rankings.",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGES 30 to 42: Section 6.4 Input Code (Modular Listings)
    
    # Page 30 (Internal 26): 6.4 Input Code - app.py Initialization
    story.append(Paragraph("Page No. 26", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4 Input Code:", styles['SecHead']))
    story.append(Paragraph("6.4.1 Application Controller (app.py):", styles['SubSecHead']))
    story.append(Paragraph("Initialization, session configuration, and state storage helper routines:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
import os, logging, traceback
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_session import Session
from config import Config
from core import (DatabaseManager, NLProcessor, SQLValidator,
                  ConversationManager, HistoryManager,
                  detect_anomalies, analyze_drivers)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    Session(app)
    return app

app = create_app()
_state = {}     # Session-isolated state store
_pending = {}   # Pending DML operations awaiting confirmation
_sql_validator = SQLValidator()
_nl_processor = None

def _get_db_manager():
    if "db_manager_id" not in session:
        session["db_manager_id"] = id(session)
    key = f"db_{session.get('db_manager_id', 'default')}"
    if key not in _state:
        _state[key] = DatabaseManager()
    return _state[key]
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 31 (Internal 27): app.py - Connect and Natural Language Query Endpoints
    story.append(Paragraph("Page No. 27", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("app.py (continued):", styles['SubSecHead']))
    story.append(Paragraph("REST API endpoints for database connection and natural language querying:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
@app.route("/api/connect", methods=["POST"])
def api_connect():
    data = request.get_json() or {}
    db_type = data.get("db_type", "sqlite")
    mgr = _get_db_manager()
    success, msg = mgr.connect(db_type=db_type, **data.get("params", {}))
    if not success:
        return jsonify({"success": False, "error": msg}), 400
    schema = mgr.get_schema()
    return jsonify({"success": True, "message": msg, "schema": schema})

@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.get_json() or {}
    user_prompt = data.get("prompt", "").strip()
    mgr = _get_db_manager()
    if not mgr.is_connected():
        return jsonify({"success": False, "error": "No database connected."}), 400
    schema = mgr.get_schema()
    nl_engine = _get_nl_processor()
    gen_result = nl_engine.generate_sql(user_prompt, schema, mgr.dialect)
    raw_sql = gen_result.get("sql", "")
    val_result = _sql_validator.validate(raw_sql, mgr)
    if not val_result["is_safe"]:
        return jsonify({"success": False, "error": val_result["reason"]}), 400
    if val_result.get("requires_confirmation"):
        op_id = os.urandom(8).hex()
        _pending[op_id] = {"sql": raw_sql, "db_id": session.get("db_manager_id")}
        return jsonify({"success": True, "requires_confirmation": True,
                        "op_id": op_id, "sql": raw_sql,
                        "affected_preview": val_result.get("affected_count")})
    result = mgr.execute_query(raw_sql)
    return jsonify({"success": True, "data": result, "sql": raw_sql})
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 32 (Internal 28): app.py - Confirmation, Anomalies & Drivers Endpoints
    story.append(Paragraph("Page No. 28", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("app.py (continued):", styles['SubSecHead']))
    story.append(Paragraph("REST API endpoints for DML two-phase commit, anomalies, and driver analysis:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
@app.route("/api/confirm", methods=["POST"])
def api_confirm():
    data = request.get_json() or {}
    op_id = data.get("op_id")
    confirmed = data.get("confirmed", False)
    if op_id not in _pending:
        return jsonify({"success": False, "error": "Operation expired."}), 404
    pending_op = _pending.pop(op_id)
    if not confirmed:
        return jsonify({"success": True, "message": "Operation cancelled."})
    mgr = _get_db_manager()
    exec_result = mgr.execute_mutation(pending_op["sql"])
    return jsonify({"success": True, "result": exec_result})

@app.route("/api/anomalies", methods=["POST"])
def api_anomalies():
    data = request.get_json() or {}
    table_name = data.get("table_name")
    mgr = _get_db_manager()
    rows, cols = mgr.get_table_data(table_name)
    results = detect_anomalies(columns=cols, rows=rows, table_name=table_name)
    return jsonify(results)

@app.route("/api/drivers", methods=["POST"])
def api_drivers():
    data = request.get_json() or {}
    table_name = data.get("table_name")
    target_col = data.get("target_column")
    mgr = _get_db_manager()
    rows, cols = mgr.get_table_data(table_name)
    results = analyze_drivers(columns=cols, rows=rows, target_column=target_col)
    return jsonify(results)
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 33 (Internal 29): 6.4.2 Database Manager Subsystem
    story.append(Paragraph("Page No. 29", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4.2 Database Manager Subsystem (core/database_manager.py):", styles['SubSecHead']))
    story.append(Paragraph("Multi-dialect database connection pool and query execution engine:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
import os
import sqlalchemy as sa
from sqlalchemy import inspect, text

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.dialect = "sqlite"
        self._connected = False

    def connect(self, db_type="sqlite", **kwargs):
        try:
            if db_type == "sqlite":
                file_path = kwargs.get("database_path", "")
                if not os.path.exists(file_path):
                    return False, f"File not found: {file_path}"
                url = f"sqlite:///{os.path.abspath(file_path)}"
                self.dialect = "sqlite"
            elif db_type == "mysql":
                u, p = kwargs.get("username"), kwargs.get("password")
                h, pt = kwargs.get("host"), kwargs.get("port", 3306)
                db = kwargs.get("database")
                url = f"mysql+pymysql://{u}:{p}@{h}:{pt}/{db}"
                self.dialect = "mysql"
            elif db_type == "postgresql":
                u, p = kwargs.get("username"), kwargs.get("password")
                h, pt = kwargs.get("host"), kwargs.get("port", 5432)
                db = kwargs.get("database")
                url = f"postgresql+psycopg2://{u}:{p}@{h}:{pt}/{db}"
                self.dialect = "postgresql"
            self.engine = sa.create_engine(url)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self._connected = True
            return True, "Connected successfully."
        except Exception as e:
            self._connected = False
            return False, str(e)
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 34 (Internal 30): core/database_manager.py Schema & Loader
    story.append(Paragraph("Page No. 30", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("core/database_manager.py (continued):", styles['SubSecHead']))
    story.append(Paragraph("Automated metadata schema reflection and tabular file ingestion:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
    def get_schema(self):
        if not self._connected:
            return {}
        inspector = inspect(self.engine)
        schema_dict = {}
        for tbl in inspector.get_table_names():
            columns = []
            for col in inspector.get_columns(tbl):
                columns.append({
                    "name": col["name"],
                    "type": str(col["type"]),
                    "primary_key": col.get("primary_key", False)
                })
            fks = inspector.get_foreign_keys(tbl)
            with self.engine.connect() as conn:
                count_res = conn.execute(text(f"SELECT COUNT(*) FROM {tbl}"))
                row_cnt = count_res.scalar() or 0
            schema_dict[tbl] = {
                "columns": columns,
                "foreign_keys": fks,
                "row_count": row_cnt
            }
        return schema_dict

    def load_spreadsheet(self, file_path, table_name):
        import pandas as pd
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        return True, len(df)
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 35 (Internal 31): 6.4.3 Natural Language Processor (core/nl_processor.py)
    story.append(Paragraph("Page No. 31", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4.3 Natural Language Processor (core/nl_processor.py):", styles['SubSecHead']))
    story.append(Paragraph("Google Gemini 2.0 Flash client initialization and schema-grounded prompting:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
import os, json
from google import genai
from google.genai import types

class NLProcessor:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash"

    def _build_system_prompt(self, schema, dialect):
        schema_text = ""
        for tbl, info in schema.items():
            cols = [f"{c['name']} ({c['type']})" for c in info['columns']]
            schema_text += f"Table {tbl}: {', '.join(cols)}; Rows: {info['row_count']}\\n"
        return f\"\"\"You are QueryMind, an expert SQL synthesizer.
Translate the user natural language query into precise {dialect} SQL.
Database Schema:
{schema_text}
Rules:
1. Generate syntactically valid {dialect} SQL.
2. Only reference existing tables and columns.
3. Return JSON: {{"sql": "...", "explanation": "...", "viz_type": "bar|table|line"}}
4. Never generate DDL statements (DROP, CREATE, ALTER).\"\"\"

    def generate_sql(self, prompt, schema, dialect):
        sys_instruction = self._build_system_prompt(schema, dialect)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.1,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 36 (Internal 32): core/nl_processor.py Context & Parser
    story.append(Paragraph("Page No. 32", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("core/nl_processor.py (continued):", styles['SubSecHead']))
    story.append(Paragraph("Multi-turn conversation context manager and query refinement handler:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
class ConversationManager:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history

    def add_turn(self, user_prompt, generated_sql, explanation):
        self.history.append({
            "user_prompt": user_prompt,
            "sql": generated_sql,
            "explanation": explanation
        })
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context_turns(self):
        context = ""
        for i, turn in enumerate(self.history):
            context += f"Turn {i+1}: User='{turn['user_prompt']}' -> SQL='{turn['sql']}'\\n"
        return context

    def clear(self):
        self.history.clear()
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 37 (Internal 33): 6.4.4 SQL AST Validator (core/sql_validator.py)
    story.append(Paragraph("Page No. 33", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4.4 SQL AST Validator (core/sql_validator.py):", styles['SubSecHead']))
    story.append(Paragraph("Abstract Syntax Tree token inspection and DDL keyword blacklisting:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import DDL, DML, Keyword

FORBIDDEN_DDL = {"DROP", "ALTER", "CREATE", "TRUNCATE", "RENAME"}
MUTATION_DML = {"UPDATE", "DELETE", "INSERT"}

class SQLValidator:
    def validate(self, sql_string, db_manager):
        if not sql_string or not sql_string.strip():
            return {"is_safe": False, "reason": "Query string is empty."}
        parsed = sqlparse.parse(sql_string)
        if len(parsed) > 1:
            return {"is_safe": False, "reason": "Multi-statement queries are forbidden."}
        stmt = parsed[0]
        root_token = stmt.get_type().upper()
        # Enforce strict DDL blacklist
        for token in stmt.flatten():
            if token.ttype in (DDL, Keyword):
                val = token.value.upper()
                if val in FORBIDDEN_DDL:
                    return {"is_safe": False,
                            "reason": f"Destructive operation blocked: {val}"}
        if root_token in MUTATION_DML:
            affected_count = self._estimate_affected_rows(sql_string, db_manager)
            return {
                "is_safe": True,
                "requires_confirmation": True,
                "statement_type": root_token,
                "affected_count": affected_count
            }
        return {"is_safe": True, "requires_confirmation": False, "type": "SELECT"}
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 38 (Internal 34): core/sql_validator.py Dry-Run & Safety Gate
    story.append(Paragraph("Page No. 34", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("core/sql_validator.py (continued):", styles['SubSecHead']))
    story.append(Paragraph("DML row-count estimation via non-committing dry-run transactions:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
    def _estimate_affected_rows(self, sql, db_manager):
        \"\"\"Executes mutation in a transaction and rolls back immediately to preview affected rows.\"\"\"
        try:
            with db_manager.engine.connect() as conn:
                trans = conn.begin()
                result = conn.execute(sqlparse.sql.text(sql))
                count = result.rowcount
                trans.rollback()
                return count if count >= 0 else 0
        except Exception:
            return -1 # Unable to estimate dry-run
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 39 (Internal 35): 6.4.5 Local ML Anomaly Detector (core/ml_analyzer.py)
    story.append(Paragraph("Page No. 35", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4.5 Local ML Anomaly Detector (core/ml_analyzer.py):", styles['SubSecHead']))
    story.append(Paragraph("Automated feature classification and Scikit-Learn preprocessing pipeline:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

def _classify_columns(df):
    num_cols, cat_cols, txt_cols = [], [], []
    for col in df.columns:
        if df[col].nunique() <= 1:
            continue
        if df[col].nunique() == len(df) and (str(col).lower().endswith('_id') or str(col).lower() == 'id'):
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            num_cols.append(col)
        elif df[col].nunique() < 20 or (df[col].nunique() / len(df) < 0.2):
            cat_cols.append(col)
        else:
            txt_cols.append(col)
    return num_cols, cat_cols, txt_cols
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 40 (Internal 36): core/ml_analyzer.py Isolation Forest + LOF Ensemble
    story.append(Paragraph("Page No. 36", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("core/ml_analyzer.py (continued):", styles['SubSecHead']))
    story.append(Paragraph("Ensemble anomaly detection and human-interpretable explanation generator:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
def detect_anomalies(columns, rows, table_name="data", contamination=0.1):
    df = pd.DataFrame(rows, columns=columns)
    num_cols, cat_cols, txt_cols = _classify_columns(df)
    if not num_cols:
        return {"success": False, "error": "No numeric columns found for anomaly detection."}
    transformers = [
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),
                          ('scaler', StandardScaler())]), num_cols)
    ]
    if cat_cols:
        transformers.append(('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                                             ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cat_cols))
    preprocessor = ColumnTransformer(transformers=transformers)
    X = preprocessor.fit_transform(df)
    
    # Model 1: Isolation Forest (200 trees)
    iso = IsolationForest(n_estimators=200, contamination=contamination, random_state=42)
    iso_preds = iso.fit_predict(X)
    
    # Model 2: Local Outlier Factor
    n_neigh = min(20, max(5, len(df) - 1))
    lof = LocalOutlierFactor(n_neighbors=n_neigh, contamination=contamination, novelty=False)
    lof_preds = lof.fit_predict(X)
    
    # Combined Ensemble Vote
    anomalies = []
    for idx in range(len(df)):
        if iso_preds[idx] == -1 or lof_preds[idx] == -1:
            row_data = df.iloc[idx].to_dict()
            reasons = _generate_human_reason(df.iloc[idx], num_cols, df)
            anomalies.append({"row_id": idx, "data": row_data, "reasons": reasons})
    return {"success": True, "total_rows": len(df), "anomalies_count": len(anomalies),
            "anomaly_rate": round(len(anomalies)/len(df)*100, 1), "anomalies": anomalies}
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 41 (Internal 37): 6.4.6 Local Feature Drivers Analyzer (core/ml_drivers.py)
    story.append(Paragraph("Page No. 37", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4.6 Local Feature Drivers Analyzer (core/ml_drivers.py):", styles['SubSecHead']))
    story.append(Paragraph("Random Forest feature importance quantification and driver ranking:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def analyze_drivers(columns, rows, target_column):
    df = pd.DataFrame(rows, columns=columns).dropna(subset=[target_column])
    if len(df) < 10 or target_column not in df.columns:
        return {"success": False, "error": "Insufficient data rows or target missing."}
    y_raw = df[target_column]
    X_df = df.drop(columns=[target_column])
    num_cols, cat_cols, _ = _classify_columns(X_df)
    is_regression = pd.api.types.is_numeric_dtype(y_raw)
    y = y_raw.values if is_regression else LabelEncoder().fit_transform(y_raw)
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),
                          ('scaler', StandardScaler())]), num_cols),
        ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                          ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cat_cols)
    ])
    X = preprocessor.fit_transform(X_df)
    model = RandomForestRegressor(n_estimators=100, random_state=42) if is_regression else RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Map back feature importances to original column names
    importances = model.feature_importances_
    col_scores = {} # Aggregate one-hot back to feature column
    # ... aggregation logic ...
    total = sum(col_scores.values()) or 1.0
    ranked = sorted([{"feature": k, "importance": round(v/total*100, 1)} for k, v in col_scores.items()],
                    key=lambda x: x["importance"], reverse=True)
    return {"success": True, "target": target_column, "drivers": ranked}
</font>""", code_style))
    story.append(PageBreak())
    
    # Page 42 (Internal 38): 6.4.7 Frontend Controller Script (static/js/app.js)
    story.append(Paragraph("Page No. 38", styles['PNum']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4.7 Frontend Controller Script (static/js/app.js):", styles['SubSecHead']))
    story.append(Paragraph("Client-side state orchestration, asynchronous dispatch, and dynamic rendering:", styles['Body']))
    story.append(Paragraph("""<font face="Courier">
// static/js/app.js - QueryMind Client Orchestrator
async function sendQuery(userPrompt) {
    appendChatMessage('user', userPrompt);
    showTypingIndicator();
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: userPrompt })
        });
        const data = await response.json();
        hideTypingIndicator();
        if (!data.success) {
            appendChatMessage('system', `Error: ${data.error}`);
            return;
        }
        if (data.requires_confirmation) {
            showConfirmationModal(data.op_id, data.sql, data.affected_preview);
            return;
        }
        appendChatMessage('assistant', data.explanation || 'Query executed successfully.');
        renderResultTable(data.data.columns, data.data.rows);
        if (data.viz_type && data.viz_type !== 'table') {
            renderChart(data.viz_type, data.data.columns, data.data.rows);
        }
        updateHistorySidebar();
    } catch (err) {
        hideTypingIndicator();
        appendChatMessage('system', `Network Exception: ${err.message}`);
    }
}
</font>""", code_style))
    story.append(PageBreak())

print("Chapter 6 defined successfully.")
