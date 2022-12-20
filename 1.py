import sys
import os
from PyQt5.QtCore import QEasingCurve, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QSizePolicy
from UiImageSlider import Ui_Form


class ImageSliderWidget(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(ImageSliderWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Инициализировать тип кривой анимации
        curve_types = [(n, c) for n, c in QEasingCurve.__dict__.items()
                       if isinstance(c, QEasingCurve.Type)]
        curve_types.sort(key=lambda ct: ct[1])
        curve_types = [c[0] for c in curve_types]
        self.comboBoxEasing.addItems(curve_types)

        # Слоты связующих сигналов
        self.spinBoxSpeed.valueChanged.connect(self.stackedWidget.setSpeed)
        self.comboBoxEasing.currentTextChanged.connect(self.setEasing)
        self.radioButtonHor.toggled.connect(self.setOrientation)
        self.radioButtonVer.toggled.connect(self.setOrientation)
        self.pushButtonPrev.clicked.connect(self.stackedWidget.slideInPrev)
        self.pushButtonNext.clicked.connect(self.stackedWidget.slideInNext)
        self.pushButtonStart.clicked.connect(self.autoStart)
        self.pushButtonStop.clicked.connect(self.autoStop)

        self.show()

        extensions = ('.jpg', '.png', '.jpeg',)

        # Добавить страницу изображения
        # ваши изображения находятся в  vvvvv  каталоге image (например)
        for name in os.listdir('image'):
            filename, file_extension = os.path.splitext(name)
            if not file_extension in extensions:
                continue

            label = QLabel(self.stackedWidget)
            label.setAlignment(Qt.AlignCenter)
            label.setMinimumSize(240, 160)

            label.setPixmap(
                # ваши изображения  в    vvvvvv  каталоге image (например)
                QPixmap('image/' + name).scaled(
                    self.stackedWidget.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation)
            )
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.stackedWidget.addWidget(label)

    def autoStart(self):
        self.pushButtonNext.setEnabled(False)
        self.pushButtonPrev.setEnabled(False)
        self.stackedWidget.autoStart()

    def autoStop(self):
        self.pushButtonNext.setEnabled(True)
        self.pushButtonPrev.setEnabled(True)
        self.stackedWidget.autoStop()

    def setEasing(self, name):
        self.stackedWidget.setEasing(getattr(QEasingCurve, name))

    def setOrientation(self, checked):
        hor = self.sender() == self.radioButtonHor
        if checked:
            self.stackedWidget.setOrientation(
                Qt.Horizontal if hor else Qt.Vertical)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ImageSliderWidget()
    w.show()
    sys.exit(app.exec_())