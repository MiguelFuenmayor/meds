from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from views.MainWindow import MainWindow
# HECHO POR MIGUEL FUENMAYOR. github.com/MiguelFuenmayor
# MIT LICENSE
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'polisur.med_admin.miguel_fuenmayor.0.3'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":

    app = QApplication()
    app.setWindowIcon(QIcon("policia.ico"))
    app.setStyle("fusion")
    window = MainWindow()
    window.showMaximized()
    app.exec()
