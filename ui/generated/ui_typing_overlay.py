# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_typing_overlay.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_TypingOverlay(object):
    def setupUi(self, TypingOverlay):
        if not TypingOverlay.objectName():
            TypingOverlay.setObjectName(u"TypingOverlay")
        TypingOverlay.resize(329, 40)
        self.verticalLayout = QVBoxLayout(TypingOverlay)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_stats = QLabel(TypingOverlay)
        self.label_stats.setObjectName(u"label_stats")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_stats.sizePolicy().hasHeightForWidth())
        self.label_stats.setSizePolicy(sizePolicy)
        self.label_stats.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_stats)

        self.label_text = QLabel(TypingOverlay)
        self.label_text.setObjectName(u"label_text")
        sizePolicy.setHeightForWidth(self.label_text.sizePolicy().hasHeightForWidth())
        self.label_text.setSizePolicy(sizePolicy)
        self.label_text.setStyleSheet(u"padding: 5px; background: transparent;")
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setWordWrap(False)

        self.verticalLayout.addWidget(self.label_text)


        self.retranslateUi(TypingOverlay)

        QMetaObject.connectSlotsByName(TypingOverlay)
    # setupUi

    def retranslateUi(self, TypingOverlay):
        TypingOverlay.setWindowTitle(QCoreApplication.translate("TypingOverlay", u"TinyType Overlay", None))
        self.label_stats.setStyleSheet(QCoreApplication.translate("TypingOverlay", u"font-size: 10px; color: #999999; background: transparent;", None))
        self.label_stats.setText(QCoreApplication.translate("TypingOverlay", u"Test: Default  |  Avg WPM: 0.0  |  Avg Accuracy: 0.0%", None))
        self.label_text.setText(QCoreApplication.translate("TypingOverlay", u"Type here to begin...", None))
    # retranslateUi

