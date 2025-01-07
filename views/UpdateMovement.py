from datetime import datetime

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QComboBox, \
    QMessageBox, QFormLayout

import queries


class UpdateMovement(QWidget):
    def __init__(self, movement_id):
        super().__init__()
        self.setStyleSheet("""
        #button {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            min-width: 300px;
            min-height: 100px;
            background-color: #00BFFF;
        }
        """)
        self.setWindowTitle("Meds")
        self.changes_made = QPushButton()
        self.movement = queries.get_movements_by_id(movement_id)
        self.main_layout = QFormLayout()
        self.setLayout(self.main_layout)
        self.paquetes = QSpinBox()
        self.paquetes.setRange(-100000, 1000000)
        self.paquetes.setValue(self.movement['paquetes'])
        self.main_layout.addRow("PAQUETES", self.paquetes)
        self.unidades = QSpinBox()
        self.unidades.setRange(-100000, 1000000)
        self.unidades.setValue(int(self.movement['unidades_por_paquete']))
        self.main_layout.addRow("UNIDADES", self.unidades)
        self.donador_retirador = QLineEdit()
        self.donador_retirador.setText(self.movement['donador_retirador'])
        self.main_layout.addRow("DONADOR/RETIRADOR", self.donador_retirador)
        self.fecha_entrega = QDateEdit()
        self.fecha_entrega.setDisplayFormat("dd-MM-yyyy")
        self.fecha_entrega.setCalendarPopup(True)
        date = datetime.strptime(self.movement['fecha_entrega'].strftime("%Y-%m-%d"), "%Y-%m-%d")
        self.fecha_entrega.setDate(date)
        self.main_layout.addRow("FECHA ENTREGA", self.fecha_entrega)
        self.fecha_vencimiento = QDateEdit()
        self.fecha_vencimiento.setCalendarPopup(True)
        self.fecha_vencimiento.setDisplayFormat("dd-MM-yyyy")
        date = datetime.strptime(self.movement['fecha_vencimiento'].strftime("%Y-%m-%d"), "%Y-%m-%d")
        self.fecha_vencimiento.setDate(date)
        self.main_layout.addWidget(self.fecha_vencimiento)
        self.fecha_creacion = QDateEdit()
        self.fecha_creacion.setDisplayFormat("dd-MM-yyyy")
        self.fecha_creacion.setCalendarPopup(True)
        date = datetime.strptime(self.movement['fecha_creacion'].strftime("%Y-%m-%d"), "%Y-%m-%d")
        self.fecha_creacion.setDate(date)
        self.main_layout.addRow("FECHA CREACION", self.fecha_creacion)
        self.entrada_salida = QComboBox()
        self.entrada_salida.addItem("Entrada", True)
        self.entrada_salida.addItem("Salida", False)
        self.entrada_salida.setCurrentIndex(self.entrada_salida.findData(self.movement['entrada_salida']))
        self.main_layout.addRow("ENTRADA/SALIDA", self.entrada_salida)

        self.buttons_layout = QHBoxLayout()
        self.update_btn = QPushButton("Actualizar")
        self.update_btn.setObjectName("button")
        self.buttons_layout.addWidget(self.update_btn)
        self.update_btn.clicked.connect(self.update_action)
        self.close_btn = QPushButton("Cancelar")
        self.close_btn.setObjectName("button")
        self.close_btn.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.close_btn)
        dummy_widget = QWidget()
        dummy_widget.setLayout(self.buttons_layout)
        self.main_layout.addWidget(dummy_widget)

    def update_action(self):
        if self.paquetes.value() == 0:
            QMessageBox.warning(self, "Error", "No puede haber 0 paquetes")
            return
        if self.donador_retirador.text() == "":
            QMessageBox.warning(self, "Error", "No puede haber un donador o retirador vacio")
            return

        queries.update_movement(id=self.movement['id'],
                                med_id=self.movement['med_id'],
                                paquetes=self.paquetes.value(),
                                unidades_por_paquete=self.unidades.value(),
                                donador_retirador=self.donador_retirador.text(),
                                entrada_salida=self.entrada_salida.currentData(),
                                lote_id=self.movement['lote_id'],
                                fecha_entrega=datetime.strptime(self.fecha_entrega.date().toString("yyyy-MM-dd"), "%Y-%m-%d"),
                                fecha_vencimiento=datetime.strptime(self.fecha_vencimiento.date().toString("yyyy-MM-dd"), "%Y-%m-%d"),
                                fecha_creacion=datetime.strptime(self.fecha_creacion.date().toString("yyyy-MM-dd"), "%Y-%m-%d"),

                                )
        self.close()
        self.changes_made.click()




