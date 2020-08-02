
"""
This is a setup.py file using cx_Freeze

Usage:
    python setup.py build_exe --excludes=matplotlib.tests,numpy.random._examples
"""

import cx_Freeze
from cx_Freeze import *
import sys
import os
import os.path
import tkinter
import matplotlib

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"  # tells the build script to hide the console



PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable("CGM_DB_FrontEnd.py", base=base)]

cx_Freeze.setup(
    name='CGMDatabase',
    options={"build_exe": {"packages": ["tkinter", "matplotlib"],
                           'include_files': [
                               os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                               os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                              ("C:/Users/JAMES ASMAH/AppData/Local/Programs/Python/Python38/Lib/site-packages/mpl_toolkits/")
                               # ("C:/Users/JAMES ASMAH/AppData/Local/Programs/Python/Python38/Lib/site-packages/pytest/")
                           ]}},
    executables=executables
)








