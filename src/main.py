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


from typing import Optional
import sys
from PySide6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu
)
from PySide6.QtGui import QIcon, QAction, QKeySequence
from PySide6.QtCore import QObject, Signal, QEvent, Qt

from project_info import Info
from src.config import Config
from src.database import Database
from src.auth import GoogleAuth
from src.typing_overlay import TypingOverlay
from src.settings_window import SettingsWindow
from ui.splash import SplashScreen


class TinyTypeApp(QObject):
    """Main application controller."""
    
    def __init__(self) -> None:
        """Initialize TinyType application."""
        super().__init__()
        self.app: QApplication = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        self.config: Config = Config()
        self.database: Database = Database()
        self.auth: GoogleAuth = GoogleAuth()

        
        self.overlay: Optional[TypingOverlay] = None
        self.settings_window: SettingsWindow = SettingsWindow(
            self.config, self.database, self.auth
        )
        
        self._setup_tray()
        self._connect_signals()
        
        self.app.installEventFilter(self)
        
        if self.auth.is_logged_in():
            self.auth.login()
        self._show_typing_overlay()
    
    def _setup_tray(self) -> None:
        """Setup system tray icon and menu."""
        self.tray_icon: QSystemTrayIcon = QSystemTrayIcon(self.app)
        self.tray_icon.setIcon(self._create_icon())
        
        tray_menu: QMenu = QMenu()

        start_action: QAction = QAction("Start Typing Test", self.app)
        start_action.triggered.connect(self._show_typing_overlay)
        tray_menu.addAction(start_action)
        
        settings_action: QAction = QAction("Settings", self.app)
        settings_action.triggered.connect(self._show_settings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        quit_action: QAction = QAction("Quit", self.app)
        quit_action.triggered.connect(self._quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._tray_activated)
        self.tray_icon.show()
    
    def _create_icon(self) -> QIcon:
        """
        Create application icon.
        
        Returns:
            QIcon for system tray
        """
        from PySide6.QtGui import QPixmap, QPainter
        from PySide6.QtCore import Qt
        
        pixmap: QPixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter: QPainter = QPainter(pixmap)
        painter.setBrush(Qt.white)
        painter.drawEllipse(8, 8, 48, 48)
        painter.end()
        
        return QIcon(pixmap)
    
    def _connect_signals(self) -> None:
        """Connect signals between components."""
        self.settings_window.start_typing_test.connect(
            self._show_typing_overlay
        )
        self.settings_window.settings_changed.connect(
            self._handle_settings_changed
        )
    
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Filter global keyboard events.
        
        Args:
            obj: Object receiving the event
            event: Event to filter
            
        Returns:
            True if event handled, False otherwise
        """
        if event.type() == QEvent.KeyPress:
            if (event.key() == Qt.Key_Comma and 
                event.modifiers() == Qt.ControlModifier):
                self._show_settings()
                return True
        return super().eventFilter(obj, event)
    
    def _tray_activated(self, reason) -> None:
        """
        Handle system tray icon activation.
        
        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_typing_overlay()
    
    def _show_typing_overlay(self) -> None:
        """Show or create typing overlay."""
        if self.overlay is None:
            user_email: Optional[str] = self.auth.user_email
            self.overlay = TypingOverlay(
                self.config, self.database, user_email
            )
            self.overlay.test_completed.connect(
                self._handle_test_completed
            )

        self.overlay.splash: SplashScreen = SplashScreen()
        # self.overlay.splash.splash_screen.finish(self.app)
        self.overlay.show()
        self.overlay.activateWindow()
        self.overlay.setFocus()
    
    def _show_settings(self) -> None:
        """Show settings window."""
        self.settings_window.show()
        self.settings_window.activateWindow()
    
    def _handle_settings_changed(self) -> None:
        """Handle settings change event."""
        if self.overlay:
            self.overlay.apply_config()
    
    def _handle_test_completed(self, results: dict) -> None:
        """
        Handle typing test completion.
        
        Args:
            results: Test results dictionary
        """
        if self.overlay:
            self.overlay.update_user(self.auth.user_email)
    
    def _quit_app(self) -> None:
        """Quit the application."""
        if self.overlay:
            self.overlay.close()
        self.settings_window.close()
        self.tray_icon.hide()
        self.app.quit()
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Application exit code
        """
        return self.app.exec()


def main() -> None:
    """Application entry point."""
    app: TinyTypeApp = TinyTypeApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
