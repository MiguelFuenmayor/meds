import os
import subprocess
from collections import Counter
from datetime import datetime

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, \
    QPushButton, QFileDialog, QInputDialog, QLineEdit, QGridLayout, QHBoxLayout

import queries
from report_template import DailyReportPDF
from views.MedEdit import MedEdit


class Totals(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Totales")
        self.setStyleSheet("""
        #button {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            min-width: 300px;
            min-height: 30px;
            background-color: #00BFFF;
        }
        """)
        self.modal_window = None
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.main_layout = QGridLayout()
        self.widget.setLayout(self.main_layout)
        self.scroll.setWidget(self.widget)
        self.scroll.setWidgetResizable(True)
        self.main_layout.addWidget(QLabel("Totales"))
        self.search_bar = QLineEdit()
        self.search_bar.setText("")
        self.search_bar.textChanged.connect(self.search)
        self.clear_search = QPushButton("LIMPIAR BUSQUEDA")
        self.clear_search.clicked.connect(self.clear)
        self.main_layout.addWidget(self.search_bar, 0, 1, 1, 1)
        self.main_layout.addWidget(self.clear_search, 0, 2, 1, 1)
        self.dummy_layout = QVBoxLayout()
        self.setLayout(self.dummy_layout)
        self.dummy_layout.addWidget(self.scroll)
        self.meds = None

        self.totals_per_med = QTableWidget()
        headers = ["CODIGO", "MEDICAMENTO", "CAJAS", "UND", "TIPO"]
        self.totals_per_med.setColumnCount(len(headers))
        self.totals_per_med.setHorizontalHeaderLabels(headers)
        self.totals_per_med.setEditTriggers(QTableWidget.NoEditTriggers)
        self.totals_per_med.setSelectionBehavior(QTableWidget.SelectRows)
        self.totals_per_med.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.totals_per_med.setFont(QFont("Arial", 12))
        self.totals_per_med.itemDoubleClicked.connect(self.edit)
        self.search()
        self.main_layout.addWidget(self.totals_per_med, 1, 0, 70, 5)
        self.types = None
        self.totals_per_type = QTableWidget()

        headers = ["TIPO", "MEDICAMENTOS", "PAQUETES"]
        self.totals_per_type.setColumnCount(len(headers))
        self.totals_per_type.setHorizontalHeaderLabels(headers)
        self.totals_per_type.setEditTriggers(QTableWidget.NoEditTriggers)
        self.totals_per_type.setSelectionBehavior(QTableWidget.SelectRows)
        self.totals_per_type.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.totals_per_type.setFont(QFont("Arial", 12))
        self.types_logic()
        self.main_layout.addWidget(self.totals_per_type, 72, 0, 30, 5)
        self.button_layout = QHBoxLayout()
        self.report_btn = QPushButton("Reporte")
        self.report_btn.clicked.connect(self.report)
        self.report_btn.setObjectName("button")
        self.button_layout.addWidget(self.report_btn)
        self.zero_report_btn = QPushButton("Reporte de todo lo que esta en cero(0)")
        self.zero_report_btn.clicked.connect(self.zero_report)
        self.zero_report_btn.setObjectName("button")
        self.button_layout.addWidget(self.zero_report_btn)
        self.main_layout.addLayout(self.button_layout, 103, 0, 1, 5)

    def zero_report(self):
        self.recharge()
        pdf = DailyReportPDF()
        pdf.set_font("Helvetica", size=7)
        place = QFileDialog.getExistingDirectory(self, "Select Directory")
        name, ok = QInputDialog().getText(self, 'NOMBRE', 'NOMBRE:', QLineEdit.Normal,
                                          f"REPORTE TOTALES {datetime.today().strftime('%d-%m-%Y')}")
        if ok:
            med_data = [
                ("CODIGO", "MEDICAMENTO", "CAJAS", "UND")
            ]

            for i in range(self.totals_per_med.rowCount()):
                if (self.totals_per_med.item(i, 3).text() == "0" and
                        self.totals_per_med.item(i, 2).text() == "0"):
                    med_data.append((self.totals_per_med.item(i, 0).text(),
                                     self.totals_per_med.item(i, 1).text(),
                                     self.totals_per_med.item(i, 2).text(),
                                     self.totals_per_med.item(i, 3).text()
                                     ))
            pdf.add_page()

            with pdf.table(
                    col_widths=(15, 50, 10, 10)
            ) as table:
                for data_row in med_data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)

            pdf.output(f"{place}/{name}.pdf")
            file = place + f"/{name}.pdf"
            pdf.output(file)
            with subprocess.Popen([os.path.abspath(file)], shell=True) as p:
                pass
    def report(self):
        self.recharge()
        pdf = DailyReportPDF()
        pdf.set_font("Helvetica", size=7)
        place = QFileDialog.getExistingDirectory(self, "Select Directory")
        name, ok = QInputDialog().getText(self, 'NOMBRE', 'NOMBRE:', QLineEdit.Normal,
                                      f"REPORTE TOTALES {datetime.today().strftime('%d-%m-%Y')}")
        if ok:
            med_data = [
                ("CODIGO", "MEDICAMENTO", "CAJAS", "UND")
            ]

            for i in range(self.totals_per_med.rowCount()):
                med_data.append((self.totals_per_med.item(i, 0).text(),
                                 self.totals_per_med.item(i, 1).text(),
                                 self.totals_per_med.item(i, 2).text(),
                                 self.totals_per_med.item(i, 3).text()
                                 ))
            pdf.add_page()

            with pdf.table(
                    col_widths=(15, 50, 10, 10)
            ) as table:
                for data_row in med_data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)

            type_data = [
                ("TIPO", "MEDICAMENTOS", "CAJAS")
            ]
            total_meds = 0
            total_packs = 0
            for i in range(self.totals_per_type.rowCount()):
                total_meds += int(self.totals_per_type.item(i, 1).text())
                total_packs += int(self.totals_per_type.item(i, 2).text())
                type_data.append((self.totals_per_type.item(i, 0).text(),
                                  self.totals_per_type.item(i, 1).text(),
                                  self.totals_per_type.item(i, 2).text(),
                                  ))
            type_data.append(("TOTAL", str(total_meds), str(total_packs)))
            pdf.add_page()
            with pdf.table(

            ) as table:
                for data_row in type_data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)

            pdf.output(f"{place}/{name}.pdf")
            file = place + f"/{name}.pdf"
            pdf.output(file)
            with subprocess.Popen([os.path.abspath(file)], shell=True) as p:
                pass
        pass

    def meds_logic(self):
        self.totals_per_med.setRowCount(len(self.meds))
        meds_totals = {}
        counter = Counter()
        unit_counter = Counter()
        for med in self.meds:
            if med['entrada_salida'] is None:
                continue
            if med['codigo'] in meds_totals:
                pass
            else:
                meds_totals[med['codigo']] = med
            if med['paquetes'] == 0:
                units = int(med['unidades'])
            elif med['paquetes'] > 0 and med['unidades'] > 0:
                units = (int(med['unidades']) * int(med['paquetes']))
            else:
                units = med['unidades']
            if med['entrada_salida'] is True:
                print("adding")
                counter[med['codigo']] += int(med['paquetes'])
                unit_counter[med['codigo']] += units
            elif med['entrada_salida'] is False:
                print("subtracting")
                counter[med['codigo']] = counter[med['codigo']] - int(med['paquetes'])
                unit_counter[med['codigo']] = unit_counter[med['codigo']] - units
        i = 0

        for med in meds_totals.values():
            if med['entrada_salida'] is None:
                continue
            if med['entrada_salida']:
                self.totals_per_med.setItem(i, 0, QTableWidgetItem(med['codigo'].upper()))
                self.totals_per_med.setItem(i, 1, QTableWidgetItem(med['nombre'].upper()))
                self.totals_per_med.setItem(i, 2, QTableWidgetItem(str(counter[med['codigo']]).upper()))
                self.totals_per_med.setItem(i, 3, QTableWidgetItem(str(unit_counter[med['codigo']]).upper()))
                self.totals_per_med.setItem(i, 4, QTableWidgetItem(str(med['tipo']).upper()))
                i += 1
        self.totals_per_med.setRowCount(i)
        pass

    def types_logic(self):
        self.types = queries.get_totales_types()
        self.totals_per_type.setRowCount(len(self.types))
        counter = Counter()
        for med in self.types:
            if med['entrada_salida'] is True:
                counter[med['id']] += int(med['paquetes'])
            elif med['entrada_salida'] is False:
                counter[med['id']] = counter[med['id']] - int(med['paquetes'])
        i = 0
        for med in self.types:
            if med['entrada_salida']:
                self.totals_per_type.setItem(i, 0, QTableWidgetItem(str(med['name']).upper()))
                self.totals_per_type.setItem(i, 1, QTableWidgetItem(str(med['meds']).upper()))
                self.totals_per_type.setItem(i, 2, QTableWidgetItem(str(counter[med['id']]).upper()))
                i += 1
        self.totals_per_type.setRowCount(i)
        pass

    def recharge(self):
        self.totals_per_med.clearContents()
        self.totals_per_type.clearContents()
        self.meds = queries.get_totales()
        self.meds_logic()
        self.types_logic()
        pass

    def search(self):
        search = self.search_bar.text()
        if search == "":
            self.meds = queries.get_totales()
        else:
            self.meds = queries.search_totales(search)
        self.totals_per_med.clearContents()
        self.meds_logic()

    def edit(self):
        selected_code = self.totals_per_med.item(self.totals_per_med.selectedItems()[0].row(), 0).text()
        self.modal_window = None
        self.modal_window = MedEdit(selected_code)
        self.modal_window.changes_made.clicked.connect(self.recharge)
        self.modal_window.show()
        pass

    def clear(self):
        self.search_bar.setText("")
