import sys
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from PyQt5.QtGui import QKeySequence, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QDialog,
                             QHBoxLayout, QPushButton, QComboBox, QSpinBox, QSlider,
                             QDialogButtonBox, QFormLayout, QFontDialog, QColorDialog, QShortcut,
                             QCheckBox, QGraphicsDropShadowEffect)

class SettingsDialog(QDialog):
    def __init__(self, preferences, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Overlay Settings")
        # Use the parent's preferences directly (live preview)
        self.preferences = preferences

        # Create a form layout for settings.
        form = QFormLayout(self)

        # --- Text Color ---
        self.text_color_label = QLabel()
        self.text_color_label.setAutoFillBackground(True)
        self.updateColorLabel(self.text_color_label, self.preferences['text_color'])
        self.text_color_button = QPushButton("Choose...")
        self.text_color_button.clicked.connect(self.chooseTextColor)
        hbox_text = QHBoxLayout()
        hbox_text.addWidget(self.text_color_label)
        hbox_text.addWidget(self.text_color_button)
        form.addRow("Text Color:", hbox_text)

        # --- Font ---
        self.font_label = QLabel(self.preferences['font'].toString())
        self.font_button = QPushButton("Choose Font...")
        self.font_button.clicked.connect(self.chooseFont)
        hbox_font = QHBoxLayout()
        hbox_font.addWidget(self.font_label)
        hbox_font.addWidget(self.font_button)
        form.addRow("Font:", hbox_font)

        # --- Background Color (Plain) ---
        self.bg_color_label = QLabel()
        self.bg_color_label.setAutoFillBackground(True)
        self.updateColorLabel(self.bg_color_label, self.preferences['bg_color'])
        self.bg_color_button = QPushButton("Choose...")
        self.bg_color_button.clicked.connect(self.chooseBgColor)
        hbox_bg = QHBoxLayout()
        hbox_bg.addWidget(self.bg_color_label)
        hbox_bg.addWidget(self.bg_color_button)
        form.addRow("Background Color:", hbox_bg)

        # --- Border Color ---
        self.border_color_label = QLabel()
        self.border_color_label.setAutoFillBackground(True)
        self.updateColorLabel(self.border_color_label, self.preferences['border_color'])
        self.border_color_button = QPushButton("Choose...")
        self.border_color_button.clicked.connect(self.chooseBorderColor)
        hbox_border = QHBoxLayout()
        hbox_border.addWidget(self.border_color_label)
        hbox_border.addWidget(self.border_color_button)
        form.addRow("Border Color:", hbox_border)

        # --- Border Style ---
        self.border_style_combo = QComboBox()
        self.border_style_combo.addItems(["solid", "dashed"])
        self.border_style_combo.setCurrentText(self.preferences['border_style'])
        self.border_style_combo.currentIndexChanged.connect(self.applyPreview)
        form.addRow("Border Style:", self.border_style_combo)

        # --- Border Width ---
        self.border_width_spin = QSpinBox()
        self.border_width_spin.setRange(0, 10)
        self.border_width_spin.setValue(self.preferences['border_width'])
        self.border_width_spin.valueChanged.connect(self.applyPreview)
        form.addRow("Border Width:", self.border_width_spin)

        # --- Padding ---
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(0, 20)
        self.padding_spin.setValue(self.preferences['padding'])
        self.padding_spin.valueChanged.connect(self.applyPreview)
        form.addRow("Padding:", self.padding_spin)

        # --- Window Opacity ---
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(self.preferences['window_opacity'] * 100))
        self.opacity_slider.valueChanged.connect(self.applyPreview)
        form.addRow("Window Opacity:", self.opacity_slider)

        # --- Use Gradient Background ---
        self.gradient_checkbox = QCheckBox()
        self.gradient_checkbox.setChecked(self.preferences.get('use_gradient', False))
        self.gradient_checkbox.toggled.connect(self.applyPreview)
        form.addRow("Use Gradient Background:", self.gradient_checkbox)

        # --- Gradient Start Color ---
        self.gradient_start_label = QLabel()
        self.gradient_start_label.setAutoFillBackground(True)
        self.updateColorLabel(self.gradient_start_label, self.preferences.get('gradient_start_color', QColor('blue')))
        self.gradient_start_button = QPushButton("Choose...")
        self.gradient_start_button.clicked.connect(self.chooseGradientStartColor)
        hbox_grad_start = QHBoxLayout()
        hbox_grad_start.addWidget(self.gradient_start_label)
        hbox_grad_start.addWidget(self.gradient_start_button)
        form.addRow("Gradient Start Color:", hbox_grad_start)

        # --- Gradient End Color ---
        self.gradient_end_label = QLabel()
        self.gradient_end_label.setAutoFillBackground(True)
        self.updateColorLabel(self.gradient_end_label, self.preferences.get('gradient_end_color', QColor('purple')))
        self.gradient_end_button = QPushButton("Choose...")
        self.gradient_end_button.clicked.connect(self.chooseGradientEndColor)
        hbox_grad_end = QHBoxLayout()
        hbox_grad_end.addWidget(self.gradient_end_label)
        hbox_grad_end.addWidget(self.gradient_end_button)
        form.addRow("Gradient End Color:", hbox_grad_end)

        # --- Enable Shadow ---
        self.shadow_checkbox = QCheckBox()
        self.shadow_checkbox.setChecked(self.preferences.get('shadow_enabled', False))
        self.shadow_checkbox.toggled.connect(self.applyPreview)
        form.addRow("Enable Shadow:", self.shadow_checkbox)

        # --- Shadow Color ---
        self.shadow_color_label = QLabel()
        self.shadow_color_label.setAutoFillBackground(True)
        self.updateColorLabel(self.shadow_color_label, self.preferences.get('shadow_color', QColor('black')))
        self.shadow_color_button = QPushButton("Choose...")
        self.shadow_color_button.clicked.connect(self.chooseShadowColor)
        hbox_shadow = QHBoxLayout()
        hbox_shadow.addWidget(self.shadow_color_label)
        hbox_shadow.addWidget(self.shadow_color_button)
        form.addRow("Shadow Color:", hbox_shadow)

        # --- Shadow Blur Radius ---
        self.shadow_blur_spin = QSpinBox()
        self.shadow_blur_spin.setRange(0, 50)
        self.shadow_blur_spin.setValue(self.preferences.get('shadow_blur_radius', 10))
        self.shadow_blur_spin.valueChanged.connect(self.applyPreview)
        form.addRow("Shadow Blur Radius:", self.shadow_blur_spin)

        # --- Shadow Offset X ---
        self.shadow_offset_x_spin = QSpinBox()
        self.shadow_offset_x_spin.setRange(-50, 50)
        self.shadow_offset_x_spin.setValue(self.preferences.get('shadow_offset_x', 3))
        self.shadow_offset_x_spin.valueChanged.connect(self.applyPreview)
        form.addRow("Shadow Offset X:", self.shadow_offset_x_spin)

        # --- Shadow Offset Y ---
        self.shadow_offset_y_spin = QSpinBox()
        self.shadow_offset_y_spin.setRange(-50, 50)
        self.shadow_offset_y_spin.setValue(self.preferences.get('shadow_offset_y', 3))
        self.shadow_offset_y_spin.valueChanged.connect(self.applyPreview)
        form.addRow("Shadow Offset Y:", self.shadow_offset_y_spin)

        # --- Fully Transparent Mode ---
        self.transparent_checkbox = QCheckBox()
        self.transparent_checkbox.setChecked(self.preferences.get('fully_transparent_mode', False))
        self.transparent_checkbox.toggled.connect(self.applyPreview)
        form.addRow("Fully Transparent Mode:", self.transparent_checkbox)

        # --- Dialog Buttons ---
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        form.addRow(self.buttonBox)

    def updateColorLabel(self, label, color):
        """Update a label to show the given QColor."""
        palette = label.palette()
        palette.setColor(label.backgroundRole(), color)
        label.setPalette(palette)
        label.setText(color.name())

    def chooseTextColor(self):
        color = QColorDialog.getColor(self.preferences['text_color'], self, "Select Text Color")
        if color.isValid():
            self.preferences['text_color'] = color
            self.updateColorLabel(self.text_color_label, color)
            self.applyPreview()

    def chooseBgColor(self):
        color = QColorDialog.getColor(self.preferences['bg_color'], self, "Select Background Color")
        if color.isValid():
            self.preferences['bg_color'] = color
            self.updateColorLabel(self.bg_color_label, color)
            self.applyPreview()

    def chooseBorderColor(self):
        color = QColorDialog.getColor(self.preferences['border_color'], self, "Select Border Color")
        if color.isValid():
            self.preferences['border_color'] = color
            self.updateColorLabel(self.border_color_label, color)
            self.applyPreview()

    def chooseFont(self):
        font, ok = QFontDialog.getFont(self.preferences['font'], self, "Select Font")
        if ok:
            self.preferences['font'] = font
            self.font_label.setText(font.toString())
            self.applyPreview()

    def chooseGradientStartColor(self):
        color = QColorDialog.getColor(self.preferences.get('gradient_start_color', QColor('blue')), self, "Select Gradient Start Color")
        if color.isValid():
            self.preferences['gradient_start_color'] = color
            self.updateColorLabel(self.gradient_start_label, color)
            self.applyPreview()

    def chooseGradientEndColor(self):
        color = QColorDialog.getColor(self.preferences.get('gradient_end_color', QColor('purple')), self, "Select Gradient End Color")
        if color.isValid():
            self.preferences['gradient_end_color'] = color
            self.updateColorLabel(self.gradient_end_label, color)
            self.applyPreview()

    def chooseShadowColor(self):
        color = QColorDialog.getColor(self.preferences.get('shadow_color', QColor('black')), self, "Select Shadow Color")
        if color.isValid():
            self.preferences['shadow_color'] = color
            self.updateColorLabel(self.shadow_color_label, color)
            self.applyPreview()

    def applyPreview(self):
        """Update preferences from widgets and apply preview to the overlay."""
        self.preferences['border_style'] = self.border_style_combo.currentText()
        self.preferences['border_width'] = self.border_width_spin.value()
        self.preferences['padding'] = self.padding_spin.value()
        self.preferences['window_opacity'] = self.opacity_slider.value() / 100.0

        # Gradient settings.
        self.preferences['use_gradient'] = self.gradient_checkbox.isChecked()

        # Shadow settings.
        self.preferences['shadow_enabled'] = self.shadow_checkbox.isChecked()
        self.preferences['shadow_blur_radius'] = self.shadow_blur_spin.value()
        self.preferences['shadow_offset_x'] = self.shadow_offset_x_spin.value()
        self.preferences['shadow_offset_y'] = self.shadow_offset_y_spin.value()

        # Fully transparent mode.
        self.preferences['fully_transparent_mode'] = self.transparent_checkbox.isChecked()

        if self.parent() is not None:
            self.parent().updateStyle()

    def getPreferences(self):
        """Return the updated preferences."""
        return self.preferences

class FPSOverlay(QWidget):
    def __init__(self):
        super().__init__()
        # Flag to track whether the user has manually moved/resized the widget
        self.manualResize = False  
        self.initUI()

        # FPS counting variables.
        self.frameCount = 0
        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFPS)
        self.timer.start(16)  # Approximately 60 updates per second

        # Edit Mode is off by default.
        self.editMode = False
        # Variables for dragging/resizing.
        self._drag_active = False
        self._resize_active = False
        self._drag_offset = None
        self._resize_origin = None
        self._original_rect = None

        # Default preferences with additional visual options.
        self.preferences = {
            'text_color': QColor('white'),
            'font': QFont('Sans Serif', 16),
            'bg_color': QColor(0, 0, 0, 150),
            'border_color': QColor('red'),
            'border_width': 2,
            'border_style': 'solid',  # or 'dashed'
            'padding': 5,
            'window_opacity': 1.0,
            'use_gradient': False,
            'gradient_start_color': QColor('blue'),
            'gradient_end_color': QColor('purple'),
            'shadow_enabled': False,
            'shadow_color': QColor('black'),
            'shadow_blur_radius': 10,
            'shadow_offset_x': 3,
            'shadow_offset_y': 3,
            'fully_transparent_mode': False,
        }
        self.updateStyle()

        # Allow the widget to receive key events.
        self.setFocusPolicy(Qt.StrongFocus)

        # Shortcuts:
        # Toggle Edit Mode with Ctrl+E.
        self.editModeShortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.editModeShortcut.activated.connect(self.toggleEditMode)
        # Open Settings dialog with Ctrl+S.
        self.settingsShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.settingsShortcut.activated.connect(self.openSettings)

    def initUI(self):
        # Set up the window: frameless, always-on-top, and transparent.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # By default, the overlay ignores mouse events.
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Set an initial size.
        self.resize(150, 40)

        # Create a layout.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a label to display the FPS value.
        self.label = QLabel("FPS: 0.0", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Position the window in the upper-right corner.
        screen_rect = QApplication.primaryScreen().availableGeometry()
        self.move(screen_rect.right() - self.width(), screen_rect.top())

    def updateStyle(self):
        """Update the overlay’s appearance based on current preferences."""
        text_color = self.preferences['text_color'].name()
        font = self.preferences['font']

        # If fully transparent mode is enabled, remove background, border, and shadow.
        if self.preferences.get('fully_transparent_mode', False):
            style = f"""
                color: {text_color};
                font: {font.pointSize()}pt "{font.family()}";
                background: transparent;
                border: 0px;
                padding: {self.preferences['padding']}px;
            """
            self.label.setStyleSheet(style)
            self.setWindowOpacity(1.0)
            self.label.setGraphicsEffect(None)
        else:
            bg = self.preferences['bg_color']
            bg_rgba = f"rgba({bg.red()}, {bg.green()}, {bg.blue()}, {bg.alpha()})"
            border_color = self.preferences['border_color'].name()

            # Use gradient if enabled.
            if self.preferences.get('use_gradient'):
                grad_start = self.preferences['gradient_start_color'].name()
                grad_end = self.preferences['gradient_end_color'].name()
                background_style = f"background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {grad_start}, stop:1 {grad_end});"
            else:
                background_style = f"background-color: {bg_rgba};"

            style = f"""
                color: {text_color};
                font: {font.pointSize()}pt "{font.family()}";
                {background_style}
                border: {self.preferences['border_width']}px {self.preferences['border_style']} {border_color};
                padding: {self.preferences['padding']}px;
            """
            self.label.setStyleSheet(style)
            self.setWindowOpacity(self.preferences['window_opacity'])

            # Apply drop shadow effect if enabled.
            if self.preferences.get('shadow_enabled'):
                shadow_effect = QGraphicsDropShadowEffect(self)
                shadow_effect.setBlurRadius(self.preferences.get('shadow_blur_radius', 10))
                shadow_effect.setColor(self.preferences.get('shadow_color'))
                shadow_effect.setOffset(self.preferences.get('shadow_offset_x', 3),
                                        self.preferences.get('shadow_offset_y', 3))
                self.label.setGraphicsEffect(shadow_effect)
            else:
                self.label.setGraphicsEffect(None)
        
        # Auto adjust size and reposition only if the widget hasn't been manually moved/resized.
        if not self.editMode and not self.manualResize:
            self.label.adjustSize()
            self.adjustSize()
            # Position in the top-right corner.
            screen_rect = QApplication.primaryScreen().availableGeometry()
            self.move(screen_rect.right() - self.width(), screen_rect.top())

    def updateFPS(self):
        self.frameCount += 1
        elapsed = self.elapsedTimer.elapsed()  # in milliseconds
        if elapsed >= 1000:  # update once per second
            fps = self.frameCount * 1000.0 / elapsed
            self.label.setText(f"FPS: {fps:.1f}")
            self.frameCount = 0
            self.elapsedTimer.restart()

    def toggleEditMode(self):
        """Toggle between non-interactive mode and Edit Mode (for dragging/resizing)."""
        self.editMode = not self.editMode
        if self.editMode:
            # Enable mouse events for moving/resizing.
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            # Change border style to dashed green for visual cue.
            self.preferences['border_style'] = 'dashed'
            self.preferences['border_color'] = QColor('green')
        else:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.preferences['border_style'] = 'solid'
            self.preferences['border_color'] = QColor('red')
        self.updateStyle()

    def openSettings(self):
        """Open the settings dialog to adjust colors, fonts, borders, transparency, gradients, shadows, and fully transparent mode."""
        # Backup current preferences.
        backup = {
            'text_color': QColor(self.preferences['text_color']),
            'font': QFont(self.preferences['font']),
            'bg_color': QColor(self.preferences['bg_color']),
            'border_color': QColor(self.preferences['border_color']),
            'border_width': self.preferences['border_width'],
            'border_style': self.preferences['border_style'],
            'padding': self.preferences['padding'],
            'window_opacity': self.preferences['window_opacity'],
            'use_gradient': self.preferences.get('use_gradient', False),
            'gradient_start_color': QColor(self.preferences.get('gradient_start_color', QColor('blue'))),
            'gradient_end_color': QColor(self.preferences.get('gradient_end_color', QColor('purple'))),
            'shadow_enabled': self.preferences.get('shadow_enabled', False),
            'shadow_color': QColor(self.preferences.get('shadow_color', QColor('black'))),
            'shadow_blur_radius': self.preferences.get('shadow_blur_radius', 10),
            'shadow_offset_x': self.preferences.get('shadow_offset_x', 3),
            'shadow_offset_y': self.preferences.get('shadow_offset_y', 3),
            'fully_transparent_mode': self.preferences.get('fully_transparent_mode', False),
        }
        dlg = SettingsDialog(self.preferences, self)
        if dlg.exec_() != QDialog.Accepted:
            # Revert if canceled.
            self.preferences = backup
            self.updateStyle()

    # --- Mouse event handlers for dragging/resizing in Edit Mode ---
    def mousePressEvent(self, event):
        if not self.editMode:
            return super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            margin = 10  # lower-right corner for resizing
            if (event.pos().x() >= self.width() - margin and
                event.pos().y() >= self.height() - margin):
                self._resize_active = True
                self._resize_origin = event.globalPos()
                self._original_rect = self.geometry()
                self.manualResize = True  # mark as manually moved/resized
            else:
                self._drag_active = True
                self._drag_offset = event.globalPos() - self.frameGeometry().topLeft()
                self.manualResize = True  # mark as manually moved
            event.accept()

    def mouseMoveEvent(self, event):
        if not self.editMode:
            return super().mouseMoveEvent(event)
        if self._drag_active:
            new_pos = event.globalPos() - self._drag_offset
            self.move(new_pos)
            event.accept()
        elif self._resize_active:
            diff = event.globalPos() - self._resize_origin
            new_width = max(50, self._original_rect.width() + diff.x())
            new_height = max(20, self._original_rect.height() + diff.y())
            self.resize(new_width, new_height)
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if not self.editMode:
            return super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            self._resize_active = False
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = FPSOverlay()
    overlay.show()
    sys.exit(app.exec_())
