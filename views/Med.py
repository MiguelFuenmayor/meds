from PySide6.QtWidgets import QVBoxLayout, QWidget, QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, \
    QSpinBox, QComboBox, QPushButton, QFormLayout, QInputDialog

import queries
from database import db


class Med(QWidget):
    def __init__(self, med_id):
        super().__init__()
        self.setWindowTitle("Meds")
        self.changes_made = QPushButton()
        self.setMinimumWidth(400)
        self.main_layout = QFormLayout()
        self.setLayout(self.main_layout)
        self.med = queries.get_med(med_id)
        self.codigo = QLineEdit()
        self.codigo.setText(self.med['codigo'])
        self.nombre = QLineEdit()
        self.nombre.setText(self.med['nombre'])
        self.tipo = QComboBox()
        for t in queries.get_tipo_meds():
            self.tipo.addItem(t['name'], t['id'])
        self.tipo.setCurrentText(self.med['tipo'])

        self.main_layout.addRow("CODIGO", self.codigo)
        self.main_layout.addRow("NOMBRE", self.nombre)
        self.main_layout.addRow("TIPO", self.tipo)
        self.cancel_btn = QPushButton("CANCELAR")
        self.cancel_btn.clicked.connect(self.close)
        self.edit_button = QPushButton("EJECUTAR EDICION")
        self.edit_button.clicked.connect(self.edit_med)
        self.delete_btn = QPushButton("ELIMINAR")
        self.delete_btn.clicked.connect(self.delete_med)
        self.main_layout.addWidget(self.edit_button)
        self.main_layout.addWidget(self.delete_btn)
        self.main_layout.addWidget(self.cancel_btn)


    def edit_med(self):
        selected_id = int(self.med['id'])
        codigo = self.codigo.text()
        nombre = self.nombre.text()
        tipo_id = self.tipo.currentData()
        ok = queries.update_med(selected_id, codigo, nombre, tipo_id)
        if ok == 1:
            QMessageBox.information(self, "Meds", "Medicamento editado exitosamente")
            self.changes_made.click()
        else:
            QMessageBox.warning(self, "Meds", "No se ha podido editar el medicamento")

    def delete_med(self):
        selected_id = int(self.med['id'])
        movements = queries.get_all_med_movements(selected_id)
        QMessageBox.warning(self, "ELIMINAR?", "Seguro que quieres eliminar este medicamento? Hay un "
                                                      f"total de {len(movements)} movimientos relacionados a el. Borrarlo "
                                                      f"resultara en la eliminacion de todos sus movimientos, lo que puede "
                                                      f"causar errores en las cuentas con respecto a la realidad. "
                                                      f"Escriba 'SI LO ENTIENDO' para confirmar")
        text, ok = QInputDialog.getText(self, "Meds", "CONFIRMACION")
        if text == "SI LO ENTIENDO":
            with db.atomic() as txn:
                for movement in movements:
                    queries.delete_movement(movement['id'])
                try:
                    ok = queries.delete_med(selected_id)
                except Exception as e:
                    print(e)
                    msg = str(e)
                    ok = 0
            if ok == 1:
                QMessageBox.information(self, "Meds", "Medicamento eliminado exitosamente")
            else:
                QMessageBox.warning(self, "Meds", "No se ha podido eliminar el medicamento, esto "
                                                  "puede ocurrir si hay movimientos relacionados a este medicamento. "
                                                  "Puede editarlo si gusta. Codigo de error: " + msg)

        elif ok and text != "SI LO ENTIENDO":
            QMessageBox.warning(self, "Meds", "No ha ingresado el texto de confirmacion correctamente")
        else:
            QMessageBox.information(self, "Meds", "SE CANCELO EL BORRADO DEL MEDICAMENTO")