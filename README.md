# QueryMind — Natural Language Database Assistant

An intelligent web application that lets you interact with databases using plain English instead of SQL. 

## Features

- 🗣️ **Natural Language Queries** — Ask questions in plain English
- 🔗 **Multi-Database Support** — SQLite, MySQL, PostgreSQL
- 📊 **Data Visualization** — Auto-generated tables and charts
- ✏️ **Data Modification** — Add, update, delete with confirmation
- 🛡️ **Safety First** — Preview changes before execution, dangerous operations blocked
- 💬 **Conversational** — Follow-up queries understand context
- 📜 **Operation History** — Full audit trail of all operations
- 🎨 **Premium UI** — Dark glassmorphism design

## Quick Start

### 1. Prerequisites
- Python 3.10 or higher

### 2. Setup

```bash
# Clone the project
cd text-to-sql

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
# Copy the example env file
copy .env.example .env     # Windows
cp .env.example .env       # macOS/Linux

### 4. Run

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

## How to Use

1. **Connect** — Click "Connect Database" and enter your database details
2. **Ask** — Type questions in natural language:
   - `"Show me all customers from Mumbai"`
   - `"What are the top 10 products by sales?"`
   - `"How many orders were placed last month?"`
3. **Modify** — Request changes with confirmation:
   - `"Add a new customer named Priya with email priya@gmail.com"`
   - `"Increase all product prices by 10%"`
   - `"Delete inactive users"`
4. **Follow up** — Continue the conversation naturally:
   - `"Now filter those by city"`
   - `"Show only the top 5"`

## Database Support

| Database   | Connection Info Required |
|-----------|------------------------|
| SQLite     | File path only |
| MySQL      | Host, port, username, password, database name |
| PostgreSQL | Host, port, username, password, database name |

## Project Structure

```
text-to-sql/
├── app.py                  # Flask server & API routes
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── core/
│   ├── database_manager.py # DB connections & schema inspection
│   ├── nl_processor.py     # Gemini AI integration
│   ├── sql_validator.py    # SQL safety validation
│   ├── conversation.py     # Conversation context
│   └── history.py          # Operation history tracking
├── templates/
│   └── index.html          # Web interface
└── static/
    ├── css/style.css        # Styling
    └── js/
        ├── app.js           # Main controller
        ├── chat.js          # Chat interface
        ├── database.js      # DB connection UI
        ├── visualization.js # Tables & charts
        └── history.js       # History sidebar
```

## Safety Features

- ⛔ DDL operations (DROP, ALTER, CREATE, TRUNCATE) are **permanently blocked**
- ⚠️ All modifications require **explicit confirmation** before execution
- 🔍 Affected row count is **previewed** before any UPDATE/DELETE
- 🚨 Large-scale operations show **extra warnings**
- 🛑 Multi-statement queries are **blocked** to prevent injection

## Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLAlchemy (multi-DB support)
- **Frontend:** Vanilla HTML/CSS/JS
- **Charts:** Chart.js

## License

This project is for educational purposes.
