# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_splash_screen(object):
    def setupUi(self, splash_screen):
        if not splash_screen.objectName():
            splash_screen.setObjectName(u"splash_screen")
        splash_screen.resize(401, 217)
        self.gridLayout = QGridLayout(splash_screen)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.label_tool_title = QLabel(splash_screen)
        self.label_tool_title.setObjectName(u"label_tool_title")
        self.label_tool_title.setMinimumSize(QSize(0, 30))
        self.label_tool_title.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        self.label_tool_title.setFont(font)
        self.label_tool_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_tool_title, 1, 0, 1, 1)

        self.label_footer = QLabel(splash_screen)
        self.label_footer.setObjectName(u"label_footer")
        self.label_footer.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_footer, 2, 0, 1, 1)


        self.retranslateUi(splash_screen)

        QMetaObject.connectSlotsByName(splash_screen)
    # setupUi

    def retranslateUi(self, splash_screen):
        splash_screen.setWindowTitle(QCoreApplication.translate("splash_screen", u"Form", None))
        self.label_tool_title.setText(QCoreApplication.translate("splash_screen", u"Tool Title Goes Here", None))
        self.label_footer.setText(QCoreApplication.translate("splash_screen", u"[Copyright and other info goes here]", None))
    # retranslateUi

