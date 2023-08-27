from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tensorflow", "os", "subprocess", "numpy", "time", "keras_preprocessing", "keras"],
    "excludes": ["tkinter"],  # Exclure tkinter car il n'est pas utilisé
    "build_exe" : "..\App",
}

base = None

setup(
    name = "app_python",
    version = "0.1",
    description = "cnn model prediction",
    options = {"build_exe": build_exe_options},
    executables = [Executable("module_TI.py", base=base)]
)