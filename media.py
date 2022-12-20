import json
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


with open('config.json', 'r') as f:
    config = json.load(f)

with open('style.json', 'r') as f:
    style = json.load(f)


class Playlist(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class SongString(QLabel):
    def __init__(self, name, author, path, image, queue, connection, parent=None):
        super().__init__(parent)

        self.connection = connection

        self.name = name
        self.author = author
        self.path = path
        self.image_path = image
        self.queue = queue

        self.setFixedHeight(70)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setAlignment(Qt.AlignLeft)

        self.image = QWidget(self)
        self.image.setFixedSize(60, 60)
        self.image.setStyleSheet("QWidget {{border-radius: 5px; border-image: url('{}')}}".format(self.image_path))
        self.layout.addWidget(self.image)

        self.text_block = QWidget(self)
        self.text_block_layout = QVBoxLayout(self.text_block)
        self.text_block_layout.setContentsMargins(11, 5, 5, 5)

        self.song_name_w = QLabel(self.text_block)
        self.song_name_w.setText(self.name)
        self.text_block_layout.addWidget(self.song_name_w)

        self.author_name_w = QLabel(self.text_block)
        self.author_name_w.setText(self.author)
        self.text_block_layout.addWidget(self.author_name_w)

        self.layout.addWidget(self.text_block)

        self.set_style()

    def set_style(self):
        global config
        global style
        self.setStyleSheet(style[config['mode']]["my_library"]["song_string_back"])
        self.song_name_w.setStyleSheet(style[config['mode']]["my_library"]["song_name"])
        self.author_name_w.setStyleSheet(style[config['mode']]["my_library"]["author"])

    def mousePressEvent(self, event):
        self.connection.start_playing(self)

    def mouseMoveEvent(self, event):
        pass