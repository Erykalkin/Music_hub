import sys
import random
import os
import json
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QMenuBar, QVBoxLayout, QLabel, QGroupBox, QFrame, QMainWindow, QGridLayout, QSplitter, QPushButton, QToolTip, QFileDialog
from PyQt5.QtCore import Qt, QMimeDatabase, QRect, QEvent, QVariantAnimation, QAbstractAnimation, QPropertyAnimation, QSize, QEasingCurve
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QPainter, QPen, QIcon, QImage


with open('config.json', 'r') as f:
    config = json.load(f)

with open('style.json', 'r') as f:
    style = json.load(f)


class HomeWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


    def resizeEvent(self, event):
        a = self.size().width()
        b = self.size().height()

    def set_style(self):
        global config
        global style
        self.setStyleSheet(style[config['mode']]["window"]["content_window"])
        self.update()