import sys
import random
import os
import json
from PyQt5.QtWidgets import QWidget, QScrollArea, QApplication, QGraphicsBlurEffect, QHBoxLayout, QMenuBar, QVBoxLayout, QLabel, QGroupBox, QFrame, QMainWindow, QGridLayout, QSplitter, QPushButton, QToolTip, QFileDialog
from PyQt5.QtCore import Qt, QUrl, QMimeDatabase, QRect, QEvent, QVariantAnimation, QAbstractAnimation, QPropertyAnimation, QSize, QEasingCurve
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QPainter, QPen, QIcon, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from media import SongString
import data_base


with open('config.json', 'r') as f:
    config = json.load(f)

with open('style.json', 'r') as f:
    style = json.load(f)


class MyMediaWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.connection = self.parent()  # связь между классами

        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("QScrollArea {background-color: rgb(0, 0, 0, 0)}")

        self.layoutV = QVBoxLayout(self)
        self.layoutV.setContentsMargins(0, 0, 0, 0)
        self.layoutV.addWidget(self.scroll)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.widget = QWidget()
        self.widget.setStyleSheet("QWidget {background-color: rgb(0, 0, 0, 0)}")
        self.scroll.setWidget(self.widget)
        self.widget_layout = QVBoxLayout(self.widget)
        self.widget_layout.setAlignment(Qt.AlignTop)
        self.widget_layout.setContentsMargins(20, 20, 20, 20)
        self.widget_layout.setSpacing(30)

        self.strings = []
        self.create_playlist()

    def resizeEvent(self, event):
        a = self.size().width()
        b = self.size().height()

    def set_style(self):
        global config
        global style
        self.setStyleSheet(style[config['mode']]["window"]["content_window"])
        self.update()

    def create_playlist(self):
        music = data_base.get_data('all_music')

        if self.strings != []:
            for i in self.strings:
                print(len(self.strings))
                i.deleteLater()
            self.strings = []

        i = 0
        for x in music:
            self.s = SongString(name=x[0], author=x[1], path=x[2], image=x[3], queue=i, connection=self.connection)
            self.widget_layout.addWidget(self.s)
            self.strings.append(self.s)
            i += 1
