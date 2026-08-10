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
from typing import Optional, Dict, Any, List
import os
import time as time_module

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, Signal, QObject, QEvent
from PySide6.QtGui import QFont, QKeyEvent, QPainter, QIcon, QWheelEvent, QKeySequence, QFontMetricsF

from ui.generated.ui_typing_overlay import Ui_TypingOverlay
from project_info import Info
from src.typing_engine import TypingEngine
from src.config import Config
from src.database import Database


WORD_COUNT_OPTIONS: List[int] = [10, 25, 50, 100]
TIME_OPTIONS: List[int] = [15, 30, 60, 120]
QUOTE_OPTIONS: List[str] = ["short", "medium", "long", "extreme"]

MODE_WORDS = "words"
MODE_TIME = "time"
MODE_QUOTES = "quotes"

STATUS_TYPING = "Typing"
STATUS_STOPPED = "Stopped"
STATUS_UNFOCUSED = "Unfocused"
STATUS_UNRESPONSIVE = "Unresponsive"


class ChildEventFilter(QObject):
    """Intercepts mouse/wheel events on child widgets for Alt+drag and wheel forwarding."""

    def __init__(self, overlay: "TypingOverlay") -> None:
        super().__init__(overlay)
        self.overlay = overlay

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        t = event.type()
        if t == QEvent.Type.MouseButtonPress:
            # Mode label clicks: switching/cycling handled in the overlay.
            if obj in (self.overlay.ui.label_wordCount,
                       self.overlay.ui.label_timedTest,
                       self.overlay.ui.label_quoteTest):
                if not (event.modifiers() & Qt.AltModifier):
                    self.overlay._handle_mode_label_click(obj)
                    return True
            # Update badge / version label clicks when an update is available.
            if obj in (self.overlay.ui.label_update, self.overlay.ui.label_version):
                if not (event.modifiers() & Qt.AltModifier):
                    self.overlay._on_update_clicked()
                    return True
            # if event.modifiers() & Qt.AltModifier:
            self.overlay.dragging = True
            self.overlay.drag_start_pos = (
                event.globalPosition().toPoint() - self.overlay.pos()
            )
            return True
        elif t == QEvent.Type.MouseMove:
            if self.overlay.dragging: # if self.overlay.dragging and event.modifiers() & Qt.AltModifier:
                self.overlay.move(
                    event.globalPosition().toPoint() - self.overlay.drag_start_pos
                )
                return True
        elif t == QEvent.Type.MouseButtonRelease:
            if self.overlay.dragging:
                self.overlay.dragging = False
                self.overlay.drag_start_pos = None
                return True
        elif t == QEvent.Type.Wheel:
            self.overlay.wheelEvent(event)
            return True
        return False


class TypingOverlay(QWidget):
    test_completed: Signal = Signal(dict)
    update_requested: Signal = Signal()

    def __init__(
        self,
        config: Config,
        database: Database,
        user_email: Optional[str]
    ) -> None:
        super().__init__()
        self.ui = Ui_TypingOverlay()
        self.ui.setupUi(self)
        self._ensure_widget_wrappers()

        self.config: Config = config
        self.database: Database = database
        self.user_email: Optional[str] = user_email
        self.engine: TypingEngine = TypingEngine()
        self.showing_results: bool = False
        self.display_word_start: int = 0
        self.current_test_name: str = "Default"

        self.dragging: bool = False
        self.drag_start_pos = None
        self.quit_prompt_active: bool = False
        self._pending_update_url: str = ""
        self._pending_update_version: str = ""

        self.active_mode: str = MODE_WORDS
        self.word_count_index: int = 2
        self.time_index: int = 1
        self.quote_index: int = 0
        self.current_quote_author: str = ""

        self.paused: bool = False
        self.paused_elapsed: float = 0.0
        self.last_keypress_time: float = time_module.time()
        self.status_text: str = ""
        self.status_anim_frame: int = 0

        self._child_filter = ChildEventFilter(self)

        self._setup_window()
        self._apply_config()
        self._update_position()
        self._load_problem_chars()
        self._start_new_test()
        self._connect_mode_label_clicks()

        self._original_height: int = self.height()

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self._update_stats_display)
        self.stats_timer.start(100)

        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._check_status)
        self.status_timer.start(500)

        self.theme_banner_timer = QTimer()
        self.theme_banner_timer.setSingleShot(True)
        self.theme_banner_timer.timeout.connect(self._clear_theme_banner)
        self._theme_banner_showing = False

        self._update_keys_label()
        self._update_version_label()
        # Resize height to fit only the currently visible widgets at startup.
        self._resize_to_fit()

    def _ensure_widget_wrappers(self) -> None:
        """Guarantee widget_details/widget_about exist after setupUi.

        The .ui file can be hand-edited to put the details/about layouts into
        the main layout as bare layouts (no QWidget wrapper). A bare layout
        cannot be shown/hidden, so at runtime we reparent each bare layout
        into a fresh QWidget and swap it back into the main layout. This keeps
        the ` and / toggles working regardless of the .ui file's state.
        """
        main_layout = getattr(self.ui, "verticalLayout", None)

        def wrap(name: str, layout_name: str, visible: bool) -> None:
            if getattr(self.ui, name, None) is not None:
                return  # already wrapped
            layout = getattr(self.ui, layout_name, None)
            if layout is None or main_layout is None:
                return  # nothing to wrap (or layout already placed)
            if not main_layout.findChild(type(layout), layout.objectName()):
                return  # layout no longer belongs to the main layout
            widget = QWidget(self)
            widget.setObjectName(name)
            widget.setVisible(visible)
            layout.setParent(widget)
            widget.setLayout(layout)
            # Replace the bare layout with the wrapped widget in the main layout.
            index = main_layout.indexOf(layout)
            if index >= 0:
                main_layout.removeItem(layout)
                main_layout.insertWidget(index, widget)
            setattr(self.ui, name, widget)

        wrap("widget_details", "horizontalBox_details", True)
        wrap("widget_about", "verticalLayout_about", False)

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_window(self) -> None:
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        favicon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "resources", "favicon.png"
        )
        if os.path.exists(favicon_path):
            self.setWindowIcon(QIcon(favicon_path))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._install_child_filter()

    def _install_child_filter(self) -> None:
        for child in self.findChildren(QWidget):
            child.installEventFilter(self._child_filter)

    def _connect_mode_label_clicks(self) -> None:
        # Clicking a label for a mode that is NOT active switches to that mode.
        # Clicking the label of the CURRENTLY active mode cycles its option.
        # Handled via ChildEventFilter so drag support stays intact.
        pass

    def _handle_mode_label_click(self, label) -> None:
        mode = {
            self.ui.label_wordCount: MODE_WORDS,
            self.ui.label_timedTest: MODE_TIME,
            self.ui.label_quoteTest: MODE_QUOTES,
        }.get(label)
        if mode is None:
            return
        if self.active_mode != mode:
            self._set_active_mode(mode)
            if self.engine.start_time is None:
                self._start_new_test()
        else:
            self._cycle_mode_option(mode, 1)

    # ------------------------------------------------------------------
    # About panel (keys + version)
    # ------------------------------------------------------------------

    def _update_keys_label(self) -> None:
        """Fill label_keys with a nicely formatted key-command table."""
        secondary = self.config.get("typed_color", "#8b047e")
        rows = [
            ("Increase Opacity",        "hotkey_increase_opacity",   "Alt+Up",       "Increase background opacity"),
            ("Decrease Opacity",        "hotkey_decrease_opacity",   "Alt+Down",     "Decrease background opacity"),
            ("Toggle Stats Bar",        "hotkey_toggle_stats",       "`",            "Show/hide the stats bar"),
            ("Toggle About Panel",      "hotkey_toggle_about",       "/",            "Show/hide commands & version info"),
            ("Cycle Word Pool Up",           "hotkey_cycle_test_up",      "Ctrl+Up",      "Change which typing word pool is used (up)."),
            ("Cycle Word Pool Down",         "hotkey_cycle_test_down",    "Ctrl+Down",    "Change which typing word pool is used (down)"),
            ("Switch Mode Left",        "hotkey_cycle_mode_left",    "Left",         "Previous mode (Words/Time/Quotes)"),
            ("Switch Mode Right",       "hotkey_cycle_mode_right",   "Right",        "Next mode (Words/Time/Quotes)"),
            ("Cycle Option Up",         "hotkey_cycle_option_up",    "Up",           "Previous option within the mode"),
            ("Cycle Option Down",       "hotkey_cycle_option_down",  "Down",         "Next option within the mode"),
            ("Previous Theme",          "hotkey_cycle_theme_left",   "Alt+Left",     "Apply the previous color theme"),
            ("Next Theme",              "hotkey_cycle_theme_right",  "Alt+Right",    "Apply the next color theme"),
        ]

        def esc(text: str) -> str:
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        header = (
            f'<tr style="color:{secondary};font-weight:bold;">'
            f'<td align="left">Key</td>'
            f'<td align="left">Command Name</td>'
            # f'<td align="left">Command</td>'
            f'<td align="left">What the Command Does</td>'
            f'</tr>'
        )
        body = []
        for name, key, default, desc in rows:
            combo = self.config.get(key, default)
            body.append(
                f'<tr style="color:{secondary};">'
                f'<td align="left" style="padding-right:24px;">{esc(combo)}</td>'
                f'<td align="left" style="padding-right:24px;">{esc(name)}</td>'
                # f'<td align="left" style="padding-right:24px;">{esc(key)}</td>'
                f'<td align="left">{esc(desc)}</td>'
                f'</tr>'
            )
        table = (
            f'<table cellspacing="0" cellpadding="2" style="border-collapse:collapse;">'
            f'{header}{"".join(body)}'
            f'</table>'
        )
        self.ui.label_keys.setText(table)
        self.ui.label_keys.setTextFormat(Qt.RichText)

    def _update_version_label(self) -> None:
        """Fill label_version with version and author info."""
        secondary = self.config.get("typed_color", "#8b047e")
        if self._pending_update_version:
            text = (
                f'<span style="color:{secondary};font-weight:bold;text-decoration:underline;">'
                f'{Info.PROJECT_TITLE} v{Info.VERSION}</span>'
                f' &mdash; {Info.COMPANY}<br>'
                f'<span style="color:{secondary};">Update available: v{self._pending_update_version}'
                f' — click to update</span>'
            )
            self.ui.label_version.setCursor(Qt.PointingHandCursor)
            self.ui.label_version.setToolTip(
                f"Click to install TinyType {self._pending_update_version}"
            )
        else:
            text = (
                f'<span style="color:{secondary};">{Info.PROJECT_TITLE} v{Info.VERSION}</span>'
                f' &mdash; {Info.COMPANY}'
            )
            self.ui.label_version.setCursor(Qt.ArrowCursor)
            self.ui.label_version.setToolTip("")
        self.ui.label_version.setText(text)
        self.ui.label_version.setTextFormat(Qt.RichText)
        # Reset click handler to "no update" state
        self.ui.label_version.mousePressEvent = None

    def _toggle_about(self) -> None:
        if self.engine.start_time is not None or self.showing_results:
            return
        about = self._get_widget("widget_about")
        if about is None:
            return
        about.setVisible(not about.isVisible())
        self._resize_to_fit()

    def _get_widget(self, name: str) -> Optional[QWidget]:
        """Safely resolve a child widget from the generated UI.

        Returns None when the widget is missing from the .ui file, so the
        overlay keeps working even after manual .ui edits.
        """
        return getattr(self.ui, name, None)

    def _resize_to_fit(self) -> None:
        """Resize window height to fit only the currently visible widgets.

        The about panel is much taller than the typing area, so when it is
        visible we let the layout's sizeHint drive the height. When it is
        hidden we shrink back to the compact typing view.
        """
        details = self._get_widget("widget_details")
        about = self._get_widget("widget_about")
        details_visible = details is not None and details.isVisible()
        about_visible = about is not None and about.isVisible()

        if about_visible:
            # Let the layout compute the full height (details + text + about).
            target = self.ui.verticalLayout.sizeHint().height()
        else:
            # Compact view: just the visible details/text rows.
            if details_visible:
                target = self._compact_height()
            else:
                # Both hidden: text-only view.
                target = self.ui.verticalLayout.spacing() + self.ui.label_text.sizeHint().height()
            target = max(40, target)

        self.setFixedHeight(target)
        self._update_display()
        self.update()

    def _compact_height(self) -> int:
        """Height of the window when the about panel is hidden (details visible)."""
        details = self._get_widget("widget_details")
        text_h = self.ui.label_text.sizeHint().height()
        details_h = details.sizeHint().height() if details is not None else 0
        return self.ui.verticalLayout.spacing() + details_h + text_h

    def _apply_config(self) -> None:
        font_family: str = self.config.get("font_family", "Consolas")
        font_size: int = self.config.get("font_size", 10)
        width: int = self.config.get("typing_width", 600)
        height: int = self.config.get("typing_height", 90)
        show_border: bool = self.config.get("show_border", False)
        text_align: str = self.config.get("text_align", "center")
        move_per_word: bool = self.config.get("move_per_word", False)

        self.ui.label_text.setFont(QFont(font_family, font_size))

        border_style = "2px solid white" if show_border else "none"
        self.ui.label_text.setStyleSheet(
            f"padding: 5px; background: transparent; border: {border_style};"
        )
        if move_per_word:
            # Keep the text visually fixed for the current word: no
            # caret-fixing padding, which would scroll the text per char.
            self.ui.label_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        elif text_align == "left":
            self.ui.label_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            self.ui.label_text.setAlignment(Qt.AlignCenter)

        self.setFixedSize(width, height)

    def _update_position(self) -> None:
        """Move the overlay to the saved position, or center it if none saved."""
        screen = QApplication.primaryScreen().geometry()
        w, h = self.width(), self.height()

        saved_x = self.config.get("position_x", None)
        saved_y = self.config.get("position_y", None)

        if saved_x is not None and saved_y is not None:
            # Clamp to the visible screen so the overlay can't be lost
            # off-screen after a resolution change.
            x = max(screen.left(), min(saved_x, screen.right() - w + 1))
            y = max(screen.top(), min(saved_y, screen.bottom() - h + 1))
        else:
            x = (screen.width() - w) // 2
            y = (screen.height() - h) // 2

        self.move(x, y)
        self._update_display()

    def _save_position(self) -> None:
        """Persist the current overlay position to config."""
        pos = self.pos()
        self.config.set("position_x", pos.x())
        self.config.set("position_y", pos.y())
        self.config.save()

    def moveEvent(self, event) -> None:
        """Remember the overlay position whenever it is moved."""
        super().moveEvent(event)
        if getattr(self, "config", None) is not None:
            self._save_position()

    def _load_problem_chars(self) -> None:
        stats: Dict[str, Any] = self.database.get_stats(self.user_email)
        self.problem_chars: list = [
            row[0] for row in stats.get("problem_chars", [])
            if len(row) >= 3 and row[2] > 0 and row[1] / row[2] > 0.2
        ]

    # ------------------------------------------------------------------
    # Mode selector
    # ------------------------------------------------------------------

    def _set_active_mode(self, mode: str) -> None:
        self.active_mode = mode
        self._update_mode_labels()

    def _cycle_active_mode(self, direction: int) -> None:
        modes = [MODE_WORDS, MODE_TIME, MODE_QUOTES]
        idx = modes.index(self.active_mode)
        self.active_mode = modes[(idx + direction) % len(modes)]
        self._update_mode_labels()
        if self.engine.start_time is None:
            self._start_new_test()

    def _cycle_mode_option(self, mode: str, direction: int = 1) -> None:
        self.active_mode = mode
        if mode == MODE_WORDS:
            self.word_count_index = (self.word_count_index + direction) % len(WORD_COUNT_OPTIONS)
        elif mode == MODE_TIME:
            self.time_index = (self.time_index + direction) % len(TIME_OPTIONS)
        elif mode == MODE_QUOTES:
            self.quote_index = (self.quote_index + direction) % len(QUOTE_OPTIONS)
        self._update_mode_labels()
        if self.engine.start_time is None:
            self._start_new_test()

    def _cycle_theme(self, direction: int) -> None:
        """Apply the next/previous saved color theme and show its name briefly."""
        themes: list = self.config.get_themes()
        if not themes:
            return

        current_colors = {
            "primary": self.config.get("untyped_color", "#808080"),
            "secondary": self.config.get("typed_color", "#8b047e"),
            "error": self.config.get("error_color", "#FF0000"),
            "window": self.config.get("window_color", "#000000"),
        }
        # Find the currently applied theme by exact color match (fall back to 0).
        idx = next(
            (i for i, t in enumerate(themes)
             if t.get("primary") == current_colors["primary"]
             and t.get("secondary") == current_colors["secondary"]
             and t.get("error") == current_colors["error"]
             and t.get("window") == current_colors["window"]),
            0,
        )
        idx = (idx + direction) % len(themes)
        theme = themes[idx]

        self.config.set("untyped_color", theme.get("primary", "#808080"))
        self.config.set("typed_color", theme.get("secondary", "#8b047e"))
        self.config.set("error_color", theme.get("error", "#FF0000"))
        self.config.set("window_color", theme.get("window", "#000000"))
        self.config.save()

        # Re-render the update badge with the new theme's secondary color.
        # label_update holds a pixmap, so it cannot be recolored via stylesheet.
        if self.ui.label_update.isVisible():
            self._render_update_icon(theme.get("secondary", "#aaaaaa"))

        # Re-render the keys and version labels so their baked-in secondary
        # color follows the new theme (they are rich-text, not stylesheet-colored).
        if self.ui.label_keys.isVisible():
            self._update_keys_label()
        if self.ui.label_version.isVisible():
            self._update_version_label()

        self._update_display()
        self._update_mode_labels()
        self.update()  # repaint background with new window color

        self._theme_banner_showing = True
        self.ui.label_status.setText(
            f'<span style="color:{theme.get("secondary", "#8b047e")};'
            f'font-size:9px;font-weight:bold;">{theme["name"]}</span>'
        )
        self.theme_banner_timer.start(2000)

    def _clear_theme_banner(self) -> None:
        self._theme_banner_showing = False
        self._set_status("")  # status timer will repopulate if a test is active

    def _update_mode_labels(self) -> None:
        secondary: str = self.config.get("typed_color", "#8b047e")
        dim: str = "#555555"

        wc = WORD_COUNT_OPTIONS[self.word_count_index]
        ti = TIME_OPTIONS[self.time_index]
        qi = QUOTE_OPTIONS[self.quote_index]

        def styled(text: str, active: bool) -> str:
            color = secondary if active else dim
            weight = "bold" if active else "normal"
            return f'<span style="color:{color}; font-weight:{weight};">{text}</span>'

        self.ui.label_wordCount.setText(styled(f"W: {wc}", self.active_mode == MODE_WORDS))
        self.ui.label_timedTest.setText(styled(f"T: {ti}s", self.active_mode == MODE_TIME))
        self.ui.label_quoteTest.setText(styled(f"Q: {qi}", self.active_mode == MODE_QUOTES))

    # ------------------------------------------------------------------
    # Test management
    # ------------------------------------------------------------------

    def _start_new_test(self, force_random: bool = False) -> None:
        self.showing_results = False
        self.display_word_start = 0
        self.paused = False
        self.paused_elapsed = 0.0
        self.last_keypress_time = time_module.time()

        typing_tests: list = self.config.get("typing_tests", [{"name": "Default", "text": ""}])
        use_random: bool = self.config.get("use_random", False)

        if force_random or use_random:
            import random
            active_test = random.randint(0, len(typing_tests) - 1)
        else:
            active_test = self.config.get("active_test", 0)
            active_test = min(active_test, len(typing_tests) - 1)

        custom_text: str = typing_tests[active_test].get("text", "")
        self.current_test_name = typing_tests[active_test]["name"]

        if self.active_mode == MODE_QUOTES:
            self._load_quote()
        else:
            if self.active_mode == MODE_TIME:
                # Generate enough words so even a 300 WPM typist can't finish
                # in the allotted time. 300 WPM = 300 words/min.
                time_limit: int = TIME_OPTIONS[self.time_index]
                word_count = int((time_limit / 60.0) * 300 * 1.5) + 50
            else:
                word_count = WORD_COUNT_OPTIONS[self.word_count_index]

            self.engine.generate_text(
                word_count,
                self.problem_chars[:5] if self.problem_chars else None,
                custom_text
            )
        self._update_display()
        self._update_mode_labels()

    def _quote_length(self, text: str) -> str:
        """Classify a quote by its character count into a length bucket."""
        n = len(text)
        if n < 100:
            return "short"
        if n < 200:
            return "medium"
        if n < 300:
            return "long"
        return "extreme"

    def _load_quote(self) -> None:
        """Pick a random quote matching the selected length and load it."""
        import random
        quotes: list = self.config.get_quotes()
        length: str = QUOTE_OPTIONS[self.quote_index]
        pool = [q for q in quotes if self._quote_length(q.get("text", "")) == length]
        if not pool:
            pool = quotes
        quote = random.choice(pool)
        self.engine.text = quote.get("text", "")
        self.engine.position = 0
        self.engine.mistakes = {}
        self.engine.error_positions = []
        self.engine.start_time = None
        self.engine.end_time = None
        self.engine.total_chars = 0
        self.engine.error_count = 0
        self.current_quote_author = quote.get("author", "")
        self.current_test_name = f"Quote ({length})"

    def _extend_timed_buffer(self) -> None:
        """Append more random words to the engine text so a timed test never ends early."""
        import random
        typing_tests: list = self.config.get("typing_tests", [{"name": "Default", "text": ""}])
        active_test: int = min(self.config.get("active_test", 0), len(typing_tests) - 1)
        custom_text: str = typing_tests[active_test].get("text", "")

        if custom_text and custom_text.strip():
            pool = custom_text.strip().split()
        else:
            pool = self.engine.COMMON_WORDS

        extra_words = random.choices(pool, k=100)
        self.engine.text += " " + " ".join(extra_words)
        self.engine.end_time = None

    def _check_timed_buffer(self) -> None:
        """Extend the buffer when fewer than 10 words remain ahead of the cursor."""
        remaining_text = self.engine.text[self.engine.position:]
        words_remaining = len(remaining_text.split())
        if words_remaining <= 10:
            self._extend_timed_buffer()

    def _cycle_active_test(self, direction: int) -> None:
        typing_tests: list = self.config.get("typing_tests", [{"name": "Default", "text": ""}])
        active_test: int = self.config.get("active_test", 0)
        active_test = (active_test + direction) % len(typing_tests)
        self.config.set("active_test", active_test)
        self.config.save()
        self._start_new_test()

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def _word_start_at(self, char_index: int) -> int:
        """Start index of the word containing the character at char_index."""
        if char_index <= 0:
            return 0
        scan = char_index
        while scan > 0 and self.engine.text[scan - 1] != " ":
            scan -= 1
        return scan

    def _update_display(self) -> None:
        if self.showing_results:
            return

        untyped_color: str = self.config.get("untyped_color", "#808080")
        typed_color: str = self.config.get("typed_color", "#8b047e")
        error_color: str = self.config.get("error_color", "#FF0000")
        text_align: str = self.config.get("text_align", "center")

        pos: int = self.engine.position
        text: str = self.engine.text

        move_per_word: bool = self.config.get("move_per_word", False)
        if move_per_word:
            # Move-per-word: anchor the view on the start of the word being
            # typed so the whole word (and its trailing space) stays in place.
            anchor = max(0, self.display_word_start)
            if anchor > pos:
                anchor = pos  # never anchor ahead of the caret
            lead = 4
            visible_start = max(0, anchor - lead)
            visible_end = min(len(text), anchor + 60)
        elif text_align == "left":
            # Caret stays at a fixed column; the text scrolls as you type.
            caret_col = 5
            visible_start = max(0, pos - caret_col)
            visible_end = min(len(text), pos + 60)
        else:
            center_chars = 30
            visible_start = max(0, pos - center_chars)
            visible_end = min(len(text), pos + center_chars)

        html_parts: list = []
        for i in range(visible_start, visible_end):
            if i >= len(text):
                break
            char = text[i]
            if char == " ":
                dc = "&nbsp;"
            elif char == "<":
                dc = "&lt;"
            elif char == ">":
                dc = "&gt;"
            elif char == "&":
                dc = "&amp;"
            else:
                dc = char

            if i < pos:
                if i in self.engine.error_positions:
                    if char == " ":
                        # A space error is invisible as text, so highlight the
                        # background with the error color instead.
                        html_parts.append(
                            f'<span style="color:{error_color};'
                            f'background-color:{error_color};">{dc}</span>'
                        )
                    else:
                        html_parts.append(f'<span style="color:{error_color}">{dc}</span>')
                else:
                    html_parts.append(f'<span style="color:{typed_color}">{dc}</span>')
            elif i == pos:
                caret_bg = typed_color
                window_color: str = self.config.get("window_color", "#000000")
                html_parts.append(
                    f'<span style="color:{window_color};'
                    f'background-color:{caret_bg};font-weight:bold;">{dc}</span>'
                )
            else:
                html_parts.append(f'<span style="color:{untyped_color}">{dc}</span>')

        if move_per_word:
            # Keep the text visually fixed for the current word: no
            # caret-fixing padding, which would scroll the text per char.
            self.ui.label_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        elif text_align == "left":
            # Left-aligned: keep the caret at a fixed column by padding the
            # window start when the cursor is still near the beginning.
            self.ui.label_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            pad_cols = caret_col - (pos - visible_start)
            if pad_cols > 0:
                html_parts.insert(0, "&nbsp;" * pad_cols)
        elif text_align == "center":
            # Left-align the rendered text and pad it so the caret character
            # lands exactly at the horizontal center of the label.
            self.ui.label_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            before = text[visible_start:pos]
            fm = QFontMetricsF(self.ui.label_text.font())
            width_before = fm.horizontalAdvance(before)
            contents = self.ui.label_text.contentsRect()
            center_x = contents.x() + contents.width() / 2.0
            space_width = fm.horizontalAdvance(" ")
            pad = max(0, int((center_x - width_before) / space_width))
            if pad > 0:
                html_parts.insert(0, "&nbsp;" * pad)

        self.ui.label_text.setText("".join(html_parts))

    def _show_quit_prompt(self) -> None:
        self.quit_prompt_active = True
        untyped_color = self.config.get("untyped_color", "#808080")
        secondary = self.config.get("typed_color", "#8b047e")
        # Always center the quit prompt, regardless of caret alignment mode.
        self.ui.label_text.setAlignment(Qt.AlignCenter)
        self.ui.label_text.setText(
            f'<span style="color:{untyped_color};">Quit TinyType? </span>'
            f'<span style="color:{secondary}; font-weight:bold;">[y]</span>'
            f'<span style="color:{untyped_color};"> yes  </span>'
            f'<span style="color:{secondary}; font-weight:bold;">[n]</span>'
            f'<span style="color:{untyped_color};"> no</span>'
        )

    def _show_results(self) -> None:
        self.showing_results = True
        wpm = self.engine.calculate_wpm()
        accuracy = self.engine.calculate_accuracy()
        duration = self.engine.get_duration()

        self.database.save_test(
            self.user_email, wpm, accuracy,
            self.engine.mistakes, duration
        )

        typed_color = self.config.get("typed_color", "#8b047e")
        self.ui.label_text.setText(
            f'<span style="color:{typed_color};">'
            f"WPM: {wpm:.1f}  |  Accuracy: {accuracy:.1f}%  |  "
            f"Time: {duration:.1f}s  |  Press TAB to restart"
            f"</span>"
        )
        self.test_completed.emit({"wpm": wpm, "accuracy": accuracy,
                                  "duration": duration, "mistakes": self.engine.mistakes})

    # ------------------------------------------------------------------
    # Hotkeys / input
    # ------------------------------------------------------------------

    def _key_matches(self, event: QKeyEvent, config_key: str, default: str) -> bool:
        configured: str = self.config.get(config_key, default)
        key_int = event.key() | int(event.modifiers().value)
        pressed = QKeySequence(key_int).toString()
        return pressed == QKeySequence(configured).toString()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.quit_prompt_active:
            text = event.text().lower()
            if text == "y":
                QApplication.quit()
                return
            elif text == "n" or event.key() == Qt.Key_Escape:
                self.quit_prompt_active = False
                self._update_display()
            return

        if event.key() == Qt.Key_Escape:
            self._show_quit_prompt()
            return

        if event.key() == Qt.Key_Tab:
            self._start_new_test()
            return
        if self._key_matches(event, "hotkey_increase_opacity", "Alt+Up"):
            self._adjust_opacity(10)
            return

        if self._key_matches(event, "hotkey_decrease_opacity", "Alt+Down"):
            self._adjust_opacity(-10)
            return

        # Ctrl+= / Ctrl+- adjust the typing font size (persisted to config)
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Equal or event.key() == Qt.Key_Plus:
                self._adjust_font_size(1)
                return
            if event.key() == Qt.Key_Minus:
                self._adjust_font_size(-1)
                return

        if self._key_matches(event, "hotkey_align_left", "Ctrl+Alt+Left"):
            self._set_caret_alignment("left")
            return

        if self._key_matches(event, "hotkey_align_center", "Ctrl+Alt+Right"):
            self._set_caret_alignment("center")
            return

        if self._key_matches(event, "hotkey_toggle_stats", "`"):
            details = self._get_widget("widget_details")
            if details is not None:
                details.setVisible(not details.isVisible())
                self._resize_to_fit()
            return

        if self._key_matches(event, "hotkey_toggle_about", "/"):
            self._toggle_about()
            return

        if self._key_matches(event, "hotkey_cycle_test_up", "Ctrl+Up"):
            self._cycle_active_test(-1)
            return

        if self._key_matches(event, "hotkey_cycle_test_down", "Ctrl+Down"):
            self._cycle_active_test(1)
            return
        if self._key_matches(event, "hotkey_cycle_mode_left", "Left"):
            if self.engine.start_time is None:
                self._cycle_active_mode(-1)
            return

        if self._key_matches(event, "hotkey_cycle_mode_right", "Right"):
            if self.engine.start_time is None:
                self._cycle_active_mode(1)
            return

        # Alt+Left / Alt+Right cycle color themes
        if event.key() == Qt.Key_Left and event.modifiers() & Qt.AltModifier:
            self._cycle_theme(-1)
            return

        if event.key() == Qt.Key_Right and event.modifiers() & Qt.AltModifier:
            self._cycle_theme(1)
            return

        if self._key_matches(event, "hotkey_cycle_option_up", "Up"):
            if self.engine.start_time is None:
                self._cycle_mode_option(self.active_mode, -1)
            return

        if self._key_matches(event, "hotkey_cycle_option_down", "Down"):
            if self.engine.start_time is None:
                self._cycle_mode_option(self.active_mode, 1)
            return

        if self.showing_results:
            return

        if event.key() == Qt.Key_Backspace:
            if self.paused:
                return
            if event.modifiers() & Qt.ControlModifier:
                self.engine.backspace_word()
            else:
                self.engine.backspace()
            move_per_word: bool = self.config.get("move_per_word", False)
            if move_per_word:
                # Re-anchor to the word containing the caret so the display
                # steps word-by-word when backspacing.
                self.display_word_start = self._word_start_at(self.engine.position - 1)
            self._update_display()
            return

        text = event.text()
        if len(text) == 1 and text.isprintable():
            self.last_keypress_time = time_module.time()
            if self.paused:
                return
            is_correct, complete = self.engine.process_char(text)
            expected = self.engine.text[self.engine.position - 1]
            self.database.update_char_stats(self.user_email, expected, not is_correct)
            move_per_word = self.config.get("move_per_word", False)
            if move_per_word:
                # Anchor on the word being typed. The trailing space belongs
                # to the completed word, so the view only advances when the
                # next word's first character is typed.
                self.display_word_start = self._word_start_at(self.engine.position - 1)
            if complete:
                if self.active_mode == MODE_TIME:
                    self._extend_timed_buffer()
                    self._update_display()
                else:
                    self._show_results()
            else:
                if self.active_mode == MODE_TIME:
                    self._check_timed_buffer()
                self._update_display()

    def _adjust_opacity(self, delta: int) -> None:
        current = self.config.get("bg_opacity", 128)
        new_val = max(0, min(255, current + delta))
        self.config.set("bg_opacity", new_val)
        self.config.save()
        self.update()

    def _adjust_font_size(self, delta: int) -> None:
        """Increase/decrease the typing font size and persist it to config."""
        current = int(self.config.get("font_size", 24))
        new_val = max(5, min(72, current + delta))
        self.config.set("font_size", new_val)
        self.config.save()
        self._apply_config()
        self._resize_to_fit()
        self._set_status(f"Font size: {new_val}")

    def _set_caret_alignment(self, mode: str) -> None:
        """Set caret alignment mode (left/center) and persist it to config."""
        mode = "left" if mode == "left" else "center"
        self.config.set("text_align", mode)
        self.config.save()
        self._apply_config()
        self._update_display()
        self._set_status(f"Caret: {'Left' if mode == 'left' else 'Center'} aligned")

    # ------------------------------------------------------------------
    # Status / pause
    # ------------------------------------------------------------------

    def _check_status(self) -> None:
        # Don't clobber the transient theme-name banner in label_status.
        if self._theme_banner_showing:
            return

        # While a quote test is active, show the quote's author as credit.
        if self.active_mode == MODE_QUOTES and self.current_quote_author:
            self._show_quote_credit()
            return

        # Never started or already showing results — clear only if not in a
        # paused-but-was-running state (so status persists while paused)
        if self.showing_results:
            self._set_status("")
            return
        if self.engine.start_time is None and not self.paused:
            self._set_status("")
            return

        has_focus = self.isActiveWindow()
        elapsed_since_key = time_module.time() - self.last_keypress_time

        if not has_focus:
            new_status = STATUS_UNFOCUSED
        elif elapsed_since_key > 5.0:
            new_status = STATUS_UNRESPONSIVE
        elif self.paused:
            new_status = STATUS_STOPPED
        else:
            new_status = STATUS_TYPING

        should_pause = new_status in (STATUS_UNFOCUSED, STATUS_UNRESPONSIVE)
        if should_pause and not self.paused:
            self.paused = True
            if self.engine.start_time is not None:
                self.paused_elapsed += time_module.time() - self.engine.start_time
                self.engine.start_time = None
        elif not should_pause and self.paused and new_status == STATUS_TYPING:
            self.paused = False
            self.engine.start_time = time_module.time() - self.paused_elapsed

        self._set_status(new_status)

    def _show_quote_credit(self) -> None:
        """Show the current quote's author in the status label."""
        color = self.config.get("typed_color", "#8b047e")
        self.ui.label_status.setText(
            f'<span style="color:{color};font-size:9px;">— {self.current_quote_author}</span>'
        )

    def _set_status(self, status: str) -> None:
        self.status_text = status
        if not status:
            self.ui.label_status.setText("")
            return

        self.status_anim_frame = (self.status_anim_frame + 1) % 4
        dots = "." * self.status_anim_frame
        color_map = {
            STATUS_TYPING: self.config.get("typed_color", "#aaaaaa"),
            STATUS_STOPPED: "#aaaaaa",
            STATUS_UNFOCUSED: "#aaaa44",
            STATUS_UNRESPONSIVE: "#aa4444",
        }
        color = color_map.get(status, "#aaaaaa")
        self.ui.label_status.setText(
            f'<span style="color:{color};font-size:9px;">{status}{dots}</span>'
        )

    # ------------------------------------------------------------------
    # Stats display
    # ------------------------------------------------------------------

    def _update_stats_display(self) -> None:
        if self.showing_results:
            return

        typed_color = self.config.get("typed_color", "#8b047e")

        if self.engine.start_time is None and not self.paused:
            stats = self.database.get_stats(self.user_email)
            avg_wpm = stats.get("avg_wpm", 0.0)
            avg_acc = stats.get("avg_accuracy", 0.0)
            text = (
                f"Test: {self.current_test_name}  |  "
                f"Avg WPM: {avg_wpm:.1f}  |  "
                f"Avg Accuracy: {avg_acc:.1f}%"
            )
        else:
            if self.engine.start_time is not None:
                elapsed = time_module.time() - self.engine.start_time
            else:
                elapsed = self.paused_elapsed

            # Timed test expiry
            if self.active_mode == MODE_TIME and not self.paused:
                time_limit = TIME_OPTIONS[self.time_index]
                if elapsed >= time_limit:
                    self.engine.end_time = self.engine.start_time + time_limit
                    self._show_results()
                    return
                remaining = time_limit - elapsed
                time_display = f"Time: {remaining:.1f}s left"
            else:
                time_display = f"Time: {elapsed:.1f}s"

            if elapsed > 0:
                current_wpm = (self.engine.total_chars / 5.0) / (elapsed / 60.0)
            else:
                current_wpm = 0.0

            text = (
                f"WPM: {current_wpm:.1f}  |  "
                f"Accuracy: {self.engine.calculate_accuracy():.1f}%  |  "
                f"{time_display}"
            )

        self.ui.label_stats.setText(
            f'<span style="color:{typed_color};">{text}</span>'
        )

    # ------------------------------------------------------------------
    # Paint / drag
    # ------------------------------------------------------------------

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        bg_opacity = self.config.get("bg_opacity", 128)
        window_color = self.config.get("window_color", "#000000")
        from PySide6.QtGui import QColor
        base = QColor(window_color)
        base.setAlpha(bg_opacity)
        painter.fillRect(self.rect(), base)

    def mousePressEvent(self, event) -> None:
        if event.modifiers(): # if event.modifiers() & Qt.AltModifier:
            self.dragging = True
            self.drag_start_pos = event.globalPosition().toPoint() - self.pos()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.dragging and event.modifiers(): # if self.dragging and event.modifiers() & Qt.AltModifier:
            self.move(event.globalPosition().toPoint() - self.drag_start_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.dragging:
            self.dragging = False
            self.drag_start_pos = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.engine.start_time is None or self.showing_results:
            delta = event.angleDelta().y()
            direction = -1 if delta > 0 else 1
            self._cycle_mode_option(self.active_mode, direction)
        else:
            super().wheelEvent(event)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def _render_update_icon(self, color: str) -> None:
        """Render the apps-16 Octicon SVG into label_update with the given fill color.

        label_update holds a pixmap, so a stylesheet color cannot recolor it —
        the fill color must be baked into the SVG at render time.
        """
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">'
            f'<path fill="{color}" d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"/>'
            # f'<path fill="{color}" d="M7.25 7.689V2a.75.75 0 0 1 1.5 0v5.689l1.97-1.969a.749.749 0 1 1 1.06 1.06l-3.25 3.25a.749.749 0 0 1-1.06 0L4.22 6.78a.749.749 0 1 1 1.06-1.06l1.97 1.969Z"/>'
            f'</svg>'
        )

#         svg = (f"""< svg
#         xmlns = "http://www.w3.org/2000/svg"
#         viewBox = "0 0 16 16"
#         width = "16"
#         height = "16" >< path
#         fill="{color}"
#         d = "" > < / path > < / svg >
# """)
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtGui import QPixmap, QPainter
        from PySide6.QtCore import QByteArray, Qt
        renderer = QSvgRenderer(QByteArray(svg.encode()))
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.ui.label_update.setPixmap(pixmap)

    def show_update_badge(self, latest_version: str) -> None:
        """Render the apps-16 Octicon SVG into label_update and make it visible."""
        secondary = self.config.get("typed_color", "#8b047e")
        self._render_update_icon(secondary)
        self.ui.label_update.setToolTip(f"TinyType {latest_version} is available — click to update")
        self.ui.label_update.setVisible(True)

        # Make the version label clickable to update too (1.d)
        self._pending_update_version = latest_version
        self._update_version_label()
        # Clicks on label_update / label_version are handled in ChildEventFilter,
        # so the version label must not reset its handler afterwards.
        self._resize_to_fit()


    def set_update_url(self, url: str) -> None:
        self._pending_update_url = url

    def _on_update_clicked(self) -> None:
        if not self._pending_update_url:
            return
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Update Available",
            f"A new version of TinyType is available.\n\nDownload and install now?\n"
            f"The app will restart automatically.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.update_requested.emit()

    def update_user(self, user_email: Optional[str]) -> None:
        self.user_email = user_email
        self._load_problem_chars()

    def apply_config(self) -> None:
        self._apply_config()
        self._update_position()
        self._update_display()
        self._update_mode_labels()
        self._install_child_filter()