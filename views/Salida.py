import os
import subprocess
from datetime import datetime

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QPushButton, \
    QFormLayout, QDateEdit, QLineEdit, QMessageBox, QInputDialog, QFileDialog

import database
import queries
from report_template import DailyReportPDF
from views.MedForm import MedForm
from views.SalidaForm import SalidaForm
from views.separator import separator


class Salida(QWidget):

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

        self.title = QLabel("CANTIDAD DE SALIDAS")
        self.hbox.addWidget(self.title)
        self.hbox.addWidget(self.amount)
        self.main_layout.addLayout(self.hbox)
        self.flay = QFormLayout()
        self.fecha_de_retiro = QDateEdit()
        self.fecha_de_retiro.setDate(QDate.currentDate())
        self.fecha_de_retiro.setCalendarPopup(True)
        self.flay.addRow("FECHA DE RETIRO", self.fecha_de_retiro)
        self.retiro = QLineEdit()

        self.flay.addRow("PERSONA QUE RETIRA", self.retiro)
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
        self.guardar_btn.clicked.connect(self.guardar_salida)
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

    def guardar_salida(self):
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
                date = self.fecha_de_retiro.date()
                date = datetime.strptime(date.toString("yyyy-MM-dd"), "%Y-%m-%d")
                ok = queries.create_movement(selected_id,
                                             cajas,
                                             self.retiro.text(),
                                             False,
                                             date,
                                             fecha_vencimiento,
                                             fecha_fabricacion,
                                             lote,
                                             unidades)
                if ok:
                    pass
                else:
                    QMessageBox.warning(self, "Error", "NO SE HA REGISTRADO LA SALIDA")
            QMessageBox.information(self, "Exito", "SALIDA REGISTRADA")
            self.changes_made.click()
            self.get_report_data()
        pass
    
    def get_report_data(self):
        ok = QMessageBox.question(self, "Reporte", "¿Desea generar el reporte?", QMessageBox.Yes | QMessageBox.No)
        if ok == QMessageBox.Yes:
            self.modal_window = None
            self.modal_window = SalidaForm()
            self.modal_window.show()
            self.modal_window.report_btn.clicked.connect(self.generate_report)

        pass

    def generate_report(self):        
    
        print("making")
        TABLE_DATA = [[
            "CODIGO",
            "NOMBRE",
            "CAJAS",
            "UNDxCAJA",
            "F. ENTREGA"]]
        nombre_emisor = self.modal_window.get_nombre_emisor()
        titulo_emisor = self.modal_window.get_titulo_emisor()
        tipo_emisor = self.modal_window.get_tipo_emisor()
        credencial_emisor = self.modal_window.get_credencial_emisor()
        nombre_receptor = self.modal_window.get_nombre_receptor()
        titulo_receptor = self.modal_window.get_titulo_receptor()
        tipo_receptor = self.modal_window.get_tipo_receptor()
        credencial_receptor = self.modal_window.get_credencial_receptor()

        for med in self.meds:
            TABLE_DATA.append([
                str(med.codigo.text()),
                str(med.nombre.text()),
                str(med.cajas.value()),
                str(med.unidades.value()),
                str(self.fecha_de_retiro.date().toString("yyyy-MM-dd"))
            ])
        pdf = DailyReportPDF()
        pdf.add_page()
        pdf.set_font("Times", size=11)
        text = (f'EL {titulo_receptor} "{nombre_receptor}" DE {tipo_receptor} "{credencial_receptor}" HA RECIBIDO '
                f'POR MEDIO DE EL {titulo_emisor} "{nombre_emisor}" DE {tipo_emisor} '
                f'"{credencial_emisor}" LOS MEDICAMENTOS LISTADOS DEBAJO '
                f"DE EL INVENTARIO DE MEDICAMENTOS DE LA POLICIA DE SAN FRANCISCO. "
                f"FECHA {datetime.today().strftime('%d/%m/%Y')}")

        pdf.write(text=text)
        pdf.set_font(size=7)
        pdf.ln(10)
        with pdf.table(
                col_widths=(18, 45, 10, 10, 12),
                line_height=5
        ) as table:
            for data_row in TABLE_DATA:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        pdf.ln(20)
        name, ok = QInputDialog.getText(self, "NOMBRE", "NOMBRE DEL REPORTE", QLineEdit.Normal,
                                        f"REPORTE MOVIMIENTOS {datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}")
        pdf.image("FIRMAS.png", w=200, h=30)
        place = QFileDialog.getExistingDirectory()
        file = place + f"/{name}.pdf"
        pdf.output(file)
        with subprocess.Popen([os.path.abspath(file)], shell=True) as p:
            pass
        self.modal_window.close()
    pass
