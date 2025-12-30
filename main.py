import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

class RingLight(QWidget):
    def __init__(self, thickness=30, color=(255, 255, 255), alpha=230):
        super().__init__()
        self.thickness = thickness
        self._rgb = color
        self._alpha = alpha

        # Window behavior: stay on top, frameless, don't accept focus
        flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        self.setWindowFlags(flags)

        # Transparent background and allow clicks to pass through
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        try:
            # Prefer not to accept focus (PyQt5 may support this)
            self.setWindowFlag(Qt.WindowDoesNotAcceptFocus, True)
        except Exception:
            pass

        self.setFocusPolicy(Qt.NoFocus)

        self.showFullScreen()

    def set_alpha(self, a: int):
        self._alpha = max(0, min(255, int(a)))
        self.update()

    def set_rgb(self, rgb_tuple):
        self._rgb = tuple(max(0, min(255, int(x))) for x in rgb_tuple)
        self.update()

    def set_thickness(self, t: int):
        self.thickness = max(1, int(t))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        t = self.thickness

        r, g, b = self._rgb
        color = QColor(r, g, b, self._alpha)

        # Top
        painter.fillRect(0, 0, w, t, color)
        # Bottom
        painter.fillRect(0, h - t, w, t, color)
        # Left
        painter.fillRect(0, t, t, h - 2*t, color)
        # Right
        painter.fillRect(w - t, t, t, h - 2*t, color)


class ControlPanel(QWidget):
    """Small floating control panel to change brightness and light type."""

    PRESETS = [
        (255, 255, 255),  # Cool / White
        (255, 244, 229),  # Natural
        (255, 214, 170),  # Warm
        (240, 240, 235),  # Soft white
    ]

    BRIGHTNESS_STEPS = [64, 128, 192, 230, 255]

    def __init__(self, ring: RingLight):
        super().__init__()
        self.ring = ring
        self.preset_idx = 0
        self.brightness_idx = len(self.BRIGHTNESS_STEPS) - 1

        # Frameless floating panel with no title text
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        # Create exactly three sliders stacked vertically (no titles/labels)
        self.sld_brightness = QSlider(Qt.Horizontal)
        self.sld_brightness.setRange(0, 255)
        self.sld_brightness.setValue(self.ring._alpha)
        self.sld_brightness.setSingleStep(1)

        self.sld_thickness = QSlider(Qt.Horizontal)
        self.sld_thickness.setRange(30, 140)
        self.sld_thickness.setValue(self.ring.thickness)
        self.sld_thickness.setSingleStep(1)

        self.sld_type = QSlider(Qt.Horizontal)
        self.sld_type.setRange(0, len(self.PRESETS) - 1)
        self.sld_type.setValue(self.preset_idx)
        self.sld_type.setSingleStep(1)
        self.sld_type.setPageStep(1)

        # Vertical stacking
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addWidget(self.sld_brightness)
        layout.addWidget(self.sld_thickness)
        layout.addWidget(self.sld_type)
        self.setLayout(layout)

        # Compact fixed size
        self.setFixedSize(300, 140)

        # Connections
        self.sld_brightness.valueChanged.connect(self.on_brightness_changed)
        self.sld_thickness.valueChanged.connect(self.on_thickness_changed)
        self.sld_type.valueChanged.connect(self.on_type_changed)

        # initialize
        self.update_controls()

    def on_thickness_changed(self, value: int):
        self.ring.set_thickness(value)

    def on_brightness_changed(self, value: int):
        self.ring.set_alpha(value)

    def on_type_changed(self, value: int):
        idx = int(value)
        self.preset_idx = idx % len(self.PRESETS)
        self.ring.set_rgb(self.PRESETS[self.preset_idx])

    def cycle_brightness(self):
        self.brightness_idx = (self.brightness_idx + 1) % len(self.BRIGHTNESS_STEPS)
        alpha = self.BRIGHTNESS_STEPS[self.brightness_idx]
        self.ring.set_alpha(alpha)
        self.update_controls()

    def cycle_type(self):
        self.preset_idx = (self.preset_idx + 1) % len(self.PRESETS)
        rgb = self.PRESETS[self.preset_idx]
        self.ring.set_rgb(rgb)
        self.update_controls()

    def update_controls(self):
        # Sync sliders with current ring state
        try:
            self.sld_brightness.blockSignals(True)
            self.sld_thickness.blockSignals(True)
            self.sld_type.blockSignals(True)
            self.sld_brightness.setValue(self.ring._alpha)
            self.sld_thickness.setValue(self.ring.thickness)
            self.sld_type.setValue(self.preset_idx)
        finally:
            self.sld_brightness.blockSignals(False)
            self.sld_thickness.blockSignals(False)
            self.sld_type.blockSignals(False)

    def move_to_bottom_center(self):
        screen = QApplication.primaryScreen()
        if not screen:
            return
        geo = screen.availableGeometry()
        sw = geo.width()
        sh = geo.height()
        w = self.width()
        h = self.height()
        x = (sw - w) // 2
        y = sh - h - 40
        self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ring = RingLight()
    control = ControlPanel(ring)
    control.show()
    # Position the control at the bottom center
    control.move_to_bottom_center()

    sys.exit(app.exec_())
