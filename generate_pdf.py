# -*- coding: utf-8 -*-
"""
Full PDF Builder for QueryMind Black Book
Generates exactly 61 pages matching sample black book.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
import pypdf

def build_pdf(filename="QueryMind_Black_Book_Harshal_Loke.pdf"):
    styles = getSampleStyleSheet()
    
    # Register custom styles matching sample black book
    styles.add(ParagraphStyle('CoverCol', fontName='Times-Bold', fontSize=15, leading=20, alignment=TA_CENTER))
    styles.add(ParagraphStyle('CoverDept', fontName='Times-Roman', fontSize=12, leading=16, alignment=TA_CENTER))
    styles.add(ParagraphStyle('CoverRep', fontName='Times-Bold', fontSize=13, leading=18, alignment=TA_CENTER))
    styles.add(ParagraphStyle('CoverTitle', fontName='Times-Bold', fontSize=14.5, leading=20, alignment=TA_CENTER))
    styles.add(ParagraphStyle('CoverMeta', fontName='Times-Roman', fontSize=11.5, leading=16, alignment=TA_CENTER))
    styles.add(ParagraphStyle('CoverMetaB', fontName='Times-Bold', fontSize=11.5, leading=16, alignment=TA_CENTER))
    
    styles.add(ParagraphStyle('ChapSep', fontName='Times-Bold', fontSize=22, leading=28, alignment=TA_CENTER))
    
    styles.add(ParagraphStyle('PNum', fontName='Times-Roman', fontSize=10.5, leading=14, alignment=TA_LEFT))
    styles.add(ParagraphStyle('SecHead', fontName='Times-Bold', fontSize=12, leading=15, alignment=TA_LEFT, spaceAfter=4))
    styles.add(ParagraphStyle('SubSecHead', fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_LEFT, spaceAfter=3))
    
    styles.add(ParagraphStyle('Body', fontName='Times-Roman', fontSize=9.5, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=4))
    styles.add(ParagraphStyle('BodyB', fontName='Times-Bold', fontSize=9.5, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=3))
    styles.add(ParagraphStyle('BodyBold', fontName='Times-Bold', fontSize=9.5, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=3))
    
    styles.add(ParagraphStyle('CodeBlock', fontName='Courier', fontSize=6.8, leading=8.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle('FigCap', fontName='Times-Italic', fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=4))
    
    styles.add(ParagraphStyle('TblCell', fontName='Times-Roman', fontSize=8, leading=10.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle('TblCellB', fontName='Times-Bold', fontSize=8, leading=10.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle('TblCellC', fontName='Times-Roman', fontSize=8, leading=10.5, alignment=TA_CENTER))
    styles.add(ParagraphStyle('TblCellCB', fontName='Times-Bold', fontSize=8, leading=10.5, alignment=TA_CENTER))
    styles.add(ParagraphStyle('DocTableCellCenter', fontName='Times-Italic', fontSize=9.5, leading=13, alignment=TA_CENTER))

    cover_col = styles['CoverCol']
    cover_dept = styles['CoverDept']
    cover_rep = styles['CoverRep']
    cover_title = styles['CoverTitle']
    cover_meta = styles['CoverMeta']
    cover_meta_b = styles['CoverMetaB']
    tbl_cell = styles['TblCell']
    tbl_cell_b = styles['TblCellB']
    tbl_cell_c = styles['TblCellC']
    tbl_cell_cb = styles['TblCellCB']
    body = styles['Body']

    story = []
    
    # ----------------------------------------------------
    # PAGE 1: TITLE / COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("S.P. Mandali's", cover_col))
    story.append(Paragraph("Ramnarain Ruia Autonomous College", cover_col))
    story.append(Paragraph("Matunga, Mumbai-400019", cover_dept))
    story.append(Paragraph("Department of Computer Science", cover_dept))
    story.append(Spacer(1, 15))
    
    if os.path.exists("college_logo.png"):
        story.append(Image("college_logo.png", width=95, height=65))
    else:
        story.append(Spacer(1, 65))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph("Research Project Report", cover_rep))
    story.append(Paragraph("On", cover_rep))
    story.append(Spacer(1, 8))
    story.append(Paragraph("QueryMind: Intelligent Natural Language to SQL Interface with Machine Learning Driven Data Diagnostics and Anomaly Detection", cover_title))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Project Guide", cover_meta_b))
    story.append(Paragraph("Mrs. Edith Juni", cover_meta))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Project By", cover_meta_b))
    story.append(Paragraph("Mr Harshal Pandharinath Loke", cover_meta_b))
    story.append(Paragraph("Seat No: 564", cover_meta))
    story.append(Spacer(1, 20))
    story.append(Paragraph("M.Sc. Computer Science", cover_meta_b))
    story.append(Paragraph("2026 - 2027", cover_meta))
    story.append(PageBreak()) # End Page 1
    
    # ----------------------------------------------------
    # PAGE 2: ACKNOWLEDGEMENT
    # ----------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("ACKNOWLEDGEMENT", ParagraphStyle('AckH', fontName='Times-Bold', fontSize=14, leading=18, alignment=TA_CENTER)))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Every project big or small is successful, largely due to the effort of a number of wonderful people who have always given their valuable advice or have always lent a helping hand.", body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("I take this opportunity of submitting this report to express my profound gratitude to the management of 'Ramnarain Ruia Autonomous College' for giving me the opportunity to accomplish this project work.", body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("I am also thankful to all the teachers for their kind support and help.", body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("I express my deepest gratitude towards my project guide <b>Mrs. Edith Juni</b> for her valuable and timely advice during the various phases in my project.", body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("I express my sincere thanks to our respected Co-ordinator <b>Mrs. Aarya Tawde</b> for allowing us to use the facilities available.", body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("I would also like to thank all those unnamed but important people and Computer Lab Assistants and supportive staff who directly or indirectly helped me in the completion of this project and to my family and friends without whose support, motivation and encouragement this would not have been possible.", body))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Thanking you,", ParagraphStyle('AckT', fontName='Times-Roman', fontSize=11, leading=14, alignment=TA_RIGHT)))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Harshal P. Loke</b>", ParagraphStyle('AckN', fontName='Times-Bold', fontSize=11, leading=14, alignment=TA_RIGHT)))
    story.append(PageBreak()) # End Page 2
    
    # ----------------------------------------------------
    # PAGE 3: TITLE FLYER
    # ----------------------------------------------------
    story.append(Spacer(1, 200))
    story.append(Paragraph("QueryMind:<br/><br/>Intelligent Natural Language<br/>to SQL Interface with<br/>Machine Learning Driven<br/>Data Diagnostics and<br/>Anomaly Detection", ParagraphStyle('Flyer', fontName='Times-Bold', fontSize=20, leading=26, alignment=TA_CENTER)))
    story.append(PageBreak()) # End Page 3
    
    # ----------------------------------------------------
    # PAGE 4: INDEX
    # ----------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("INDEX", ParagraphStyle('IndH', fontName='Times-Bold', fontSize=14, leading=18, alignment=TA_CENTER)))
    story.append(Spacer(1, 15))
    
    index_data = [
        [Paragraph("<b>Sr. No.</b>", tbl_cell_cb), Paragraph("<b>Contents</b>", tbl_cell_b), Paragraph("<b>Page No.</b>", tbl_cell_cb)],
        [Paragraph("<b>1</b>", tbl_cell_c), Paragraph("<b>Problem Statement</b>", tbl_cell_b), Paragraph("<b>1 - 2</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("1.1 Problem Definition", tbl_cell), Paragraph("2", tbl_cell_c)],
        [Paragraph("<b>2</b>", tbl_cell_c), Paragraph("<b>Abstract</b>", tbl_cell_b), Paragraph("<b>3 - 4</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("2.1 Project Abstract", tbl_cell), Paragraph("4", tbl_cell_c)],
        [Paragraph("<b>3</b>", tbl_cell_c), Paragraph("<b>Introduction</b>", tbl_cell_b), Paragraph("<b>5 - 9</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("3.1 Project Introduction", tbl_cell), Paragraph("6", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("3.2 Developed System Overview", tbl_cell), Paragraph("7", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("3.3 Unique Selling Propositions (USP) of the System", tbl_cell), Paragraph("7", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("3.4 Advantages of the Project", tbl_cell), Paragraph("8", tbl_cell_c)],
        [Paragraph("<b>4</b>", tbl_cell_c), Paragraph("<b>Literature Review</b>", tbl_cell_b), Paragraph("<b>10 - 13</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("4.1 Literature Review for the Project", tbl_cell), Paragraph("11", tbl_cell_c)],
        [Paragraph("<b>5</b>", tbl_cell_c), Paragraph("<b>Research Methodology</b>", tbl_cell_b), Paragraph("<b>14 - 17</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("5.1 Agile Methodology", tbl_cell), Paragraph("15", tbl_cell_c)],
        [Paragraph("<b>6</b>", tbl_cell_c), Paragraph("<b>Experimental Setup</b>", tbl_cell_b), Paragraph("<b>18 - 38</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("6.1 Requirements Analysis", tbl_cell), Paragraph("19", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("6.2 System Architecture Diagram", tbl_cell), Paragraph("24", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("6.3 Block Diagram of System Flow", tbl_cell), Paragraph("25", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("6.4 Input Code", tbl_cell), Paragraph("26", tbl_cell_c)],
        [Paragraph("<b>7</b>", tbl_cell_c), Paragraph("<b>Results</b>", tbl_cell_b), Paragraph("<b>39 - 52</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("7.1 Results Obtained", tbl_cell), Paragraph("40", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("7.2 Test Cases", tbl_cell), Paragraph("51", tbl_cell_c)],
        [Paragraph("<b>8</b>", tbl_cell_c), Paragraph("<b>Conclusion &amp; Future Scope</b>", tbl_cell_b), Paragraph("<b>53 - 54</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("8.1 Conclusion", tbl_cell), Paragraph("54", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("8.2 Future Scope", tbl_cell), Paragraph("54", tbl_cell_c)],
        [Paragraph("<b>9</b>", tbl_cell_c), Paragraph("<b>References</b>", tbl_cell_b), Paragraph("<b>55 - 57</b>", tbl_cell_c)],
        [Paragraph("", tbl_cell_c), Paragraph("9.1 References", tbl_cell), Paragraph("56", tbl_cell_c)],
    ]
    
    t_idx = Table(index_data, colWidths=[45, 360, 75])
    t_idx.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_idx)
    story.append(PageBreak()) # End Page 4
    
    return story, styles

print("Base builder structure created.")
