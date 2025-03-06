"""
PDF Generator module for ROI Automation Dashboard.
This module handles creating PDF reports from the OpenAI analysis.
"""

import os
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    ListFlowable,
    ListItem,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime


class PDFGenerator:
    def __init__(self, output_dir="reports"):
        """Initialize the PDF generator with an output directory."""
        self.output_dir = output_dir

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom styles for the PDF document."""
        # Title style - check if it already exists to avoid KeyError
        if "Title" not in self.styles:
            self.styles.add(
                ParagraphStyle(
                    name="Title",
                    parent=self.styles["Heading1"],
                    fontSize=24,
                    spaceAfter=12,
                    textColor=colors.HexColor("#4a6bff"),
                )
            )

        # Heading styles
        if "Heading2" not in self.styles:
            self.styles.add(
                ParagraphStyle(
                    name="Heading2",
                    parent=self.styles["Heading2"],
                    fontSize=16,
                    spaceAfter=8,
                    textColor=colors.HexColor("#343a40"),
                )
            )

        if "Heading3" not in self.styles:
            self.styles.add(
                ParagraphStyle(
                    name="Heading3",
                    parent=self.styles["Heading3"],
                    fontSize=14,
                    spaceAfter=6,
                    textColor=colors.HexColor("#343a40"),
                )
            )

        # Body text style
        if "BodyText" not in self.styles:
            self.styles.add(
                ParagraphStyle(
                    name="BodyText",
                    parent=self.styles["Normal"],
                    fontSize=11,
                    leading=14,
                    spaceAfter=6,
                )
            )

        # Bullet point style
        if "Bullet" not in self.styles:
            self.styles.add(
                ParagraphStyle(
                    name="Bullet",
                    parent=self.styles["BodyText"],
                    fontSize=11,
                    leading=14,
                    leftIndent=20,
                    bulletIndent=10,
                    spaceBefore=0,
                    spaceAfter=5,
                )
            )

    def _convert_markdown_to_reportlab(self, md_text):
        """Convert markdown text to ReportLab elements."""
        elements = []

        # First convert markdown to HTML using the markdown library
        html = markdown.markdown(md_text)

        # Split the HTML by headers for easier processing
        html_parts = html.split("<h1>")

        # Process the first part (before any h1 tag)
        first_part = html_parts[0]
        if first_part.strip():
            # Process paragraphs
            for p in first_part.split("<p>"):
                if not p.strip():
                    continue
                # Clean up paragraph closing tags
                p = p.replace("</p>", "").strip()
                if p:
                    # Convert <strong> tags to bold in ReportLab
                    p = p.replace("<strong>", "<b>").replace("</strong>", "</b>")
                    # Convert <em> tags to italic in ReportLab
                    p = p.replace("<em>", "<i>").replace("</em>", "</i>")
                    elements.append(Paragraph(p, self.styles["BodyText"]))

        # Process remaining parts with headers
        for part in html_parts[1:]:
            if not part.strip():
                continue

            # Split header from content
            header_parts = part.split("</h1>", 1)
            header = header_parts[0].strip()

            # Add the h1 header
            elements.append(Paragraph(header, self.styles["Title"]))
            elements.append(Spacer(1, 0.1 * inch))

            if len(header_parts) > 1:
                content = header_parts[1].strip()

                # Process h2 headers
                h2_parts = content.split("<h2>")

                # Content before first h2
                first_h2_part = h2_parts[0]
                self._process_content_part(first_h2_part, elements)

                # Process each h2 section
                for h2_part in h2_parts[1:]:
                    if not h2_part.strip():
                        continue

                    # Split h2 header from content
                    h2_header_parts = h2_part.split("</h2>", 1)
                    h2_header = h2_header_parts[0].strip()

                    # Add the h2 header
                    elements.append(Paragraph(h2_header, self.styles["Heading2"]))
                    elements.append(Spacer(1, 0.1 * inch))

                    if len(h2_header_parts) > 1:
                        h2_content = h2_header_parts[1].strip()
                        self._process_content_part(h2_content, elements)

        return elements

    def _process_content_part(self, content, elements):
        """Process a content part and add elements."""
        if not content:
            return

        # Process paragraphs
        for p in content.split("<p>"):
            if not p.strip():
                continue

            # Clean up paragraph closing tags
            p = p.replace("</p>", "").strip()
            if p:
                # Convert <strong> tags to bold in ReportLab
                p = p.replace("<strong>", "<b>").replace("</strong>", "</b>")
                # Convert <em> tags to italic in ReportLab
                p = p.replace("<em>", "<i>").replace("</em>", "</i>")
                elements.append(Paragraph(p, self.styles["BodyText"]))
                elements.append(Spacer(1, 0.1 * inch))

        # Process unordered lists
        if "<ul>" in content:
            ul_parts = content.split("<ul>")
            for ul_part in ul_parts[1:]:
                if "</ul>" in ul_part:
                    list_content = ul_part.split("</ul>")[0].strip()
                    list_items = []

                    for li in list_content.split("<li>"):
                        li = li.replace("</li>", "").strip()
                        if li:
                            # Convert <strong> tags to bold in ReportLab
                            li = li.replace("<strong>", "<b>").replace(
                                "</strong>", "</b>"
                            )
                            # Convert <em> tags to italic in ReportLab
                            li = li.replace("<em>", "<i>").replace("</em>", "</i>")
                            list_items.append(
                                ListItem(
                                    Paragraph(li, self.styles["Bullet"]), leftIndent=20
                                )
                            )

                    if list_items:
                        elements.append(
                            ListFlowable(list_items, bulletType="bullet", start="•")
                        )
                        elements.append(Spacer(1, 0.1 * inch))

    def generate_pdf_from_markdown(self, markdown_content, filename="report.pdf"):
        """Generate a PDF file from markdown content."""
        try:
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not filename.endswith(".pdf"):
                filename = filename + ".pdf"
            output_filename = f"{os.path.splitext(filename)[0]}_{timestamp}.pdf"
            output_path = os.path.join(self.output_dir, output_filename)

            # Set up the PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
            )

            # Convert markdown to ReportLab elements
            elements = self._convert_markdown_to_reportlab(markdown_content)

            # Add a footer with page numbers
            def add_page_number(canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica", 9)
                page_num = canvas.getPageNumber()
                text = f"Page {page_num}"
                canvas.drawRightString(letter[0] - 72, 40, text)
                canvas.restoreState()

            # Build the PDF
            doc.build(
                elements, onFirstPage=add_page_number, onLaterPages=add_page_number
            )

            return True, output_path

        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"

    def convert_html_to_pdf(self, html_content, filename="report.pdf"):
        """Convert HTML content to a PDF file."""
        try:
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not filename.endswith(".pdf"):
                filename = filename + ".pdf"
            output_filename = f"{os.path.splitext(filename)[0]}_{timestamp}.pdf"
            output_path = os.path.join(self.output_dir, output_filename)

            # Create a file buffer
            result_file = open(output_path, "w+b")

            # Convert HTML to PDF
            pisa_status = pisa.CreatePDF(html_content, dest=result_file)

            # Close the file
            result_file.close()

            # Return True if conversion was successful
            if pisa_status.err:
                return False, f"Error generating PDF: {pisa_status.err}"
            else:
                return True, output_path

        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
