from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem

import queries
from views.Med import Med


class Meds(QWidget):

    def __init__(self):
        super().__init__()
        self.modal_window = None
        self.setWindowTitle("Medicamentos")
        self.changes_made = QPushButton()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        title = QLabel("MEDICAMENTOS")
        title.setMaximumHeight(20)
        self.main_layout.addWidget(title)
        self.meds = None
        self.meds_table = QTableWidget()
        headers = ["ID", "CODIGO", "NOMBRE", "TIPO", "PAQUETES"]
        self.meds_table.setColumnCount(len(headers))
        self.meds_table.setHorizontalHeaderLabels(headers)
        self.meds_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.meds_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.meds_table.setSelectionMode(QTableWidget.SingleSelection)
        self.meds_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.meds_table.itemDoubleClicked.connect(self.open_med)
        self.meds_table.setColumnHidden(0, True)
        self.fill_table()
        self.main_layout.addWidget(self.meds_table)

    def fill_table(self):
        self.meds = queries.get_meds()
        self.meds_table.clearContents()
        self.meds_table.setRowCount(len(self.meds))
        i = 0
        for med in self.meds:
            self.meds_table.setItem(i, 0, QTableWidgetItem(str(med['id'])))
            self.meds_table.setItem(i, 1, QTableWidgetItem(str(med['codigo'])))
            self.meds_table.setItem(i, 2, QTableWidgetItem(med['nombre']))
            self.meds_table.setItem(i, 3, QTableWidgetItem(med['tipo']))
            self.meds_table.setItem(i, 4, QTableWidgetItem(str(med['paquetes'])))
            i += 1


    def open_med(self):
        selected_id = self.meds_table.item(self.meds_table.currentRow(), 0).text()
        self.modal_window = None
        self.modal_window = Med(selected_id)
        self.modal_window.changes_made.clicked.connect(self.fill_table)
        self.modal_window.changes_made.clicked.connect(self.changes_made_action)
        self.modal_window.show()
        pass

    def changes_made_action(self):
        self.changes_made.click()
