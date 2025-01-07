from PySide6.QtWidgets import QWidget, QTableWidget, QLineEdit, QVBoxLayout, QRadioButton, QHBoxLayout, \
    QTableWidgetItem, QHeaderView, QPushButton

import queries
from views.Med import Med


class Searcher(QWidget):

    def __init__(self):
        super().__init__()
        self.modal_window = None
        self.setWindowTitle("Meds")
        main_layout = QVBoxLayout()
        self.search = QLineEdit()
        self.changes_made = QPushButton()
        main_layout.addWidget(self.search)
        h_lay = QHBoxLayout()
        self.med_check = QRadioButton("Medicamentos")
        self.med_check.setChecked(True)
        self.med_type_check = QRadioButton("Tipos de Medicamentos")
        self.lote_check = QRadioButton("Lote")
        self.movement_check = QRadioButton("Movimientos")
        h_lay.addWidget(self.med_check)
        h_lay.addWidget(self.med_type_check)
        h_lay.addWidget(self.lote_check)
        h_lay.addWidget(self.movement_check)
        main_layout.addLayout(h_lay)
        self.results = None
        self.results_table = QTableWidget()
        self.results_table.itemDoubleClicked.connect(self.open_med)
        main_layout.addWidget(self.results_table)
        self.results_logic()
        self.search.textChanged.connect(self.results_logic)
        self.med_check.clicked.connect(self.results_logic)
        self.movement_check.clicked.connect(self.results_logic)
        self.lote_check.clicked.connect(self.results_logic)
        self.med_type_check.clicked.connect(self.results_logic)
        self.setLayout(main_layout)

    def results_logic(self):
        self.results_table.clear()
        if self.med_check.isChecked():
            self.results = queries.search_med(self.search.text())

            columns = ["id", "codigo", "nombre", "tipo"]
        elif self.med_type_check.isChecked():
            print("lookin med_type")
            self.results = queries.search_med_type(self.search.text())
            columns = ["id", "nombre", "productos"]
        elif self.lote_check.isChecked():
            self.results = queries.search_lote(self.search.text())
            columns = ["id", "name"]
        elif self.movement_check.isChecked():
            self.results = queries.search_movement(self.search.text())
            columns = ["id", "Entrada/Salida", "donador/retirador", "Medicamento", "#", "paquetes","u./paquete", "F. Entrega"]
        else:
            columns = []
            self.results = []

        self.results_table.setRowCount(len(self.results))
        self.results_table.setColumnCount(len(columns))
        self.results_table.setHorizontalHeaderLabels(columns)
        self.results_table.horizontalHeader().setVisible(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setColumnHidden(0, True)

        if self.results:
            names = list(self.results[0].keys())
            print(names)
        else:
            names = []
        i = 0
        print(self.results)
        if self.med_type_check.isChecked():
            for row in self.results:
                self.results_table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                self.results_table.setItem(i, 1, QTableWidgetItem(row['name']))
                self.results_table.setItem(i, 2, QTableWidgetItem(str(row['productos'])))
                i += 1
        elif self.med_check.isChecked():
            for row in self.results:
                self.results_table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                self.results_table.setItem(i, 1, QTableWidgetItem(row['codigo']))
                self.results_table.setItem(i, 2, QTableWidgetItem(row['nombre']))
                self.results_table.setItem(i, 3, QTableWidgetItem(row['tipo']))
                i += 1
        elif self.lote_check.isChecked():
            for row in self.results:
                self.results_table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                self.results_table.setItem(i, 1, QTableWidgetItem(row['name']))
                i += 1
        elif self.movement_check.isChecked():
            for row in self.results:
                if row['entrada_salida'] == True:
                    row['entrada_salida'] = "Entrada"
                else:
                    row['entrada_salida'] = "Salida"
                self.results_table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                self.results_table.setItem(i, 1, QTableWidgetItem(row['entrada_salida']))
                self.results_table.setItem(i, 2, QTableWidgetItem(row['donador_retirador']))
                self.results_table.setItem(i, 3, QTableWidgetItem(row['med']))
                self.results_table.setItem(i, 4, QTableWidgetItem(row['med_code']))
                self.results_table.setItem(i, 5, QTableWidgetItem(str(row['paquetes'])))
                self.results_table.setItem(i, 6, QTableWidgetItem(str(row['unidades_por_paquete'])))
                self.results_table.setItem(i, 7, QTableWidgetItem(row['fecha_entrega'].strftime("%d/%m/%Y")))
                i += 1

        else:
            for row in self.results:
                print(row)
                j = 0
                for name in names:
                    self.results_table.setItem(i, j, QTableWidgetItem(row[name]))
                    j += 1
                i += 1

    def open_med(self, item):
        print(item.row())
        if self.med_check.isChecked():
            selected_id = self.results_table.item(item.row(), 0).text()
            self.modal_window = None
            self.modal_window = Med(selected_id)
            self.modal_window.changes_made.clicked.connect(self.results_logic)
            self.modal_window.changes_made.clicked.connect(self.changes_made_action)
            self.modal_window.show()

    def changes_made_action(self):
        self.changes_made.click()
