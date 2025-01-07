from datetime import datetime

from fpdf import FPDF


class DailyReportPDF(FPDF):

    def header(self):
        # Rendering logo:
        # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.image(f"logo.jpg", 10, 10, 12, 12)
        self.set_font("helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, f"REPORTE MEDICAMENTOS {datetime.today().strftime('%d/%m/%Y')} ", align="C")

        # Performing a line break:
        self.ln(5)
        self.set_font("helvetica", "I", 10)
        self.cell(0, 10, "POLICIA DE SAN FRANCISCO", align="C")
        self.ln(3)
        self.set_font("helvetica", "I", 5)
        self.cell(0, 10, "CANT=CANTIDAD, UND=UNIDADES", align="C")
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 10)
        # Printing page number:
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")