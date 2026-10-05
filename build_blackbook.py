# -*- coding: utf-8 -*-
"""
Black Book Generation Script for QueryMind
Author: Mr Harshal Pandharinath Loke (Seat No: 564, Batch: 2026 - 2027)
Institution: S.P. Mandali's Ramnarain Ruia Autonomous College, Matunga, Mumbai - 400019
Department of Computer Science
Degree: M.Sc. Computer Science
Project Guide: Mrs. Edith Juni
Coordinator: Mrs. Aarya Tawde
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
import pypdf

# Document Constants
PROJECT_TITLE = "QueryMind: Intelligent Natural Language to SQL Interface with Machine Learning Driven Data Diagnostics and Anomaly Detection"
SHORT_TITLE = "QueryMind: Natural Language to SQL & Local ML Diagnostics"
STUDENT_NAME = "Mr Harshal Pandharinath Loke"
STUDENT_SHORT = "Harshal P. Loke"
SEAT_NO = "564"
BATCH_YEAR = "2026 - 2027"
COLLEGE_NAME_1 = "S.P. Mandali's"
COLLEGE_NAME_2 = "Ramnarain Ruia Autonomous College"
COLLEGE_ADDR = "Matunga, Mumbai-400019"
DEPT_NAME = "Department of Computer Science"
GUIDE_NAME = "Mrs. Edith Juni"
COORDINATOR_NAME = "Mrs. Aarya Tawde"
DEGREE_NAME = "M.Sc. Computer Science"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 54
MARGIN_RIGHT = 54
MARGIN_TOP = 40
MARGIN_BOTTOM = 40
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 487.28 pt

def get_styles():
    styles = getSampleStyleSheet()
    
    # Custom styles matching sample black book
    styles.add(ParagraphStyle(
        'CoverCollege',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'CoverDept',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'CoverReportType',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'CoverProjectTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'CoverMetaBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    
    # Chapter Separator Title
    styles.add(ParagraphStyle(
        'ChapterSeparatorTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    
    # Page Header (Page No. X)
    styles.add(ParagraphStyle(
        'DocPageNumber',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.black
    ))
    
    # Section Heading (e.g. 1.1 Problem Definition:)
    styles.add(ParagraphStyle(
        'DocSectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.black
    ))
    
    # Subsection Heading (e.g. 6.1.1 Software Requirements:)
    styles.add(ParagraphStyle(
        'DocSubsectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.black
    ))
    
    # Body Text (formal, justified, Times-Roman 10.5 pt, 14 pt leading)
    styles.add(ParagraphStyle(
        'DocBodyText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=5
    ))
    
    # Body Bold Lead
    styles.add(ParagraphStyle(
        'DocBodyBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=4
    ))
    
    # Code snippet style (Courier 7.5 pt, 9.5 pt leading)
    styles.add(ParagraphStyle(
        'DocCodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.0,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1A202C')
    ))
    
    # Figure Caption
    styles.add(ParagraphStyle(
        'DocFigureCaption',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    ))
    
    # Table cell styles
    styles.add(ParagraphStyle(
        'DocTableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'DocTableCellBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'DocTableCellCenter',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'DocTableCellCenterBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.black
    ))
    
    return styles

print("Styles initialized successfully.")
