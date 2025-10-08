"""
PDF Export Service
Converts HTML resumes to ATS-compatible PDF files using WeasyPrint
"""
from weasyprint import HTML, CSS
from typing import Optional
import io

class PDFExporter:
    """Generate ATS-compatible PDF resumes from HTML"""

    def __init__(self):
        # ATS-safe CSS for PDF generation
        self.base_css = CSS(string="""
            @page {
                size: Letter;
                margin: 0.5in;
            }

            body {
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.15;
                color: #000000;
            }

            h1 {
                font-size: 18pt;
                margin: 0 0 5px 0;
                font-weight: bold;
                color: #000000;
            }

            h2 {
                font-size: 12pt;
                margin: 15px 0 5px 0;
                font-weight: bold;
                text-transform: uppercase;
                border-bottom: 1px solid #000000;
                color: #000000;
            }

            h3 {
                font-size: 11pt;
                margin: 10px 0 3px 0;
                font-weight: bold;
                color: #000000;
            }

            p {
                margin: 2px 0;
            }

            ul {
                margin: 5px 0;
                padding-left: 20px;
            }

            li {
                margin-bottom: 3px;
            }

            /* Ensure print-friendly */
            * {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            /* No page breaks inside important sections */
            .experience-item, .education-item {
                page-break-inside: avoid;
            }
        """)

    def html_to_pdf(self, html_content: str) -> bytes:
        """
        Convert HTML resume to PDF bytes

        Args:
            html_content: HTML string of resume

        Returns:
            PDF file as bytes
        """
        # Create PDF from HTML
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf(stylesheets=[self.base_css])

        return pdf_bytes

    def html_to_pdf_file(self, html_content: str, output_path: str) -> None:
        """
        Convert HTML resume to PDF file

        Args:
            html_content: HTML string of resume
            output_path: Path to save PDF file
        """
        pdf_bytes = self.html_to_pdf(html_content)

        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)

    def generate_ats_safe_pdf(
        self,
        html_content: str,
        optimize_for_ats: bool = True
    ) -> bytes:
        """
        Generate PDF with extra ATS compatibility checks

        Args:
            html_content: HTML string of resume
            optimize_for_ats: Apply extra ATS-safe styling

        Returns:
            PDF file as bytes
        """
        if optimize_for_ats:
            # Add extra ATS-safe CSS rules
            ats_css = CSS(string="""
                /* Remove any colors that might not print well */
                * {
                    color: #000000 !important;
                    background-color: #ffffff !important;
                }

                /* Ensure standard margins */
                @page {
                    margin: 0.75in;
                }

                /* Remove any borders except for section headers */
                * {
                    border: none !important;
                }

                h2 {
                    border-bottom: 1px solid #000000 !important;
                }

                /* Ensure readable line height */
                body {
                    line-height: 1.2 !important;
                }
            """)

            html = HTML(string=html_content)
            pdf_bytes = html.write_pdf(stylesheets=[self.base_css, ats_css])
        else:
            pdf_bytes = self.html_to_pdf(html_content)

        return pdf_bytes

    def get_pdf_stream(self, html_content: str) -> io.BytesIO:
        """
        Get PDF as BytesIO stream for FastAPI response

        Args:
            html_content: HTML string of resume

        Returns:
            BytesIO stream containing PDF
        """
        pdf_bytes = self.html_to_pdf(html_content)
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_stream.seek(0)

        return pdf_stream
