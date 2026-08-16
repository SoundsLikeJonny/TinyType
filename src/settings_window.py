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
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import QMainWindow, QColorDialog, QMessageBox
from PySide6.QtGui import QColor, QCloseEvent, QKeySequence, QIcon
from PySide6.QtCore import Signal

from project_info import Info
from ui.generated.ui_settings_window import Ui_SettingsWindow
from src.config import Config
from src.database import Database
from src.auth import GoogleAuth


class SettingsWindow(QMainWindow):
    """Settings window for TinyType application."""

    start_typing_test: Signal = Signal()
    settings_changed: Signal = Signal()

    def __init__(self, config: Config, database: Database, auth: GoogleAuth) -> None:
        super().__init__()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(Info.ICON_PATH))

        self.config: Config = config
        self.database: Database = database
        self.auth: GoogleAuth = auth

        self._load_settings()
        self._connect_signals()
        self._update_auth_status()
        self._update_stats()
        self._refresh_color_buttons()

    # ------------------------------------------------------------------
    # Load / save settings
    # ------------------------------------------------------------------

    def _load_settings(self) -> None:
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

        self.ui.checkBox_pauseOnFocus.setChecked(self.config.get("pause_on_focus", False))

        self.typing_tests: list = self.config.get(
            "typing_tests", [{"name": "Default", "text": ""}]
        )
        self.ui.listWidget_tests.clear()
        for test in self.typing_tests:
            self.ui.listWidget_tests.addItem(test["name"])

        active_test: int = self.config.get("active_test", 0)
        if 0 <= active_test < len(self.typing_tests):
            self.ui.listWidget_tests.setCurrentRow(active_test)
            self._load_selected_test()

        self.ui.btn_randomTest.setChecked(self.config.get("use_random", False))
        self.ui.spinBox_width.setValue(self.config.get("typing_width", 1200))
        self.ui.spinBox_height.setValue(self.config.get("typing_height", 120))
        self.ui.checkBox_showBorder.setChecked(self.config.get("show_border", False))

        text_align: str = self.config.get("text_align", "center")
        if text_align == "left":
            self.ui.radio_alignLeft.setChecked(True)
        else:
            self.ui.radio_alignCenter.setChecked(True)

        self.ui.keySeq_cycleOptionLeft.setKeySequence(
            QKeySequence(self.config.get("hotkey_cycle_mode_left", "Left"))
        )
        self.ui.keySeq_cycleOptionRight.setKeySequence(
            QKeySequence(self.config.get("hotkey_cycle_mode_right", "Right"))
        )
        self.ui.keySeq_cycleTestUp.setKeySequence(
            QKeySequence(self.config.get("hotkey_cycle_option_up", "Up"))
        )
        self.ui.keySeq_cycleTestDown.setKeySequence(
            QKeySequence(self.config.get("hotkey_cycle_option_down", "Down"))
        )
        self.ui.keySeq_cycleTestUpKey.setKeySequence(
            QKeySequence(self.config.get("hotkey_cycle_test_up", "Ctrl+Up"))
        )
        self.ui.keySeq_cycleTestDownKey.setKeySequence(
            QKeySequence(self.config.get("hotkey_cycle_test_down", "Ctrl+Down"))
        )
        self.ui.keySeq_toggleStats.setKeySequence(
            QKeySequence(self.config.get("hotkey_toggle_stats", "`"))
        )
        self.ui.keySeq_increaseOpacity.setKeySequence(
            QKeySequence(self.config.get("hotkey_increase_opacity", "Ctrl+Shift+Up"))
        )
        self.ui.keySeq_decreaseOpacity.setKeySequence(
            QKeySequence(self.config.get("hotkey_decrease_opacity", "Ctrl+Shift+Down"))
        )
        self.ui.keySeq_alignLeft.setKeySequence(
            QKeySequence(self.config.get("hotkey_align_left", "Ctrl+Alt+Left"))
        )
        self.ui.keySeq_alignCenter.setKeySequence(
            QKeySequence(self.config.get("hotkey_align_center", "Ctrl+Alt+Right"))
        )

        self._load_themes_list()

    def _apply_settings(self) -> None:
        self.config.set("font_family", self.ui.fontComboBox.currentFont().family())
        self.config.set("font_size", self.ui.spinBox_fontSize.value())
        self.config.set("bg_opacity", self.ui.slider_bgOpacity.value())
        self.config.set("move_per_word", self.ui.radio_movePerWord.isChecked())
        self.config.set("pause_on_focus", self.ui.checkBox_pauseOnFocus.isChecked())
        self.config.set("text_align", "left" if self.ui.radio_alignLeft.isChecked() else "center")

        if not self.typing_tests:
            self.typing_tests = [{"name": "Default", "text": ""}]
        self.config.set("typing_tests", self.typing_tests)
        self.config.set("active_test", max(0, self.ui.listWidget_tests.currentRow()))
        self.config.set("use_random", self.ui.btn_randomTest.isChecked())
        self.config.set("typing_width", self.ui.spinBox_width.value())
        self.config.set("typing_height", self.ui.spinBox_height.value())
        self.config.set("show_border", self.ui.checkBox_showBorder.isChecked())

        self.config.set("hotkey_cycle_mode_left",
                        self.ui.keySeq_cycleOptionLeft.keySequence().toString())
        self.config.set("hotkey_cycle_mode_right",
                        self.ui.keySeq_cycleOptionRight.keySequence().toString())
        self.config.set("hotkey_cycle_option_up",
                        self.ui.keySeq_cycleTestUp.keySequence().toString())
        self.config.set("hotkey_cycle_option_down",
                        self.ui.keySeq_cycleTestDown.keySequence().toString())
        self.config.set("hotkey_cycle_test_up",
                        self.ui.keySeq_cycleTestUpKey.keySequence().toString())
        self.config.set("hotkey_cycle_test_down",
                        self.ui.keySeq_cycleTestDownKey.keySequence().toString())
        self.config.set("hotkey_toggle_stats",
                        self.ui.keySeq_toggleStats.keySequence().toString())
        self.config.set("hotkey_increase_opacity",
                        self.ui.keySeq_increaseOpacity.keySequence().toString())
        self.config.set("hotkey_decrease_opacity",
                        self.ui.keySeq_decreaseOpacity.keySequence().toString())
        self.config.set("hotkey_align_left",
                        self.ui.keySeq_alignLeft.keySequence().toString())
        self.config.set("hotkey_align_center",
                        self.ui.keySeq_alignCenter.keySequence().toString())

        self.config.save()
        self.settings_changed.emit()

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        self.ui.btn_untypedColor.clicked.connect(
            lambda: self._choose_color("untyped_color"))
        self.ui.btn_typedColor.clicked.connect(
            lambda: self._choose_color("typed_color"))
        self.ui.btn_errorColor.clicked.connect(
            lambda: self._choose_color("error_color"))
        self.ui.btn_windowColor.clicked.connect(
            lambda: self._choose_color("window_color"))

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
        self.ui.comboBox_testCategory.currentIndexChanged.connect(self._update_test_category)
        self.ui.comboBox_testCategory.addItem("Error Gen")

        self.ui.btn_applyTheme.clicked.connect(self._apply_theme)
        self.ui.btn_saveTheme.clicked.connect(self._save_theme)
        self.ui.btn_updateTheme.clicked.connect(self._update_theme)
        self.ui.btn_deleteTheme.clicked.connect(self._delete_theme)
        self.ui.listWidget_themes.currentRowChanged.connect(self._preview_theme_name)

        self.ui.tabWidget.currentChanged.connect(self._tab_changed)

    # ------------------------------------------------------------------
    # Color picking
    # ------------------------------------------------------------------

    def _choose_color(self, config_key: str) -> None:
        current: str = self.config.get(config_key, "#808080")
        color: QColor = QColorDialog.getColor(QColor(current), self, "Choose Color")
        if color.isValid():
            self.config.set(config_key, color.name())
            self._refresh_color_buttons()

    def _refresh_color_buttons(self) -> None:
        for btn, key in [
            (self.ui.btn_untypedColor, "untyped_color"),
            (self.ui.btn_typedColor, "typed_color"),
            (self.ui.btn_errorColor, "error_color"),
            (self.ui.btn_windowColor, "window_color"),
        ]:
            color = self.config.get(key, "#808080")
            btn.setStyleSheet(
                f"background-color: {color}; color: {'#ffffff' if _is_dark(color) else '#000000'};"
            )

    # ------------------------------------------------------------------
    # Themes
    # ------------------------------------------------------------------

    def _load_themes_list(self) -> None:
        self.ui.listWidget_themes.clear()
        themes: list = self.config.get_themes()
        for theme in themes:
            self.ui.listWidget_themes.addItem(theme["name"])

    def _preview_theme_name(self, row: int) -> None:
        themes: list = self.config.get_themes()
        if 0 <= row < len(themes):
            self.ui.lineEdit_themeName.setText(themes[row]["name"])

    def _apply_theme(self) -> None:
        row = self.ui.listWidget_themes.currentRow()
        themes: list = self.config.get_themes()
        if 0 <= row < len(themes):
            theme = themes[row]
            self.config.set("untyped_color", theme.get("primary", "#808080"))
            self.config.set("typed_color", theme.get("secondary", "#8b047e"))
            self.config.set("error_color", theme.get("error", "#FF0000"))
            self.config.set("window_color", theme.get("window", "#000000"))
            self._refresh_color_buttons()

    def _save_theme(self) -> None:
        name = self.ui.lineEdit_themeName.text().strip()
        if not name:
            QMessageBox.warning(self, "Theme Name", "Please enter a theme name.")
            return
        new_theme = {
            "name": name,
            "primary": self.config.get("untyped_color", "#808080"),
            "secondary": self.config.get("typed_color", "#8b047e"),
            "error": self.config.get("error_color", "#FF0000"),
            "window": self.config.get("window_color", "#000000"),
        }
        custom: list = self.config.get("custom_themes", [])
        custom.append(new_theme)
        self.config.set_custom_themes(custom)
        self.config.save()
        self._load_themes_list()
        built_in_count = len(self.config.get("themes", []))
        self.ui.listWidget_themes.setCurrentRow(built_in_count + len(custom) - 1)

    def _update_theme(self) -> None:
        row = self.ui.listWidget_themes.currentRow()
        built_in_count = len(self.config.get("themes", []))
        custom: list = self.config.get("custom_themes", [])
        custom_row = row - built_in_count
        if 0 <= custom_row < len(custom):
            name = self.ui.lineEdit_themeName.text().strip() or custom[custom_row]["name"]
            custom[custom_row] = {
                "name": name,
                "primary": self.config.get("untyped_color", "#808080"),
                "secondary": self.config.get("typed_color", "#8b047e"),
                "error": self.config.get("error_color", "#FF0000"),
                "window": self.config.get("window_color", "#000000"),
            }
            self.config.set_custom_themes(custom)
            self.config.save()
            self._load_themes_list()
            self.ui.listWidget_themes.setCurrentRow(row)

    def _delete_theme(self) -> None:
        row = self.ui.listWidget_themes.currentRow()
        built_in_count = len(self.config.get("themes", []))
        custom: list = self.config.get("custom_themes", [])
        custom_row = row - built_in_count
        if 0 <= custom_row < len(custom):
            custom.pop(custom_row)
            self.config.set_custom_themes(custom)
            self.config.save()
            self._load_themes_list()

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    def _add_test(self) -> None:
        new_test = {"name": f"Test {len(self.typing_tests) + 1}", "text": "", "category": "word_pool"}
        self.typing_tests.append(new_test)
        self.ui.listWidget_tests.addItem(new_test["name"])
        self.ui.listWidget_tests.setCurrentRow(len(self.typing_tests) - 1)

    def _remove_test(self) -> None:
        row = self.ui.listWidget_tests.currentRow()
        if row >= 0 and self.typing_tests:
            self.typing_tests.pop(row)
            self.ui.listWidget_tests.takeItem(row)

    def _load_selected_test(self) -> None:
        row = self.ui.listWidget_tests.currentRow()
        if 0 <= row < len(self.typing_tests):
            test = self.typing_tests[row]
            for w in (self.ui.lineEdit_testName,
                      self.ui.textEdit_testText,
                      self.ui.comboBox_testCategory):
                w.blockSignals(True)
            self.ui.lineEdit_testName.setText(test["name"])
            self.ui.textEdit_testText.setPlainText(test.get("text", ""))
            cat = test.get("category", "word_pool")
            idx = 0 if cat == "word_pool" else (2 if cat == "error_gen" else 1)
            self.ui.comboBox_testCategory.setCurrentIndex(idx)
            for w in (self.ui.lineEdit_testName,
                      self.ui.textEdit_testText,
                      self.ui.comboBox_testCategory):
                w.blockSignals(False)

    def _update_test_name(self, name: str) -> None:
        row = self.ui.listWidget_tests.currentRow()
        if 0 <= row < len(self.typing_tests):
            self.typing_tests[row]["name"] = name
            self.ui.listWidget_tests.item(row).setText(name)

    def _update_test_text(self) -> None:
        row = self.ui.listWidget_tests.currentRow()
        if 0 <= row < len(self.typing_tests):
            self.typing_tests[row]["text"] = self.ui.textEdit_testText.toPlainText()

    def _update_test_category(self, index: int) -> None:
        row = self.ui.listWidget_tests.currentRow()
        if 0 <= row < len(self.typing_tests):
            self.typing_tests[row]["category"] = (
                "word_pool" if index == 0 else ("error_gen" if index == 2 else "quote")
            )

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def _handle_login(self) -> None:
        success = self.auth.login()
        if success:
            self._update_auth_status()
            QMessageBox.information(self, "Login Successful",
                                    f"Logged in as {self.auth.user_email}")
        else:
            QMessageBox.warning(self, "Login Failed",
                                "Failed to login with Google. Please try again.")

    def _handle_logout(self) -> None:
        self.auth.logout()
        self._update_auth_status()

    def _update_auth_status(self) -> None:
        if self.auth.is_logged_in():
            self.ui.label_accountStatus.setText(f"Logged in as: {self.auth.user_email or 'Unknown'}")
            self.ui.btn_login.setEnabled(False)
            self.ui.btn_logout.setEnabled(True)
        else:
            self.ui.label_accountStatus.setText("Not logged in")
            self.ui.btn_login.setEnabled(True)
            self.ui.btn_logout.setEnabled(False)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def _tab_changed(self, index: int) -> None:
        if index == 3:
            self._update_stats()

    def _update_stats(self) -> None:
        stats = self.database.get_stats(self.auth.user_email)
        html = f"""
        <h2>Your Statistics</h2>
        <p><b>Total Tests:</b> {stats['total_tests']}</p>
        <p><b>Average WPM:</b> {stats['avg_wpm']:.1f}</p>
        <p><b>Average Accuracy:</b> {stats['avg_accuracy']:.1f}%</p>
        <h3>Most Problematic Characters:</h3>
        <table border="1" cellpadding="5">
        <tr><th>Character</th><th>Errors</th><th>Total</th><th>Error Rate</th></tr>
        """
        for char, errors, total in stats["problem_chars"]:
            rate = (errors / total * 100) if total > 0 else 0
            html += (f"<tr><td>{char}</td><td>{errors}</td>"
                     f"<td>{total}</td><td>{rate:.1f}%</td></tr>")
        html += "</table>"
        self.ui.textBrowser_stats.setHtml(html)

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def _start_typing(self) -> None:
        self.start_typing_test.emit()
        self.hide()

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.hide()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.ui.slider_bgOpacity.setValue(self.config.get("bg_opacity", 128))
        self._refresh_color_buttons()
        self._load_themes_list()


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _is_dark(hex_color: str) -> bool:
    try:
        c = QColor(hex_color)
        return (c.red() * 299 + c.green() * 587 + c.blue() * 114) / 1000 < 128
    except Exception:
        return True
