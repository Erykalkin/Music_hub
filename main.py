import sys
import json
from PyQt5.QtWidgets import QWidget, QSlider, QCompleter, QGraphicsBlurEffect, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QUrl, QEvent, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from my_library import MyMediaWindow
from search_window import SearchWindow
from settings_window import SettingsWindow
from control_button import ControlButton
import data_base


with open('config.json', 'r') as f:
    config = json.load(f)

with open('style.json', 'r') as f:
    style = json.load(f)


class Window(QWidget):
    def __init__(self, app):
        super().__init__()

        self.theme = config['mode']

        '''Плеер'''
        self.player = QMediaPlayer(self)
        self.player.setNotifyInterval(10)

        self.playlist = QMediaPlaylist()
        self.create_playlist()

        self.player.mediaStatusChanged.connect(self.set_panel_icon)
        self.player.positionChanged.connect(self.connect_slider_with_player)

        '''Переменные'''
        self.is_playing = False
        self.current_song = 0
        self.random = False
        self.queue = []
        self.completer = QCompleter()

        '''Окно'''
        self.resize(1200, 700)
        self.setMinimumSize(500, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)  # убрали верхнюю панель
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(1)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(11)
        #self.main_layout.setSpacing(0)  # если нужно склеить

        self.setStyleSheet(
            """
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10))

        '''Виджет подложка c фоном'''
        self.background = QLabel(self)
        #self.background.setStyleSheet("QWidget{background-color: rgb(100, 100, 100, 0)}")
        self.background.setStyleSheet("border-radius: 10px; border-image: url('image/img_4.png')")

        '''Создаём тулбар'''
        self.bar = QWidget(self)
        self.bar_height = 70
        self.bar.setFixedHeight(self.bar_height)
        self.bar_layout = QHBoxLayout(self.bar)
        self.bar_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.bar)
        self.bar_layout.setAlignment(Qt.AlignVCenter)

        '''Создаём менюшки'''
        #self.HomeW = HomeWindow(self)
        self.MediaW = MyMediaWindow(self)
        self.SearchW = SearchWindow(self)
        self.SettingsW = SettingsWindow(self)
        #self.HomeW.show()
        self.MediaW.show()
        self.SearchW.hide()
        self.SettingsW.hide()

        '''Виджеты с кнопками управления окном'''
        self.left_window_control = QWidget()
        self.right_window_control = QWidget()
        self.left_window_control.setFixedWidth(100)
        self.right_window_control.setFixedWidth(100)
        self.left_window_control.setAttribute(Qt.WA_TranslucentBackground, True)
        self.right_window_control.setAttribute(Qt.WA_TranslucentBackground, True)
        self.left_window_control_layout = QHBoxLayout(self.left_window_control)
        self.right_window_control_layout = QHBoxLayout(self.right_window_control)

        self.carousel_button = ControlButton(("carousel_button", "carousel_button+"), QSize(20, 20))
        self.left_window_control_layout.addWidget(self.carousel_button)

        self.fullscreen_button = ControlButton(("fullscreen_button", "fullscreen_button+"), QSize(20, 20))
        self.left_window_control_layout.addWidget(self.fullscreen_button)

        self.collapse_button = ControlButton(("collapse_button", "collapse_button+"), QSize(30, 30))
        self.right_window_control_layout.addWidget(self.collapse_button)

        self.exit_button = ControlButton(("exit_button", "exit_button+"), QSize(30, 30))
        self.right_window_control_layout.addWidget(self.exit_button)

        '''Создаём окно контента'''
        self.main_layout.addWidget(self.MediaW)
        self.main_layout.addWidget(self.SearchW)
        self.main_layout.addWidget(self.SettingsW)

        '''Нижняя панель'''
        self.panel = QWidget(self)
        self.panel_layout = QGridLayout(self.panel)
        self.main_layout.addWidget(self.panel)
        self.panel.setFixedHeight(80)
        self.panel_layout.setContentsMargins(10, 5, 5, 5)

        self.front_image = QWidget()  # картинка трека
        self.front_image.setFixedSize(60, 60)
        self.blur_image = QWidget()  # заблюренная подложка
        self.blur_image.setFixedSize(70, 60)
        self.panel_layout.addWidget(self.blur_image, 0, 0)
        self.panel_layout.addWidget(self.front_image, 0, 0)
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(40)
        self.blur_image.setGraphicsEffect(blur_effect)

        self.song_name = QLabel()
        self.song_author = QLabel()

        self.set_panel_icon()

        self.play_button = QPushButton(self)
        self.left_skip_button = QPushButton(self)
        self.right_skip_button = QPushButton(self)
        self.shuffle_button = QPushButton(self)
        self.sound_button = QPushButton(self)

        '''Сигналы кнопок управления'''
        self.play_button.clicked.connect(self.play_or_pause)
        self.left_skip_button.clicked.connect(lambda: self.player.playlist().previous())
        self.right_skip_button.clicked.connect(lambda: self.player.playlist().next())
        self.shuffle_button.clicked.connect(lambda: self.player.playlist().shuffle())
        self.sound_button.clicked.connect(self.mute)

        self.function_bar = QWidget()
        self.function_bar.setStyleSheet("QWidget {background-color: rgb(100, 0, 0, 0)}")
        self.function_bar_layout = QHBoxLayout(self.function_bar)
        self.function_bar_layout.addWidget(self.shuffle_button)
        self.function_bar_layout.addWidget(self.left_skip_button)
        self.function_bar_layout.addWidget(self.play_button)
        self.function_bar_layout.addWidget(self.right_skip_button)
        self.function_bar_layout.addWidget(self.sound_button)
        self.function_bar.setFixedSize(200, 40)
        self.function_bar.setContentsMargins(0, 0, 0, 0)
        self.function_bar_layout.setSpacing(10)

        '''Слайдер'''
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFixedHeight(20)
        self.panel_layout.addWidget(self.slider, 0, 1)
        self.slider.sliderMoved.connect(self.connect_player_with_slider)
        self.slider.sliderPressed.connect(lambda: self.player.pause())
        self.slider.sliderReleased.connect(lambda: self.player.play())

        self.fb_sl = QWidget()
        self.fb_sl.setContentsMargins(0, 0, 0, 0)
        self.fb_sl.setStyleSheet("QWidget {background-color: rgb(0, 0, 0, 0)}")
        self.fb_sl_layout = QVBoxLayout(self.fb_sl)
        self.fb_sl_layout.setSpacing(20)
        self.fb_sl_layout.addWidget(self.function_bar, alignment=Qt.AlignHCenter)
        self.fb_sl_layout.addWidget(self.slider)
        self.panel_layout.addWidget(self.fb_sl, 0, 2)
        self.song_text = QWidget()
        self.song_text.setStyleSheet("QWidget {background-color: rgb(0, 0, 0, 0)}")
        self.song_text_layout = QVBoxLayout(self.song_text)
        self.song_text_layout.addWidget(self.song_name)
        self.song_text_layout.addWidget(self.song_author)
        self.panel_layout.addWidget(self.song_text, 0, 1)

        '''Создаём кнопки для менюшек тулбара'''
        self.bar_layout.addWidget(self.left_window_control)

        self.HomeW_button = QPushButton('Главное Меню')
        self.HomeW_button.setFixedHeight(70)
        #self.bar_layout.addWidget(self.HomeW_button)

        self.MediaW_button = QPushButton('Моя Медиатека', self.bar)
        self.MediaW_button.setFixedHeight(70)
        self.bar_layout.addWidget(self.MediaW_button)

        self.SearchW_button = QPushButton('Поиск', self.bar)
        self.SearchW_button.setFixedHeight(70)
        self.bar_layout.addWidget(self.SearchW_button)

        self.SettingsW_button = QPushButton('Настройки', self.bar)
        self.SettingsW_button.setFixedHeight(70)
        self.bar_layout.addWidget(self.SettingsW_button)

        self.bar_layout.addWidget(self.right_window_control)

        '''Функционал кнопок'''
        @self.HomeW_button.clicked.connect
        def slot():
            #self.HomeW.show()
            self.MediaW.hide()
            self.SearchW.hide()
            self.SettingsW.hide()
            self.HomeW_button.setStyleSheet(style[config['mode']]["window"]["icons+"])
            self.MediaW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.SearchW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.SettingsW_button.setStyleSheet(style[config['mode']]["window"]["icons"])

        @self.MediaW_button.clicked.connect
        def slot():
            #self.HomeW.hide()
            self.MediaW.show()
            self.SearchW.hide()
            self.SettingsW.hide()
            self.HomeW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.MediaW_button.setStyleSheet(style[config['mode']]["window"]["icons+"])
            self.SearchW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.SettingsW_button.setStyleSheet(style[config['mode']]["window"]["icons"])

        @self.SearchW_button.clicked.connect
        def slot():
            #self.HomeW.hide()
            self.MediaW.hide()
            self.SearchW.show()
            self.SettingsW.hide()
            self.HomeW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.MediaW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.SearchW_button.setStyleSheet(style[config['mode']]["window"]["icons+"])
            self.SettingsW_button.setStyleSheet(style[config['mode']]["window"]["icons"])

        @self.SettingsW_button.clicked.connect
        def slot():
            #self.HomeW.hide()
            self.MediaW.hide()
            self.SearchW.hide()
            self.SettingsW.show()
            self.HomeW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.MediaW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.SearchW_button.setStyleSheet(style[config['mode']]["window"]["icons"])
            self.SettingsW_button.setStyleSheet(style[config['mode']]["window"]["icons+"])

        @self.fullscreen_button.clicked.connect
        def slot():
            if not self.isFullScreen():
                self.showFullScreen()
            else:
                self.showNormal()

        @self.collapse_button.clicked.connect
        def slot():
            self.showMinimized()

        @self.exit_button.clicked.connect
        def slot():
            sys.exit(app.exec_())

        self.restyle()

    def restyle(self):
        global config
        #self.HomeW.set_style()
        self.MediaW.set_style()
        self.SearchW.set_style()
        self.SettingsW.set_style()
        self.bar.setStyleSheet(style[config['mode']]['window']['bar'])
        self.panel.setStyleSheet(style[config['mode']]['window']['panel'])
        self.slider.setStyleSheet(style[config['mode']]['window']['slider'])
        self.song_name.setStyleSheet(style[config['mode']]['my_library']['song_name'])
        self.song_author.setStyleSheet(style[config['mode']]['my_library']['author'])

        #self.HomeW_button.setStyleSheet(style[config['mode']]['window']['icons'])
        self.MediaW_button.setStyleSheet(style[config['mode']]['window']['icons'])
        self.SearchW_button.setStyleSheet(style[config['mode']]['window']['icons'])
        self.SettingsW_button.setStyleSheet(style[config['mode']]['window']['icons'])

        self.play_button.setStyleSheet(style[config['mode']]['window']['play'])
        self.left_skip_button.setStyleSheet(style[config['mode']]['window']['back'])
        self.right_skip_button.setStyleSheet(style[config['mode']]['window']['next'])
        self.shuffle_button.setStyleSheet(style[config['mode']]['window']['shuffle'])
        self.sound_button.setStyleSheet(style[config['mode']]['window']['sound'])

        self.update()

    def resizeEvent(self, event):
        x = self.size().width()
        y = self.size().height()
        print(x, y)
        self.background.setGeometry(0, 0, x, y)

        self.update()

    def mousePressEvent(self, event):
        """Получение позиции при нажатии ЛКМ"""
        self.dragPos = event.globalPos()

    """def mouseMoveEvent(self, event):
        Перемещение при нажатии ЛКМ
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()"""   # Проблемы с реализацией: при перетягивании на активных элементах вылетает

    def start_playing(self, string):
        self.player.playlist().setCurrentIndex(self.MediaW.strings.index(string))
        self.player.play()
        self.is_playing = True
        self.play_button.setStyleSheet(style[config['mode']]['window']['pause'])

    def play_or_pause(self):
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.play_button.setStyleSheet(style[config['mode']]['window']['play'])
        else:
            self.player.play()
            self.is_playing = True
            self.play_button.setStyleSheet(style[config['mode']]['window']['pause'])

    def rewind(self, delta):
        self.player.setPosition(self.player.position() + delta * 1000)
        self.slider.setValue(self.player.position())

    def mute(self):
        if self.player.isMuted():
            self.player.setMuted(False)
        else:
            self.player.setMuted(True)

    def volume_up(self):
        self.player.setVolume(self.player.volume() + 1)

    def volume_down(self):
        self.player.setVolume(self.player.volume() - 1)

    def shuffle(self):
        self.player.playlist().shuffle()
        self.shuffling = True

    def connect_slider_with_player(self):
        if self.player.position() > 0:
            self.slider.setMaximum(self.player.duration())
        self.slider.setValue(self.player.position())

    def connect_player_with_slider(self):
        self.player.setPosition(self.slider.value())

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Backspace:
            self.player.setPosition(0)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_Right:
                self.rewind(1)
                event.accept()
                return True

            if key == Qt.Key_Left:
                self.rewind(-1)
                event.accept()
                return True

            if key == Qt.Key_Up:
                self.volume_up()
                event.accept()
                return True

            if key == Qt.Key_Down:
                self.volume_down()
                event.accept()
                return True

            if key == Qt.Key_Space:
                if self.SearchW.isHidden():
                    self.play_or_pause()
                    return True
                if not self.SearchW.isHidden():
                    return False
                event.accept()

        return False

    def download_from_internet(self, text):
        track = data_base.parcing(text)
        if type(track) == str:
            self.SearchW.error_bar.setText('К сожалению, не удалось найти аудиофайл')
        else:
            data_base.download(track[0], track[1], track[2], track[3])
            print(f'Трек {track[0]} успешно добавлен в вашу медиатеку')
            self.create_playlist()
            self.MediaW.create_playlist()
            self.SearchW.error_bar.setText(f'Трек {track[0]} успешно добавлен в вашу медиатеку')

    def create_playlist(self):
        try:
            self.playlist.deleteLater()
        except AttributeError:
            pass

        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        music = data_base.get_data('all_music')
        for song in music:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song[2])))

    def set_panel_icon(self):
        try:
            icon = self.MediaW.strings[self.player.playlist().currentIndex()].image_path
            self.front_image.setStyleSheet("border-radius: 10px; border-image: url({})".format(icon))
            self.blur_image.setStyleSheet("border-radius: 10px; border-image: url('{}')".format(icon))
            self.song_name.setText(self.MediaW.strings[self.player.playlist().currentIndex()].name)
            self.song_author.setText(self.MediaW.strings[self.player.playlist().currentIndex()].author)
        except IndexError:
            pass

    def add_to_playlist_beginning(self, song):
        self.player.playlist().addMedia(QMediaContent(QUrl.fromLocalFile(song[2])))


def application():
    app = QApplication(sys.argv)
    window = Window(app=app)
    app.installEventFilter(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()

# C:\Users\George.LAPTOP-TLP259VH\Music_hub\venv\Scripts\qta-browser.exe