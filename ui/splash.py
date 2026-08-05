#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import (
    Qt,
    QTimer,
    QCoreApplication, Signal
)
from PySide6.QtGui import (
    QFont,
    QPixmap,
    QColor, QMouseEvent,

)
from PySide6.QtWidgets import (
    QLabel,
    QSplashScreen,
    QVBoxLayout,
    QWidget, QDialog, QMainWindow,
)
from project_info import Info
import resources
from ui.generated.splash_screen import Ui_splash_screen


class SplashScreen(QDialog, Ui_splash_screen):
    signal_splash_screen_closed = Signal()

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setupUi(self)
        self.splash_screen = QSplashScreen()
        self.splash_screen.setPixmap(QPixmap(Info.SPLASH_PATH))
        self.splash_screen.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.label_footer.setText(f'{Info.COPYRIGHT}\n'
                                  f'{Info.NOTICE}')
        self.label_tool_title.setText(Info.PROJECT_TITLE)
        layout = QVBoxLayout()
        layout.addWidget(self.topLevelWidget())
        self.splash_screen.setLayout(layout)
        self.splash_screen.show()
        QCoreApplication.processEvents()
        print('New splash screen')

    def mousePressEvent(self, mouse_event: QMouseEvent) -> None:
        self.splash_screen.close()
        self.close()

    def close(self) -> None:
        super().close()
        self.signal_splash_screen_closed.emit()
