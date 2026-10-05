"""
QueryMind Black Book Generation Script
Generates both PDF (61 pages matching sample black book) and DOCX formats.
Author: Harshal Pandharinath Loke (Seat No: 564)
Institution: S.P. Mandali's Ramnarain Ruia Autonomous College
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Document metadata
PROJECT_TITLE = "QueryMind: Intelligent Natural Language to SQL Interface with Machine Learning Driven Data Diagnostics and Anomaly Detection"
SHORT_TITLE = "QueryMind: Natural Language to SQL & Local ML"
COLLEGE_NAME_1 = "S.P. Mandali's"
COLLEGE_NAME_2 = "Ramnarain Ruia Autonomous College"
COLLEGE_ADDR = "Matunga, Mumbai - 400019"
DEPT_NAME = "Department of Computer Science"
REPORT_TYPE = "Research Project Report\nOn"
GUIDE_NAME = "Mrs. Edith Juni"
STUDENT_NAME = "Mr Harshal Pandharinath Loke"
STUDENT_NAME_SHORT = "Harshal P. Loke"
SEAT_NO = "564"
DEGREE_NAME = "M.Sc. Computer Science"
BATCH_YEAR = "2026 - 2027"
COORDINATOR_NAME = "Mrs. Aarya Tawde"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 54
MARGIN_RIGHT = 54
MARGIN_TOP = 40
MARGIN_BOTTOM = 40
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 487.28 pt
CONTENT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM # 761.89 pt

print(f"Content width: {CONTENT_WIDTH} pt, Content height: {CONTENT_HEIGHT} pt")
