from PySide6.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QFormLayout, QLabel, QPushButton


class SalidaForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("scroll")
        self.vbox = QFormLayout()
        self.setLayout(self.vbox)
        self.vbox.addWidget(QLabel("DATOS DEL EMISOR"))
        self.titulo_emisor = QLineEdit()
        self.vbox.addRow("TITULO DEL EMISOR", self.titulo_emisor)
        self.nombre_emisor = QLineEdit()
        self.vbox.addRow("NOMBRE DEL EMISOR", self.nombre_emisor)
        self.tipo_data_emisor = QLineEdit()
        self.tipo_data_emisor.setPlaceholderText("CI, Carnet, Identificación, etc.")
        self.vbox.addRow("TIPO DE IDENTIFICACION EMISOR", self.tipo_data_emisor)
        self.credencial_emisor = QLineEdit()
        self.credencial_emisor.setPlaceholderText("Ejemplo: 12918765 (cedula)")
        self.vbox.addRow("CREDENCIAL EMISOR", self.credencial_emisor)
        self.vbox.addWidget(QLabel("DATOS DEL RECEPTOR"))
        self.titulo_receptor = QLineEdit()
        self.titulo_receptor.setPlaceholderText("Doctor, funcionario, ciudadano, etc.")
        self.vbox.addRow("TITULO DEL RECEPTOR", self.titulo_receptor)
        self.nombre_receptor = QLineEdit()
        self.vbox.addRow("NOMBRE DEL RECEPTOR", self.nombre_receptor)
        self.tipo_data = QLineEdit()
        self.tipo_data.setPlaceholderText("CI, Carnet, Identificación, etc.")
        self.vbox.addRow("TIPO DE IDENTIFICACION", self.tipo_data)
        self.credencial = QLineEdit()
        self.credencial.setPlaceholderText("Ejemplo: 12918765 (cedula)")
        self.vbox.addRow("CREDENCIAL", self.credencial)
        self.report_btn = QPushButton("Generar reporte")
        self.cancel_btn = QPushButton("Cancelar")
        self.vbox.addWidget(self.report_btn)
        self.vbox.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.close)
        pass

    def get_nombre_emisor(self):
        return self.nombre_emisor.text()

    def get_titulo_emisor(self):
        return self.titulo_emisor.text()

    def get_tipo_emisor(self):
        return self.tipo_data_emisor.text()

    def get_credencial_emisor(self):
        return self.credencial_emisor.text()

    def get_nombre_receptor(self):
        return self.nombre_receptor.text()

    def get_titulo_receptor(self):
        return self.titulo_receptor.text()

    def get_tipo_receptor(self):
        return self.tipo_data.text()

    def get_credencial_receptor(self):
        return self.credencial.text()




