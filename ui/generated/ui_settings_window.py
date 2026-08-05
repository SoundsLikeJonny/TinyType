# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFontComboBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QKeySequenceEdit,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QTabWidget,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(600, 667)
        self.centralwidget = QWidget(SettingsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_appearance = QWidget()
        self.tab_appearance.setObjectName(u"tab_appearance")
        self.verticalLayout_2 = QVBoxLayout(self.tab_appearance)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_font = QGroupBox(self.tab_appearance)
        self.groupBox_font.setObjectName(u"groupBox_font")
        self.formLayout = QFormLayout(self.groupBox_font)
        self.formLayout.setObjectName(u"formLayout")
        self.label_font = QLabel(self.groupBox_font)
        self.label_font.setObjectName(u"label_font")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_font)

        self.fontComboBox = QFontComboBox(self.groupBox_font)
        self.fontComboBox.setObjectName(u"fontComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.fontComboBox)

        self.label_fontSize = QLabel(self.groupBox_font)
        self.label_fontSize.setObjectName(u"label_fontSize")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_fontSize)

        self.spinBox_fontSize = QSpinBox(self.groupBox_font)
        self.spinBox_fontSize.setObjectName(u"spinBox_fontSize")
        self.spinBox_fontSize.setMinimum(5)
        self.spinBox_fontSize.setMaximum(72)
        self.spinBox_fontSize.setValue(24)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinBox_fontSize)


        self.verticalLayout_2.addWidget(self.groupBox_font)

        self.groupBox_colors = QGroupBox(self.tab_appearance)
        self.groupBox_colors.setObjectName(u"groupBox_colors")
        self.formLayout_2 = QFormLayout(self.groupBox_colors)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_untypedColor = QLabel(self.groupBox_colors)
        self.label_untypedColor.setObjectName(u"label_untypedColor")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_untypedColor)

        self.btn_untypedColor = QPushButton(self.groupBox_colors)
        self.btn_untypedColor.setObjectName(u"btn_untypedColor")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.btn_untypedColor)

        self.label_typedColor = QLabel(self.groupBox_colors)
        self.label_typedColor.setObjectName(u"label_typedColor")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_typedColor)

        self.btn_typedColor = QPushButton(self.groupBox_colors)
        self.btn_typedColor.setObjectName(u"btn_typedColor")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.btn_typedColor)

        self.label_errorColor = QLabel(self.groupBox_colors)
        self.label_errorColor.setObjectName(u"label_errorColor")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_errorColor)

        self.btn_errorColor = QPushButton(self.groupBox_colors)
        self.btn_errorColor.setObjectName(u"btn_errorColor")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.btn_errorColor)

        self.label_bgOpacity = QLabel(self.groupBox_colors)
        self.label_bgOpacity.setObjectName(u"label_bgOpacity")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_bgOpacity)

        self.slider_bgOpacity = QSlider(self.groupBox_colors)
        self.slider_bgOpacity.setObjectName(u"slider_bgOpacity")
        self.slider_bgOpacity.setMaximum(255)
        self.slider_bgOpacity.setValue(128)
        self.slider_bgOpacity.setOrientation(Qt.Horizontal)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.slider_bgOpacity)


        self.verticalLayout_2.addWidget(self.groupBox_colors)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_appearance, "")
        self.tab_typing = QWidget()
        self.tab_typing.setObjectName(u"tab_typing")
        self.verticalLayout_3 = QVBoxLayout(self.tab_typing)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_typingBehavior = QGroupBox(self.tab_typing)
        self.groupBox_typingBehavior.setObjectName(u"groupBox_typingBehavior")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_typingBehavior)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radio_movePerChar = QRadioButton(self.groupBox_typingBehavior)
        self.radio_movePerChar.setObjectName(u"radio_movePerChar")
        self.radio_movePerChar.setChecked(True)

        self.verticalLayout_4.addWidget(self.radio_movePerChar)

        self.radio_movePerWord = QRadioButton(self.groupBox_typingBehavior)
        self.radio_movePerWord.setObjectName(u"radio_movePerWord")

        self.verticalLayout_4.addWidget(self.radio_movePerWord)


        self.verticalLayout_3.addWidget(self.groupBox_typingBehavior)

        self.groupBox_position = QGroupBox(self.tab_typing)
        self.groupBox_position.setObjectName(u"groupBox_position")
        self.gridLayout = QGridLayout(self.groupBox_position)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radio_topLeft = QRadioButton(self.groupBox_position)
        self.radio_topLeft.setObjectName(u"radio_topLeft")

        self.gridLayout.addWidget(self.radio_topLeft, 0, 0, 1, 1)

        self.radio_topCenter = QRadioButton(self.groupBox_position)
        self.radio_topCenter.setObjectName(u"radio_topCenter")
        self.radio_topCenter.setChecked(True)

        self.gridLayout.addWidget(self.radio_topCenter, 0, 1, 1, 1)

        self.radio_topRight = QRadioButton(self.groupBox_position)
        self.radio_topRight.setObjectName(u"radio_topRight")

        self.gridLayout.addWidget(self.radio_topRight, 0, 2, 1, 1)

        self.radio_center = QRadioButton(self.groupBox_position)
        self.radio_center.setObjectName(u"radio_center")

        self.gridLayout.addWidget(self.radio_center, 1, 1, 1, 1)

        self.radio_bottomLeft = QRadioButton(self.groupBox_position)
        self.radio_bottomLeft.setObjectName(u"radio_bottomLeft")

        self.gridLayout.addWidget(self.radio_bottomLeft, 2, 0, 1, 1)

        self.radio_bottomCenter = QRadioButton(self.groupBox_position)
        self.radio_bottomCenter.setObjectName(u"radio_bottomCenter")

        self.gridLayout.addWidget(self.radio_bottomCenter, 2, 1, 1, 1)

        self.radio_bottomRight = QRadioButton(self.groupBox_position)
        self.radio_bottomRight.setObjectName(u"radio_bottomRight")

        self.gridLayout.addWidget(self.radio_bottomRight, 2, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_position)

        self.groupBox_typingTests = QGroupBox(self.tab_typing)
        self.groupBox_typingTests.setObjectName(u"groupBox_typingTests")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_typingTests)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_testControls = QHBoxLayout()
        self.horizontalLayout_testControls.setObjectName(u"horizontalLayout_testControls")
        self.btn_addTest = QPushButton(self.groupBox_typingTests)
        self.btn_addTest.setObjectName(u"btn_addTest")

        self.horizontalLayout_testControls.addWidget(self.btn_addTest)

        self.btn_removeTest = QPushButton(self.groupBox_typingTests)
        self.btn_removeTest.setObjectName(u"btn_removeTest")

        self.horizontalLayout_testControls.addWidget(self.btn_removeTest)

        self.btn_randomTest = QPushButton(self.groupBox_typingTests)
        self.btn_randomTest.setObjectName(u"btn_randomTest")
        self.btn_randomTest.setCheckable(True)

        self.horizontalLayout_testControls.addWidget(self.btn_randomTest)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_testControls.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_testControls)

        self.listWidget_tests = QListWidget(self.groupBox_typingTests)
        self.listWidget_tests.setObjectName(u"listWidget_tests")

        self.verticalLayout_9.addWidget(self.listWidget_tests)

        self.label_testName = QLabel(self.groupBox_typingTests)
        self.label_testName.setObjectName(u"label_testName")

        self.verticalLayout_9.addWidget(self.label_testName)

        self.lineEdit_testName = QLineEdit(self.groupBox_typingTests)
        self.lineEdit_testName.setObjectName(u"lineEdit_testName")

        self.verticalLayout_9.addWidget(self.lineEdit_testName)

        self.label_testText = QLabel(self.groupBox_typingTests)
        self.label_testText.setObjectName(u"label_testText")

        self.verticalLayout_9.addWidget(self.label_testText)

        self.textEdit_testText = QTextEdit(self.groupBox_typingTests)
        self.textEdit_testText.setObjectName(u"textEdit_testText")

        self.verticalLayout_9.addWidget(self.textEdit_testText)


        self.verticalLayout_3.addWidget(self.groupBox_typingTests)

        self.groupBox_display = QGroupBox(self.tab_typing)
        self.groupBox_display.setObjectName(u"groupBox_display")
        self.formLayout_4 = QFormLayout(self.groupBox_display)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_width = QLabel(self.groupBox_display)
        self.label_width.setObjectName(u"label_width")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_width)

        self.spinBox_width = QSpinBox(self.groupBox_display)
        self.spinBox_width.setObjectName(u"spinBox_width")
        self.spinBox_width.setMinimum(100)
        self.spinBox_width.setMaximum(2400)
        self.spinBox_width.setSingleStep(100)
        self.spinBox_width.setValue(1200)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.spinBox_width)

        self.label_height = QLabel(self.groupBox_display)
        self.label_height.setObjectName(u"label_height")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_height)

        self.spinBox_height = QSpinBox(self.groupBox_display)
        self.spinBox_height.setObjectName(u"spinBox_height")
        self.spinBox_height.setMinimum(20)
        self.spinBox_height.setMaximum(300)
        self.spinBox_height.setSingleStep(10)
        self.spinBox_height.setValue(120)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.spinBox_height)

        self.label_showBorder = QLabel(self.groupBox_display)
        self.label_showBorder.setObjectName(u"label_showBorder")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_showBorder)

        self.checkBox_showBorder = QCheckBox(self.groupBox_display)
        self.checkBox_showBorder.setObjectName(u"checkBox_showBorder")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.checkBox_showBorder)


        self.verticalLayout_3.addWidget(self.groupBox_display)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_typing, "")
        self.tab_account = QWidget()
        self.tab_account.setObjectName(u"tab_account")
        self.verticalLayout_5 = QVBoxLayout(self.tab_account)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_account = QGroupBox(self.tab_account)
        self.groupBox_account.setObjectName(u"groupBox_account")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_account)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_accountStatus = QLabel(self.groupBox_account)
        self.label_accountStatus.setObjectName(u"label_accountStatus")

        self.verticalLayout_6.addWidget(self.label_accountStatus)

        self.btn_login = QPushButton(self.groupBox_account)
        self.btn_login.setObjectName(u"btn_login")

        self.verticalLayout_6.addWidget(self.btn_login)

        self.btn_logout = QPushButton(self.groupBox_account)
        self.btn_logout.setObjectName(u"btn_logout")
        self.btn_logout.setEnabled(False)

        self.verticalLayout_6.addWidget(self.btn_logout)


        self.verticalLayout_5.addWidget(self.groupBox_account)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_account, "")
        self.tab_stats = QWidget()
        self.tab_stats.setObjectName(u"tab_stats")
        self.verticalLayout_7 = QVBoxLayout(self.tab_stats)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.textBrowser_stats = QTextBrowser(self.tab_stats)
        self.textBrowser_stats.setObjectName(u"textBrowser_stats")

        self.verticalLayout_7.addWidget(self.textBrowser_stats)

        self.tabWidget.addTab(self.tab_stats, "")
        self.tab_keybindings = QWidget()
        self.tab_keybindings.setObjectName(u"tab_keybindings")
        self.verticalLayout_11 = QVBoxLayout(self.tab_keybindings)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.groupBox_keybindings = QGroupBox(self.tab_keybindings)
        self.groupBox_keybindings.setObjectName(u"groupBox_keybindings")
        self.formLayout_5 = QFormLayout(self.groupBox_keybindings)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_increaseOpacity = QLabel(self.groupBox_keybindings)
        self.label_increaseOpacity.setObjectName(u"label_increaseOpacity")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_increaseOpacity)

        self.keySeq_increaseOpacity = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_increaseOpacity.setObjectName(u"keySeq_increaseOpacity")

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.keySeq_increaseOpacity)

        self.label_decreaseOpacity = QLabel(self.groupBox_keybindings)
        self.label_decreaseOpacity.setObjectName(u"label_decreaseOpacity")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_decreaseOpacity)

        self.keySeq_decreaseOpacity = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_decreaseOpacity.setObjectName(u"keySeq_decreaseOpacity")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.keySeq_decreaseOpacity)


        self.verticalLayout_11.addWidget(self.groupBox_keybindings)

        self.label_keybindingInfo = QLabel(self.tab_keybindings)
        self.label_keybindingInfo.setObjectName(u"label_keybindingInfo")
        self.label_keybindingInfo.setWordWrap(True)

        self.verticalLayout_11.addWidget(self.label_keybindingInfo)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab_keybindings, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_startTyping = QPushButton(self.centralwidget)
        self.btn_startTyping.setObjectName(u"btn_startTyping")

        self.horizontalLayout.addWidget(self.btn_startTyping)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_apply = QPushButton(self.centralwidget)
        self.btn_apply.setObjectName(u"btn_apply")

        self.horizontalLayout.addWidget(self.btn_apply)

        self.btn_close = QPushButton(self.centralwidget)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout)

        SettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"TinyType Settings", None))
        self.groupBox_font.setTitle(QCoreApplication.translate("SettingsWindow", u"Font Settings", None))
        self.label_font.setText(QCoreApplication.translate("SettingsWindow", u"Font:", None))
        self.label_fontSize.setText(QCoreApplication.translate("SettingsWindow", u"Font Size:", None))
        self.groupBox_colors.setTitle(QCoreApplication.translate("SettingsWindow", u"Color Settings", None))
        self.label_untypedColor.setText(QCoreApplication.translate("SettingsWindow", u"Untyped Text Color:", None))
        self.btn_untypedColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_typedColor.setText(QCoreApplication.translate("SettingsWindow", u"Typed Text Color:", None))
        self.btn_typedColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_errorColor.setText(QCoreApplication.translate("SettingsWindow", u"Error Text Color:", None))
        self.btn_errorColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_bgOpacity.setText(QCoreApplication.translate("SettingsWindow", u"Background Opacity:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_appearance), QCoreApplication.translate("SettingsWindow", u"Appearance", None))
        self.groupBox_typingBehavior.setTitle(QCoreApplication.translate("SettingsWindow", u"Typing Behavior", None))
        self.radio_movePerChar.setText(QCoreApplication.translate("SettingsWindow", u"Move text per character", None))
        self.radio_movePerWord.setText(QCoreApplication.translate("SettingsWindow", u"Move text per word", None))
        self.groupBox_position.setTitle(QCoreApplication.translate("SettingsWindow", u"Screen Position", None))
        self.radio_topLeft.setText(QCoreApplication.translate("SettingsWindow", u"Top Left", None))
        self.radio_topCenter.setText(QCoreApplication.translate("SettingsWindow", u"Top Center", None))
        self.radio_topRight.setText(QCoreApplication.translate("SettingsWindow", u"Top Right", None))
        self.radio_center.setText(QCoreApplication.translate("SettingsWindow", u"Center", None))
        self.radio_bottomLeft.setText(QCoreApplication.translate("SettingsWindow", u"Bottom Left", None))
        self.radio_bottomCenter.setText(QCoreApplication.translate("SettingsWindow", u"Bottom Center", None))
        self.radio_bottomRight.setText(QCoreApplication.translate("SettingsWindow", u"Bottom Right", None))
        self.groupBox_typingTests.setTitle(QCoreApplication.translate("SettingsWindow", u"Typing Tests", None))
        self.btn_addTest.setText(QCoreApplication.translate("SettingsWindow", u"Add Test", None))
        self.btn_removeTest.setText(QCoreApplication.translate("SettingsWindow", u"Remove Selected", None))
        self.btn_randomTest.setText(QCoreApplication.translate("SettingsWindow", u"Use Random", None))
        self.label_testName.setText(QCoreApplication.translate("SettingsWindow", u"Test Name:", None))
        self.lineEdit_testName.setPlaceholderText(QCoreApplication.translate("SettingsWindow", u"Enter test name...", None))
        self.label_testText.setText(QCoreApplication.translate("SettingsWindow", u"Test Text:", None))
        self.textEdit_testText.setPlaceholderText(QCoreApplication.translate("SettingsWindow", u"Enter typing test text (leave empty for random words)...", None))
        self.groupBox_display.setTitle(QCoreApplication.translate("SettingsWindow", u"Display Settings", None))
        self.label_width.setText(QCoreApplication.translate("SettingsWindow", u"Typing Area Width:", None))
        self.label_height.setText(QCoreApplication.translate("SettingsWindow", u"Typing Area Height:", None))
        self.label_showBorder.setText(QCoreApplication.translate("SettingsWindow", u"Show Border:", None))
        self.checkBox_showBorder.setText(QCoreApplication.translate("SettingsWindow", u"Enable border around typing area", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_typing), QCoreApplication.translate("SettingsWindow", u"Typing", None))
        self.groupBox_account.setTitle(QCoreApplication.translate("SettingsWindow", u"Google Account", None))
        self.label_accountStatus.setText(QCoreApplication.translate("SettingsWindow", u"Not logged in", None))
        self.btn_login.setText(QCoreApplication.translate("SettingsWindow", u"Login with Google", None))
        self.btn_logout.setText(QCoreApplication.translate("SettingsWindow", u"Logout", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_account), QCoreApplication.translate("SettingsWindow", u"Account", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_stats), QCoreApplication.translate("SettingsWindow", u"Statistics", None))
        self.groupBox_keybindings.setTitle(QCoreApplication.translate("SettingsWindow", u"Global Hotkeys", None))
        self.label_increaseOpacity.setText(QCoreApplication.translate("SettingsWindow", u"Increase Opacity:", None))
        self.keySeq_increaseOpacity.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Up", None))
        self.label_decreaseOpacity.setText(QCoreApplication.translate("SettingsWindow", u"Decrease Opacity:", None))
        self.keySeq_decreaseOpacity.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Down", None))
        self.label_keybindingInfo.setText(QCoreApplication.translate("SettingsWindow", u"Click on a key sequence field and press your desired key combination. These work globally when the typing overlay is visible.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_keybindings), QCoreApplication.translate("SettingsWindow", u"Keybindings", None))
        self.btn_startTyping.setText(QCoreApplication.translate("SettingsWindow", u"Start Typing Test", None))
        self.btn_apply.setText(QCoreApplication.translate("SettingsWindow", u"Apply", None))
        self.btn_close.setText(QCoreApplication.translate("SettingsWindow", u"Close", None))
    # retranslateUi

