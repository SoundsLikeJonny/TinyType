#  Copyright (c) 2024 Jon Evans.
#
#  The original Wwise-Python Tool Template and source code is provided by Jon Evans,
#  Copyright 2024 (c) Jon Evans Audio under the Apache License, Version 2.0
#  for the purposes of distributing internal tools
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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
