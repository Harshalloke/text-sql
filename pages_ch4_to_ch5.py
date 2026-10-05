# -*- coding: utf-8 -*-
"""
Chapters 4 and 5 Page Definitions
"""
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def add_ch4_literature_review(story, styles):
    # PAGE 14 (Internal 10): Chapter 4 Separator
    story.append(Spacer(1, 250))
    story.append(Paragraph("4. LITERATURE<br/>REVIEW", styles['ChapSep']))
    story.append(PageBreak())
    
    # PAGE 15 (Internal 11): Section 4.1 Literature Review (Items 1 to 4)
    story.append(Paragraph("Page No. 11", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("4.1 Literature Review for the Project:", styles['SecHead']))
    story.append(Paragraph(
        "<b>1. Natural Language Interfaces to Databases (NLIDBs):</b><br/>"
        "Early NLIDB architectures relied on rigid semantic grammars, pattern-matching rules, and intermediate logical representations (such as LUNAR and PRECISE). While historically foundational, these systems failed when presented with conversational ambiguity or slight deviations in user phrasing. The advent of neural sequence-to-sequence models (e.g., Seq2SQL, Pointer Networks) introduced probabilistic semantic parsing, demonstrating that deep neural networks can map unconstrained natural language queries into valid SQL syntax. These foundational works establish the feasibility of automated query synthesis while underscoring the necessity of modern neural language models to handle natural human linguistic variation. [1] [2]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Large Language Models in Structured Query Synthesis:</b><br/>"
        "The introduction of Transformer-based Large Language Models (LLMs) such as Google Gemini, Codex, and GPT-4 revolutionized code generation. Research by Rajkumar et al. and Floratou et al. demonstrates that pre-trained foundational models possess deep understanding of relational schemas, SQL dialect semantics, and query optimization rules. When provided with appropriate context, modern LLMs achieve high zero-shot and few-shot translation accuracy. In QueryMind, Google Gemini 2.0 Flash is selected for its balance of rapid inference latency, contextual reasoning, and structured output formatting. [3] [4]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Schema Grounding and In-Context Prompt Engineering:</b><br/>"
        "A critical limitation of raw LLM generation is 'hallucination'—the synthesis of queries referencing non-existent tables or invalid column names. Literature in in-context learning establishes that dynamically grounding the prompt with explicit schema catalogs, data types, and primary-foreign key relationships dramatically reduces hallucination rates. QueryMind employs dynamic runtime schema introspection via SQLAlchemy, extracting active schema structures and injecting them directly into system prompts, ensuring that every synthesized SQL query strictly conforms to physical database constraints. [5]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>4. Abstract Syntax Tree (AST) Parsing for Query Security:</b><br/>"
        "Allowing unconstrained generative models to execute queries directly against databases introduces severe security vulnerabilities, including destructive DDL commands and multi-statement injection attacks. Scholarly works on database firewalls emphasize lexical and AST-level query inspection over simple string regex filtering. By parsing queries into structured token trees using <code>sqlparse</code>, QueryMind deterministically identifies statement types, permanently eliminating catastrophic <code>DROP</code> or <code>ALTER</code> statements and isolating DML mutations for administrative verification. [6]",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGE 16 (Internal 12): Section 4.1 Literature Review (Items 5 to 8)
    story.append(Paragraph("Page No. 12", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>5. Conversational Semantic Parsing and Discourse State Tracking:</b><br/>"
        "Real-world data exploration is inherently iterative. Benchmarks such as SParC and CoSQL established standards for multi-turn semantic parsing, demonstrating that users rarely express complete analytical requests in a single isolated prompt. Rather, they ask follow-up questions ('Now filter by city', 'Show only top 5'). Academic literature highlights the need for dialogue state trackers that preserve conversational history and previously generated SQL ASTs. QueryMind implements a multi-turn conversation memory that injects prior turns into the prompt context, supporting seamless incremental query refinement. [7]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>6. Isolation Forest for Unsupervised Anomaly Detection:</b><br/>"
        "Proposed by Liu, Ting, and Zhou, Isolation Forest is an unsupervised tree-based ensemble designed specifically for multidimensional anomaly detection. Unlike distance-based or density-based algorithms that suffer from the 'curse of dimensionality' and high computational complexity, Isolation Forest explicitly isolates outliers by randomly partitioning feature spaces. Outliers require fewer recursive splits to isolate than normal data points, resulting in shorter average path lengths in isolation trees. QueryMind deploys an Isolation Forest ensemble (200 trees) to detect multivariate tabular outliers efficiently and deterministically. [8]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>7. Local Outlier Factor (LOF) for Density-Based Outlier Identification:</b><br/>"
        "Breunig et al. introduced Local Outlier Factor (LOF), which evaluates an object's anomaly score by comparing its local density to the density of its k-nearest neighbors. LOF excels at identifying 'local' outliers in datasets with varying density clusters where global isolation models might struggle. QueryMind combines Isolation Forest with Local Outlier Factor in an ensemble framework, ensuring robust detection across both global distribution anomalies and localized dense clusters. [9]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>8. Feature Importance and Driver Analysis using Random Forests:</b><br/>"
        "Breiman's seminal work on Random Forests establishes ensemble decision trees as powerful estimators of feature importance through Mean Decrease Impurity (MDI) and out-of-bag permutation metrics. In enterprise data analysis, identifying which independent features drive a key business outcome (such as customer churn, revenue, or transaction status) is essential. QueryMind utilizes Random Forest regressors and classifiers to compute normalized feature importance percentages, providing users with mathematically grounded drivers for any selected database column. [10]",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGE 17 (Internal 13): Section 4.1 Literature Review (Items 9 to 12)
    story.append(Paragraph("Page No. 13", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>9. Privacy-Preserving On-Premise Analytics vs. Cloud Offloading:</b><br/>"
        "Transmitting private enterprise databases to external cloud-hosted machine learning APIs introduces substantial regulatory compliance risks under GDPR, HIPAA, and data protection statutes. Literature on enterprise AI architectures highlights the critical importance of keeping diagnostic and analytical computations strictly within the local host boundary. QueryMind executes its entire machine learning diagnostic suite locally using Scikit-Learn, ensuring that sensitive customer records, financial figures, and operational data never traverse external networks. [11]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>10. Database Abstraction and Dialect Neutrality with SQLAlchemy:</b><br/>"
        "Relational database management systems vary significantly in their SQL syntax dialects, quotation conventions, function naming, and connection drivers. Bayer's SQLAlchemy architecture provides a unified Object-Relational Mapping (ORM) and Core abstraction layer that standardizes query compilation and schema introspection across disparate relational backends. QueryMind leverages SQLAlchemy to seamlessly interface with SQLite, MySQL, and PostgreSQL without dialect lock-in. [12]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>11. Modern Web Application Architectures and Dynamic Visualizations:</b><br/>"
        "Modern business intelligence platforms demand responsive, ergonomic client interfaces capable of rendering tabular data alongside reactive visual graphs. Research into human-computer interaction (HCI) shows that combining conversational chat with synchronized tabular and graphic views accelerates user comprehension. QueryMind integrates vanilla JavaScript with Chart.js, delivering high-performance, interactive bar, line, and pie visualizations directly within a dark glassmorphic dashboard. [13]",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>12. Automated Heuristic Profiling and Statistical Summarization:</b><br/>"
        "Studies in automated exploratory data analysis (AutoEDA) show that computing initial summary statistics (category aggregations, stock levels, geographic clustering) upon data ingestion reduces cognitive load on analysts. QueryMind incorporates an automated heuristic scanner that immediately computes revenue dominance trends, critical inventory warnings, and regional customer clusters upon database connection. [14]",
        styles['Body']
    ))
    story.append(PageBreak())

def add_ch5_research_methodology(story, styles):
    # PAGE 18 (Internal 14): Chapter 5 Separator
    story.append(Spacer(1, 250))
    story.append(Paragraph("5. RESEARCH<br/>METHODOLOGY", styles['ChapSep']))
    story.append(PageBreak())
    
    # PAGE 19 (Internal 15): Section 5.1 Agile Methodology (Items 1 to 3)
    story.append(Paragraph("Page No. 15", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("5.1 Agile Methodology:", styles['SecHead']))
    story.append(Paragraph(
        "The development of QueryMind was governed by the Agile software development methodology. Agile's iterative lifecycle, continuous feedback loops, and rapid prototyping capabilities make it uniquely suited for a multi-disciplinary system that integrates modern generative AI, deterministic AST security compilers, local machine learning pipelines, and responsive web user interfaces.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>1. Agile Dual-Purpose Framework:</b><br/>"
        "i. <i>Technical Agility:</i> Facilitates rapid architectural adaptation to evolving LLM API response formats, token context windows, database dialect quirks, and Scikit-Learn memory constraints.<br/>"
        "ii. <i>Research Agility:</i> Enables rapid empirical validation of semantic translation accuracy, AST security boundary robustness, and anomaly detection precision against real-world relational schemas.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Requirement Analysis &amp; Feasibility Study:</b><br/>"
        "i. <i>Functional Requirements:</i> Natural language query translation; multi-database connectivity (SQLite, MySQL, PostgreSQL); CSV/Excel dynamic ingestion; AST security validation; guarded two-phase DML execution; local Isolation Forest + LOF anomaly detection; Random Forest feature driver analysis; and automated heuristic insight discovery.<br/>"
        "ii. <i>Non-Functional Requirements:</i> Sub-2.5-second end-to-end query synthesis latency; 100% interception of destructive DDL commands; zero cloud data transmission during ML execution; memory usage under 250 MB; responsive cross-platform web UI.<br/>"
        "iii. <i>Feasibility Checks:</i> Evaluated Google Gemini 2.0 Flash token latency, SQLAlchemy dialect compatibility, Scikit-Learn in-memory execution throughput, and browser DOM rendering limits.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Sprint Breakdown and Iterative Milestones:</b><br/>"
        "• <i>Sprint 1 (Architecture &amp; Ingestion):</i> Core Flask micro-service setup; SQLAlchemy connection manager for SQLite, MySQL, and PostgreSQL; Pandas CSV/Excel ingestion pipeline.<br/>"
        "• <i>Sprint 2 (Natural Language Engine):</i> Google Gemini 2.0 Flash integration; dynamic schema introspection; prompt grounding; JSON structured response parsing.<br/>"
        "• <i>Sprint 3 (Security Firewall):</i> <code>sqlparse</code> AST parser implementation; DDL blacklist; multi-statement injection blocking; DML dry-run transaction row-count preview.<br/>"
        "• <i>Sprint 4 (Local ML Diagnostic Suite):</i> Column classification pipeline; Isolation Forest + LOF ensemble; statistical reason generator; Random Forest feature drivers.<br/>"
        "• <i>Sprint 5 (Presentation &amp; Visual Analytics):</i> Dark glassmorphic UI; real-time chat; schema explorer tree; Chart.js dynamic graphing; diagnostic modals.<br/>"
        "• <i>Sprint 6 (Testing &amp; Integration):</i> Unit testing, end-to-end load benchmarks, security penetration validation, and user acceptance testing.",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGE 20 (Internal 16): Section 5.1 Agile Methodology (Items 4 to 6)
    story.append(Paragraph("Page No. 16", styles['PNum']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>4. Iterative Development &amp; Continuous Integration:</b><br/>"
        "i. <i>Short Development Cycles:</i> Each sprint was structured in 1-to-2 week cycles, delivering modular, independently testable software components.<br/>"
        "ii. <i>Version Control:</i> Managed via Git and GitHub repository branches, enforcing feature-branch isolation and granular commit logs.<br/>"
        "iii. <i>Modular Unit &amp; Integration Testing:</i> Each component was rigorously verified prior to integration:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a. <i>Database Unit Tests:</i> Validated connection pooling, dialect-specific query execution, and transactional rollback stability.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b. <i>LLM Parser Unit Tests:</i> Evaluated SQL syntax validity, schema adherence, and multi-turn context retention across test queries.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c. <i>Security AST Unit Tests:</i> Verified that 100% of injected DDL statements (DROP, ALTER, TRUNCATE) and multi-statement queries were intercepted and blocked.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d. <i>Machine Learning Unit Tests:</i> Validated column classification accuracy, preprocessing pipeline robustness, and outlier scoring repeatability on benchmark tables.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e. <i>API Integration Tests:</i> Confirmed REST endpoint contract integrity, session state persistence, and error response formatting.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>5. Validation &amp; Empirical Testing:</b><br/>"
        "i. <i>Multi-Database Testing:</i> Deployed and validated against diverse relational engines: local SQLite files, remote MySQL instances, and PostgreSQL databases.<br/>"
        "ii. <i>Security Penetration Testing:</i> Executed simulated adversarial prompts attempting prompt injections, privilege escalations, and silent data destruction to confirm AST firewall efficacy.<br/>"
        "iii. <i>Machine Learning Benchmarks:</i> Tested the anomaly detection and driver analysis engines on multi-table datasets (331+ records) to evaluate precision, recall, and processing latency under 500 ms.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>6. Deployment &amp; User Acceptance Testing (UAT):</b><br/>"
        "i. Deployed the application locally and conducted hands-on evaluation sessions with target non-technical users and technical peer reviewers.<br/>"
        "ii. Collected qualitative and quantitative usability feedback regarding query accuracy, modal interaction clarity, chart readability, and insight usefulness.<br/>"
        "iii. Integrated stakeholder feedback into subsequent UI refinement cycles, enhancing the modal workflow and explanation verbosity.",
        styles['Body']
    ))
    story.append(PageBreak())
    
    # PAGE 21 (Internal 17): Section 5.1 Agile Methodology (Advantages in QueryMind)
    story.append(Paragraph("Page No. 17", styles['PNum']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>7. Advantages of Agile Methodology in QueryMind:</b>", styles['SecHead']))
    story.append(Paragraph(
        "Adopting the Agile development methodology provided essential architectural and operational advantages throughout the lifecycle of the QueryMind project:",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>1. Early Functional Prototyping:</b> Developing functional prototypes in initial sprints enabled early verification of LLM prompt grounding and SQLAlchemy schema extraction before implementing complex security gates or machine learning pipelines.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Rapid Adaptation to Generative AI Nuances:</b> LLM behavior and prompt sensitivities required continuous calibration. Agile's short iterations allowed prompt templates, schema serialization formats, and few-shot examples to be refined dynamically based on real query synthesis errors.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Decoupled Parallel Development:</b> The modular separation of frontend UI, Flask REST API, security validation gate, and local Scikit-Learn pipelines allowed independent, concurrent development, significantly accelerating delivery schedules.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>4. Continuous Risk Mitigation:</b> High-risk components—particularly the prevention of accidental database deletion via DDL/DML—were isolated, validated, and stress-tested in early sprints, ensuring the security firewall was impenetrable before opening queries to end users.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>5. Direct User-Centric Evolution:</b> Iterative user testing highlighted the necessity of providing human-readable statistical explanations for anomalies (e.g., 'unit_price is 3.2x higher than average') rather than raw outlier scores, directly driving the implementation of the explanation generator in Sprint 4.",
        styles['Body']
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "In conclusion, the Agile methodology ensured that QueryMind matured systematically from conceptual architecture to a fully hardened, feature-complete, and rigorously tested research project.",
        styles['Body']
    ))
    story.append(PageBreak())

print("Chapters 4 and 5 defined successfully.")
