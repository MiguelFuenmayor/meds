from collections import Counter
from datetime import datetime

from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLineEdit, QComboBox, QSpinBox, QFormLayout, \
    QMessageBox, QHBoxLayout, QInputDialog, QLabel
from pymsgbox import buttonsFrame

import queries


class MedEdit(QWidget):
    def __init__(self, med_code):
        super().__init__()
        self.setWindowTitle("Editar Medicamento")
        self.setStyleSheet("""#button {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            min-width: 300px;
            min-height: 30px;
            background-color: #00BFFF;
        }""")
        self.changes_made = QPushButton()
        self.main_layout = QFormLayout()
        self.setLayout(self.main_layout)
        self.med = queries.get_full_med(med_code)
        counter = Counter()
        unit_counter = Counter()
        self.og_med = self.med[0]
        for med in self.med:
            if med['entrada_salida'] is None:
                continue
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
        self.og_paquetes = counter[self.og_med['codigo']]
        self.og_unidades = unit_counter[self.og_med['codigo']]
        self.codigo = QLineEdit()
        self.codigo.setText(self.og_med['codigo'])
        self.codigo.setPlaceholderText("Codigo del Medicamento")
        self.main_layout.addRow("CODIGO: ", self.codigo)
        self.nombre = QLineEdit()
        self.nombre.setText(self.og_med['nombre'])
        self.nombre.setPlaceholderText("Nombre del Medicamento")
        self.main_layout.addRow("NOMBRE: ", self.nombre)
        self.tipo = QComboBox()
        self.main_layout.addRow("TIPO: ", self.tipo)
        for tipo in queries.get_tipo_meds():
            self.tipo.addItem(tipo['name'], tipo['id'])
        self.tipo.setCurrentIndex(self.tipo.findData(self.og_med['tipo_id']))
        self.cajas = QPushButton("Editar por cajas")
        self.cajas.clicked.connect(self.modify_cajas)
        self.main_layout.addRow("CAJAS: ", self.cajas)
        # self.cajas = QSpinBox()
        # self.cajas.setRange(-1000000, 100000)
        # self.cajas.setValue(counter[self.og_med['codigo']])
        # self.main_layout.addRow("ADVERTENCIA:", QLabel("Edite solo uno de los datos (cajas, unidades) a la vez"))
        # self.main_layout.addRow("CAJAS: ", self.cajas)
        self.unidades = QPushButton("Editar por unidades")
        self.unidades.clicked.connect(self.modify_units)
        self.main_layout.addRow("UNIDADES: ", self.unidades)
        # self.unidades = QSpinBox()
        # self.unidades.setRange(-10000000,100000)
        # self.unidades.setValue(unit_counter[self.og_med['codigo']])
        # self.main_layout.addRow("UNIDADES: ",  self.unidades)
        self.buttons_layout = QHBoxLayout()
        buttons_widget = QWidget()
        buttons_widget.setLayout(self.buttons_layout)
        self.main_layout.addWidget(buttons_widget)
        self.edit_button = QPushButton("EDITAR")
        self.edit_button.clicked.connect(self.update_med)
        self.buttons_layout.addWidget(self.edit_button)

        self.cancel_btn = QPushButton("CANCELAR")
        self.cancel_btn.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.cancel_btn)

    def update_med(self):
        tipo = self.tipo.currentData()
        nombre = self.nombre.text()
        codigo = self.codigo.text()
        ok = queries.update_med(self.og_med['id'], codigo, nombre, tipo)
        if ok:
            QMessageBox.information(self, "Meds", "Medicamento editado exitosamente")
        else:
            QMessageBox.warning(self, "Meds", "No se ha podido editar el medicamento")
        self.changes_made.click()
        self.close()

    def modify_cajas(self):
        old_value = int(self.og_paquetes)
        new_value, ok = QInputDialog.getInt(self, "Cajas", "Nueva cantidad total de Cajas:", old_value)
        diff = new_value - old_value
        if not ok:
            QMessageBox.warning(self, "Meds", "No se ha podido modificar las cajas, porque no ingreso una cantidad"
                                              " de unidades por paquete.")
            return
        lote_id = queries.no_def_lote()
        date = datetime.today()
        print(new_value, old_value, diff)
        if diff > 0:
            in_out = True
        else:
            in_out = False
        diff = abs(diff)
        queries.create_movement(med_id=self.og_med['id'],
                                paquetes=diff,
                                donador_retirador="No Definido",
                                entrada_salida=in_out,
                                fecha_entrega=date,
                                fecha_creacion=date,
                                fecha_vencimiento=date,
                                lote_id=lote_id,
                                unidades_por_paquete=0)
        self.changes_made.click()
        self.close()

    def modify_units(self):
        old_value = int(self.og_unidades)
        new_value, ok = QInputDialog.getInt(self, "Unidades a añadir", "Nueva Cantidad Total de Unidades:", old_value)
        diff = new_value - old_value
        print(new_value, old_value, diff)
        lote_id = queries.no_def_lote()
        date = datetime.today()
        if diff > 0:
            in_out = True
        else:
            in_out = False
        diff = abs(diff)
        queries.create_movement(med_id=self.og_med['id'],
                                paquetes=0,
                                donador_retirador="No Definido",
                                entrada_salida=in_out,
                                fecha_entrega=date,
                                fecha_creacion=date,
                                fecha_vencimiento=date,
                                lote_id=lote_id,
                                unidades_por_paquete=diff)
        self.changes_made.click()
        self.close()

    def change_tipo(self):

        pass

    def change_nombre(self):
        pass

    def change_codigo(self):
        pass

