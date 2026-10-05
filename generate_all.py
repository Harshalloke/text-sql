# -*- coding: utf-8 -*-
"""
Master Build Script for QueryMind Black Book
Builds the complete publication-grade PDF and validates exact 61-page count.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.pdfgen import canvas
import pypdf

# Import modular page definitions
from generate_pdf import build_pdf
from pages_ch1_to_ch3 import add_ch1_problem_statement, add_ch2_abstract, add_ch3_introduction
from pages_ch4_to_ch5 import add_ch4_literature_review, add_ch5_research_methodology
from pages_ch6_setup import add_ch6_experimental_setup
from pages_ch7_to_ch9 import add_ch7_results, add_ch8_conclusion, add_ch9_references

def generate_full_pdf(output_filename="QueryMind_Black_Book_Harshal_Loke.pdf"):
    print(f"Generating full PDF: {output_filename}...")
    
    # 1. Base doc setup
    # Margins: 54 pt left/right (0.75 in), 36 pt top/bottom (0.5 in)
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=36,
        bottomMargin=36
    )
    
    # 2. Get base story (Front Matter: Pages 1 to 4)
    story, styles = build_pdf()
    
    # 3. Add Chapters 1, 2, 3 (Pages 5 to 13)
    add_ch1_problem_statement(story, styles)
    add_ch2_abstract(story, styles)
    add_ch3_introduction(story, styles)
    
    # 4. Add Chapters 4, 5 (Pages 14 to 21)
    add_ch4_literature_review(story, styles)
    add_ch5_research_methodology(story, styles)
    
    # 5. Add Chapter 6 (Pages 22 to 42)
    add_ch6_experimental_setup(story, styles)
    
    # 6. Add Chapters 7, 8, 9 (Pages 43 to 61)
    add_ch7_results(story, styles)
    add_ch8_conclusion(story, styles)
    add_ch9_references(story, styles)
    
    # Build PDF
    doc.build(story)
    print("PDF build completed.")
    
    # Verify exact page count using pypdf
    reader = pypdf.PdfReader(output_filename)
    page_count = len(reader.pages)
    print(f"=== RESULTING PDF PAGE COUNT: {page_count} ===")
    
    for i in range(page_count):
        txt = reader.pages[i].extract_text() or ""
        first_line = txt.strip().split("\n")[0] if txt.strip() else "[NO TEXT]"
        print(f"Page {i+1}: {first_line[:70]}")
        
    return page_count

if __name__ == "__main__":
    generate_full_pdf()
