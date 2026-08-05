"""
Settings window implementation.
"""
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QColorDialog, QMessageBox
)
from PySide6.QtGui import QColor, QCloseEvent
from PySide6.QtCore import Signal
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ui', 'generated'))
from ui_settings_window import Ui_SettingsWindow

from src.config import Config
from src.database import Database
from src.auth import GoogleAuth


class SettingsWindow(QMainWindow):
    """Settings window for TinyType application."""
    
    start_typing_test: Signal = Signal()
    settings_changed: Signal = Signal()
    
    def __init__(
        self,
        config: Config,
        database: Database,
        auth: GoogleAuth
    ) -> None:
        """
        Initialize settings window.
        
        Args:
            config: Configuration manager
            database: Database manager
            auth: Google authentication manager
        """
        super().__init__()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        
        self.config: Config = config
        self.database: Database = database
        self.auth: GoogleAuth = auth
        
        self._load_settings()
        self._connect_signals()
        self._update_auth_status()
        self._update_stats()
    
    def _load_settings(self) -> None:
        """Load settings from config into UI."""
        font_family: str = self.config.get("font_family", "Consolas")
        font_size: int = self.config.get("font_size", 24)
        
        self.ui.fontComboBox.setCurrentFont(font_family)
        self.ui.spinBox_fontSize.setValue(font_size)
        
        bg_opacity: int = self.config.get("bg_opacity", 128)
        self.ui.slider_bgOpacity.setValue(bg_opacity)
        
        move_per_word: bool = self.config.get("move_per_word", False)
        if move_per_word:
            self.ui.radio_movePerWord.setChecked(True)
        else:
            self.ui.radio_movePerChar.setChecked(True)
        
        position: str = self.config.get("position", "top_center")
        self._set_position_radio(position)
        
        self.typing_tests: list = self.config.get("typing_tests", [
            {"name": "Default", "text": ""}
        ])
        
        for test in self.typing_tests:
            self.ui.listWidget_tests.addItem(test["name"])
        
        active_test: int = self.config.get("active_test", 0)
        if 0 <= active_test < len(self.typing_tests):
            self.ui.listWidget_tests.setCurrentRow(active_test)
            self._load_selected_test()
        
        use_random: bool = self.config.get("use_random", False)
        self.ui.btn_randomTest.setChecked(use_random)
        
        width: int = self.config.get("typing_width", 1200)
        self.ui.spinBox_width.setValue(width)
        
        height: int = self.config.get("typing_height", 120)
        self.ui.spinBox_height.setValue(height)
        
        show_border: bool = self.config.get("show_border", False)
        self.ui.checkBox_showBorder.setChecked(show_border)
        
        from PySide6.QtGui import QKeySequence
        hotkey_inc: str = self.config.get("hotkey_increase_opacity", "Ctrl+Up")
        self.ui.keySeq_increaseOpacity.setKeySequence(QKeySequence(hotkey_inc))
        
        hotkey_dec: str = self.config.get("hotkey_decrease_opacity", "Ctrl+Down")
        self.ui.keySeq_decreaseOpacity.setKeySequence(QKeySequence(hotkey_dec))
    
    def _set_position_radio(self, position: str) -> None:
        """
        Set position radio button.
        
        Args:
            position: Position string
        """
        position_map = {
            "top_left": self.ui.radio_topLeft,
            "top_center": self.ui.radio_topCenter,
            "top_right": self.ui.radio_topRight,
            "center": self.ui.radio_center,
            "bottom_left": self.ui.radio_bottomLeft,
            "bottom_center": self.ui.radio_bottomCenter,
            "bottom_right": self.ui.radio_bottomRight
        }
        
        radio = position_map.get(position, self.ui.radio_topCenter)
        radio.setChecked(True)
    
    def _connect_signals(self) -> None:
        """Connect UI signals to slots."""
        self.ui.btn_untypedColor.clicked.connect(
            lambda: self._choose_color("untyped_color")
        )
        self.ui.btn_typedColor.clicked.connect(
            lambda: self._choose_color("typed_color")
        )
        self.ui.btn_errorColor.clicked.connect(
            lambda: self._choose_color("error_color")
        )
        
        self.ui.btn_login.clicked.connect(self._handle_login)
        self.ui.btn_logout.clicked.connect(self._handle_logout)
        
        self.ui.btn_apply.clicked.connect(self._apply_settings)
        self.ui.btn_close.clicked.connect(self.hide)
        self.ui.btn_startTyping.clicked.connect(self._start_typing)
        
        self.ui.btn_addTest.clicked.connect(self._add_test)
        self.ui.btn_removeTest.clicked.connect(self._remove_test)
        self.ui.listWidget_tests.currentRowChanged.connect(self._load_selected_test)
        self.ui.lineEdit_testName.textChanged.connect(self._update_test_name)
        self.ui.textEdit_testText.textChanged.connect(self._update_test_text)
        
        self.ui.tabWidget.currentChanged.connect(self._tab_changed)
    
    def _choose_color(self, config_key: str) -> None:
        """
        Open color picker dialog.
        
        Args:
            config_key: Configuration key for color
        """
        current: str = self.config.get(config_key, "#808080")
        color: QColor = QColorDialog.getColor(
            QColor(current), self, "Choose Color"
        )
        
        if color.isValid():
            self.config.set(config_key, color.name())
    
    def _handle_login(self) -> None:
        """Handle Google login button click."""
        success: bool = self.auth.login()
        if success:
            self._update_auth_status()
            QMessageBox.information(
                self, "Login Successful", 
                f"Logged in as {self.auth.user_email}"
            )
        else:
            QMessageBox.warning(
                self, "Login Failed", 
                "Failed to login with Google. Please try again."
            )
    
    def _handle_logout(self) -> None:
        """Handle logout button click."""
        self.auth.logout()
        self._update_auth_status()
    
    def _update_auth_status(self) -> None:
        """Update authentication status display."""
        if self.auth.is_logged_in():
            email: str = self.auth.user_email or "Unknown"
            self.ui.label_accountStatus.setText(
                f"Logged in as: {email}"
            )
            self.ui.btn_login.setEnabled(False)
            self.ui.btn_logout.setEnabled(True)
        else:
            self.ui.label_accountStatus.setText("Not logged in")
            self.ui.btn_login.setEnabled(True)
            self.ui.btn_logout.setEnabled(False)
    
    def _add_test(self) -> None:
        """Add a new typing test."""
        new_test: dict = {
            "name": f"Test {len(self.typing_tests) + 1}",
            "text": ""
        }
        self.typing_tests.append(new_test)
        self.ui.listWidget_tests.addItem(new_test["name"])
        self.ui.listWidget_tests.setCurrentRow(len(self.typing_tests) - 1)
    
    def _remove_test(self) -> None:
        """Remove the selected typing test."""
        current_row: int = self.ui.listWidget_tests.currentRow()
        if current_row >= 0 and len(self.typing_tests) > 0:
            self.typing_tests.pop(current_row)
            self.ui.listWidget_tests.takeItem(current_row)
    
    def _load_selected_test(self) -> None:
        """Load the selected test into the editor."""
        current_row: int = self.ui.listWidget_tests.currentRow()
        if 0 <= current_row < len(self.typing_tests):
            test: dict = self.typing_tests[current_row]
            self.ui.lineEdit_testName.setText(test["name"])
            self.ui.textEdit_testText.setPlainText(test["text"])
    
    def _update_test_name(self, name: str) -> None:
        """Update the name of the current test."""
        current_row: int = self.ui.listWidget_tests.currentRow()
        if 0 <= current_row < len(self.typing_tests):
            self.typing_tests[current_row]["name"] = name
            self.ui.listWidget_tests.item(current_row).setText(name)
    
    def _update_test_text(self) -> None:
        """Update the text of the current test."""
        current_row: int = self.ui.listWidget_tests.currentRow()
        if 0 <= current_row < len(self.typing_tests):
            text: str = self.ui.textEdit_testText.toPlainText()
            self.typing_tests[current_row]["text"] = text
    
    def _apply_settings(self) -> None:
        """Apply settings from UI to config."""
        self.config.set(
            "font_family", 
            self.ui.fontComboBox.currentFont().family()
        )
        self.config.set(
            "font_size", 
            self.ui.spinBox_fontSize.value()
        )
        self.config.set(
            "bg_opacity", 
            self.ui.slider_bgOpacity.value()
        )
        self.config.set(
            "move_per_word", 
            self.ui.radio_movePerWord.isChecked()
        )
        
        position: str = self._get_selected_position()
        self.config.set("position", position)
        
        if len(self.typing_tests) == 0:
            self.typing_tests = [{"name": "Default", "text": ""}]
        
        self.config.set("typing_tests", self.typing_tests)
        
        current_row: int = self.ui.listWidget_tests.currentRow()
        self.config.set("active_test", max(0, current_row))
        
        use_random: bool = self.ui.btn_randomTest.isChecked()
        self.config.set("use_random", use_random)
        
        width: int = self.ui.spinBox_width.value()
        self.config.set("typing_width", width)
        
        height: int = self.ui.spinBox_height.value()
        self.config.set("typing_height", height)
        
        show_border: bool = self.ui.checkBox_showBorder.isChecked()
        self.config.set("show_border", show_border)
        
        hotkey_inc: str = self.ui.keySeq_increaseOpacity.keySequence().toString()
        self.config.set("hotkey_increase_opacity", hotkey_inc)
        
        hotkey_dec: str = self.ui.keySeq_decreaseOpacity.keySequence().toString()
        self.config.set("hotkey_decrease_opacity", hotkey_dec)
        
        self.config.save()
        self.settings_changed.emit()
    
    def _get_selected_position(self) -> str:
        """
        Get selected position from radio buttons.
        
        Returns:
            Position string
        """
        if self.ui.radio_topLeft.isChecked():
            return "top_left"
        elif self.ui.radio_topCenter.isChecked():
            return "top_center"
        elif self.ui.radio_topRight.isChecked():
            return "top_right"
        elif self.ui.radio_center.isChecked():
            return "center"
        elif self.ui.radio_bottomLeft.isChecked():
            return "bottom_left"
        elif self.ui.radio_bottomCenter.isChecked():
            return "bottom_center"
        elif self.ui.radio_bottomRight.isChecked():
            return "bottom_right"
        return "top_center"
    
    def _start_typing(self) -> None:
        """Handle start typing button click."""
        self.start_typing_test.emit()
        self.hide()
    
    def _tab_changed(self, index: int) -> None:
        """
        Handle tab change event.
        
        Args:
            index: New tab index
        """
        if index == 3:
            self._update_stats()
    
    def _update_stats(self) -> None:
        """Update statistics display."""
        email: Optional[str] = self.auth.user_email
        stats = self.database.get_stats(email)
        
        stats_html: str = f"""
        <h2>Your Statistics</h2>
        <p><b>Total Tests:</b> {stats['total_tests']}</p>
        <p><b>Average WPM:</b> {stats['avg_wpm']:.1f}</p>
        <p><b>Average Accuracy:</b> {stats['avg_accuracy']:.1f}%</p>
        
        <h3>Most Problematic Characters:</h3>
        <table border="1" cellpadding="5">
        <tr><th>Character</th><th>Errors</th><th>Total</th><th>Error Rate</th></tr>
        """
        
        for char, errors, total in stats['problem_chars']:
            rate: float = (errors / total * 100) if total > 0 else 0
            stats_html += (
                f"<tr><td>{char}</td><td>{errors}</td>"
                f"<td>{total}</td><td>{rate:.1f}%</td></tr>"
            )
        
        stats_html += "</table>"
        self.ui.textBrowser_stats.setHtml(stats_html)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Handle window close event.
        
        Args:
            event: Close event
        """
        event.ignore()
        self.hide()
