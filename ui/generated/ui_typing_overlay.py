# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_typing_overlay.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QSizePolicy, QVBoxLayout, QWidget)

from src.wpm_graph_widget import WpmGraphWidget

class Ui_TypingOverlay(object):
    def setupUi(self, TypingOverlay):
        if not TypingOverlay.objectName():
            TypingOverlay.setObjectName(u"TypingOverlay")
        TypingOverlay.resize(616, 40)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TypingOverlay.sizePolicy().hasHeightForWidth())
        TypingOverlay.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(TypingOverlay)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_details = QWidget(TypingOverlay)
        self.widget_details.setObjectName(u"widget_details")
        self.horizontalBox_details = QHBoxLayout(self.widget_details)
        self.horizontalBox_details.setObjectName(u"horizontalBox_details")
        self.horizontalBox_details.setContentsMargins(0, 0, 0, 0)
        self.label_update = QLabel(self.widget_details)
        self.label_update.setObjectName(u"label_update")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_update.sizePolicy().hasHeightForWidth())
        self.label_update.setSizePolicy(sizePolicy1)
        self.label_update.setMinimumSize(QSize(18, 18))
        self.label_update.setMaximumSize(QSize(18, 18))
        self.label_update.setVisible(False)
        self.label_update.setStyleSheet(u"background: transparent; padding: 1px;")
        self.label_update.setAlignment(Qt.AlignCenter)

        self.horizontalBox_details.addWidget(self.label_update)

        self.label_status = QLabel(self.widget_details)
        self.label_status.setObjectName(u"label_status")
        sizePolicy1.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy1)
        self.label_status.setMinimumSize(QSize(80, 0))
        self.label_status.setStyleSheet(u"font-size: 9px; color: #666666; background: transparent; padding: 1px 4px;")
        self.label_status.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalBox_details.addWidget(self.label_status)

        self.label_stats = QLabel(self.widget_details)
        self.label_stats.setObjectName(u"label_stats")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_stats.sizePolicy().hasHeightForWidth())
        self.label_stats.setSizePolicy(sizePolicy2)
        self.label_stats.setStyleSheet(u"font-size: 10px; color: #999999; background: transparent;")
        self.label_stats.setAlignment(Qt.AlignCenter)

        self.horizontalBox_details.addWidget(self.label_stats)

        self.label_wordCount = QLabel(self.widget_details)
        self.label_wordCount.setObjectName(u"label_wordCount")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_wordCount.sizePolicy().hasHeightForWidth())
        self.label_wordCount.setSizePolicy(sizePolicy3)
        self.label_wordCount.setCursor(QCursor(Qt.PointingHandCursor))
        self.label_wordCount.setStyleSheet(u"font-size: 9px; background: transparent; padding: 1px 4px;")
        self.label_wordCount.setAlignment(Qt.AlignCenter)

        self.horizontalBox_details.addWidget(self.label_wordCount)

        self.label_timedTest = QLabel(self.widget_details)
        self.label_timedTest.setObjectName(u"label_timedTest")
        sizePolicy3.setHeightForWidth(self.label_timedTest.sizePolicy().hasHeightForWidth())
        self.label_timedTest.setSizePolicy(sizePolicy3)
        self.label_timedTest.setCursor(QCursor(Qt.PointingHandCursor))
        self.label_timedTest.setStyleSheet(u"font-size: 9px; background: transparent; padding: 1px 4px;")
        self.label_timedTest.setAlignment(Qt.AlignCenter)

        self.horizontalBox_details.addWidget(self.label_timedTest)

        self.label_quoteTest = QLabel(self.widget_details)
        self.label_quoteTest.setObjectName(u"label_quoteTest")
        sizePolicy3.setHeightForWidth(self.label_quoteTest.sizePolicy().hasHeightForWidth())
        self.label_quoteTest.setSizePolicy(sizePolicy3)
        self.label_quoteTest.setCursor(QCursor(Qt.PointingHandCursor))
        self.label_quoteTest.setStyleSheet(u"font-size: 9px; background: transparent; padding: 1px 4px;")
        self.label_quoteTest.setAlignment(Qt.AlignCenter)

        self.horizontalBox_details.addWidget(self.label_quoteTest)


        self.verticalLayout.addWidget(self.widget_details)

        self.label_text = QLabel(TypingOverlay)
        self.label_text.setObjectName(u"label_text")
        sizePolicy3.setHeightForWidth(self.label_text.sizePolicy().hasHeightForWidth())
        self.label_text.setSizePolicy(sizePolicy3)
        self.label_text.setStyleSheet(u"padding: 5px; background: transparent;")
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setWordWrap(False)

        self.verticalLayout.addWidget(self.label_text)

        self.widget_wpm_graph = WpmGraphWidget(TypingOverlay)
        self.widget_wpm_graph.setObjectName(u"widget_wpm_graph")
        self.widget_wpm_graph.setVisible(False)
        self.widget_wpm_graph.setMinimumSize(QSize(0, 60))
        self.widget_wpm_graph.setStyleSheet(u"background: transparent;")

        self.verticalLayout.addWidget(self.widget_wpm_graph)

        self.widget_about = QWidget(TypingOverlay)
        self.widget_about.setObjectName(u"widget_about")
        self.widget_about.setVisible(False)
        self.verticalLayout_about = QVBoxLayout(self.widget_about)
        self.verticalLayout_about.setObjectName(u"verticalLayout_about")
        self.verticalLayout_about.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_about.setContentsMargins(0, 10, 0, 10)
        self.label_keys = QLabel(self.widget_about)
        self.label_keys.setObjectName(u"label_keys")
        self.label_keys.setAlignment(Qt.AlignCenter)

        self.verticalLayout_about.addWidget(self.label_keys)

        self.label_version = QLabel(self.widget_about)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setAlignment(Qt.AlignCenter)

        self.verticalLayout_about.addWidget(self.label_version)


        self.verticalLayout.addWidget(self.widget_about)


        self.retranslateUi(TypingOverlay)

        QMetaObject.connectSlotsByName(TypingOverlay)
    # setupUi

    def retranslateUi(self, TypingOverlay):
        TypingOverlay.setWindowTitle(QCoreApplication.translate("TypingOverlay", u"TinyType Overlay", None))
#if QT_CONFIG(tooltip)
        self.label_update.setToolTip(QCoreApplication.translate("TypingOverlay", u"A new version of TinyType is available!", None))
#endif // QT_CONFIG(tooltip)
        self.label_update.setText("")
        self.label_status.setText("")
        self.label_stats.setText(QCoreApplication.translate("TypingOverlay", u"Test: Default  |  Avg WPM: 0.0  |  Avg Accuracy: 0.0%", None))
        self.label_wordCount.setText(QCoreApplication.translate("TypingOverlay", u"W: 50", None))
        self.label_timedTest.setText(QCoreApplication.translate("TypingOverlay", u"T: 30s", None))
        self.label_quoteTest.setText(QCoreApplication.translate("TypingOverlay", u"Q: short", None))
        self.label_text.setText(QCoreApplication.translate("TypingOverlay", u"Type here to begin...", None))
        self.label_keys.setText(QCoreApplication.translate("TypingOverlay", u"Commands", None))
        self.label_version.setText(QCoreApplication.translate("TypingOverlay", u"Version Info", None))
    # retranslateUi

