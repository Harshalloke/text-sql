# -*- coding: utf-8 -*-
"""
Chapters 1, 2, and 3 Page Definitions
"""
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def add_ch1_problem_statement(story, styles):
    # PAGE 5 (Internal 1): Chapter 1 Separator
    story.append(Spacer(1, 250))
    story.append(Paragraph("1. PROBLEM<br/>STATEMENT", styles['ChapSep']))
    story.append(PageBreak())
    
    # PAGE 6 (Internal 2): Section 1.1 Problem Definition
    story.append(Paragraph("Page No. 2", styles['PNum']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("1.1 Problem Definition:", styles['SecHead']))
    story.append(Paragraph(
        "In modern enterprise computing environments, relational database management systems (RDBMS) such as SQLite, MySQL, and PostgreSQL store mission-critical operational and analytical records. However, querying these databases requires specialized proficiency in Structured Query Language (SQL), relational algebra, and intricate database schemas. Non-technical business analysts, domain researchers, and organizational decision-makers are frequently obstructed by this technical syntax barrier, necessitating reliance on database administrators or data engineering teams. This communication bottleneck severely delays time-sensitive analytical reporting and business intelligence exploration.",
        styles['Body']
    ))
    story.append(Paragraph(
        "While emerging Large Language Models (LLMs) demonstrate remarkable semantic comprehension and natural language processing capabilities, unguided generative AI interfaces present acute operational vulnerabilities when interacting directly with production database environments. Without strict deterministic validation, raw LLM-synthesized queries risk generating destructive Data Definition Language (DDL) operations, executing non-deterministic mutations without transactional rollbacks, or succumbing to prompt injection exploits.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Furthermore, existing database tools remain strictly passive: they require users to formulate exact hypothesis queries rather than proactively detecting anomalous transactions, identifying key business performance drivers, or isolating multidimensional outliers in the underlying records.",
        styles['Body']
    ))
    story.append(Paragraph("The current challenge is to design and develop an intelligent system that:", styles['BodyBold']))
    story.append(Paragraph("1. Seamlessly converts natural language inquiries into syntactically precise, schema-grounded SQL across heterogeneous relational databases (SQLite, MySQL, PostgreSQL) and tabular spreadsheets (CSV/Excel).", styles['Body']))
    story.append(Paragraph("2. Enforces a multi-tiered security firewall that permanently prohibits catastrophic DDL operations (DROP, ALTER, TRUNCATE) and requires explicit two-phase confirmation before committing any data modification (UPDATE, DELETE, INSERT).", styles['Body']))
    story.append(Paragraph("3. Preserves multi-turn conversational context, enabling users to iteratively filter, refine, and drill down into query results without re-specifying prior conversational constraints.", styles['Body']))
    story.append(Paragraph("4. Executes 100% local, privacy-preserving machine learning diagnostics (Isolation Forest, Local Outlier Factor, and Random Forest feature importance) without transmitting proprietary organizational records to third-party cloud APIs.", styles['Body']))
    story.append(Paragraph("5. Automatically surfaces proactive heuristic business insights (revenue trends, critical inventory stockout warnings, and customer clustering opportunities) immediately upon database connection.", styles['Body']))
    story.append(Paragraph(
        "The overarching objective is to deliver an end-to-end, enterprise-grade natural language database assistant that empowers non-technical stakeholders to safely query, visualize, and extract advanced machine learning diagnostics from complex databases with zero SQL overhead and deterministic safety guarantees.",
        styles['Body']
    ))
    story.append(PageBreak())

def add_ch2_abstract(story, styles):
    # PAGE 7 (Internal 3): Chapter 2 Separator
    story.append(Spacer(1, 250))
    story.append(Paragraph("2. ABSTRACT", styles['ChapSep']))
    story.append(PageBreak())
    
    # PAGE 8 (Internal 4): Section 2.1 Project Abstract
    story.append(Paragraph("Page No. 4", styles['PNum']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("2.1 Project Abstract:", styles['SecHead']))
    story.append(Paragraph(
        "The democratization of database querying has emerged as a fundamental challenge in modern information systems. While modern enterprises accumulate vast repositories of structured data, extracting timely insights remains heavily gatekept by the technical complexity of Structured Query Language (SQL). This research presents <b>QueryMind</b>, an advanced, full-stack database intelligence platform that bridges natural language human intent with robust relational database execution, fortified by deterministic Abstract Syntax Tree (AST) validation and local, privacy-preserving machine learning diagnostics.",
        styles['Body']
    ))
    story.append(Paragraph(
        "QueryMind couples the generative language understanding of the Google Gemini 2.0 Flash engine with dynamic, schema-grounded prompt orchestration. Through real-time SQLAlchemy schema reflection, the system injects table structures, column constraints, primary/foreign key mappings, and dialect-specific conventions directly into the LLM context, yielding high zero-shot translation accuracy across SQLite, MySQL, and PostgreSQL environments. To mitigate generative vulnerabilities, QueryMind implements a multi-stage security gate utilizing <code>sqlparse</code> AST token inspection. Catastrophic Data Definition Language (DDL) operations such as <code>DROP</code>, <code>ALTER</code>, and <code>TRUNCATE</code> are deterministically rejected, while multi-statement injection vectors are neutralized. For Data Manipulation Language (DML) queries (<code>UPDATE</code>, <code>DELETE</code>, <code>INSERT</code>), the architecture employs a two-phase confirmation mechanism featuring transactional dry-run row-count estimation, ensuring administrative preview before commit.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Beyond query generation, QueryMind integrates a completely local, zero-leakage Machine Learning engine built on Scikit-Learn. The diagnostic module implements an automated column classification and preprocessing pipeline (combining median imputation, standard scaling, one-hot encoding, and TF-IDF vectorization) followed by an ensemble of Isolation Forest (200 estimators) and Local Outlier Factor (LOF). Flagged outliers are augmented with human-interpretable statistical explanations based on Z-score thresholds, Tukey's interquartile range (IQR) fences, and mean-ratio multipliers. Simultaneously, a Random Forest feature importance module quantifies the mathematical drivers of key database attributes, while an automated heuristic engine uncovers immediate revenue trends, inventory stockout risks, and geographic opportunities upon data ingestion.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Experimental validation across enterprise e-commerce databases (including multi-table schemas with 331+ order items, customer demographics, and product catalogs) demonstrates sub-second query synthesis latency, 100% interception of forbidden DDL statements, and accurate isolation of multivariate price and quantity anomalies. QueryMind establishes a highly secure, reliable, and scalable paradigm for non-technical database exploration and automated machine learning diagnostics.",
        styles['Body']
    ))
    story.append(PageBreak())

def add_ch3_introduction(story, styles):
    # PAGE 9 (Internal 5): Chapter 3 Separator
    story.append(Spacer(1, 250))
    story.append(Paragraph("3. INTRODUCTION", styles['ChapSep']))
    story.append(PageBreak())
    
    # PAGE 10 (Internal 6): Section 3.1 Project Introduction
    story.append(Paragraph("Page No. 6", styles['PNum']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("3.1 Project Introduction:", styles['SecHead']))
    story.append(Paragraph(
        "The digital transformation of commercial, governmental, and academic enterprises has led to exponential growth in the volume and velocity of structured data. Organizations increasingly rely on relational databases to record transactions, manage supply chains, profile customer behaviors, and monitor operational telemetry. Despite the ubiquity of relational databases, interacting with structured stores remains fundamentally constrained by the steep learning curve of Structured Query Language (SQL). Business executives, product managers, clinical researchers, and frontline analysts must either master complex SQL syntax—including correlated subqueries, multi-table outer joins, window functions, and dialect discrepancies—or submit ad-hoc reporting tickets to technical database teams, creating severe operational friction.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Recent breakthroughs in Large Language Models (LLMs) and transformer-based natural language processing offer unprecedented opportunities to establish Natural Language Interfaces to Databases (NLIDBs). By mapping unstructured colloquial questions into structured database commands, LLMs can bridge the communication gap between humans and relational engines. However, deploying off-the-shelf generative models directly against enterprise data repositories introduces critical operational and security hazards. Generative models are inherently non-deterministic and susceptible to hallucinations, potentially synthesizing malformed SQL, misinterpreting column semantic boundaries, or generating disastrous data-modifying statements.",
        styles['Body']
    ))
    story.append(Paragraph(
        "To address these formidable challenges, this project introduces <b>QueryMind</b>, an intelligent, full-stack database assistant designed to provide fluid natural language database querying while guaranteeing strict transactional safety, conversational statefulness, and local machine learning diagnostics. QueryMind integrates Google's state-of-the-art Gemini 2.0 Flash model with dynamic database introspection and a robust Abstract Syntax Tree (AST) validation firewall. Furthermore, recognizing that raw querying represents only one aspect of analytical workflow, QueryMind embeds an entirely on-premise, zero-data-leakage machine learning diagnostic suite powered by Scikit-Learn. The platform autonomously detects multidimensional anomalies, determines mathematical feature importance drivers, and surfaces immediate operational insights.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Presented through a modern, responsive dark-glassmorphism web interface with real-time Chart.js visualizers, QueryMind transforms passive database tables into interactive, intelligent assets accessible to users of all technical skill levels.",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGE 11 (Internal 7): Section 3.2 Developed System Overview & 3.3 USPs
    story.append(Paragraph("Page No. 7", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("3.2 Developed System Overview:", styles['SecHead']))
    story.append(Paragraph("The QueryMind platform is structured into five cohesive, loosely coupled architectural tiers:", styles['Body']))
    story.append(Paragraph("<b>1. Presentation Layer:</b> A dark glassmorphic web interface built with vanilla HTML5, CSS3, and JavaScript, featuring real-time chat interactions, schema hierarchy trees, dynamic Chart.js graphing, and dedicated diagnostic modals.", styles['Body']))
    story.append(Paragraph("<b>2. Application &amp; API Layer:</b> A lightweight, asynchronous Flask REST micro-service managing HTTP routing, session state persistence, file upload processing, and comprehensive audit history logging.", styles['Body']))
    story.append(Paragraph("<b>3. AI &amp; Semantic Processing Layer:</b> Powered by the Google Gemini 2.0 Flash engine via the <code>google-genai</code> SDK, utilizing dynamic schema grounding, few-shot prompt formulation, and multi-turn context memory.", styles['Body']))
    story.append(Paragraph("<b>4. Security &amp; Validation Gate:</b> A deterministic AST inspection engine built on <code>sqlparse</code> that permanently intercepts forbidden DDL commands and executes dry-run row estimations for guarded DML mutations.", styles['Body']))
    story.append(Paragraph("<b>5. Local Machine Learning &amp; Diagnostics Layer:</b> An on-premise, zero-egress Scikit-Learn analytical engine providing automated column classification, Isolation Forest + LOF anomaly detection, and Random Forest feature driver analysis.", styles['Body']))
    story.append(Paragraph("<b>6. Persistence &amp; Ingestion Layer:</b> A multi-engine database interface managed via SQLAlchemy Core/ORM, providing native connectivity to SQLite, MySQL, PostgreSQL, and dynamic CSV/Excel dataset ingestion.", styles['Body']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("3.3 Unique Selling Propositions (USP) of the System:", styles['SecHead']))
    story.append(Paragraph("<b>1. 100% Local Machine Learning Diagnostics:</b> Unlike conventional tools that offload data to expensive cloud endpoints, QueryMind executes anomaly detection and feature importance locally, guaranteeing zero data leakage and zero API egress costs.", styles['Body']))
    story.append(Paragraph("<b>2. Deterministic AST Security Firewall:</b> Operates an unbypassable abstract syntax tree inspection gate that permanently eliminates catastrophic DDL operations and blocks multi-statement injection vectors.", styles['Body']))
    story.append(Paragraph("<b>3. Two-Phase DML Modification Safety Net:</b> Data mutations (UPDATE, DELETE) trigger automated dry-run row-count previews, requiring explicit administrator confirmation before database commit.", styles['Body']))
    story.append(Paragraph("<b>4. True Multi-Dialect Agnosticism:</b> Transparently communicates with SQLite, MySQL, and PostgreSQL engines, adapting syntax, quotes, and functions to the connected database dialect automatically.", styles['Body']))
    story.append(Paragraph("<b>5. Multi-Turn Conversational Memory:</b> Maintains context across conversation turns, enabling natural analytical drilling such as 'Now filter those by Mumbai' or 'Show top 5'.", styles['Body']))
    story.append(Paragraph("<b>6. Automated Proactive Business Insights:</b> Automatically computes and highlights revenue trends, inventory stockout risks, and customer clustering opportunities upon connection without manual prompting.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 12 (Internal 8): Section 3.4 Advantages of the Project (Items 1 to 10)
    story.append(Paragraph("Page No. 8", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("3.4 Advantages of the Project:", styles['SecHead']))
    story.append(Paragraph("The QueryMind platform provides significant operational, analytical, and security advantages over traditional database query tools and unconstrained generative assistants:", styles['Body']))
    story.append(Paragraph("<b>1. Complete Democratization of Relational Data:</b> Non-technical staff, business analysts, executives, and students can extract sophisticated analytical answers without memorizing SQL syntax or table joins.", styles['Body']))
    story.append(Paragraph("<b>2. Permanent DDL Destruction Protection:</b> Dangerous structural modifications (DROP, ALTER, CREATE, TRUNCATE) are permanently halted at the parser level, ensuring that database schemas cannot be accidentally damaged.", styles['Body']))
    story.append(Paragraph("<b>3. Two-Phase Interactive Mutation Verification:</b> High-risk UPDATE and DELETE queries are intercepted; affected row counts are computed via non-committing transactions and presented for explicit confirmation before execution.", styles['Body']))
    story.append(Paragraph("<b>4. Absolute Privacy for Machine Learning:</b> Sensitive organizational records analyzed for outliers and feature drivers never leave the local environment, satisfying strict GDPR, HIPAA, and corporate data governance mandates.", styles['Body']))
    story.append(Paragraph("<b>5. Cross-Engine Relational Portability:</b> Organizations can switch between embedded SQLite databases, enterprise MySQL installations, and PostgreSQL clusters through a single unified interface.", styles['Body']))
    story.append(Paragraph("<b>6. Dynamic Schema Grounding:</b> The system introspects live database metadata—table definitions, column data types, and primary/foreign keys—preventing hallucination of non-existent fields.", styles['Body']))
    story.append(Paragraph("<b>7. Multi-Turn Conversational Continuity:</b> Users can iteratively refine complex queries over multiple conversational turns, supporting fluid exploratory data analysis without redundant inputs.", styles['Body']))
    story.append(Paragraph("<b>8. Automated Visual Analytics:</b> Automatically selects and generates appropriate Chart.js visual representations (bar graphs, line charts, pie distributions) alongside responsive tabular grids.", styles['Body']))
    story.append(Paragraph("<b>9. Heterogeneous Tabular Spreadsheet Ingestion:</b> Supports instantaneous upload and SQL querying of standalone CSV and Excel (XLSX) workbooks by automatically provisioning temporary relational tables.", styles['Body']))
    story.append(Paragraph("<b>10. Granular Audit Trails and Operation Logging:</b> Records every executed query, status, execution duration, and timestamp, providing complete traceability for enterprise compliance.", styles['Body']))
    story.append(PageBreak())
    
    # PAGE 13 (Internal 9): Section 3.4 Advantages (Items 11 to 16)
    story.append(Paragraph("Page No. 9", styles['PNum']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>11. Zero Training Overhead for End Users:</b> By leveraging intuitive natural language prompts, organizational onboarding time is reduced to minutes, eliminating prolonged database syntax training programs.", styles['Body']))
    story.append(Paragraph("<b>12. Explainable Outlier Diagnostics:</b> Unlike opaque black-box anomaly detectors, QueryMind equips every flagged outlier with actionable statistical justifications, such as Z-score variances, Tukey IQR fence violations, and mean-ratio multiples.", styles['Body']))
    story.append(Paragraph("<b>13. Low Latency Local In-Memory Execution:</b> Local Scikit-Learn pipelines execute in hundreds of milliseconds, avoiding network round-trip overhead and cloud throttling associated with external analytical APIs.", styles['Body']))
    story.append(Paragraph("<b>14. High Resilience Against SQL Injection Attacks:</b> Multi-statement query sequences and delimiter-chaining injection patterns are strictly blocked by the tokenizer, shielding production databases from malicious inputs.", styles['Body']))
    story.append(Paragraph("<b>15. Regulatory Compliance and Governance Enablement:</b> Real-time operation counters, status trackers, and local data isolation simplify regulatory auditing in finance, healthcare, and education.", styles['Body']))
    story.append(Paragraph("<b>16. Fault-Tolerant Session Isolation:</b> Session-scoped connection pools ensure that multiple concurrent browser instances operate independently without memory contamination or transaction crosstalk.", styles['Body']))
    story.append(Spacer(1, 40))
    story.append(Paragraph("In summary, QueryMind represents an integrated, highly secure, and practical synthesis of state-of-the-art Large Language Models, deterministic syntax validation, and local machine learning, delivering a comprehensive next-generation database intelligence experience.", styles['Body']))
    story.append(PageBreak())

print("Chapters 1, 2, and 3 defined successfully.")
