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


class ControlButton(QPushButton):
    def __init__(self, t, s, parent=None):
        super().__init__(parent)

        self.t = t
        self.setStyleSheet(style[config['mode']]["window"][self.t[0]])
        self.setIconSize(s)

    def enterEvent(self, event):
        self.setStyleSheet(style[config['mode']]["window"][self.t[1]])

    def leaveEvent(self, event):
        self.setStyleSheet(style[config['mode']]["window"][self.t[0]])

    def mouseMoveEvent(self, event):
        pass