from datetime import datetime

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, \
    QLabel, QWidget, QSizePolicy, QStackedLayout, QStackedWidget, QDateEdit, QMessageBox, QRadioButton, QSpinBox, \
    QInputDialog, QFileDialog

import queries
from report_template import DailyReportPDF
from views.BulkReport import BulkReport
from views.Entrada import Entrada
from views.Meds import Meds
from views.Reports import Reports
from views.Salida import Salida
from views.Searcher import Searcher
from views.Totals import Totals
from views.VerBaseDatos import BaseDatos


class Home(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meds")
        self.changes_made = QPushButton()
        self.selected_id = None
        self.setStyleSheet(
            """
            #title {
                font-size: 54px;
                font-weight: bold;
                text-align: center;
            }
            #subtitle {
                font-size: 24px;
                text-align: left;
                font-weight: bold;
            }
            #button {
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                min-width: 200px;
                min-height: 50px;
                background-color: #00BFFF;
            }
            #input {
                font-size: 24px;
                min-height: 30px;
                max-width: 500px;
            }
            QLabel {
                font-size: 24px;
            }
            """
        )
        self.main_layout = QVBoxLayout()
        self.main_dummy = QWidget()
        self.main_dummy.setLayout(self.main_layout)
        self.addWidget(self.main_dummy)

        self.h_lay = QHBoxLayout()
        self.h_lay.addStretch(1)
        self.form_layout = QFormLayout()
        self.form_layout_dummy = QWidget()
        self.form_layout_dummy.setLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.codigo = QLineEdit()
        self.codigo.setObjectName("input")
        self.codigo.textChanged.connect(self.check_code)
        self.codigo.setMinimumWidth(600)

        self.nombre = QLineEdit()
        self.nombre.setObjectName("input")
        self.nombre.setMinimumWidth(600)
        self.nombre.setAlignment(Qt.AlignCenter)
        self.tipo = QComboBox()
        self.tipo.setObjectName("input")
        self.tipo_recharge()
        self.tipo.setMinimumWidth(600)

        self.paquetes = QSpinBox()
        self.paquetes.setRange(-1000000, 10000)
        self.paquetes.setObjectName("input")
        self.paquetes.setMinimumWidth(600)
        self.paquetes.setAlignment(Qt.AlignCenter)
        self.unidades_por_paquete = QSpinBox()
        self.unidades_por_paquete.setRange(-1000000, 10000000)
        self.unidades_por_paquete.setObjectName("input")
        self.unidades_por_paquete.setMinimumWidth(600)
        self.unidades_por_paquete.setAlignment(Qt.AlignCenter)
        self.lote = QLineEdit()
        self.lote.setObjectName("input")
        self.lote.setMinimumWidth(600)
        self.lote.setAlignment(Qt.AlignCenter)
        self.proveedor_donador = QLineEdit()
        self.proveedor_donador.setObjectName("input")
        self.proveedor_donador.setMinimumWidth(600)
        self.proveedor_donador.setAlignment(Qt.AlignCenter)

        self.fecha_fabricacion = QDateEdit()
        self.fecha_fabricacion.setDate(QDate.currentDate())
        self.fecha_fabricacion.setDisplayFormat("dd/MM/yyyy")
        self.fecha_fabricacion.setCalendarPopup(True)
        self.fecha_fabricacion.setObjectName("input")
        self.fecha_fabricacion.setMinimumWidth(600)
        self.fecha_fabricacion.setAlignment(Qt.AlignCenter)
        self.fecha_vencimiento = QDateEdit()
        self.fecha_vencimiento.setDate(QDate.currentDate())
        self.fecha_vencimiento.setDisplayFormat("dd/MM/yyyy")
        self.fecha_vencimiento.setCalendarPopup(True)
        self.fecha_vencimiento.setObjectName("input")
        self.fecha_vencimiento.setMinimumWidth(600)
        self.fecha_vencimiento.setAlignment(Qt.AlignCenter)
        self.fecha_entrega = QDateEdit()
        self.fecha_entrega.setObjectName("input")
        self.fecha_entrega.setDisplayFormat("dd/MM/yyyy")
        self.fecha_entrega.setCalendarPopup(True)
        self.fecha_entrega.setDate(QDate.currentDate())
        self.fecha_entrega.setMinimumWidth(600)
        self.fecha_entrega.setAlignment(Qt.AlignCenter)
        title_2 = QLabel("MEDICAMENTO")
        title_2.setObjectName("subtitle")
        self.form_layout.addWidget(title_2)
        self.form_layout.addRow("CODIGO", self.codigo)
        self.form_layout.addRow("NOMBRE", self.nombre)
        self.form_layout.addRow("TIPO", self.tipo)
        self.form_layout.addRow("CAJAS", self.paquetes)
        self.form_layout.addRow("CANTIDAD POR CAJA", self.unidades_por_paquete)
        in_out = QHBoxLayout()

        self.is_in = QRadioButton("ENTRADA")
        self.is_in.setChecked(True)
        self.is_in.setObjectName("input")
        in_out.addWidget(self.is_in)

        self.is_out = QRadioButton("SALIDA")
        self.is_out.setObjectName("input")
        in_out.addWidget(self.is_out)
        self.form_layout.addRow("LOTE", self.lote)
        self.form_layout.addRow("DONADOR/RETIRADOR", self.proveedor_donador)
        self.form_layout.addRow("F. FABRICACION", self.fecha_fabricacion)
        self.form_layout.addRow("F. VENCIMIENTO", self.fecha_vencimiento)
        self.form_layout.addRow("F. ENTREGA", self.fecha_entrega)
        self.form_layout.addRow("ENTRADA/SALIDA", in_out)
        self.regist_btn = QPushButton("GUARDAR")
        self.regist_btn.clicked.connect(self.registrar)
        self.regist_btn.setObjectName("button")

        self.clean_btn = QPushButton("NUEVO")
        self.clean_btn.clicked.connect(self.clean)
        self.clean_btn.setObjectName("button")
        self.db_btn = QPushButton("VER BASE DE DATOS")
        self.db_btn.clicked.connect(self.ver_base)
        self.db_btn.setObjectName("button")
        self.totals_btn = QPushButton("TOTALES")
        self.totals_btn.clicked.connect(self.totals_action)
        self.totals_btn.setObjectName("button")
        self.search_btn = QPushButton("BUSCAR")
        self.search_btn.setObjectName("button")
        # self.search_btn.clicked.connect(self.search)
        self.buttons_layout.addWidget(self.regist_btn)
        self.buttons_layout.addWidget(self.clean_btn)
        self.buttons_layout.addWidget(self.search_btn)
        self.buttons_layout.addWidget(self.db_btn)
        self.buttons_layout.addWidget(self.totals_btn)
        self.title = QLabel("REGISTRO DE MEDICAMENTOS POLICIALES")
        self.title.setObjectName("title")
        self.title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)
        self.h_lay.addWidget(self.form_layout_dummy)

        self.main_layout.addLayout(self.h_lay)
        self.main_layout.addLayout(self.buttons_layout)
        self.h_lay.addStretch(1)
        self.base = BaseDatos()
        self.addWidget(self.base)
        self.searcher = Searcher()
        self.addWidget(self.searcher)
        self.totals = Totals()
        self.addWidget(self.totals)
        self.reports = Reports()
        self.addWidget(self.reports)
        self.meds = Meds()
        self.addWidget(self.meds)
        self.entrada = Entrada()
        self.addWidget(self.entrada)
        self.salida = Salida()
        self.addWidget(self.salida)

    def check_code(self):
        print(self.codigo.text())
        med = queries.check_code(self.codigo.text())
        if med == []:
            self.selected_id = None
            self.nombre.setText("")
            self.unidades_por_paquete.setValue(0)
            self.tipo.setCurrentIndex(0)
            self.nombre.setEnabled(True)
            self.unidades_por_paquete.setEnabled(True)
            self.tipo.setEnabled(True)
            return False
        med = med[0]
        self.selected_id = med['id']
        self.nombre.setText(med['nombre'])
        self.nombre.setEnabled(False)
        self.tipo.setCurrentIndex(self.tipo.findData(med['tipo_id']))
        self.tipo.setEnabled(False)
        pass

    def clean(self):
        self.codigo.setText("")
        self.nombre.setText("")
        self.unidades_por_paquete.setValue(0)
        self.lote.setText("")
        self.proveedor_donador.setText("")
        self.is_in.setChecked(True)
        self.selected_id = 0
        self.paquetes.setValue(0)
        self.tipo.setCurrentIndex(0)
        self.fecha_entrega.setDate(QDate.currentDate())
        self.fecha_fabricacion.setDate(QDate.currentDate())
        self.fecha_vencimiento.setDate(QDate.currentDate())
        pass

    def totals_action(self):
        self.setCurrentIndex(3)
        pass

    def tipo_recharge(self):
        self.tipo.clear()
        for tipo in queries.get_tipo_meds():
            self.tipo.addItem(tipo['name'], tipo['id'])

    def ver_base(self):
        self.setCurrentWidget(self.base)

    def verifications(self):
        ok = True
        msg = []
        if self.codigo.text() == "":
            ok = False
            msg.append("El campo 'Código' es obligatorio.")
        if self.nombre.text() == "":
            ok = False
            msg.append("El campo 'Nombre' es obligatorio.")
        if self.paquetes.text() == "":
            ok = False
            msg.append("El campo 'Paquetes' es obligatorio.")
        if self.unidades_por_paquete.text() == "":
            ok = False
            msg.append("El campo 'Unidades por paquete' es obligatorio.")
        if self.lote.text() == "":
            ok = False
            msg.append("El campo 'Lote' es obligatorio.")
        if self.proveedor_donador.text() == "":
            ok = False
            msg.append("El campo 'Proveedoredor/donador' es obligatorio.")
        if self.fecha_fabricacion.text() == "":
            ok = False
            msg.append("El campo 'Fecha de fabricación' es obligatorio.")
        if self.fecha_vencimiento.text() == "":
            ok = False
            msg.append("El campo 'Fecha de vencimiento' es obligatorio.")
        if self.fecha_entrega.text() == "":
            ok = False
            msg.append("El campo 'Fecha de entrega' es obligatorio.")
        return ok, msg

    def registrar(self):
        print(self.is_out.isChecked())
        ok, msg = self.verifications()
        if ok and msg == []:
            codigo = self.codigo.text()
            nombre = self.nombre.text()
            tipo = self.tipo.currentData()
            paquetes = self.paquetes.value()
            unidades_por_paquete = self.unidades_por_paquete.value()
            lote = self.lote.text()
            proveedor_donador = self.proveedor_donador.text()
            fecha_fabricacion = datetime.strptime(self.fecha_fabricacion.date().toString("dd/MM/yyyy"), "%d/%m/%Y")
            fecha_vencimiento = datetime.strptime(self.fecha_vencimiento.date().toString("dd/MM/yyyy"), "%d/%m/%Y")
            fecha_entrega = datetime.strptime(self.fecha_entrega.date().toString("dd/MM/yyyy"), "%d/%m/%Y")
            if self.selected_id is None:
                ok = queries.create_med(codigo, nombre, tipo)
                if ok:
                    self.selected_id = ok.id
                else:
                    QMessageBox.warning(self, "Error", "NO SE HA CREADO EL MEDICAMENTO")

            lote = queries.check_lote(lote)
            if lote:
                lote = lote.id
                ok = queries.create_movement(self.selected_id,
                                             paquetes,
                                             proveedor_donador,
                                             self.is_in.isChecked(),
                                             fecha_entrega,
                                             fecha_vencimiento,
                                             fecha_fabricacion,
                                             lote,
                                             unidades_por_paquete)
            if self.is_out.isChecked():
                self.out_report()
            if ok:
                self.changes_made.click()
                self.clean()
                self.base.refill_table()

        else:
            QMessageBox.warning(self, "Error", "\n".join(msg))
        self.changes_made.click()

    def out_report(self):
        entrega, ok = QInputDialog.getText(self, "Reporte de salida", "NOMBRE DE QUIEN ENTREGA:")
        credencial_2, ok = QInputDialog.getText(self, "Reporte de salida", "CREDENCIAL DE QUIEN ENTREGA:")
        credencial, ok = QInputDialog.getText(self, "Reporte de salida", "CREDENCIAL DE QUIEN RECIBE:")
        pdf = DailyReportPDF()
        text = (f'EL FUNCIONARIO "{self.proveedor_donador.text()}" DE CREDENCIAL "{credencial}" HA RECIBIDO '
                f'POR MEDIO DE EL FUNCIONARIO "{entrega}" DE CREDENCIAL '
                f'"{credencial_2}" LOS MEDICAMENTOS LISTADOS DEBAJO '
                f"DE EL INVENTARIO DE MEDICAMENTOS DE LA POLICIA DE SAN FRANCISCO. "
                f"FECHA {datetime.today().strftime('%d/%m/%Y')}")
        pdf.add_page()
        pdf.ln(10)
        pdf.set_font(size=12)
        pdf.write(text=text)
        pdf.ln(20)
        table_data = [
            ["CODIGO", "MEDICAMENTO", "U.PAQ", "PAQUETES", "TIPO"],
            [str(self.codigo.text()), str(self.nombre.text()),
             str(self.unidades_por_paquete.value()), str(self.paquetes.value()), str(self.tipo.currentText())]
        ]
        with pdf.table(cell_fill_color=200, cell_fill_mode="ROWS", col_widths=[15, 30, 20, 15, 25]) as table:
            for data_row in table_data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

        pdf.ln(20)
        pdf.image("FIRMAS.png", w=200, h=30)

        place = QFileDialog.getExistingDirectory(self, "Select Directory")
        if place:
            pdf.output(f"{place}/REPORTE_DE_SALIDA_{datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}.pdf")

        pass