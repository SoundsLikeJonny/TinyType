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

from typing import List, Tuple

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QFont
from PySide6.QtWidgets import QSizePolicy, QWidget


class WpmGraphWidget(QWidget):
    """A lightweight, dependency-free line chart that plots WPM over time.

    Draws two overlapping lines: the instantaneous WPM at each sample point
    (primary color) and the running average WPM up to that point (secondary
    color). Drawn with QPainter so no chart library is required. The widget is
    placed in the .ui file so its size/position can be edited in Qt Designer;
    the drawing logic lives here in src.
    """

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._samples: List[Tuple[float, float]] = []
        self._primary: QColor = QColor("#808080")
        self._secondary: QColor = QColor("#8b047e")
        self._text_color: QColor = QColor("#aaaaaa")
        self._grid_color: QColor = QColor("#555555")
        self._window_color: QColor = QColor("#000000")
        self._hover_index: int = -1
        self.setMinimumHeight(60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    def set_data(
        self,
        samples: List[Tuple[float, float]],
        primary: str = "#808080",
        secondary: str = "#8b047e",
        text_color: str = "#aaaaaa",
        window_color: str = "#000000",
    ) -> None:
        """Set the (elapsed_seconds, wpm) samples and line colors, then repaint."""
        self._samples = list(samples)
        self._primary = QColor(primary)
        self._secondary = QColor(secondary)
        self._text_color = QColor(text_color)
        self._window_color = QColor(window_color)
        self.update()

    def set_colors(
        self,
        primary: str,
        secondary: str,
        window_color: str = "#000000",
    ) -> None:
        """Update the line colors without changing the data (theme changes)."""
        self._primary = QColor(primary)
        self._secondary = QColor(secondary)
        self._window_color = QColor(window_color)
        self.update()

    def clear(self) -> None:
        self._samples = []
        self.update()

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(0, 60)

    def _running_average(self) -> List[float]:
        """Cumulative average WPM up to each sample point."""
        avg: List[float] = []
        total = 0.0
        for i, (_, w) in enumerate(self._samples, start=1):
            total += w
            avg.append(total / i)
        return avg

    def _plot_rect(self) -> "QRect":
        from PySide6.QtCore import QRect
        rect = self.rect()
        return rect.adjusted(34, 8, -8, -16)

    def _index_at_x(self, x: float) -> int:
        """Return the index of the sample nearest to the given widget X."""
        if not self._samples:
            return -1
        plot = self._plot_rect()
        if plot.width() <= 0:
            return 0
        times = [s[0] for s in self._samples]
        t_min, t_max = 0.0, times[-1]
        if t_max - t_min < 0.001:
            return 0
        frac = (x - plot.left()) / plot.width()
        t = t_min + frac * (t_max - t_min)
        best = 0
        best_dist = abs(times[0] - t)
        for i, tv in enumerate(times):
            d = abs(tv - t)
            if d < best_dist:
                best_dist = d
                best = i
        return best

    def mouseMoveEvent(self, event) -> None:
        idx = self._index_at_x(event.position().x())
        if idx != self._hover_index:
            self._hover_index = idx
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event) -> None:
        self._hover_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        if rect.width() < 20 or rect.height() < 20:
            return

        margin_left = 34
        margin_right = 8
        margin_top = 8
        margin_bottom = 16
        plot = rect.adjusted(margin_left, margin_top, -margin_right, -margin_bottom)

        if not self._samples:
            painter.setPen(QPen(self._text_color, 1))
            painter.drawText(rect, Qt.AlignCenter, "No WPM data")
            return

        times = [s[0] for s in self._samples]
        wpm = [s[1] for s in self._samples]
        avg = self._running_average()

        # Prepend a synthetic point at 0 seconds holding the first sample's
        # value, so both lines begin at the 0-second mark at their actual
        # starting WPM (a flat lead-in) rather than at 0 WPM. The running
        # average is still computed over the real samples only.
        disp_times = [0.0] + times
        disp_wpm = [wpm[0]] + wpm
        disp_avg = [avg[0]] + avg

        # Show the full test duration: the X axis starts at 0 seconds rather
        # than at the first sample's time.
        t_min, t_max = 0.0, times[-1]
        all_vals = wpm + avg
        w_min, w_max = min(all_vals), max(all_vals)
        if t_max - t_min < 0.001:
            t_max = t_min + 1.0
        if w_max - w_min < 0.001:
            w_max = w_min + 1.0
        w_max = max(w_max, 1.0)

        def to_x(t: float) -> float:
            return plot.left() + (t - t_min) / (t_max - t_min) * plot.width()

        def to_y(w: float) -> float:
            return plot.bottom() - (w - w_min) / (w_max - w_min) * plot.height()

        # Grid + axis labels
        font = QFont(self.font())
        font.setPointSizeF(max(6.0, font.pointSizeF() - 2))
        painter.setFont(font)
        painter.setPen(QPen(self._grid_color, 1, Qt.PenStyle.DotLine))
        for i in range(5):
            frac = i / 4.0
            gy = plot.top() + frac * plot.height()
            painter.drawLine(QPointF(plot.left(), gy), QPointF(plot.right(), gy))
            w_val = w_max - frac * (w_max - w_min)
            painter.setPen(QPen(self._text_color, 1))
            painter.drawText(
                QPointF(plot.left() - 4, gy + 3),
                f"{w_val:.0f}",
            )
            painter.setPen(QPen(self._grid_color, 1, Qt.PenStyle.DotLine))

        # X axis labels (start / end time)
        painter.setPen(QPen(self._text_color, 1))
        painter.drawText(
            QPointF(plot.left(), plot.bottom() + 12),
            f"{t_min:.0f}s",
        )
        painter.drawText(
            QPointF(plot.right() - 20, plot.bottom() + 12),
            f"{t_max:.0f}s",
        )

        # Plot border
        painter.setPen(QPen(self._grid_color, 1))
        painter.drawRect(plot)

        # WPM line + fill (primary color), starting from the origin.
        if len(self._samples) >= 1:
            path = QPainterPath()
            path.moveTo(to_x(disp_times[0]), to_y(disp_wpm[0]))
            for t, w in zip(disp_times[1:], disp_wpm[1:]):
                path.lineTo(to_x(t), to_y(w))

            fill = QPainterPath(path)
            fill.lineTo(to_x(disp_times[-1]), plot.bottom())
            fill.lineTo(to_x(disp_times[0]), plot.bottom())
            fill.closeSubpath()
            fill_color = QColor(self._primary)
            fill_color.setAlpha(50)
            painter.fillPath(fill, fill_color)

            painter.setPen(QPen(self._primary, 2))
            painter.drawPath(path)

        # Running average line (secondary color), starting from the origin.
        if len(self._samples) >= 1:
            avg_path = QPainterPath()
            avg_path.moveTo(to_x(disp_times[0]), to_y(disp_avg[0]))
            for t, a in zip(disp_times[1:], disp_avg[1:]):
                avg_path.lineTo(to_x(t), to_y(a))
            painter.setPen(QPen(self._secondary, 2))
            painter.drawPath(avg_path)

        # Points (primary for WPM, secondary for average)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._primary)
        for t, w in self._samples:
            painter.drawEllipse(QPointF(to_x(t), to_y(w)), 2.0, 2.0)
        painter.setBrush(self._secondary)
        for t, a in zip(times, avg):
            painter.drawEllipse(QPointF(to_x(t), to_y(a)), 2.0, 2.0)

        # Hover indicator: vertical guide + WPM / Average readout at the
        # sample nearest the mouse's X position.
        if self._hover_index >= 0 and self._hover_index < len(self._samples):
            hx = to_x(times[self._hover_index])
            hy = to_y(wpm[self._hover_index])
            ay = to_y(avg[self._hover_index])

            painter.setPen(QPen(self._text_color, 1, Qt.PenStyle.DashLine))
            painter.drawLine(
                QPointF(hx, plot.top()), QPointF(hx, plot.bottom())
            )

            # Highlight the hovered points.
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._primary)
            painter.drawEllipse(QPointF(hx, hy), 3.5, 3.5)
            painter.setBrush(self._secondary)
            painter.drawEllipse(QPointF(hx, ay), 3.5, 3.5)

            # Readout text, drawn inside the plot area so it is never clipped
            # by the widget's top edge. WPM text matches the primary line,
            # Avg text matches the secondary line, and the background uses the
            # theme's window color.
            wpm_label = f"WPM: {wpm[self._hover_index]:.0f}"
            avg_label = f"Avg: {avg[self._hover_index]:.0f}"
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_w = fm.horizontalAdvance(wpm_label) + 8 + fm.horizontalAdvance(avg_label)
            text_h = fm.height()
            box = QRectF(
                plot.left() + 2,
                plot.top() + 2,
                text_w + 12,
                text_h + 4,
            )
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._window_color)
            painter.drawRoundedRect(box, 3, 3)

            text_rect = box.adjusted(4, 2, -4, -2)
            painter.setPen(QPen(self._primary, 1))
            painter.drawText(
                text_rect,
                Qt.AlignLeft | Qt.AlignVCenter,
                wpm_label,
            )
            painter.setPen(QPen(self._secondary, 1))
            painter.drawText(
                text_rect.adjusted(fm.horizontalAdvance(wpm_label) + 8, 0, 0, 0),
                Qt.AlignLeft | Qt.AlignVCenter,
                avg_label,
            )
