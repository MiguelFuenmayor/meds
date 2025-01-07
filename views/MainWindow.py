from PySide6.QtWidgets import QMainWindow, QInputDialog

from database import TipoMed
from views.Home import Home


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meds")
        self.home = Home()
        self.home.changes_made.clicked.connect(self.recharge)
        self.setCentralWidget(self.home)
        self.menu = self.menuBar()
        self.inicio = self.menu.addAction("INICIO")
        self.inicio.triggered.connect(self.inicio_action)
        self.agregar_tipo = self.menu.addAction("AGREGAR TIPO")
        self.agregar_tipo.triggered.connect(self.agregar_tipo_action)
        self.searcher_action = self.menu.addAction("BUSCAR")
        self.searcher_action.triggered.connect(self.searcher)
        self.totales_action = self.menu.addAction("TOTALES")
        self.totales_action.triggered.connect(self.totales)
        self.reportes_action = self.menu.addAction("REPORTES")
        self.reportes_action.triggered.connect(self.reports)
        self.meds_action = self.menu.addAction("MEDICAMENTOS")
        self.meds_action.triggered.connect(self.meds)
        self.entrada = self.menu.addAction("ENTRADA")
        self.entrada.triggered.connect(self.entrada_action)
        self.salida = self.menu.addAction("SALIDA")
        self.salida.triggered.connect(self.salida_action)
        self.home.base.changes_made.clicked.connect(self.recharge)
        self.home.meds.changes_made.clicked.connect(self.recharge)
        self.home.entrada.changes_made.clicked.connect(self.recharge)
        self.home.salida.changes_made.clicked.connect(self.recharge)

    def salida_action(self):
        self.home.setCurrentIndex(7)

    def entrada_action(self):
        self.home.setCurrentIndex(6)

    def bulk_report(self):
        self.home.setCurrentIndex(6)
        pass

    def meds(self):
        self.home.setCurrentIndex(5)

    def reports(self):
        self.home.setCurrentIndex(4)
        pass


    def totales(self):
        self.home.setCurrentIndex(3)


    def inicio_action(self):
        self.home.setCurrentIndex(0)

    def searcher(self):
        self.home.setCurrentIndex(2)
    def agregar_tipo_action(self):
        tipo, ok = QInputDialog.getText(self, "Añadir tipo", "Tipo:")
        print(tipo, ok)
        if ok and tipo:
            ok = TipoMed.create(name=tipo)
            if ok:
                self.home.tipo_recharge()

    def recharge(self):
        print("RECHARGING")
        self.home.totals.recharge()
        self.home.base.refill_table()

        pass

