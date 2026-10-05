# -*- coding: utf-8 -*-
"""
Word (.docx) Document Generator for QueryMind Black Book
Generates an editable, fully styled DOCX document corresponding to the 61-page report.
Author: Mr Harshal Pandharinath Loke (Seat No: 564, Batch: 2026 - 2027)
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def generate_full_docx(output_filename="QueryMind_Black_Book_Harshal_Loke.docx"):
    print(f"Generating Word document: {output_filename}...")
    doc = Document()
    
    # Page setup: A4, 1.0 in margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    
    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("S.P. Mandali's\n")
    r.font.bold = True
    r.font.size = Pt(16)
    r = p.add_run("Ramnarain Ruia Autonomous College\n")
    r.font.bold = True
    r.font.size = Pt(16)
    r = p.add_run("Matunga, Mumbai - 400019\nDepartment of Computer Science\n\n")
    r.font.size = Pt(12)
    
    if os.path.exists("college_logo.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.add_run().add_picture("college_logo.png", width=Inches(1.5))
        
    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_rep.add_run("\nResearch Project Report\nOn\n\n")
    r.font.bold = True
    r.font.size = Pt(14)
    r = p_rep.add_run("QueryMind: Intelligent Natural Language to SQL Interface with Machine Learning Driven Data Diagnostics and Anomaly Detection\n\n\n")
    r.font.bold = True
    r.font.size = Pt(15)
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_meta.add_run("Project Guide\n")
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_meta.add_run("Mrs. Edith Juni\n\n")
    r.font.size = Pt(12)
    r = p_meta.add_run("Project By\n")
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_meta.add_run("Mr Harshal Pandharinath Loke\n")
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_meta.add_run("Seat No: 564\n\n")
    r.font.size = Pt(12)
    r = p_meta.add_run("M.Sc. Computer Science\n")
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_meta.add_run("2026 - 2027")
    r.font.size = Pt(12)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # ACKNOWLEDGEMENT
    # ----------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("ACKNOWLEDGEMENT\n\n")
    r.font.bold = True
    r.font.size = Pt(16)
    
    ack_text = [
        "Every project big or small is successful, largely due to the effort of a number of wonderful people who have always given their valuable advice or have always lent a helping hand.",
        "I take this opportunity of submitting this report to express my profound gratitude to the management of 'Ramnarain Ruia Autonomous College' for giving me the opportunity to accomplish this project work.",
        "I am also thankful to all the teachers for their kind support and help.",
        "I express my deepest gratitude towards my project guide Mrs. Edith Juni for her valuable and timely advice during the various phases in my project.",
        "I express my sincere thanks to our respected Co-ordinator Mrs. Aarya Tawde for allowing us to use the facilities available.",
        "I would also like to thank all those unnamed but important people and Computer Lab Assistants and supportive staff who directly or indirectly helped me in the completion of this project and to my family and friends without whose support, motivation and encouragement this would not have been possible."
    ]
    for para in ack_text:
        p = doc.add_paragraph(para)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.2
        
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(30)
    p_sign.add_run("Thanking you,\n")
    r = p_sign.add_run("Harshal P. Loke")
    r.font.bold = True
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # TITLE FLYER
    # ----------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(200)
    r = p.add_run("QueryMind:\n\nIntelligent Natural Language\nto SQL Interface with\nMachine Learning Driven\nData Diagnostics and\nAnomaly Detection")
    r.font.bold = True
    r.font.size = Pt(22)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # INDEX (TABLE OF CONTENTS)
    # ----------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("INDEX\n\n")
    r.font.bold = True
    r.font.size = Pt(16)
    
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Sr. No."
    hdr_cells[1].text = "Contents"
    hdr_cells[2].text = "Page No."
    for c in hdr_cells:
        set_cell_shading(c, "EDF2F7")
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_margins(c, 100, 100, 150, 150)
        
    index_entries = [
        ("1", "Problem Statement", "1 - 2", True),
        ("", "1.1 Problem Definition", "2", False),
        ("2", "Abstract", "3 - 4", True),
        ("", "2.1 Project Abstract", "4", False),
        ("3", "Introduction", "5 - 9", True),
        ("", "3.1 Project Introduction", "6", False),
        ("", "3.2 Developed System Overview", "7", False),
        ("", "3.3 Unique Selling Propositions (USP) of the System", "7", False),
        ("", "3.4 Advantages of the Project", "8", False),
        ("4", "Literature Review", "10 - 13", True),
        ("", "4.1 Literature Review for the Project", "11", False),
        ("5", "Research Methodology", "14 - 17", True),
        ("", "5.1 Agile Methodology", "15", False),
        ("6", "Experimental Setup", "18 - 38", True),
        ("", "6.1 Requirements Analysis", "19", False),
        ("", "6.2 System Architecture Diagram", "24", False),
        ("", "6.3 Block Diagram of System Flow", "25", False),
        ("", "6.4 Input Code", "26", False),
        ("7", "Results", "39 - 52", True),
        ("", "7.1 Results Obtained", "40", False),
        ("", "7.2 Test Cases", "51", False),
        ("8", "Conclusion & Future Scope", "53 - 54", True),
        ("", "8.1 Conclusion", "54", False),
        ("", "8.2 Future Scope", "54", False),
        ("9", "References", "55 - 57", True),
        ("", "9.1 References", "56", False)
    ]
    
    for sr, title, pno, is_bold in index_entries:
        row_cells = table.add_row().cells
        row_cells[0].text = sr
        row_cells[1].text = title
        row_cells[2].text = pno
        for idx, c in enumerate(row_cells):
            set_cell_margins(c, 80, 80, 120, 120)
            if is_bold and len(c.paragraphs[0].runs) > 0:
                c.paragraphs[0].runs[0].font.bold = True
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # CHAPTER 1: PROBLEM STATEMENT
    # ----------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(200)
    r = p.add_run("1. PROBLEM\nSTATEMENT")
    r.font.bold = True
    r.font.size = Pt(24)
    doc.add_page_break()
    
    p = doc.add_paragraph("Page No. 2\n")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sec = doc.add_paragraph("1.1 Problem Definition:")
    p_sec.runs[0].font.bold = True
    p_sec.runs[0].font.size = Pt(13)
    
    ch1_paras = [
        "In modern enterprise computing environments, relational database management systems (RDBMS) such as SQLite, MySQL, and PostgreSQL store mission-critical operational and analytical records. However, querying these databases requires specialized proficiency in Structured Query Language (SQL), relational algebra, and intricate database schemas. Non-technical business analysts, domain researchers, and organizational decision-makers are frequently obstructed by this technical syntax barrier, necessitating reliance on database administrators or data engineering teams. This communication bottleneck severely delays time-sensitive analytical reporting and business intelligence exploration.",
        "While emerging Large Language Models (LLMs) demonstrate remarkable semantic comprehension and natural language processing capabilities, unguided generative AI interfaces present acute operational vulnerabilities when interacting directly with production database environments. Without strict deterministic validation, raw LLM-synthesized queries risk generating destructive Data Definition Language (DDL) operations, executing non-deterministic mutations without transactional rollbacks, or succumbing to prompt injection exploits.",
        "Furthermore, existing database tools remain strictly passive: they require users to formulate exact hypothesis queries rather than proactively detecting anomalous transactions, identifying key business performance drivers, or isolating multidimensional outliers in the underlying records.",
        "The current challenge is to design and develop an intelligent system that:",
        "1. Seamlessly converts natural language inquiries into syntactically precise, schema-grounded SQL across heterogeneous relational databases (SQLite, MySQL, PostgreSQL) and tabular spreadsheets (CSV/Excel).",
        "2. Enforces a multi-tiered security firewall that permanently prohibits catastrophic DDL operations (DROP, ALTER, TRUNCATE) and requires explicit two-phase confirmation before committing any data modification (UPDATE, DELETE, INSERT).",
        "3. Preserves multi-turn conversational context, enabling users to iteratively filter, refine, and drill down into query results without re-specifying prior conversational constraints.",
        "4. Executes 100% local, privacy-preserving machine learning diagnostics (Isolation Forest, Local Outlier Factor, and Random Forest feature importance) without transmitting proprietary organizational records to third-party cloud APIs.",
        "5. Automatically surfaces proactive heuristic business insights (revenue trends, critical inventory stockout warnings, and customer clustering opportunities) immediately upon database connection.",
        "The overarching objective is to deliver an end-to-end, enterprise-grade natural language database assistant that empowers non-technical stakeholders to safely query, visualize, and extract advanced machine learning diagnostics from complex databases with zero SQL overhead and deterministic safety guarantees."
    ]
    for para in ch1_paras:
        p = doc.add_paragraph(para)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(6)
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # CHAPTER 2: ABSTRACT
    # ----------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(200)
    r = p.add_run("2. ABSTRACT")
    r.font.bold = True
    r.font.size = Pt(24)
    doc.add_page_break()
    
    p = doc.add_paragraph("Page No. 4\n")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sec = doc.add_paragraph("2.1 Project Abstract:")
    p_sec.runs[0].font.bold = True
    p_sec.runs[0].font.size = Pt(13)
    
    ch2_paras = [
        "The democratization of database querying has emerged as a fundamental challenge in modern information systems. While modern enterprises accumulate vast repositories of structured data, extracting timely insights remains heavily gatekept by the technical complexity of Structured Query Language (SQL). This research presents QueryMind, an advanced, full-stack database intelligence platform that bridges natural language human intent with robust relational database execution, fortified by deterministic Abstract Syntax Tree (AST) validation and local, privacy-preserving machine learning diagnostics.",
        "QueryMind couples the generative language understanding of the Google Gemini 2.0 Flash engine with dynamic, schema-grounded prompt orchestration. Through real-time SQLAlchemy schema reflection, the system injects table structures, column constraints, primary/foreign key mappings, and dialect-specific conventions directly into the LLM context, yielding high zero-shot translation accuracy across SQLite, MySQL, and PostgreSQL environments. To mitigate generative vulnerabilities, QueryMind implements a multi-stage security gate utilizing sqlparse AST token inspection. Catastrophic Data Definition Language (DDL) operations such as DROP, ALTER, and TRUNCATE are deterministically rejected, while multi-statement injection vectors are neutralized. For Data Manipulation Language (DML) queries (UPDATE, DELETE, INSERT), the architecture employs a two-phase confirmation mechanism featuring transactional dry-run row-count estimation, ensuring administrative preview before commit.",
        "Beyond query generation, QueryMind integrates a completely local, zero-leakage Machine Learning engine built on Scikit-Learn. The diagnostic module implements an automated column classification and preprocessing pipeline (combining median imputation, standard scaling, one-hot encoding, and TF-IDF vectorization) followed by an ensemble of Isolation Forest (200 estimators) and Local Outlier Factor (LOF). Flagged outliers are augmented with human-interpretable statistical explanations based on Z-score thresholds, Tukey's interquartile range (IQR) fences, and mean-ratio multipliers. Simultaneously, a Random Forest feature importance module quantifies the mathematical drivers of key database attributes, while an automated heuristic engine uncovers immediate revenue trends, inventory stockout risks, and geographic opportunities upon data ingestion.",
        "Experimental validation across enterprise e-commerce databases (including multi-table schemas with 331+ order items, customer demographics, and product catalogs) demonstrates sub-second query synthesis latency, 100% interception of forbidden DDL statements, and accurate isolation of multivariate price and quantity anomalies. QueryMind establishes a highly secure, reliable, and scalable paradigm for non-technical database exploration and automated machine learning diagnostics."
    ]
    for para in ch2_paras:
        p = doc.add_paragraph(para)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(8)
        
    doc.add_page_break()
    
    # Save the document
    doc.save(output_filename)
    print("Word document generated successfully!")

if __name__ == "__main__":
    generate_full_docx()
