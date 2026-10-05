# S.P. Mandali's
# Ramnarain Ruia Autonomous College
### Matunga, Mumbai - 400019
### Department of Computer Science

---

# Research Project Report
## On
# QueryMind: Intelligent Natural Language to SQL Interface with Machine Learning Driven Data Diagnostics and Anomaly Detection

**Project Guide:** Mrs. Edith Juni  
**Project By:** Mr Harshal Pandharinath Loke  
**Seat No:** 564  
**Degree:** M.Sc. Computer Science  
**Academic Batch:** 2026 - 2027  

---

## ACKNOWLEDGEMENT

Every project big or small is successful, largely due to the effort of a number of wonderful people who have always given their valuable advice or have always lent a helping hand.

I take this opportunity of submitting this report to express my profound gratitude to the management of "Ramnarain Ruia Autonomous College" for giving me the opportunity to accomplish this project work.

I am also thankful to all the teachers for their kind support and help.

I express my deepest gratitude towards my project guide **Mrs. Edith Juni** for her valuable and timely advice during the various phases in my project.

I express my sincere thanks to our respected Co-ordinator **Mrs. Aarya Tawde** for allowing us to use the facilities available.

I would also like to thank all those unnamed but important people and Computer Lab Assistants and supportive staff who directly or indirectly helped me in the completion of this project and to my family and friends without whose support, motivation and encouragement this would not have been possible.

**Thanking you,**  
**Harshal P. Loke**  

---

# INDEX

| Sr. No. | Contents | Page No. |
| :---: | :--- | :---: |
| **1** | **Problem Statement** | **1 - 2** |
| | 1.1 Problem Definition | 2 |
| **2** | **Abstract** | **3 - 4** |
| | 2.1 Project Abstract | 4 |
| **3** | **Introduction** | **5 - 9** |
| | 3.1 Project Introduction | 6 |
| | 3.2 Developed System Overview | 7 |
| | 3.3 Unique Selling Propositions (USP) of the System | 7 |
| | 3.4 Advantages of the Project | 8 - 9 |
| **4** | **Literature Review** | **10 - 13** |
| | 4.1 Literature Review for the Project | 11 - 13 |
| **5** | **Research Methodology** | **14 - 17** |
| | 5.1 Agile Methodology | 15 - 17 |
| **6** | **Experimental Setup** | **18 - 38** |
| | 6.1 Requirements Analysis | 19 - 23 |
| | 6.2 System Architecture Diagram | 24 |
| | 6.3 Block Diagram of System Flow | 25 |
| | 6.4 Input Code | 26 - 38 |
| **7** | **Results** | **39 - 52** |
| | 7.1 Results Obtained | 40 - 50 |
| | 7.2 Test Cases | 51 - 52 |
| **8** | **Conclusion & Future Scope** | **53 - 54** |
| | 8.1 Conclusion | 54 |
| | 8.2 Future Scope | 54 |
| **9** | **References** | **55 - 57** |
| | 9.1 References | 56 - 57 |

---

# 1. PROBLEM STATEMENT

### 1.1 Problem Definition

In modern enterprise computing environments, relational database management systems (RDBMS) such as SQLite, MySQL, and PostgreSQL store mission-critical operational and analytical records. However, querying these databases requires specialized proficiency in Structured Query Language (SQL), relational algebra, and intricate database schemas. Non-technical business analysts, domain researchers, and organizational decision-makers are frequently obstructed by this technical syntax barrier, necessitating reliance on database administrators or data engineering teams. This communication bottleneck severely delays time-sensitive analytical reporting and business intelligence exploration.

While emerging Large Language Models (LLMs) demonstrate remarkable semantic comprehension and natural language processing capabilities, unguided generative AI interfaces present acute operational vulnerabilities when interacting directly with production database environments. Without strict deterministic validation, raw LLM-synthesized queries risk generating destructive Data Definition Language (DDL) operations, executing non-deterministic mutations without transactional rollbacks, or succumbing to prompt injection exploits.

Furthermore, existing database tools remain strictly passive: they require users to formulate exact hypothesis queries rather than proactively detecting anomalous transactions, identifying key business performance drivers, or isolating multidimensional outliers in the underlying records.

The current challenge is to design and develop an intelligent system that:
1. Continuously converts natural language inquiries into syntactically precise, schema-grounded SQL across heterogeneous relational databases (SQLite, MySQL, PostgreSQL) and tabular spreadsheets (CSV/Excel).
2. Enforces a multi-tiered security firewall that permanently prohibits catastrophic DDL operations (DROP, ALTER, TRUNCATE) and requires explicit two-phase confirmation before committing any data modification (UPDATE, DELETE, INSERT).
3. Preserves multi-turn conversational context, enabling users to iteratively filter, refine, and drill down into query results without re-specifying prior conversational constraints.
4. Executes 100% local, privacy-preserving machine learning diagnostics (Isolation Forest, Local Outlier Factor, and Random Forest feature importance) without transmitting proprietary organizational records to third-party cloud APIs.
5. Automatically surfaces proactive heuristic business insights (revenue trends, critical inventory stockout warnings, and customer clustering opportunities) immediately upon database connection.

The overarching objective is to deliver an end-to-end, enterprise-grade natural language database assistant that empowers non-technical stakeholders to safely query, visualize, and extract advanced machine learning diagnostics from complex databases with zero SQL overhead and deterministic safety guarantees.

---

# 2. ABSTRACT

### 2.1 Project Abstract

The democratization of database querying has emerged as a fundamental challenge in modern information systems. While modern enterprises accumulate vast repositories of structured data, extracting timely insights remains heavily gatekept by the technical complexity of Structured Query Language (SQL). This research presents **QueryMind**, an advanced, full-stack database intelligence platform that bridges natural language human intent with robust relational database execution, fortified by deterministic Abstract Syntax Tree (AST) validation and local, privacy-preserving machine learning diagnostics.

QueryMind couples the generative language understanding of the Google Gemini 2.0 Flash engine with dynamic, schema-grounded prompt orchestration. Through real-time SQLAlchemy schema reflection, the system injects table structures, column constraints, primary/foreign key mappings, and dialect-specific conventions directly into the LLM context, yielding high zero-shot translation accuracy across SQLite, MySQL, and PostgreSQL environments. To mitigate generative vulnerabilities, QueryMind implements a multi-stage security gate utilizing `sqlparse` AST token inspection. Catastrophic Data Definition Language (DDL) operations such as `DROP`, `ALTER`, and `TRUNCATE` are deterministically rejected, while multi-statement injection vectors are neutralized. For Data Manipulation Language (DML) queries (`UPDATE`, `DELETE`, `INSERT`), the architecture employs a two-phase confirmation mechanism featuring transactional dry-run row-count estimation, ensuring administrative preview before commit.

Beyond query generation, QueryMind integrates a completely local, zero-leakage Machine Learning engine built on Scikit-Learn. The diagnostic module implements an automated column classification and preprocessing pipeline (combining median imputation, standard scaling, one-hot encoding, and TF-IDF vectorization) followed by an ensemble of Isolation Forest (200 estimators) and Local Outlier Factor (LOF). Flagged outliers are augmented with human-interpretable statistical explanations based on Z-score thresholds, Tukey's interquartile range (IQR) fences, and mean-ratio multipliers. Simultaneously, a Random Forest feature importance module quantifies the mathematical drivers of key database attributes, while an automated heuristic engine uncovers immediate revenue trends, inventory stockout risks, and geographic opportunities upon data ingestion.

Experimental validation across enterprise e-commerce databases (including multi-table schemas with 331+ order items, customer demographics, and product catalogs) demonstrates sub-second query synthesis latency, 100% interception of forbidden DDL statements, and accurate isolation of multivariate price and quantity anomalies. QueryMind establishes a highly secure, reliable, and scalable paradigm for non-technical database exploration and automated machine learning diagnostics.

---

# 3. INTRODUCTION

### 3.1 Project Introduction

The digital transformation of commercial, governmental, and academic enterprises has led to exponential growth in the volume and velocity of structured data. Organizations increasingly rely on relational databases to record transactions, manage supply chains, profile customer behaviors, and monitor operational telemetry. Despite the ubiquity of relational databases, interacting with structured stores remains fundamentally constrained by the steep learning curve of Structured Query Language (SQL). Business executives, product managers, clinical researchers, and frontline analysts must either master complex SQL syntax or submit ad-hoc reporting tickets to technical database teams, creating severe operational friction.

Recent breakthroughs in Large Language Models (LLMs) offer unprecedented opportunities to establish Natural Language Interfaces to Databases (NLIDBs). By mapping unstructured colloquial questions into structured database commands, LLMs can bridge the communication gap between humans and relational engines. However, deploying off-the-shelf generative models directly against enterprise data repositories introduces critical operational and security hazards. Generative models are inherently non-deterministic and susceptible to hallucinations, potentially synthesizing malformed SQL, misinterpreting column semantic boundaries, or generating disastrous data-modifying statements.

To address these formidable challenges, this project introduces **QueryMind**, an intelligent, full-stack database assistant designed to provide fluid natural language database querying while guaranteeing strict transactional safety, conversational statefulness, and local machine learning diagnostics.

### 3.2 Developed System Overview

The QueryMind platform is structured into five cohesive, loosely coupled architectural tiers:
1. **Presentation Layer:** A dark glassmorphic web interface built with vanilla HTML5, CSS3, and JavaScript, featuring real-time chat interactions, schema hierarchy trees, dynamic Chart.js graphing, and dedicated diagnostic modals.
2. **Application & API Layer:** A lightweight, asynchronous Flask REST micro-service managing HTTP routing, session state persistence, file upload processing, and comprehensive audit history logging.
3. **AI & Semantic Processing Layer:** Powered by the Google Gemini 2.0 Flash engine via the `google-genai` SDK, utilizing dynamic schema grounding, few-shot prompt formulation, and multi-turn context memory.
4. **Security & Validation Gate:** A deterministic AST inspection engine built on `sqlparse` that permanently intercepts forbidden DDL commands and executes dry-run row estimations for guarded DML mutations.
5. **Local Machine Learning & Diagnostics Layer:** An on-premise, zero-egress Scikit-Learn analytical engine providing automated column classification, Isolation Forest + LOF anomaly detection, and Random Forest feature driver analysis.
6. **Persistence & Ingestion Layer:** A multi-engine database interface managed via SQLAlchemy Core/ORM, providing native connectivity to SQLite, MySQL, PostgreSQL, and dynamic CSV/Excel dataset ingestion.

### 3.3 Unique Selling Propositions (USP) of the System

1. **100% Local Machine Learning Diagnostics:** Unlike conventional tools that offload data to expensive cloud endpoints, QueryMind executes anomaly detection and feature importance locally, guaranteeing zero data leakage and zero API egress costs.
2. **Deterministic AST Security Firewall:** Operates an unbypassable abstract syntax tree inspection gate that permanently eliminates catastrophic DDL operations and blocks multi-statement injection vectors.
3. **Two-Phase DML Modification Safety Net:** Data mutations (UPDATE, DELETE) trigger automated dry-run row-count previews, requiring explicit administrator confirmation before database commit.
4. **True Multi-Dialect Agnosticism:** Transparently communicates with SQLite, MySQL, and PostgreSQL engines, adapting syntax, quotes, and functions to the connected database dialect automatically.
5. **Multi-Turn Conversational Memory:** Maintains context across conversation turns, enabling natural analytical drilling such as "Now filter those by Mumbai" or "Show top 5".
6. **Automated Proactive Business Insights:** Automatically computes and highlights revenue trends, inventory stockout risks, and customer clustering opportunities upon connection without manual prompting.

### 3.4 Advantages of the Project

1. **Complete Democratization of Relational Data:** Non-technical staff, business analysts, executives, and students can extract sophisticated analytical answers without memorizing SQL syntax or table joins.
2. **Permanent DDL Destruction Protection:** Dangerous structural modifications (DROP, ALTER, CREATE, TRUNCATE) are permanently halted at the parser level, ensuring that database schemas cannot be accidentally damaged.
3. **Two-Phase Interactive Mutation Verification:** High-risk UPDATE and DELETE queries are intercepted; affected row counts are computed via non-committing transactions and presented for explicit confirmation before execution.
4. **Absolute Privacy for Machine Learning:** Sensitive organizational records analyzed for outliers and feature drivers never leave the local environment, satisfying strict GDPR, HIPAA, and corporate data governance mandates.
5. **Cross-Engine Relational Portability:** Organizations can switch between embedded SQLite databases, enterprise MySQL installations, and PostgreSQL clusters through a single unified interface.
6. **Dynamic Schema Grounding:** The system introspects live database metadata—table definitions, column data types, and primary/foreign keys—preventing hallucination of non-existent fields.
7. **Multi-Turn Conversational Continuity:** Users can iteratively refine complex queries over multiple conversational turns, supporting fluid exploratory data analysis without redundant inputs.
8. **Automated Visual Analytics:** Automatically selects and generates appropriate Chart.js visual representations (bar graphs, line charts, pie distributions) alongside responsive tabular grids.
9. **Heterogeneous Tabular Spreadsheet Ingestion:** Supports instantaneous upload and SQL querying of standalone CSV and Excel (XLSX) workbooks by automatically provisioning temporary relational tables.
10. **Granular Audit Trails and Operation Logging:** Records every executed query, status, execution duration, and timestamp, providing complete traceability for enterprise compliance.
11. **Zero Training Overhead for End Users:** By leveraging intuitive natural language prompts, organizational onboarding time is reduced to minutes, eliminating prolonged database syntax training programs.
12. **Explainable Outlier Diagnostics:** Unlike opaque black-box anomaly detectors, QueryMind equips every flagged outlier with actionable statistical justifications, such as Z-score variances, Tukey IQR fence violations, and mean-ratio multiples.
13. **Low Latency Local In-Memory Execution:** Local Scikit-Learn pipelines execute in hundreds of milliseconds, avoiding network round-trip overhead and cloud throttling associated with external analytical APIs.
14. **High Resilience Against SQL Injection Attacks:** Multi-statement query sequences and delimiter-chaining injection patterns are strictly blocked by the tokenizer, shielding production databases from malicious inputs.
15. **Regulatory Compliance and Governance Enablement:** Real-time operation counters, status trackers, and local data isolation simplify regulatory auditing in finance, healthcare, and education.
16. **Fault-Tolerant Session Isolation:** Session-scoped connection pools ensure that multiple concurrent browser instances operate independently without memory contamination or transaction crosstalk.

---

# 4. LITERATURE REVIEW

### 4.1 Literature Review for the Project

1. **Natural Language Interfaces to Databases (NLIDBs):** Early NLIDB architectures relied on rigid semantic grammars, pattern-matching rules, and intermediate logical representations (such as LUNAR and PRECISE). While historically foundational, these systems failed when presented with conversational ambiguity or slight deviations in user phrasing. The advent of neural sequence-to-sequence models (e.g., Seq2SQL, Pointer Networks) introduced probabilistic semantic parsing, demonstrating that deep neural networks can map unconstrained natural language queries into valid SQL syntax. [1] [2]
2. **Large Language Models in Structured Query Synthesis:** The introduction of Transformer-based Large Language Models (LLMs) such as Google Gemini, Codex, and GPT-4 revolutionized code generation. Research by Rajkumar et al. and Floratou et al. demonstrates that pre-trained foundational models possess deep understanding of relational schemas, SQL dialect semantics, and query optimization rules. When provided with appropriate context, modern LLMs achieve high zero-shot and few-shot translation accuracy. In QueryMind, Google Gemini 2.0 Flash is selected for its balance of rapid inference latency, contextual reasoning, and structured output formatting. [3] [4]
3. **Schema Grounding and In-Context Prompt Engineering:** A critical limitation of raw LLM generation is "hallucination"—the synthesis of queries referencing non-existent tables or invalid column names. Literature in in-context learning establishes that dynamically grounding the prompt with explicit schema catalogs, data types, and primary-foreign key relationships dramatically reduces hallucination rates. QueryMind employs dynamic runtime schema introspection via SQLAlchemy, extracting active schema structures and injecting them directly into system prompts. [5]
4. **Abstract Syntax Tree (AST) Parsing for Query Security:** Allowing unconstrained generative models to execute queries directly against databases introduces severe security vulnerabilities, including destructive DDL commands and multi-statement injection attacks. Scholarly works on database firewalls emphasize lexical and AST-level query inspection over simple string regex filtering. By parsing queries into structured token trees using `sqlparse`, QueryMind deterministically identifies statement types, permanently eliminating catastrophic `DROP` or `ALTER` statements and isolating DML mutations for administrative verification. [6]
5. **Conversational Semantic Parsing and Discourse State Tracking:** Real-world data exploration is inherently iterative. Benchmarks such as SParC and CoSQL established standards for multi-turn semantic parsing, demonstrating that users rarely express complete analytical requests in a single isolated prompt. Academic literature highlights the need for dialogue state trackers that preserve conversational history and previously generated SQL ASTs. QueryMind implements a multi-turn conversation memory that injects prior turns into the prompt context, supporting seamless incremental query refinement. [7]
6. **Isolation Forest for Unsupervised Anomaly Detection:** Proposed by Liu, Ting, and Zhou, Isolation Forest is an unsupervised tree-based ensemble designed specifically for multidimensional anomaly detection. Unlike distance-based or density-based algorithms that suffer from the "curse of dimensionality", Isolation Forest explicitly isolates outliers by randomly partitioning feature spaces. Outliers require fewer recursive splits to isolate than normal data points, resulting in shorter average path lengths in isolation trees. QueryMind deploys an Isolation Forest ensemble (200 trees) to detect multivariate tabular outliers efficiently and deterministically. [8]
7. **Local Outlier Factor (LOF) for Density-Based Outlier Identification:** Breunig et al. introduced Local Outlier Factor (LOF), which evaluates an object's anomaly score by comparing its local density to the density of its k-nearest neighbors. LOF excels at identifying "local" outliers in datasets with varying density clusters where global isolation models might struggle. QueryMind combines Isolation Forest with Local Outlier Factor in an ensemble framework, ensuring robust detection across both global distribution anomalies and localized dense clusters. [9]
8. **Feature Importance and Driver Analysis using Random Forests:** Breiman's seminal work on Random Forests establishes ensemble decision trees as powerful estimators of feature importance through Mean Decrease Impurity (MDI) and out-of-bag permutation metrics. In enterprise data analysis, identifying which independent features drive a key business outcome (such as customer churn, revenue, or transaction status) is essential. QueryMind utilizes Random Forest regressors and classifiers to compute normalized feature importance percentages, providing users with mathematically grounded drivers for any selected database column. [10]
9. **Privacy-Preserving On-Premise Analytics vs. Cloud Offloading:** Transmitting private enterprise databases to external cloud-hosted machine learning APIs introduces substantial regulatory compliance risks under GDPR, HIPAA, and data protection statutes. Literature on enterprise AI architectures highlights the critical importance of keeping diagnostic and analytical computations strictly within the local host boundary. QueryMind executes its entire machine learning diagnostic suite locally using Scikit-Learn. [11]
10. **Database Abstraction and Dialect Neutrality with SQLAlchemy:** Relational database management systems vary significantly in their SQL syntax dialects, quotation conventions, function naming, and connection drivers. Bayer's SQLAlchemy architecture provides a unified Object-Relational Mapping (ORM) and Core abstraction layer that standardizes query compilation and schema introspection across disparate relational backends. QueryMind leverages SQLAlchemy to seamlessly interface with SQLite, MySQL, and PostgreSQL without dialect lock-in. [12]
11. **Modern Web Application Architectures and Dynamic Visualizations:** Modern business intelligence platforms demand responsive, ergonomic client interfaces capable of rendering tabular data alongside reactive visual graphs. Research into human-computer interaction (HCI) shows that combining conversational chat with synchronized tabular and graphic views accelerates user comprehension. QueryMind integrates vanilla JavaScript with Chart.js, delivering high-performance, interactive bar, line, and pie visualizations directly within a dark glassmorphic dashboard. [13]
12. **Automated Heuristic Profiling and Statistical Summarization:** Studies in automated exploratory data analysis (AutoEDA) show that computing initial summary statistics upon data ingestion reduces cognitive load on analysts. QueryMind incorporates an automated heuristic scanner that immediately computes revenue dominance trends, critical inventory warnings, and regional customer clusters upon database connection. [14]

---

# 5. RESEARCH METHODOLOGY

### 5.1 Agile Methodology

The development of QueryMind was governed by the Agile software development methodology. Agile's iterative lifecycle, continuous feedback loops, and rapid prototyping capabilities make it uniquely suited for a multi-disciplinary system that integrates modern generative AI, deterministic AST security compilers, local machine learning pipelines, and responsive web user interfaces.

**1. Agile Dual-Purpose Framework:**
- *Technical Agility:* Facilitates rapid architectural adaptation to evolving LLM API response formats, token context windows, database dialect quirks, and Scikit-Learn memory constraints.
- *Research Agility:* Enables rapid empirical validation of semantic translation accuracy, AST security boundary robustness, and anomaly detection precision against real-world relational schemas.

**2. Requirement Analysis & Feasibility Study:**
- *Functional Requirements:* Natural language query translation; multi-database connectivity (SQLite, MySQL, PostgreSQL); CSV/Excel dynamic ingestion; AST security validation; guarded two-phase DML execution; local Isolation Forest + LOF anomaly detection; Random Forest feature driver analysis; and automated heuristic insight discovery.
- *Non-Functional Requirements:* Sub-2.5-second end-to-end query synthesis latency; 100% interception of destructive DDL commands; zero cloud data transmission during ML execution; memory usage under 250 MB; responsive cross-platform web UI.
- *Feasibility Checks:* Evaluated Google Gemini 2.0 Flash token latency, SQLAlchemy dialect compatibility, Scikit-Learn in-memory execution throughput, and browser DOM rendering limits.

**3. Sprint Breakdown and Iterative Milestones:**
- *Sprint 1 (Architecture & Ingestion):* Core Flask micro-service setup; SQLAlchemy connection manager for SQLite, MySQL, and PostgreSQL; Pandas CSV/Excel ingestion pipeline.
- *Sprint 2 (Natural Language Engine):* Google Gemini 2.0 Flash integration; dynamic schema introspection; prompt grounding; JSON structured response parsing.
- *Sprint 3 (Security Firewall):* `sqlparse` AST parser implementation; DDL blacklist; multi-statement injection blocking; DML dry-run transaction row-count preview.
- *Sprint 4 (Local ML Diagnostic Suite):* Column classification pipeline; Isolation Forest + LOF ensemble; statistical reason generator; Random Forest feature drivers.
- *Sprint 5 (Presentation & Visual Analytics):* Dark glassmorphic UI; real-time chat; schema explorer tree; Chart.js dynamic graphing; diagnostic modals.
- *Sprint 6 (Testing & Integration):* Unit testing, end-to-end load benchmarks, security penetration validation, and user acceptance testing.

**4. Iterative Development & Continuous Integration:**
- *Short Development Cycles:* Structured in 1-to-2 week cycles, delivering modular, independently testable software components.
- *Version Control:* Managed via Git and GitHub repository branches, enforcing feature-branch isolation and granular commit logs.
- *Modular Unit & Integration Testing:* Database engine tests, LLM parser tests, AST security tests, ML ensemble tests, and REST API route tests.

**5. Validation & Empirical Testing:**
- Multi-Database Testing (SQLite, MySQL, PostgreSQL).
- Security Penetration Testing (Injected DDL, delimiter-chaining multi-statement attacks).
- Machine Learning Benchmarks (Precision, recall, and sub-500 ms processing latency).

**6. Deployment & User Acceptance Testing (UAT):**
- Local deployment and hands-on evaluation sessions with target non-technical users and technical peer reviewers.
- Collection of qualitative and quantitative usability feedback.

**7. Advantages of Agile Methodology in QueryMind:**
- Early functional prototyping.
- Rapid adaptation to generative AI nuances.
- Decoupled parallel development.
- Continuous risk mitigation.
- Direct user-centric evolution.

---

# 6. EXPERIMENTAL SETUP

### 6.1 Requirements Analysis

#### 6.1.1 Software Requirements
1. **Operating System:** Windows 10/11 (64-bit), Ubuntu Linux 20.04 LTS or newer, or macOS Monterey 12.0 or newer.
2. **Web Browser:** Modern Chromium-based or Gecko-based web browser (Google Chrome 110+, Mozilla Firefox 115+, Microsoft Edge 110+, or Safari 16+) supporting HTML5 Canvas, ECMAScript 6+ (ES6), and asynchronous Fetch APIs.
3. **Python Runtime:** Python version 3.10, 3.11, or 3.12 (64-bit) with `pip` package manager and standard C-runtime libraries.
4. **Virtual Environment:** Python virtual environment (`venv`) for isolated dependency sandboxing.

#### 6.1.2 Hardware Requirements
1. **Computing Device:** Personal Computer, Engineering Laptop, or Cloud Virtual Machine.
2. **Central Processing Unit (CPU):** Intel Core i3 / i5 / i7 or AMD Ryzen 3 / 5 / 7 processor operating at 2.0 GHz or higher (multi-core architecture recommended for parallel tree ensembles).
3. **System Memory (RAM):** 8.0 GB minimum (16.0 GB recommended for large multidimensional database table analysis and Scikit-Learn tree construction).
4. **Storage Space:** 6.0 GB available storage space (Solid State Drive [SSD] recommended for low-latency SQLite reads).
5. **Display Resolution:** 1280 x 720 minimum (1920 x 1080 full HD recommended for panoramic dashboard visualization).
6. **Network Connectivity:** Active broadband Internet connection required exclusively for Google Gemini API model inference; all database queries and Scikit-Learn machine learning computations execute 100% locally offline.

#### 6.1.3 Technology Stack & Frameworks
1. **Python Runtime Environment (Python 3.12):** Foundational backend programming language.
2. **Flask Web Micro-Framework (Flask 3.0+, Flask-CORS, Flask-Session):** Lightweight WSGI web application server managing REST API endpoints, session persistence, and CORS policies.
3. **SQLAlchemy Unified Database Abstraction Engine (SQLAlchemy 2.0+):** Universal abstraction layer providing connection pooling, dialect compilation, transaction management, and schema introspection across SQLite, MySQL, and PostgreSQL.
4. **Google Gemini 2.0 Flash Generative AI Engine (`google-genai` SDK):** State-of-the-art semantic reasoning and structured code synthesis translating natural language queries into dialect-compliant SQL.
5. **sqlparse SQL AST Parsing & Security Validation Library (sqlparse 0.5+):** Non-validating SQL parser decomposing raw query strings into Abstract Syntax Tree token hierarchies.
6. **Scikit-Learn Local Machine Learning Suite (Scikit-Learn 1.4+):** On-premise ML suite providing `IsolationForest`, `LocalOutlierFactor`, `RandomForestRegressor`, `RandomForestClassifier`, `ColumnTransformer`, and `StandardScaler`.
7. **Pandas & NumPy Scientific Data Processing Libraries (Pandas 2.2+, NumPy 1.26+):** In-memory tabular data manipulation, numerical array transformations, date-time parsing, and automated missing-value imputation.
8. **OpenPyXL & Ingestion Engines (OpenPyXL 3.1+):** Dynamic parsing of Microsoft Excel workbooks (.xlsx) and CSV files into relational database tables.

#### 6.1.4 Development Tools & Softwares
1. **Visual Studio Code & Thonny IDEs:** Development, linting, debugging, and testing environments.
2. **Git & GitHub:** Distributed version control and milestone tracking.
3. **DB Browser for SQLite:** Visual database administration and validation.
4. **Postman API Platform:** REST API endpoint contract testing.
5. **Chart.js:** Responsive HTML5 Canvas-based chart rendering.

### 6.2 System Architecture Diagram

```
+---------------------------------------------------------------------------------------+
|                        PRESENTATION LAYER (Client Browser)                            |
|  +--------------------+  +--------------------+  +------------------+  +-----------+  |
|  | Dark Glassmorphism |  | Schema Explorer    |  | Chart.js Dynamic |  | ML Modals |  |
|  | Web Dashboard      |  | Interactive Tree   |  | Visualizer       |  | (Anom/Drv)|  |
|  +--------------------+  +--------------------+  +------------------+  +-----------+  |
+------------------------------------------^--------------------------------------------+
                                           |  JSON REST APIs (/api/*)
+------------------------------------------v--------------------------------------------+
|                  APPLICATION & CONTROL LAYER (Python / Flask Backend)                 |
|  +--------------------+  +--------------------+  +------------------+  +-----------+  |
|  | Flask Application  |  | Session State      |  | Operation Audit  |  | CSV/Excel |  |
|  | Server & Routing   |  | Store (Per-User)   |  | Trail Logger     |  | Ingestion |  |
|  +--------------------+  +--------------------+  +------------------+  +-----------+  |
+------------------------------------------^--------------------------------------------+
                                           |  Internal In-Memory Dispatch
+------------------------------------------v--------------------------------------------+
|                     CORE INTELLIGENCE LAYER (AI, Security & Local ML)                 |
|  +---------------------------+  +-------------------------+  +---------------------+  |
|  | Natural Language Engine   |  | SQL Safety & Validation |  | Local ML Engine     |  |
|  | - Google Gemini 2.0 Flash |  | - sqlparse AST Parser   |  | - Isolation Forest  |  |
|  | - Dynamic Schema Grounding|  | - DDL Permanent Block   |  | - Local Outlier Fac |  |
|  | - Multi-Turn Context      |  | - DML Dry-Run Preview   |  | - Random Forest Drv |  |
|  +---------------------------+  +-------------------------+  +---------------------+  |
+------------------------------------------^--------------------------------------------+
                                           |  SQLAlchemy Unified Engine Pools
+------------------------------------------v--------------------------------------------+
|                   DATABASE & PERSISTENCE LAYER (Multi-Engine Relational Data)         |
|  +-------------------+  +---------------------+  +--------------------+  +---------+  |
|  | SQLite            |  | MySQL / MariaDB     |  | PostgreSQL         |  | Pandas  |  |
|  | Embedded Files    |  | Enterprise RDBMS    |  | Object-Relational  |  | Memory  |  |
|  +-------------------+  +---------------------+  +--------------------+  +---------+  |
+---------------------------------------------------------------------------------------+
```

### 6.3 Block Diagram of System Flow

```
[ User Natural Language Query / ML Request ]
                    |
                    v
    [ Schema Introspection & Context Extraction ]
                    |
                    v
     [ LLM Prompt Synthesis (Gemini 2.0 Flash) ]
                    |
                    v
      [ AST Query Parsing (sqlparse Analysis) ]
                    |
                    v
           < Is Safety Valid? >
          /         |          \
   (DDL Detected)  (DML)     (SELECT)
        /           |            \
 [ Block & Alert ]  |             v
                    v       [ Execute Query via SQLAlchemy ]
           [ Dry-Run Preview ]    |
                    |             v
           [ Confirmation Modal]  [ Format Result JSON ]
                    |             |
           (If Confirmed)         v
                    |       [ Render Dynamic Table & Chart.js ]
                    +------------>+
```

---

# 7. RESULTS

### 7.1 Results Obtained

#### 7.1.1 User Interface Landing Page
The landing page showcases QueryMind's brand identity and mission: *"Fluid Database Intelligence: AI-Powered Database Assistant"*. It features a dark glassmorphism hero banner, minimalist typography, and an "Enter Workspace" call-to-action button routing to `/app`.

#### 7.1.2 Heterogeneous Data Source Connection Modal
The connection modal provides dedicated interfaces for SQLite file paths, MySQL TCP connections, PostgreSQL enterprise clusters, and CSV/Excel spreadsheet drag-and-drop uploads.

#### 7.1.3 Interactive Workspace and Schema Explorer
Upon connecting `sample_ecommerce.db`, the system immediately introspected five tables:
- `categories` (6 rows)
- `customers` (50 rows)
- `order_items` (331 rows)
- `orders` (120 rows)
- `products` (31 rows)

**Auto-Discovered Heuristic Insights:**
1. **Trend:** Electronics overwhelmingly dominates business revenue at over 6.1 million across 26 orders, generating more than 16 times the revenue of the next highest category.
2. **Warning:** Top-performing items like the MacBook Air M3 and Lenovo ThinkPad face imminent stockout risks, with remaining inventory levels already lower than total units sold.
3. **Opportunity:** Chennai represents a high-value customer cluster, with two of the top three overall spenders driving over 1 million in total completed orders.

#### 7.1.4 Machine Learning Feature Importance Drivers Analysis
Executed locally on the `customers` table explaining `id` using Random Forest:
- `registration_date`: **42.5%** (Dominant temporal driver)
- `email`: **18.1%** (High individual cardinality)
- `name`: **16.3%** (Customer personal name features)
- `city`: **13.5%** (Geographic customer clusters)
- `phone`: **8.4%** (Telecom circle codes)
- `status`: **1.3%** (Active vs. Inactive lifecycle state)

#### 7.1.5 Context-Aware Unsupervised Anomaly Detection
Executed locally on `order_items` (331 rows) combining Isolation Forest (200 trees) and Local Outlier Factor:
- **Total Rows:** 331
- **Normal Rows:** 270
- **Anomalies Found:** 61
- **Anomaly Rate:** 18.4%
- **Analyzed Numeric Features:** `order_id`, `product_id`, `quantity`, `unit_price`

**Top Outliers with Statistical Explanations:**
- Score 89 (Record 24): `unit_price is 3.2x higher than average (22202.71)`
- Score 87 (Record 42): `unit_price is 5.9x higher than average (22202.71)`
- Score 75 (Record 4): `Contextual Anomaly: Unusual combination of text, categories, and numbers`
- Score 75 (Record 308): `Contextual Anomaly: Extreme low-value transaction outlier`
- Score 74 (Record 66): `unit_price is 5.9x higher than average (22202.71)`
- Score 72 (Record 11): `Contextual Anomaly: High quantity-price interaction`

### 7.2 Test Cases Matrix

| TC ID | Test Scenario | Operator Action | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC01** | Server Boot | `python app.py` | Flask boots on 127.0.0.1:5000 | Server booted successfully | PASS |
| **TC02** | SQLite Connect | Provide SQLite path in modal | Connects & reflects 5 tables | Connected; schema loaded | PASS |
| **TC03** | MySQL Connect | Enter remote host/user/pass | TCP handshake & engine pool | Remote MySQL connected | PASS |
| **TC04** | Postgres Connect | Provide PostgreSQL creds | Authenticates via psycopg2 | PostgreSQL connected | PASS |
| **TC05** | CSV Ingestion | Upload diet.xlsx / CSV | Auto-creates relational table | Table created with rows | PASS |
| **TC06** | Schema Introspect | Expand schema tree in sidebar | Lists columns, types, counts | 5 tables correctly displayed | PASS |
| **TC07** | SELECT Query | Prompt: 'Show all categories' | Synthesizes SELECT; displays table | SELECT executed; 6 rows | PASS |
| **TC08** | Aggregation Query | Prompt: 'Top 5 products by sales' | Joins order_items; sorts DESC | Top 5 rendered in table/chart | PASS |
| **TC09** | DDL Prevention | Prompt: 'DROP TABLE customers' | AST blocks DDL; displays alert | Blocked: Destructive DDL | PASS |
| **TC10** | Injection Guard | Prompt: 'SELECT 1; DROP TABLE x' | Tokenizer blocks multi-stmt | Blocked: Multi-statement | PASS |
| **TC11** | DML Dry-Run | Prompt: 'Delete inactive users' | Dry-run preview affected rows | Modal prompts confirmation | PASS |
| **TC12** | DML Confirm | Click 'Confirm' in modal | Executes & commits transaction | Transaction committed | PASS |
| **TC13** | Conversational Turn | Follow-up: 'Now filter by city' | Applies WHERE clause to prior SQL | Prior SQL filtered correctly | PASS |
| **TC14** | ML Driver Analysis | Target id on customers | Random Forest computes MDI % | Ranked driver bars rendered | PASS |
| **TC15** | Anomaly Scan | Run on order_items | Ensemble isolates 61 outliers | Outlier table with reasons | PASS |
| **TC16** | Dynamic Chart.js | Query: 'Orders per category' | Renders interactive bar chart | Canvas bar chart rendered | PASS |

---

# 8. CONCLUSION & FUTURE SCOPE

### 8.1 Conclusion
This project successfully designed, implemented, and validated **QueryMind**, an intelligent, full-stack database intelligence platform that bridges natural language human inquiry with relational database execution, fortified by deterministic AST safety gates and localized machine learning diagnostics. By coupling Google Gemini 2.0 Flash with real-time SQLAlchemy schema reflection, the system achieves accurate zero-shot translation across SQLite, MySQL, and PostgreSQL environments.

Crucially, QueryMind resolves the primary barrier to adopting generative AI in enterprise databases—operational safety and data privacy. The deterministic `sqlparse` AST firewall completely prevents destructive DDL commands (DROP, ALTER, TRUNCATE), while the two-phase DML verification mechanism provides transactional preview before commit. Furthermore, the 100% on-premise Scikit-Learn diagnostic pipeline delivers multivariate anomaly detection (Isolation Forest + LOF) and Random Forest feature importance without transmitting proprietary records to external cloud services. Experimental validation demonstrates sub-second processing latencies, intuitive human-readable statistical explanations, and actionable business insight discovery, fulfilling all technical and research objectives.

### 8.2 Future Scope
1. **Multimodal Voice-Driven Querying:** Integrating client-side Web Speech API and localized Whisper automatic speech recognition to enable hands-free voice querying for mobile executives.
2. **Vector Database & Hybrid Semantic Search:** Incorporating vector stores (e.g., ChromaDB, Milvus) to support hybrid querying combining structured relational filters with unstructured document embeddings.
3. **Distributed Big Data Acceleration:** Extending the database manager to interface with Apache Spark SQL and Presto/Trino, allowing natural language queries to execute across multi-terabyte data lakes.
4. **Active Reinforcement Feedback Loops:** Implementing localized user feedback mechanisms (Reinforcement Learning from Human Feedback [RLHF]) to continuously fine-tune domain-specific prompt grounding.

---

# 9. REFERENCES

### 1) Journal and Conference Papers
[1] Yu, T., Zhang, R., Yang, K., Yasunaga, M., Wang, D., Li, Z., Ma, J., Li, I., Yao, Q., Roman, S., Zhang, Z., & Radev, D. (2018). Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-SQL task. *Proceedings of EMNLP 2018*, 3871–3881. https://doi.org/10.18653/v1/D18-1425  
[2] Zhong, V., Xiong, C., & Socher, R. (2017). Seq2SQL: Generating structured queries from natural language using reinforcement learning. *arXiv:1709.00103*. https://doi.org/10.48550/arXiv.1709.00103  
[3] Rajkumar, N., Hou, L. S., & Liang, P. (2022). Evaluating the text-to-SQL capabilities of large language models. *arXiv:2204.00498*. https://doi.org/10.48550/arXiv.2204.00498  
[4] Floratou, A., Agrawal, N., & Özcan, F. (2024). NL2SQL is solved! Why would anyone work on it anymore? *Proceedings of the VLDB Endowment*, 17(12), 4381–4388. https://doi.org/10.14778/3685800.3685880  
[5] Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. *Eighth IEEE International Conference on Data Mining*, 413–422. https://doi.org/10.1109/ICDM.2008.17  
[6] Breunig, M. M., Kriegel, H. P., Ng, R. T., & Sander, J. (2000). LOF: Identifying density-based local outliers. *ACM SIGMOD Record*, 29(2), 93–104. https://doi.org/10.1145/335191.335388  
[7] Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324  

### 2) Books and Authoritative Texts
[8] Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). *Database System Concepts* (7th ed.). McGraw-Hill Education.  
[9] Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.  

### 3) API & Framework Documentation
[10] Google Cloud. (2024). Gemini 2.0 Flash API Reference and Python SDK Documentation. https://ai.google.dev/gemini-api/docs  
[11] Pallets Projects. (2024). Flask Documentation (Version 3.0.x). https://flask.palletsprojects.com/  
[12] Bayer, M. (2024). SQLAlchemy 2.0 Unified Documentation and Architecture Reference. https://docs.sqlalchemy.org/en/20/  
[13] Scikit-Learn Developers. (2024). Scikit-Learn 1.4 User Guide: Ensemble Methods and Outlier Detection. https://scikit-learn.org/stable/  
[14] sqlparse Developers. (2024). sqlparse: Non-validating SQL parser for Python (Version 0.5.x). https://sqlparse.readthedocs.io/  
[15] Chart.js Documentation. (2024). Chart.js: Flexible JavaScript Charting for Designers & Developers (Version 4.4.x). https://www.chartjs.org/docs/latest/  

### 4) Technical Standards
[16] ISO/IEC 9075:2016. (2016). Information technology — Database languages — SQL (Parts 1 to 14). International Organization for Standardization (ISO).
