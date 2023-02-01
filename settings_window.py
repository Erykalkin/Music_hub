import json
from PyQt5.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


with open('config.json', 'r') as f:
    config = json.load(f)

with open('style.json', 'r') as f:
    style = json.load(f)


class SettingsWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.connection = self.parent()

        self.scroll = QScrollArea(self)
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
        self.widget_layout.setSpacing(50)

        '''Настройки темы'''
        self.theme_widget = QGroupBox(self.widget)
        self.theme_widget_layout = QGridLayout(self.theme_widget)
        self.theme_widget_layout.setAlignment(Qt.AlignTop)
        self.theme_widget_layout.setContentsMargins(0, 50, 0, 0)
        self.theme_widget.setTitle("Тема")
        self.widget_layout.addWidget(self.theme_widget)

        self.themes = []
        self.th1 = ThemeButton(self.widget, "Тёмная тема", "dark theme", connection=self.connection)
        self.themes.append(self.th1)
        self.theme_widget_layout.addWidget(self.th1, 1, 0)

        self.th2 = ThemeButton(self.widget, "Светлая тема", "light theme", connection=self.connection)
        self.themes.append(self.th2)
        self.theme_widget_layout.addWidget(self.th2, 1, 1)

        '''Настройки фона'''
        self.back_widget = QGroupBox(self.widget)
        self.back_widget_layout = QHBoxLayout(self.back_widget)
        self.back_widget.setTitle("Фон")
        self.widget_layout.addWidget(self.back_widget)

    def resizeEvent(self, event):
        a = self.size().width()
        b = self.size().height()

    def set_style(self):
        global config
        global style
        self.setStyleSheet(style[config['mode']]["window"]["content_window"])
        self.theme_widget.setStyleSheet(style[config['mode']]["settings_window"]["string"])
        for i in self.themes:
            i.set_style()
        self.back_widget.setStyleSheet(style[config['mode']]["settings_window"]["string"])
        self.update()

    def change_config(self):
        print('sssss')


class ThemeButton(QPushButton):
    def __init__(self, parent=None, name="", theme="", connection=None):

        self.connection = connection

        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setFixedSize(150, 150)
        self.setStyleSheet("QPushButton {background-color: rgb(0, 0, 0, 0)}")
        self.name = name
        self.theme = theme

        "Макет темы"
        self.image = QLabel(self)
        self.image.setFixedSize(100, 100)
        self.image_l = QGridLayout(self.image)
        self.image_l.setContentsMargins(0, 0, 0, 0)
        self.image_l.setSpacing(0)
        self.b = QLabel(self.image)
        self.b.setFixedWidth(40)
        self.b_l = QGridLayout(self.b)
        self.b_l.setContentsMargins(10, 10, 10, 10)
        self.b_l.setSpacing(10)
        self.w1 = QLabel(self.image)
        self.w2 = QLabel()
        self.w2.setFixedSize(20, 20)
        self.w3 = QLabel()
        self.w3.setFixedSize(20, 20)
        self.w4 = QLabel()
        self.w4.setFixedSize(20, 20)

        self.image_l.addWidget(self.b, 0, 0)
        self.image_l.addWidget(self.w1, 0, 1)
        self.b_l.addWidget(self.w2, 0, 0)
        self.b_l.addWidget(self.w3, 1, 0)
        self.b_l.addWidget(self.w4, 2, 0)
        self.layout.addWidget(self.image, alignment=Qt.AlignCenter)

        "Надпись"
        self.text = QLabel()
        self.text.setText(self.name)
        self.text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.text)

    def set_style(self):
        global config
        global style
        self.image.setStyleSheet(style[self.theme]["settings_window"]["theme_button_image"]["c0"])
        self.b.setStyleSheet(style[self.theme]["settings_window"]["theme_button_image"]["c1"])
        self.w1.setStyleSheet(style[self.theme]["settings_window"]["theme_button_image"]["c2"])
        self.w2.setStyleSheet(style[self.theme]["settings_window"]["theme_button_image"]["c3"])
        self.w3.setStyleSheet(style[self.theme]["settings_window"]["theme_button_image"]["c3"])
        self.w4.setStyleSheet(style[self.theme]["settings_window"]["theme_button_image"]["c3"])

    def mousePressEvent(self, event):
        pass
        global config
        if config['mode'] == 'light theme':
            config['mode'] = 'dark theme'
            with open('config.json', 'w') as f1:
                json.dump(config, f1, indent=1)
            self.connection.restyle()
        else:
            config['mode'] = 'light theme'
            with open('config.json', 'w') as f1:
                json.dump(config, f1, indent=1)
            self.connection.restyle()

    def mouseMoveEvent(self, event):
        pass
