import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "include_files": [("logo.jpg", "logo.jpg"), ("db", "db"), ('FIRMAS.png', 'FIRMAS.png'),
                      ('policia.ico', 'policia.ico')],
}

setup(
    name="ADMINISTRACION DE MEDICAMENTOS",
    version="0.3",
    description="Hecho en 3.1 dias",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="gui", icon="policia.ico")],
)
