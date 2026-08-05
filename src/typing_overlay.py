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
from typing import Optional, Dict, Any
import sys
import os
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QColor, QKeyEvent, QPainter, QIcon

from project_info import Info

from ui.generated.ui_typing_overlay import Ui_TypingOverlay

from src.typing_engine import TypingEngine
from src.config import Config
from src.database import Database
from ui.splash import SplashScreen


class TypingOverlay(QWidget):
    """Frameless, translucent typing test overlay."""
    
    test_completed: Signal = Signal(dict)
    
    def __init__(
        self,
        config: Config,
        database: Database,
        user_email: Optional[str]
    ) -> None:
        """
        Initialize typing overlay.
        
        Args:
            config: Configuration manager
            database: Database manager
            user_email: Current user email (None if not logged in)
        """
        super().__init__()
        self.ui = Ui_TypingOverlay()
        self.ui.setupUi(self)
        
        self.config: Config = config
        self.database: Database = database
        self.user_email: Optional[str] = user_email
        self.engine: TypingEngine = TypingEngine()
        self.showing_results: bool = False
        self.display_word_start: int = 0
        self.current_test_name: str = "Default"
        self.dragging: bool = False
        self.drag_start_pos = None
        
        self._setup_window()
        self._apply_config()
        self._update_position()
        self._load_problem_chars()
        self._start_new_test()
        
        self.stats_timer: QTimer = QTimer()
        self.stats_timer.timeout.connect(self._update_stats_display)
        self.stats_timer.start(100)
    
    def _setup_window(self) -> None:
        """Setup window properties."""
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setWindowIcon(QIcon(Info.ICON_PATH))
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def _apply_config(self) -> None:
        """Apply configuration to overlay appearance."""
        font_family: str = self.config.get("font_family", "Consolas")
        font_size: int = self.config.get("font_size", 24)
        width: int = self.config.get("typing_width", 1200)
        height: int = self.config.get("typing_height", 120)
        show_border: bool = self.config.get("show_border", False)
        
        font: QFont = QFont(font_family, font_size)
        self.ui.label_text.setFont(font)
        
        border_style: str = "2px solid white" if show_border else "none"
        self.ui.label_text.setStyleSheet(
            f"padding: 5px; background: transparent; border: {border_style};"
        )
        
        self.setFixedSize(width, height)
    
    def _update_position(self) -> None:
        """Update overlay position on screen."""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        position: str = self.config.get("position", "top_center")
        
        x: int = 0
        y: int = 0
        
        if "top" in position:
            y = 50
        elif "center" in position and "top" not in position:
            if "bottom" not in position:
                y = (screen.height() - self.height()) // 2
        elif "bottom" in position:
            y = screen.height() - self.height() - 50
        
        if "left" in position:
            x = 50
        elif "center" in position:
            x = (screen.width() - self.width()) // 2
        elif "right" in position:
            x = screen.width() - self.width() - 50
        
        self.move(x, y)
    
    def _load_problem_chars(self) -> None:
        """Load problematic characters from database."""
        stats: Dict[str, Any] = self.database.get_stats(self.user_email)
        self.problem_chars: list = [
            row[0] for row in stats.get("problem_chars", [])
            if row[1] > row[2] * 0.2
        ]
    
    def _start_new_test(self, force_random: bool = False) -> None:
        """
        Start a new typing test.
        
        Args:
            force_random: Force random test selection
        """
        self.showing_results = False
        self.display_word_start = 0
        
        typing_tests: list = self.config.get("typing_tests", [
            {"name": "Default", "text": ""}
        ])
        
        use_random: bool = self.config.get("use_random", False)
        
        if force_random or use_random:
            import random
            active_test: int = random.randint(0, len(typing_tests) - 1)
        else:
            active_test: int = self.config.get("active_test", 0)
            active_test = min(active_test, len(typing_tests) - 1)
        
        custom_text: str = typing_tests[active_test]["text"]
        self.current_test_name: str = typing_tests[active_test]["name"]
        
        text: str = self.engine.generate_text(
            50, 
            self.problem_chars[:5] if self.problem_chars else None,
            custom_text
        )
        self._update_display()
    
    def _update_display(self) -> None:
        """Update the text display."""
        if self.showing_results:
            return
        
        untyped_color: str = self.config.get("untyped_color", "#808080")
        typed_color: str = self.config.get("typed_color", "#808080")
        error_color: str = self.config.get("error_color", "#FF0000")
        move_per_word: bool = self.config.get("move_per_word", False)
        
        pos: int = self.engine.position
        text: str = self.engine.text
        
        center_chars: int = 30
        visible_start: int = max(0, pos - center_chars)
        visible_end: int = min(len(text), pos + center_chars)
        
        html_parts: list = []
        
        for i in range(visible_start, visible_end):
            if i >= len(text):
                break
                
            char: str = text[i]
            
            if i < pos:
                color: str = error_color if i in self.engine.error_positions else typed_color
                html_parts.append(f'<span style="color: {color}">{char}</span>')
            elif i == pos:
                html_parts.append(
                    f'<span style="color: {untyped_color}; '
                    f'background-color: white; font-weight: bold;">{char}</span>'
                )
            else:
                html_parts.append(f'<span style="color: {untyped_color}">{char}</span>')
        
        html: str = ''.join(html_parts)
        self.ui.label_text.setText(html)
    
    def _show_results(self) -> None:
        """Show test results."""
        self.showing_results = True
        wpm: float = self.engine.calculate_wpm()
        accuracy: float = self.engine.calculate_accuracy()
        duration: float = self.engine.get_duration()
        
        self.database.save_test(
            self.user_email, wpm, accuracy, 
            self.engine.mistakes, duration
        )
        
        results_text: str = (
            f"WPM: {wpm:.1f} | "
            f"Accuracy: {accuracy:.1f}% | "
            f"Time: {duration:.1f}s | "
            f"Press TAB to restart"
        )
        
        self.ui.label_text.setText(
            f'<span style="color: white;">{results_text}</span>'
        )
        
        self.test_completed.emit({
            "wpm": wpm,
            "accuracy": accuracy,
            "duration": duration,
            "mistakes": self.engine.mistakes
        })
    
    def _handle_hotkeys(self, event: QKeyEvent) -> bool:
        """
        Handle global hotkey events.
        
        Args:
            event: Key event
            
        Returns:
            True if hotkey was handled, False otherwise
        """
        from PySide6.QtGui import QKeySequence
        
        key_combo: int = event.key() | int(event.modifiers().value)
        key_seq: str = QKeySequence(key_combo).toString()
        
        hotkey_inc: str = self.config.get("hotkey_increase_opacity", "Ctrl+Up")
        hotkey_dec: str = self.config.get("hotkey_decrease_opacity", "Ctrl+Down")
        
        if key_seq == hotkey_inc:
            self._adjust_opacity(10)
            return True
        elif key_seq == hotkey_dec:
            self._adjust_opacity(-10)
            return True
        
        return False
    
    def _adjust_opacity(self, delta: int) -> None:
        """
        Adjust background opacity.
        
        Args:
            delta: Amount to change opacity (+/-)
        """
        current_opacity: int = self.config.get("bg_opacity", 128)
        new_opacity: int = max(0, min(255, current_opacity + delta))
        self.config.set("bg_opacity", new_opacity)
        self.config.save()
        self.update()
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handle key press events.
        
        Args:
            event: Key event
        """
        if event.key() == Qt.Key_Tab:
            if self.engine.start_time is None:
                self._start_new_test(force_random=True)
            else:
                self._start_new_test()
            return
        
        if self._handle_hotkeys(event):
            return
        
        if self.showing_results:
            return
        
        if event.key() == Qt.Key_Backspace:
            old_pos: int = self.engine.position
            if event.modifiers() & Qt.ControlModifier:
                self.engine.backspace_word()
            else:
                self.engine.backspace()
            
            move_per_word: bool = self.config.get("move_per_word", False)
            if move_per_word and self.engine.position < self.display_word_start:
                word_start: int = self.engine.position
                while word_start > 0 and self.engine.text[word_start - 1] != ' ':
                    word_start -= 1
                self.display_word_start = word_start
            
            self._update_display()
            return
        
        text: str = event.text()
        if len(text) == 1 and text.isprintable():
            is_correct, complete = self.engine.process_char(text)
            
            expected_char: str = self.engine.text[self.engine.position - 1]
            self.database.update_char_stats(
                self.user_email, expected_char, not is_correct
            )
            
            move_per_word: bool = self.config.get("move_per_word", False)
            if move_per_word and expected_char == ' ':
                self.display_word_start = self.engine.position
            
            if complete:
                self._show_results()
            else:
                self._update_display()
    
    def paintEvent(self, event) -> None:
        """
        Paint semi-transparent background.
        
        Args:
            event: Paint event
        """
        painter: QPainter = QPainter(self)
        bg_opacity: int = self.config.get("bg_opacity", 128)
        painter.fillRect(
            self.rect(), 
            QColor(0, 0, 0, bg_opacity)
        )
    
    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press events for dragging.
        
        Args:
            event: Mouse event
        """
        if event.modifiers() & Qt.AltModifier:
            self.dragging = True
            self.drag_start_pos = event.globalPosition().toPoint() - self.pos()
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event) -> None:
        """
        Handle mouse move events for dragging.
        
        Args:
            event: Mouse event
        """
        if self.dragging and event.modifiers() & Qt.AltModifier:
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event) -> None:
        """
        Handle mouse release events for dragging.
        
        Args:
            event: Mouse event
        """
        if self.dragging:
            self.dragging = False
            self.drag_start_pos = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def update_user(self, user_email: Optional[str]) -> None:
        """
        Update current user.
        
        Args:
            user_email: New user email
        """
        self.user_email = user_email
        self._load_problem_chars()
    
    def apply_config(self) -> None:
        """Apply updated configuration."""
        self._apply_config()
        self._update_position()
        self._update_display()
    
    def _update_stats_display(self) -> None:
        """Update the stats header display."""
        if self.showing_results:
            return
        
        if self.engine.start_time is None:
            stats: Dict[str, Any] = self.database.get_stats(self.user_email)
            avg_wpm: float = stats.get("avg_wpm", 0.0)
            avg_accuracy: float = stats.get("avg_accuracy", 0.0)
            stats_text: str = (
                f'Test: {self.current_test_name}  |  '
                f'Avg WPM: {avg_wpm:.1f}  |  '
                f'Avg Accuracy: {avg_accuracy:.1f}%'
            )
        else:
            elapsed: float = self.engine.get_duration()
            if elapsed > 0:
                words: float = self.engine.total_chars / 5.0
                minutes: float = elapsed / 60.0
                current_wpm: float = words / minutes if minutes > 0 else 0.0
            else:
                current_wpm: float = 0.0
            
            current_accuracy: float = self.engine.calculate_accuracy()
            stats_text: str = (
                f'WPM: {current_wpm:.1f}  |  '
                f'Accuracy: {current_accuracy:.1f}%  |  '
                f'Time: {elapsed:.1f}s'
            )
        
        self.ui.label_stats.setText(stats_text)
