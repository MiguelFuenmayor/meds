from datetime import datetime

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QSpinBox, QDateEdit, QFormLayout, QMessageBox

import queries
from views.separator import separator


class MedForm(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Med")
        self.setStyleSheet("""#button {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            min-width: 300px;
            min-height: 30px;
            background-color: #00BFFF;
        }""")
        self.main_layout = QFormLayout()
        self.setLayout(self.main_layout)
        self.codigo = QLineEdit()
        self.codigo.textChanged.connect(self.check_code)
        self.selected_id = None
        self.nombre = QLineEdit()
        self.tipo = QComboBox()
        self.tipo_recharge()
        self.main_layout.addRow("CODIGO", self.codigo)
        self.main_layout.addRow("NOMBRE", self.nombre)
        self.main_layout.addRow("TIPO", self.tipo)
        self.cajas = QSpinBox()
        self.cajas.setRange(-10000000, 100000)
        self.main_layout.addRow("CAJAS", self.cajas)
        self.unidades = QSpinBox()
        self.unidades.setRange(-1000000, 100000)
        self.main_layout.addRow("UNIDADES", self.unidades)
        self.lote = QLineEdit()
        self.main_layout.addRow("LOTE", self.lote)
        self.fecha_vencimiento = QDateEdit()
        self.fecha_vencimiento.setDate(QDate.currentDate())
        self.fecha_vencimiento.setCalendarPopup(True)
        self.fecha_vencimiento.setDisplayFormat("yyyy-MM-dd")
        self.fecha_fabricacion = QDateEdit()
        self.fecha_fabricacion.setDisplayFormat("yyyy-MM-dd")
        self.fecha_fabricacion.setDate(QDate.currentDate())
        self.fecha_fabricacion.setCalendarPopup(True)
        self.main_layout.addRow("FECHA DE VENCIMIENTO", self.fecha_vencimiento)

        self.main_layout.addRow("FECHA DE FABRICACION", self.fecha_fabricacion)
        self.main_layout.addRow("----------------------", separator())

    def check_code(self):
        med = queries.check_code(self.codigo.text())
        if med == []:
            self.selected_id = None
            self.nombre.setText("")
            self.unidades.setValue(0)
            self.tipo.setCurrentIndex(0)
            self.nombre.setEnabled(True)
            self.unidades.setEnabled(True)
            self.tipo.setEnabled(True)
            return False
        med = med[0]
        self.selected_id = med['id']
        self.nombre.setText(med['nombre'])
        self.nombre.setEnabled(False)
        self.tipo.setCurrentIndex(self.tipo.findData(med['tipo_id']))
        self.tipo.setEnabled(False)
        pass

    def tipo_recharge(self):
        self.tipo.clear()
        for tipo in queries.get_tipo_meds():
            self.tipo.addItem(tipo['name'], tipo['id'])


