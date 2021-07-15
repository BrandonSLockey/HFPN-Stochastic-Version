# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 19:53:44 2021

@author: brand
"""
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("sHFPN GUI")
        self.setWindowIcon(QIcon("mng.png"))
        self.setGeometry(500,300, 400, 300)
        self.setStyleSheet("background-color:red")
        



app = QApplication([])

window = Window()
window.show()
sys.exit(app.exec())