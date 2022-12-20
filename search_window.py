import json
from PyQt5.QtWidgets import QWidget, QScrollArea, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


with open('config.json', 'r') as f:
    config = json.load(f)

with open('style.json', 'r') as f:
    style = json.load(f)


class SearchWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.connection = self.parent()

        self.layout = QVBoxLayout(self)

        '''Поисковик'''
        self.searchbar = QLineEdit()
        self.searchbar.setFixedHeight(70)
        self.searchbar_layout = QHBoxLayout(self.searchbar)
        self.searchbar_layout.setContentsMargins(5, 5, 5, 5)
        self.layout.addWidget(self.searchbar, alignment=Qt.AlignTop)
        # self.searchbar.textChanged.connect(self.update_display)

        '''Кнопка поиска в интернете'''
        self.internet_button = QPushButton(self)
        self.internet_button.setFixedSize(60, 60)
        self.searchbar_layout.addWidget(self.internet_button, alignment=Qt.AlignLeft)
        self.internet_button.clicked.connect(lambda: self.search(self.searchbar.text()))
        self.internet_button.setCursor(Qt.ArrowCursor)

        '''Error bar'''
        self.error_bar = QLabel()
        self.layout.addWidget(self.error_bar)
        self.error_bar.setAlignment(Qt.AlignCenter)
        self.error_bar.setFixedHeight(400)

        '''Скрол'''
        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("QScrollArea {background-color: rgb(0, 0, 0, 0)}")

        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.scroll)

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

        '''Виджет с найденным треком'''

        self.set_style()

    def resizeEvent(self, event):
        a = self.size().width()
        b = self.size().height()

    def set_style(self):
        global config
        global style
        self.setStyleSheet(style[config['mode']]["window"]["content_window"])
        self.searchbar.setStyleSheet(style[config['mode']]["search_window"]["searchbar"])
        self.error_bar.setStyleSheet(style[config['mode']]["search_window"]["error_bar"])
        self.update()

    def update_display(self, text):
        pass

    def search(self, text):
        self.connection.download_from_internet(text)