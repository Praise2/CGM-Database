
"""
This is a setup.py file using cx_Freeze

Usage:
    python setup.py build_exe --excludes=matplotlib.tests,numpy.random._examples

    after build up...whilst first running. [gcloud error pops up]
    delete previous gcloud folder and replace by these 3 files: gcloud, gcloud-0.17.0 ...., google
    #***NB: ignore lines 8 an 9. Issue fixed by adding their path to setup file code
"""

import cx_Freeze
# from cx_Freeze import *
import sys
# import os
import os.path
# import tkinter
# import matplotlib

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
                              ("C:/Users/JAMES ASMAH/AppData/Local/Programs/Python/Python38/Lib/site-packages/mpl_toolkits/"),
                              ("C:/Users/JAMES ASMAH/AppData/Local/Programs/Python/Python38/Lib/site-packages/gcloud"),
                               ("C:/Users/JAMES ASMAH/AppData/Local/Programs/Python/Python38/Lib/site-packages/gcloud-0.17.0-py3.8.egg-info")
                               # ("C:/Users/JAMES ASMAH/AppData/Local/Programs/Python/Python38/Lib/site-packages/pytest/")
                           ]}},
    executables=executables
)








