from datetime import datetime

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QPushButton, \
    QFormLayout, QDateEdit, QLineEdit, QMessageBox

import database
import queries
from views.MedForm import MedForm
from views.separator import separator


class Entrada(QWidget):

    def __init__(self, entrada_salida=None):
        super().__init__()
        self.setWindowTitle("Entrada")
        self.setStyleSheet("""#button {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            min-width: 300px;
            min-height: 30px;
            background-color: #00BFFF;
        
        }
        #med {
            max-height: 260px;
        }
        #scroll {
            max-width: 800px;
        }
        """)
        self.meds = []
        self.changes_made = QPushButton()
        self.main_layout = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.amount = QSpinBox()
        self.amount.setRange(-100000000, 1000000000)

        self.title = QLabel("CANTIDAD DE ENTRADAS")
        self.hbox.addWidget(self.title)
        self.hbox.addWidget(self.amount)
        self.main_layout.addLayout(self.hbox)
        self.flay = QFormLayout()
        self.fecha_de_entrega = QDateEdit()
        self.fecha_de_entrega.setDate(QDate.currentDate())
        self.fecha_de_entrega.setCalendarPopup(True)
        self.flay.addRow("FECHA DE ENTREGA", self.fecha_de_entrega)
        self.entrega = QLineEdit()

        self.flay.addRow("PERSONA QUE ENTREGA", self.entrega)
        self.main_layout.addLayout(self.flay)



        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll.setObjectName('scroll')
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.widget.setObjectName('scroll')
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.amount.valueChanged.connect(self.amount_changed)
        self.amount.setValue(4)
        self.amount.setRange(-100000000, 1000000000)
        self.main_layout.addWidget(self.scroll)
        self.setLayout(self.main_layout)
        self.buttons_layout = QHBoxLayout()
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.guardar_entrada)
        self.cancelar_btn = QPushButton("Cancelar")
        self.buttons_layout.addWidget(self.guardar_btn)
        self.buttons_layout.addWidget(self.cancelar_btn)
        self.main_layout.addLayout(self.buttons_layout)

    def amount_changed(self):
        for med in self.meds:
            self.vbox.removeWidget(med)
            med.deleteLater()
        self.meds = []
        for i in range(self.amount.value()):
            object = MedForm()
            object.setObjectName("med")
            self.vbox.addWidget(object)
            self.meds.append(object)


            pass
        pass

    def guardar_entrada(self):
        with database.db.atomic() as txn:
            for med in self.meds:
                codigo = med.codigo.text()
                nombre = med.nombre.text()
                tipo_id = med.tipo.currentData()
                cajas = med.cajas.value()
                unidades = med.unidades.value()
                lote = med.lote.text()
                fecha_vencimiento = datetime.strptime(med.fecha_vencimiento.text(), "%Y-%m-%d")
                fecha_fabricacion = datetime.strptime(med.fecha_fabricacion.text(), "%Y-%m-%d")
                selected_id = med.selected_id
                if selected_id is None:
                    ok = queries.create_med(codigo, nombre, tipo_id)
                    if ok:
                        selected_id = ok.id
                    else:
                        QMessageBox.warning(self, "Error", "NO SE HA CREADO EL MEDICAMENTO")
                if lote != '':
                    lote = queries.check_lote(lote)
                else:
                    lote = queries.no_def_lote()
                date = self.fecha_de_entrega.date()
                date = datetime.strptime(date.toString("yyyy-MM-dd"), "%Y-%m-%d")
                ok = queries.create_movement(selected_id,
                                             cajas,
                                             self.entrega.text(),
                                             True,
                                             date,
                                             fecha_vencimiento,
                                             fecha_fabricacion,
                                             lote,
                                             unidades)
                if ok:
                    pass
                else:
                    QMessageBox.warning(self, "Error", "NO SE HA CREADO LA ENTRADA")
            QMessageBox.information(self, "Exito", "ENTRADA CREADA")
            self.changes_made.click()
            self.amount.setValue(2)
            self.amount.setValue(4)
        pass
