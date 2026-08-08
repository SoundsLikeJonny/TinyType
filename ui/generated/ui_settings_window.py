# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_settings_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
    QFormLayout, QGroupBox, QHBoxLayout, QKeySequenceEdit,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QTabWidget,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(640, 720)
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
        self.label_primaryColor = QLabel(self.groupBox_colors)
        self.label_primaryColor.setObjectName(u"label_primaryColor")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_primaryColor)

        self.btn_untypedColor = QPushButton(self.groupBox_colors)
        self.btn_untypedColor.setObjectName(u"btn_untypedColor")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.btn_untypedColor)

        self.label_secondaryColor = QLabel(self.groupBox_colors)
        self.label_secondaryColor.setObjectName(u"label_secondaryColor")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_secondaryColor)

        self.btn_typedColor = QPushButton(self.groupBox_colors)
        self.btn_typedColor.setObjectName(u"btn_typedColor")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.btn_typedColor)

        self.label_errorColor = QLabel(self.groupBox_colors)
        self.label_errorColor.setObjectName(u"label_errorColor")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_errorColor)

        self.btn_errorColor = QPushButton(self.groupBox_colors)
        self.btn_errorColor.setObjectName(u"btn_errorColor")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.btn_errorColor)

        self.label_windowColor = QLabel(self.groupBox_colors)
        self.label_windowColor.setObjectName(u"label_windowColor")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_windowColor)

        self.btn_windowColor = QPushButton(self.groupBox_colors)
        self.btn_windowColor.setObjectName(u"btn_windowColor")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.btn_windowColor)

        self.label_bgOpacity = QLabel(self.groupBox_colors)
        self.label_bgOpacity.setObjectName(u"label_bgOpacity")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_bgOpacity)

        self.slider_bgOpacity = QSlider(self.groupBox_colors)
        self.slider_bgOpacity.setObjectName(u"slider_bgOpacity")
        self.slider_bgOpacity.setMaximum(255)
        self.slider_bgOpacity.setValue(128)
        self.slider_bgOpacity.setOrientation(Qt.Horizontal)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.slider_bgOpacity)


        self.verticalLayout_2.addWidget(self.groupBox_colors)

        self.groupBox_themes = QGroupBox(self.tab_appearance)
        self.groupBox_themes.setObjectName(u"groupBox_themes")
        self.verticalLayout_themes = QVBoxLayout(self.groupBox_themes)
        self.verticalLayout_themes.setObjectName(u"verticalLayout_themes")
        self.horizontalLayout_themes = QHBoxLayout()
        self.horizontalLayout_themes.setObjectName(u"horizontalLayout_themes")
        self.listWidget_themes = QListWidget(self.groupBox_themes)
        self.listWidget_themes.setObjectName(u"listWidget_themes")

        self.horizontalLayout_themes.addWidget(self.listWidget_themes)

        self.verticalLayout_themeButtons = QVBoxLayout()
        self.verticalLayout_themeButtons.setObjectName(u"verticalLayout_themeButtons")
        self.btn_applyTheme = QPushButton(self.groupBox_themes)
        self.btn_applyTheme.setObjectName(u"btn_applyTheme")

        self.verticalLayout_themeButtons.addWidget(self.btn_applyTheme)

        self.btn_saveTheme = QPushButton(self.groupBox_themes)
        self.btn_saveTheme.setObjectName(u"btn_saveTheme")

        self.verticalLayout_themeButtons.addWidget(self.btn_saveTheme)

        self.btn_updateTheme = QPushButton(self.groupBox_themes)
        self.btn_updateTheme.setObjectName(u"btn_updateTheme")

        self.verticalLayout_themeButtons.addWidget(self.btn_updateTheme)

        self.btn_deleteTheme = QPushButton(self.groupBox_themes)
        self.btn_deleteTheme.setObjectName(u"btn_deleteTheme")

        self.verticalLayout_themeButtons.addWidget(self.btn_deleteTheme)

        self.verticalSpacer_themes = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_themeButtons.addItem(self.verticalSpacer_themes)


        self.horizontalLayout_themes.addLayout(self.verticalLayout_themeButtons)


        self.verticalLayout_themes.addLayout(self.horizontalLayout_themes)

        self.horizontalLayout_themeName = QHBoxLayout()
        self.horizontalLayout_themeName.setObjectName(u"horizontalLayout_themeName")
        self.label_themeName = QLabel(self.groupBox_themes)
        self.label_themeName.setObjectName(u"label_themeName")

        self.horizontalLayout_themeName.addWidget(self.label_themeName)

        self.lineEdit_themeName = QLineEdit(self.groupBox_themes)
        self.lineEdit_themeName.setObjectName(u"lineEdit_themeName")

        self.horizontalLayout_themeName.addWidget(self.lineEdit_themeName)


        self.verticalLayout_themes.addLayout(self.horizontalLayout_themeName)


        self.verticalLayout_2.addWidget(self.groupBox_themes)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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

        self.checkBox_pauseOnFocus = QCheckBox(self.groupBox_typingBehavior)
        self.checkBox_pauseOnFocus.setObjectName(u"checkBox_pauseOnFocus")

        self.verticalLayout_4.addWidget(self.checkBox_pauseOnFocus)


        self.verticalLayout_3.addWidget(self.groupBox_typingBehavior)

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

        self.horizontalLayout_testName = QHBoxLayout()
        self.horizontalLayout_testName.setObjectName(u"horizontalLayout_testName")
        self.lineEdit_testName = QLineEdit(self.groupBox_typingTests)
        self.lineEdit_testName.setObjectName(u"lineEdit_testName")

        self.horizontalLayout_testName.addWidget(self.lineEdit_testName)

        self.comboBox_testCategory = QComboBox(self.groupBox_typingTests)
        self.comboBox_testCategory.addItem("")
        self.comboBox_testCategory.addItem("")
        self.comboBox_testCategory.setObjectName(u"comboBox_testCategory")

        self.horizontalLayout_testName.addWidget(self.comboBox_testCategory)


        self.verticalLayout_9.addLayout(self.horizontalLayout_testName)

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

        self.label_textAlign = QLabel(self.groupBox_display)
        self.label_textAlign.setObjectName(u"label_textAlign")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_textAlign)

        self.horizontalLayout_align = QHBoxLayout()
        self.horizontalLayout_align.setObjectName(u"horizontalLayout_align")
        self.radio_alignCenter = QRadioButton(self.groupBox_display)
        self.radio_alignCenter.setObjectName(u"radio_alignCenter")
        self.radio_alignCenter.setChecked(True)

        self.horizontalLayout_align.addWidget(self.radio_alignCenter)

        self.radio_alignLeft = QRadioButton(self.groupBox_display)
        self.radio_alignLeft.setObjectName(u"radio_alignLeft")

        self.horizontalLayout_align.addWidget(self.radio_alignLeft)


        self.formLayout_4.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_align)


        self.verticalLayout_3.addWidget(self.groupBox_display)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        self.label_cycleModeLeft = QLabel(self.groupBox_keybindings)
        self.label_cycleModeLeft.setObjectName(u"label_cycleModeLeft")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_cycleModeLeft)

        self.keySeq_cycleOptionLeft = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_cycleOptionLeft.setObjectName(u"keySeq_cycleOptionLeft")

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.keySeq_cycleOptionLeft)

        self.label_cycleModeRight = QLabel(self.groupBox_keybindings)
        self.label_cycleModeRight.setObjectName(u"label_cycleModeRight")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_cycleModeRight)

        self.keySeq_cycleOptionRight = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_cycleOptionRight.setObjectName(u"keySeq_cycleOptionRight")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.keySeq_cycleOptionRight)

        self.label_cycleOptionUp = QLabel(self.groupBox_keybindings)
        self.label_cycleOptionUp.setObjectName(u"label_cycleOptionUp")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.label_cycleOptionUp)

        self.keySeq_cycleTestUp = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_cycleTestUp.setObjectName(u"keySeq_cycleTestUp")

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.keySeq_cycleTestUp)

        self.label_cycleOptionDown = QLabel(self.groupBox_keybindings)
        self.label_cycleOptionDown.setObjectName(u"label_cycleOptionDown")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.label_cycleOptionDown)

        self.keySeq_cycleTestDown = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_cycleTestDown.setObjectName(u"keySeq_cycleTestDown")

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.keySeq_cycleTestDown)

        self.label_cycleTestUp = QLabel(self.groupBox_keybindings)
        self.label_cycleTestUp.setObjectName(u"label_cycleTestUp")

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.label_cycleTestUp)

        self.keySeq_cycleTestUpKey = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_cycleTestUpKey.setObjectName(u"keySeq_cycleTestUpKey")

        self.formLayout_5.setWidget(4, QFormLayout.FieldRole, self.keySeq_cycleTestUpKey)

        self.label_cycleTestDown = QLabel(self.groupBox_keybindings)
        self.label_cycleTestDown.setObjectName(u"label_cycleTestDown")

        self.formLayout_5.setWidget(5, QFormLayout.LabelRole, self.label_cycleTestDown)

        self.keySeq_cycleTestDownKey = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_cycleTestDownKey.setObjectName(u"keySeq_cycleTestDownKey")

        self.formLayout_5.setWidget(5, QFormLayout.FieldRole, self.keySeq_cycleTestDownKey)

        self.label_toggleStats = QLabel(self.groupBox_keybindings)
        self.label_toggleStats.setObjectName(u"label_toggleStats")

        self.formLayout_5.setWidget(6, QFormLayout.LabelRole, self.label_toggleStats)

        self.keySeq_toggleStats = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_toggleStats.setObjectName(u"keySeq_toggleStats")

        self.formLayout_5.setWidget(6, QFormLayout.FieldRole, self.keySeq_toggleStats)

        self.label_increaseOpacity = QLabel(self.groupBox_keybindings)
        self.label_increaseOpacity.setObjectName(u"label_increaseOpacity")

        self.formLayout_5.setWidget(7, QFormLayout.LabelRole, self.label_increaseOpacity)

        self.keySeq_increaseOpacity = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_increaseOpacity.setObjectName(u"keySeq_increaseOpacity")

        self.formLayout_5.setWidget(7, QFormLayout.FieldRole, self.keySeq_increaseOpacity)

        self.label_decreaseOpacity = QLabel(self.groupBox_keybindings)
        self.label_decreaseOpacity.setObjectName(u"label_decreaseOpacity")

        self.formLayout_5.setWidget(8, QFormLayout.LabelRole, self.label_decreaseOpacity)

        self.keySeq_decreaseOpacity = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_decreaseOpacity.setObjectName(u"keySeq_decreaseOpacity")

        self.formLayout_5.setWidget(8, QFormLayout.FieldRole, self.keySeq_decreaseOpacity)

        self.label_alignLeft = QLabel(self.groupBox_keybindings)
        self.label_alignLeft.setObjectName(u"label_alignLeft")

        self.formLayout_5.setWidget(9, QFormLayout.LabelRole, self.label_alignLeft)

        self.keySeq_alignLeft = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_alignLeft.setObjectName(u"keySeq_alignLeft")

        self.formLayout_5.setWidget(9, QFormLayout.FieldRole, self.keySeq_alignLeft)

        self.label_alignCenter = QLabel(self.groupBox_keybindings)
        self.label_alignCenter.setObjectName(u"label_alignCenter")

        self.formLayout_5.setWidget(10, QFormLayout.LabelRole, self.label_alignCenter)

        self.keySeq_alignCenter = QKeySequenceEdit(self.groupBox_keybindings)
        self.keySeq_alignCenter.setObjectName(u"keySeq_alignCenter")

        self.formLayout_5.setWidget(10, QFormLayout.FieldRole, self.keySeq_alignCenter)


        self.verticalLayout_11.addWidget(self.groupBox_keybindings)

        self.label_keybindingInfo = QLabel(self.tab_keybindings)
        self.label_keybindingInfo.setObjectName(u"label_keybindingInfo")
        self.label_keybindingInfo.setWordWrap(True)

        self.verticalLayout_11.addWidget(self.label_keybindingInfo)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab_keybindings, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.btn_startTyping = QPushButton(self.centralwidget)
        self.btn_startTyping.setObjectName(u"btn_startTyping")

        self.horizontalLayout_bottom.addWidget(self.btn_startTyping)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer)

        self.btn_apply = QPushButton(self.centralwidget)
        self.btn_apply.setObjectName(u"btn_apply")

        self.horizontalLayout_bottom.addWidget(self.btn_apply)

        self.btn_close = QPushButton(self.centralwidget)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout_bottom.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout_bottom)

        SettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsWindow)

        self.tabWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"TinyType Settings", None))
        self.groupBox_font.setTitle(QCoreApplication.translate("SettingsWindow", u"Font Settings", None))
        self.label_font.setText(QCoreApplication.translate("SettingsWindow", u"Font:", None))
        self.label_fontSize.setText(QCoreApplication.translate("SettingsWindow", u"Font Size:", None))
        self.groupBox_colors.setTitle(QCoreApplication.translate("SettingsWindow", u"Color Settings", None))
        self.label_primaryColor.setText(QCoreApplication.translate("SettingsWindow", u"Primary Color:", None))
        self.btn_untypedColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_secondaryColor.setText(QCoreApplication.translate("SettingsWindow", u"Secondary Color:", None))
        self.btn_typedColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_errorColor.setText(QCoreApplication.translate("SettingsWindow", u"Error Color:", None))
        self.btn_errorColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_windowColor.setText(QCoreApplication.translate("SettingsWindow", u"Window Color:", None))
        self.btn_windowColor.setText(QCoreApplication.translate("SettingsWindow", u"Choose Color", None))
        self.label_bgOpacity.setText(QCoreApplication.translate("SettingsWindow", u"Background Opacity:", None))
        self.groupBox_themes.setTitle(QCoreApplication.translate("SettingsWindow", u"Color Themes", None))
        self.btn_applyTheme.setText(QCoreApplication.translate("SettingsWindow", u"Apply Theme", None))
        self.btn_saveTheme.setText(QCoreApplication.translate("SettingsWindow", u"Save as New", None))
        self.btn_updateTheme.setText(QCoreApplication.translate("SettingsWindow", u"Update Theme", None))
        self.btn_deleteTheme.setText(QCoreApplication.translate("SettingsWindow", u"Delete Theme", None))
        self.label_themeName.setText(QCoreApplication.translate("SettingsWindow", u"Theme Name:", None))
        self.lineEdit_themeName.setPlaceholderText(QCoreApplication.translate("SettingsWindow", u"Enter theme name...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_appearance), QCoreApplication.translate("SettingsWindow", u"Appearance", None))
        self.groupBox_typingBehavior.setTitle(QCoreApplication.translate("SettingsWindow", u"Typing Behavior", None))
        self.radio_movePerChar.setText(QCoreApplication.translate("SettingsWindow", u"Move text per character", None))
        self.radio_movePerWord.setText(QCoreApplication.translate("SettingsWindow", u"Move text per word", None))
        self.checkBox_pauseOnFocus.setText(QCoreApplication.translate("SettingsWindow", u"Pause test on focus loss or 5s inactivity", None))
        self.groupBox_typingTests.setTitle(QCoreApplication.translate("SettingsWindow", u"Typing Tests", None))
        self.btn_addTest.setText(QCoreApplication.translate("SettingsWindow", u"Add Test", None))
        self.btn_removeTest.setText(QCoreApplication.translate("SettingsWindow", u"Remove Selected", None))
        self.btn_randomTest.setText(QCoreApplication.translate("SettingsWindow", u"Use Random", None))
        self.label_testName.setText(QCoreApplication.translate("SettingsWindow", u"Test Name / Category:", None))
        self.lineEdit_testName.setPlaceholderText(QCoreApplication.translate("SettingsWindow", u"Enter test name...", None))
        self.comboBox_testCategory.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Word Pool", None))
        self.comboBox_testCategory.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Quote", None))

        self.label_testText.setText(QCoreApplication.translate("SettingsWindow", u"Test Text:", None))
        self.textEdit_testText.setPlaceholderText(QCoreApplication.translate("SettingsWindow", u"Enter typing test text (leave empty for random words)...", None))
        self.groupBox_display.setTitle(QCoreApplication.translate("SettingsWindow", u"Display Settings", None))
        self.label_width.setText(QCoreApplication.translate("SettingsWindow", u"Typing Area Width:", None))
        self.label_height.setText(QCoreApplication.translate("SettingsWindow", u"Typing Area Height:", None))
        self.label_showBorder.setText(QCoreApplication.translate("SettingsWindow", u"Show Border:", None))
        self.checkBox_showBorder.setText(QCoreApplication.translate("SettingsWindow", u"Enable border around typing area", None))
        self.label_textAlign.setText(QCoreApplication.translate("SettingsWindow", u"Caret Alignment:", None))
        self.radio_alignCenter.setText(QCoreApplication.translate("SettingsWindow", u"Centered", None))
        self.radio_alignLeft.setText(QCoreApplication.translate("SettingsWindow", u"Left-aligned", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_typing), QCoreApplication.translate("SettingsWindow", u"Typing", None))
        self.groupBox_account.setTitle(QCoreApplication.translate("SettingsWindow", u"Google Account", None))
        self.label_accountStatus.setText(QCoreApplication.translate("SettingsWindow", u"Not logged in", None))
        self.btn_login.setText(QCoreApplication.translate("SettingsWindow", u"Login with Google", None))
        self.btn_logout.setText(QCoreApplication.translate("SettingsWindow", u"Logout", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_account), QCoreApplication.translate("SettingsWindow", u"Account", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_stats), QCoreApplication.translate("SettingsWindow", u"Statistics", None))
        self.groupBox_keybindings.setTitle(QCoreApplication.translate("SettingsWindow", u"Key Commands", None))
#if QT_CONFIG(tooltip)
        self.label_cycleModeLeft.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to cycle to the previous test mode: Words \u2192 Quotes \u2192 Time \u2192 Words. Only works when no test is running.", None))
#endif // QT_CONFIG(tooltip)
        self.label_cycleModeLeft.setText(QCoreApplication.translate("SettingsWindow", u"Switch Mode Left (Words/Time/Quotes):", None))
        self.keySeq_cycleOptionLeft.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Left", None))
#if QT_CONFIG(tooltip)
        self.label_cycleModeRight.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to cycle to the next test mode: Words \u2192 Time \u2192 Quotes \u2192 Words. Only works when no test is running.", None))
#endif // QT_CONFIG(tooltip)
        self.label_cycleModeRight.setText(QCoreApplication.translate("SettingsWindow", u"Switch Mode Right (Words/Time/Quotes):", None))
        self.keySeq_cycleOptionRight.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Right", None))
#if QT_CONFIG(tooltip)
        self.label_cycleOptionUp.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to increase the value of the current mode option \u2014 e.g. 25\u219250 words, 30s\u219260s, or short\u2192medium quotes. Only works when no test is running.", None))
#endif // QT_CONFIG(tooltip)
        self.label_cycleOptionUp.setText(QCoreApplication.translate("SettingsWindow", u"Cycle Test Variation Up (within mode):", None))
        self.keySeq_cycleTestUp.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Up", None))
#if QT_CONFIG(tooltip)
        self.label_cycleOptionDown.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to decrease the value of the current mode option \u2014 e.g. 50\u219225 words, 60s\u219230s, or medium\u2192short quotes. Only works when no test is running.", None))
#endif // QT_CONFIG(tooltip)
        self.label_cycleOptionDown.setText(QCoreApplication.translate("SettingsWindow", u"Cycle Test Variation Down (within mode):", None))
        self.keySeq_cycleTestDown.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Down", None))
#if QT_CONFIG(tooltip)
        self.label_cycleTestUp.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to switch to the previous typing test in your list (e.g. Default \u2192 Test 2).", None))
#endif // QT_CONFIG(tooltip)
        self.label_cycleTestUp.setText(QCoreApplication.translate("SettingsWindow", u"Cycle Test Text Up:", None))
        self.keySeq_cycleTestUpKey.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Up", None))
#if QT_CONFIG(tooltip)
        self.label_cycleTestDown.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to switch to the next typing test in your list (e.g. Test 2 \u2192 Default).", None))
#endif // QT_CONFIG(tooltip)
        self.label_cycleTestDown.setText(QCoreApplication.translate("SettingsWindow", u"Cycle Test Text Down:", None))
        self.keySeq_cycleTestDownKey.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Down", None))
#if QT_CONFIG(tooltip)
        self.label_toggleStats.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to show or hide the stats bar (WPM, accuracy, time, and the Words/Time/Quotes mode selector).", None))
#endif // QT_CONFIG(tooltip)
        self.label_toggleStats.setText(QCoreApplication.translate("SettingsWindow", u"Toggle Stats Bar:", None))
        self.keySeq_toggleStats.setKeySequence(QCoreApplication.translate("SettingsWindow", u"`", None))
#if QT_CONFIG(tooltip)
        self.label_increaseOpacity.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to make the overlay background more opaque (0\u2013255).", None))
#endif // QT_CONFIG(tooltip)
        self.label_increaseOpacity.setText(QCoreApplication.translate("SettingsWindow", u"Increase Opacity:", None))
        self.keySeq_increaseOpacity.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Shift+Up", None))
#if QT_CONFIG(tooltip)
        self.label_decreaseOpacity.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to make the overlay background more transparent (0\u2013255).", None))
#endif // QT_CONFIG(tooltip)
        self.label_decreaseOpacity.setText(QCoreApplication.translate("SettingsWindow", u"Decrease Opacity:", None))
        self.keySeq_decreaseOpacity.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Shift+Down", None))
#if QT_CONFIG(tooltip)
        self.label_alignLeft.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to switch the typing caret to left-aligned (stays at a fixed column).", None))
#endif // QT_CONFIG(tooltip)
        self.label_alignLeft.setText(QCoreApplication.translate("SettingsWindow", u"Caret Align Left:", None))
        self.keySeq_alignLeft.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Alt+Left", None))
#if QT_CONFIG(tooltip)
        self.label_alignCenter.setToolTip(QCoreApplication.translate("SettingsWindow", u"Press this key to switch the typing caret to centered in the overlay.", None))
#endif // QT_CONFIG(tooltip)
        self.label_alignCenter.setText(QCoreApplication.translate("SettingsWindow", u"Caret Align Center:", None))
        self.keySeq_alignCenter.setKeySequence(QCoreApplication.translate("SettingsWindow", u"Ctrl+Alt+Right", None))
        self.label_keybindingInfo.setText(QCoreApplication.translate("SettingsWindow", u"Click a field and press your desired key combination. Overlay keys work when the typing overlay is focused.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_keybindings), QCoreApplication.translate("SettingsWindow", u"Keybindings", None))
        self.btn_startTyping.setText(QCoreApplication.translate("SettingsWindow", u"Start Typing Test", None))
        self.btn_apply.setText(QCoreApplication.translate("SettingsWindow", u"Apply", None))
        self.btn_close.setText(QCoreApplication.translate("SettingsWindow", u"Close", None))
    # retranslateUi

