import os
import re
import subprocess
from datetime import datetime

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QHBoxLayout, \
    QPushButton, QInputDialog, QMessageBox, QLineEdit, QFileDialog

import queries
from report_template import DailyReportPDF


class BulkReport(QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.title = QLabel("IMPRIMIR REPORTE AGRUPADO")
        self.table = QTableWidget()
        self.ins = queries.get_movements()
        self.table.setRowCount(len(self.ins))
        headers = ["ID",
                   "F. ENTREGA",
                   "ENTRADA/SALIDA",
                   "CODIGO",
                   "NOMBRE",
                   "TIPO",
                   "LOTE",
                   "CAJAS",
                   "UNDxCAJA",
                   "PROVEEDOR/DONADOR",
                   "F. FABRIC",
                   "F. VENC",
                   ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.main_layout.addWidget(self.table)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        i = 0
        for med in self.ins:
            if med["entrada_salida"]:
                med["entrada_salida"] = "Entrada"
            else:
                med["entrada_salida"] = "Salida"
            self.table.setItem(i, 0, QTableWidgetItem(str(med["id"]).upper()))
            self.table.setItem(i, 1, QTableWidgetItem(med["fecha_entrega"].strftime("%d/%m/%Y")))
            self.table.setItem(i, 2, QTableWidgetItem(str(med["entrada_salida"]).upper()))
            self.table.setItem(i, 3, QTableWidgetItem(med["codigo"].upper()))
            self.table.setItem(i, 4, QTableWidgetItem(med["nombre"].upper()))
            self.table.setItem(i, 5, QTableWidgetItem(med["tipo"].upper()))
            self.table.setItem(i, 6, QTableWidgetItem(med["lote"].upper()))
            self.table.setItem(i, 8, QTableWidgetItem(str(med["unidades_por_paquete"]).upper()))
            self.table.setItem(i, 7, QTableWidgetItem(str(med["paquetes"]).upper()))
            self.table.setItem(i, 9, QTableWidgetItem(med["donador_retirador"].upper()))

            self.table.setItem(i, 10, QTableWidgetItem(med["fecha_creacion"].strftime("%d/%m/%Y")))
            self.table.setItem(i, 11, QTableWidgetItem(med["fecha_vencimiento"].strftime("%d/%m/%Y")))
            i += 1
        self.buttons_layout = QHBoxLayout()
        self.generate_report_btn = QPushButton("GENERAR REPORTE")
        self.generate_report_btn.setStyleSheet("height:20px")
        self.buttons_layout.addWidget(self.generate_report_btn)
        self.generate_report_btn.clicked.connect(self.generate_report)
        self.main_layout.addLayout(self.buttons_layout)

    def generate_report(self):
        msg, ok = QInputDialog.getText(self, "GENERAR REPORTE", "AGREGUE LAS ID \n DE LOS MOVIMIENTOS QUE DESEE INCLUIR \n"
                                                      " EN EL REPORTE, SEPARADAS POR UNA COMA \n "
                                                      "EJ: 1,3,4,6,19")
        if ok and msg:
            result = re.match("[0-9]+(,[0-9]+)*", f"{msg}")
            print(result)
            if result:
                print("making")
                TABLE_DATA = [[
                   "CODIGO",
                   "NOMBRE",
                   "CAJAS",
                   "UNDxCAJA",
                   "PROVEEDOR/ DONADOR",
                   "F. ENTREGA"]]
                for movement_id in msg.split(','):
                    movement = queries.get_movements_by_id(movement_id)
                    codigo = movement['codigo']
                    nombre = movement['nombre']
                    cant = movement['paquetes']
                    und = movement['unidades_por_paquete']
                    related = movement['donador_retirador']
                    f_entrega = movement['fecha_entrega']
                    list_ = [ str(codigo), nombre, str(cant), str(und), related, str(f_entrega)]
                    TABLE_DATA.append(list_)
                entrega, ok_1 = QInputDialog.getText(self, "Reporte de salida", "NOMBRE DE QUIEN ENTREGA:")
                recibe, ok_2 = QInputDialog.getText(self, "Reporte de salida", "NOMBRE DE QUIEN RECIBE:")
                credencial_2, ok_3 = QInputDialog.getText(self, "Reporte de salida", "CREDENCIAL DE QUIEN ENTREGA:")
                credencial, ok_4 = QInputDialog.getText(self, "Reporte de salida", "CREDENCIAL DE QUIEN RECIBE:")
                pdf = DailyReportPDF()
                pdf.add_page()
                print(ok_1, ok_2, ok_3, ok_4)
                if ok_1 and ok_2 and ok_3 and ok_4:
                    pass
                else:
                    QMessageBox.information(self, "DATOS", "INGRESE TODOS LOS DATOS")
                    return
                pdf.set_font("Times", size=11)
                text = (f'EL FUNCIONARIO "{recibe}" DE CREDENCIAL "{credencial}" HA RECIBIDO '
                        f'POR MEDIO DE EL FUNCIONARIO "{entrega}" DE CREDENCIAL '
                        f'"{credencial_2}" LOS MEDICAMENTOS LISTADOS DEBAJO '
                        f"DE EL INVENTARIO DE MEDICAMENTOS DE LA POLICIA DE SAN FRANCISCO. "
                        f"FECHA {datetime.today().strftime('%d/%m/%Y')}")

                pdf.write(text=text)
                pdf.set_font(size=9)
                pdf.ln(10)
                with pdf.table(
                    col_widths=(18, 45, 7, 7, 14, 12),
                    line_height=5
                ) as table:
                    for data_row in TABLE_DATA:
                        row = table.row()
                        for datum in data_row:
                            row.cell(datum)
                pdf.ln(20)
                name, ok = QInputDialog.getText(self, "NOMBRE", "NOMBRE DEL REPORTE", QLineEdit.Normal,
                                                f"REPORTE MOVIMIENTOS {datetime.today().strftime('%d-%m-%Y')}")
                pdf.image("FIRMAS.png", w=200, h=30)
                place = QFileDialog.getExistingDirectory()
                file = place + f"/{name}.pdf"
                pdf.output(file)
                with subprocess.Popen([os.path.abspath(file)], shell=True) as p:
                    pass

        pass

    def refill_table(self):
        self.ins = queries.get_movements()
        self.table.clearContents()
        self.table.setRowCount(len(self.ins))
        i = 0
        for med in self.ins:
            if med["entrada_salida"]:
                med["entrada_salida"] = "Entrada"
            else:
                med["entrada_salida"] = "Salida"
            self.table.setItem(i, 0, QTableWidgetItem(str(med["id"]).upper()))
            self.table.setItem(i, 1, QTableWidgetItem(med["fecha_entrega"].strftime("%d/%m/%Y")))
            self.table.setItem(i, 2, QTableWidgetItem(str(med["entrada_salida"]).upper()))
            self.table.setItem(i, 3, QTableWidgetItem(med["codigo"].upper()))
            self.table.setItem(i, 4, QTableWidgetItem(med["nombre"].upper()))
            self.table.setItem(i, 5, QTableWidgetItem(med["tipo"].upper()))
            self.table.setItem(i, 6, QTableWidgetItem(med["lote"].upper()))
            self.table.setItem(i, 8, QTableWidgetItem(str(med["unidades_por_paquete"]).upper()))
            self.table.setItem(i, 7, QTableWidgetItem(str(med["paquetes"]).upper()))
            self.table.setItem(i, 9, QTableWidgetItem(med["donador_retirador"].upper()))

            self.table.setItem(i, 10, QTableWidgetItem(med["fecha_creacion"].strftime("%d/%m/%Y")))
            self.table.setItem(i, 11, QTableWidgetItem(med["fecha_vencimiento"].strftime("%d/%m/%Y")))
            i += 1

