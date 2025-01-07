import os
import subprocess
from datetime import datetime

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QPushButton, QSizePolicy, \
    QFormLayout, QDateEdit, QFileDialog, QInputDialog, QLineEdit, QComboBox

import queries
from report_template import DailyReportPDF


class Reports(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes")
        earliest_date = queries.earliest_date()
        latest_date = queries.latest_date()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.title = QLabel("GENERAR REPORTE DE MOVIMIENTOS")
        self.title.setMaximumHeight(20)
        self.dates_form = QFormLayout()
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setMaximumHeight(20)
        self.date_end = QDateEdit()

        self.date_end.setDate(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        self.date_end.setMaximumHeight(20)
        if earliest_date is not None and latest_date is not None:
            ear_date = QDate.fromString(earliest_date['fecha_entrega'].strftime("%Y-%m-%d"), "yyyy-MM-dd")
            lat_date = QDate.fromString(latest_date['fecha_entrega'].strftime("%Y-%m-%d"), "yyyy-MM-dd")
            self.date_start.setDate(ear_date)
            self.date_end.setDate(lat_date)


        self.main_layout.addWidget(self.title)
        self.dates_form.addRow("FECHA INICIO", self.date_start)
        self.dates_form.addRow("FECHA FINAL", self.date_end)
        self.tipo_report = QComboBox()
        self.tipo_report.addItem("SOLO ENTRADAS")
        self.tipo_report.addItem("SOLO SALIDAS")
        self.tipo_report.addItem("TODOS")
        self.dates_form.addRow("REPORTE DE:", self.tipo_report)
        self.main_layout.addLayout(self.dates_form)

        self.subtitle = QLabel("CAMPOS")
        self.subtitle.setMaximumHeight(20)
        self.codigo = QCheckBox("CODIGO")
        self.nombre = QCheckBox("NOMBRE")
        self.unidades_por_paquete = QCheckBox("UNIDADES POR PAQUETE")
        self.lote = QCheckBox("LOTE")
        self.paquetes = QCheckBox("PAQUETES")
        self.donador_retirador = QCheckBox("DONADOR/RETIRADOR")
        self.entrada_salida = QCheckBox("ENTRADA/SALIDA")
        self.tipo = QCheckBox("TIPO")
        self.fecha_creacion = QCheckBox("FECHA CREACION")
        self.fecha_vencimiento = QCheckBox("FECHA VENCIMIENTO")
        self.fecha_entrega = QCheckBox("FECHA ENTREGA")
        self.codigo.setChecked(True)
        self.nombre.setChecked(True)
        self.unidades_por_paquete.setChecked(True)
        self.lote.setChecked(True)
        self.paquetes.setChecked(True)
        self.donador_retirador.setChecked(True)
        self.entrada_salida.setChecked(True)
        self.tipo.setChecked(True)
        self.fecha_creacion.setChecked(True)
        self.fecha_vencimiento.setChecked(True)
        self.fecha_entrega.setChecked(True)
        self.horizonal_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generar")
        self.generate_btn.clicked.connect(self.generate_report)
        self.horizonal_layout.addWidget(self.generate_btn)
        self.main_layout.addWidget(self.subtitle)
        self.main_layout.addWidget(self.codigo)
        self.main_layout.addWidget(self.nombre)
        self.main_layout.addWidget(self.unidades_por_paquete)
        self.main_layout.addWidget(self.lote)
        self.main_layout.addWidget(self.paquetes)
        self.main_layout.addWidget(self.donador_retirador)
        self.main_layout.addWidget(self.entrada_salida)
        self.main_layout.addWidget(self.fecha_creacion)
        self.main_layout.addWidget(self.fecha_vencimiento)
        self.main_layout.addWidget(self.fecha_entrega)
        self.main_layout.addWidget(self.tipo)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.horizonal_layout)

    def generate_report(self):
        if self.tipo_report.currentText() == "TODOS":
            rows = queries.get_report_data(self.date_start.date().toString("yyyy-MM-dd"),
                                       self.date_end.date().toString("yyyy-MM-dd"), 'TODOS')
        elif self.tipo_report.currentText() == "SOLO ENTRADAS":
            # change this
            rows = queries.get_report_data(self.date_start.date().toString("yyyy-MM-dd"),
                                       self.date_end.date().toString("yyyy-MM-dd"), 'SOLO ENTRADAS')
        elif self.tipo_report.currentText() == "SOLO SALIDAS":
            # change_this
            rows = queries.get_report_data(self.date_start.date().toString("yyyy-MM-dd"),
                                       self.date_end.date().toString("yyyy-MM-dd"), 'SOLO SALIDAS')
        headers = []
        columns = []
        widths = []
        if self.codigo.isChecked():
            headers.append("#")
            columns.append("codigo")
            widths.append(20)
        if self.nombre.isChecked():
            headers.append("NOMBRE")
            columns.append("nombre")
            widths.append(50)
        if self.lote.isChecked():
            headers.append("LOTE")
            columns.append("lote")
            widths.append(10)
        if self.paquetes.isChecked():
            headers.append("CANT")
            columns.append("paquetes")
            widths.append(9)
        if self.unidades_por_paquete.isChecked():
            headers.append("UND")
            columns.append("unidades_por_paquete")
            widths.append(7)
        if self.donador_retirador.isChecked():
            headers.append("PERSONA")
            columns.append("donador_retirador")
            widths.append(20)
        if self.entrada_salida.isChecked():
            headers.append("EN/SAL")
            columns.append("entrada_salida")
            widths.append(10)
        if self.tipo.isChecked():
            headers.append("TIPO")
            columns.append("tipo")
            widths.append(10)
        if self.fecha_creacion.isChecked():
            headers.append("CREAC")
            columns.append("fecha_creacion")
            widths.append(10)
        if self.fecha_vencimiento.isChecked():
            headers.append("VENC")
            columns.append("fecha_vencimiento")
            widths.append(10)
        if self.fecha_entrega.isChecked():
            headers.append("ENTREGA")
            columns.append("fecha_entrega")
            widths.append(15)
        TABLE_DATA = [
            headers
        ]
        for row in rows:
            line = []
            for header in columns:
                if not isinstance(row[header], str) and not isinstance(row[header], int):
                    line.append(row[header].strftime("%d/%m/%Y"))
                elif isinstance(row[header], bool):
                    if row[header] == True:
                        line.append("Entrada")
                    else:
                        line.append("Salida")
                elif isinstance(row[header], int):
                    line.append(str(row[header]))
                else:
                    line.append(row[header])
            TABLE_DATA.append(line)

        pdf = DailyReportPDF()
        pdf.set_font("Times", size=7)

        print(TABLE_DATA)
        place = QFileDialog.getExistingDirectory()
        name, ok = QInputDialog.getText(self, "NOMBRE", "NOMBRE DEL REPORTE", QLineEdit.Normal,
                                    f"REPORTE MOVIMIENTOS {datetime.today().strftime('%d-%m-%Y')}")
        if ok:
            pdf.add_page()
            with pdf.table(
                    col_widths=widths
            ) as table:
                for data_row in TABLE_DATA:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            file = place + f"/{name}.pdf"
            pdf.output(file)
            with subprocess.Popen([os.path.abspath(file)], shell=True) as p:
                pass


        pass

