from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, \
    QPushButton, QMessageBox

import queries
from database import *
from views.UpdateMovement import UpdateMovement


class BaseDatos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meds")
        self.selected_id = None
        self.changes_made = QPushButton()
        self.changes_made.clicked.connect(self.refill_table)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QTableWidget()
        self.ins = queries.get_movements()
        self.setStyleSheet("""
        QTableWidget {
            font-size: 11px;
        }
        QHeaderView {
            font-size: 13px;
        }
        """)
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
        self.update_btn = QPushButton("Actualizar")
        self.buttons_layout.addWidget(self.update_btn)
        self.update_btn.clicked.connect(self.update_table)
        self.delete_btn = QPushButton("Eliminar")
        self.buttons_layout.addWidget(self.delete_btn)
        self.delete_btn.clicked.connect(self.delete_action)
        self.main_layout.addLayout(self.buttons_layout)

    def update_table(self):
        self.selected_id = self.table.item(self.table.selectedItems()[0].row(), 0).text()
        self.modal_window = None
        self.modal_window = UpdateMovement(self.selected_id)
        self.modal_window.changes_made.clicked.connect(self.changes_made_action)
        self.modal_window.setWindowModality(Qt.ApplicationModal)
        self.modal_window.show()

    def delete_action(self):
        self.selected_id = self.table.item(self.table.selectedItems()[0].row(), 0).text()
        ok = QMessageBox.warning(self, "Advertencia", "¿Desea eliminar la medicina seleccionada?", QMessageBox.Yes | QMessageBox.No)
        if ok == QMessageBox.Yes:
            queries.delete_movement(self.selected_id)

            self.refill_table()
            self.changes_made_action()
            QMessageBox.information(self, "Exito", "El movimiento ha sido eliminado")

    def changes_made_action(self):
        self.changes_made.click()

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



