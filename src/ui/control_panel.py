"""
Control Panel Widget
====================
User controls for stellar evolution simulation.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QPushButton, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from physics import PHASE_NAMES

class ControlPanel(QWidget):
    """
    Control panel for simulation parameters.
    """
    
    mass_changed = Signal(float)  # Emits new mass in solar masses
    time_changed = Signal(float)  # Emits time fraction (0-1)
    play_pause_toggled = Signal(bool)  # True = playing, False = paused
    reset_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_playing = False
        
        self._setup_ui()
        self._apply_stylesheet()
        
    def _setup_ui(self):
        """Setup UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("CosmicStudio")
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Stellar Evolution Simulator")
        subtitle_font = QFont("Arial", 10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #888888;")
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(20)
        
        # Stellar Parameters Group
        params_group = QGroupBox("Stellar Parameters")
        params_layout = QVBoxLayout()
        
        # Mass control
        mass_layout = QVBoxLayout()
        mass_label = QLabel("Initial Mass")
        mass_layout.addWidget(mass_label)
        
        mass_control_layout = QHBoxLayout()
        
        self.mass_spinbox = QDoubleSpinBox()
        self.mass_spinbox.setRange(0.1, 100.0)
        self.mass_spinbox.setValue(1.0)
        self.mass_spinbox.setSuffix(" M☉")
        self.mass_spinbox.setDecimals(1)
        self.mass_spinbox.setSingleStep(0.1)
        self.mass_spinbox.valueChanged.connect(self._on_mass_spinbox_changed)
        
        mass_control_layout.addWidget(self.mass_spinbox)
        
        # Preset buttons
        preset_layout = QHBoxLayout()
        
        preset_masses = [
            ("0.5 M☉", 0.5),
            ("1.0 M☉", 1.0),
            ("5.0 M☉", 5.0),
            ("20 M☉", 20.0),
        ]
        
        for label, mass in preset_masses:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, m=mass: self._set_preset_mass(m))
            preset_layout.addWidget(btn)
        
        mass_layout.addLayout(mass_control_layout)
        mass_layout.addLayout(preset_layout)
        
        params_layout.addLayout(mass_layout)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Evolution Control Group
        evolution_group = QGroupBox("Evolution Control")
        evolution_layout = QVBoxLayout()
        
        # Time slider
        time_layout = QVBoxLayout()
        time_label = QLabel("Evolutionary Time")
        time_layout.addWidget(time_label)
        
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(0, 1000)
        self.time_slider.setValue(0)
        self.time_slider.valueChanged.connect(self._on_time_slider_changed)
        time_layout.addWidget(self.time_slider)
        
        self.time_display = QLabel("0.000 Gyr")
        self.time_display.setAlignment(Qt.AlignCenter)
        time_layout.addWidget(self.time_display)
        
        evolution_layout.addLayout(time_layout)
        
        # Playback controls
        playback_layout = QHBoxLayout()
        
        self.play_pause_button = QPushButton("▶ Play")
        self.play_pause_button.clicked.connect(self._on_play_pause_clicked)
        playback_layout.addWidget(self.play_pause_button)
        
        self.reset_button = QPushButton("↺ Reset")
        self.reset_button.clicked.connect(self._on_reset_clicked)
        playback_layout.addWidget(self.reset_button)
        
        evolution_layout.addLayout(playback_layout)
        
        evolution_group.setLayout(evolution_layout)
        layout.addWidget(evolution_group)
        
        # Current State Display Group
        state_group = QGroupBox("Current State")
        state_layout = QVBoxLayout()
        
        self.phase_label = QLabel("Phase: Main Sequence")
        self.phase_label.setWordWrap(True)
        state_layout.addWidget(self.phase_label)
        
        self.mass_label = QLabel("Mass: 1.000 M☉")
        state_layout.addWidget(self.mass_label)
        
        self.radius_label = QLabel("Radius: 1.000 R☉")
        state_layout.addWidget(self.radius_label)
        
        self.luminosity_label = QLabel("Luminosity: 1.000 L☉")
        state_layout.addWidget(self.luminosity_label)
        
        self.temperature_label = QLabel("Temperature: 5772 K")
        state_layout.addWidget(self.temperature_label)
        
        self.spectral_label = QLabel("Spectral Class: G")
        state_layout.addWidget(self.spectral_label)
        
        state_group.setLayout(state_layout)
        layout.addWidget(state_group)
        
        # Composition Display
        composition_group = QGroupBox("Composition")
        composition_layout = QVBoxLayout()
        
        self.hydrogen_label = QLabel("Hydrogen (X): 0.7381")
        composition_layout.addWidget(self.hydrogen_label)
        
        self.helium_label = QLabel("Helium (Y): 0.2477")
        composition_layout.addWidget(self.helium_label)
        
        self.metals_label = QLabel("Metals (Z): 0.0142")
        composition_layout.addWidget(self.metals_label)
        
        composition_group.setLayout(composition_layout)
        layout.addWidget(composition_group)
        
        # Spacer
        layout.addStretch()
        
        # Info label
        info_label = QLabel("Tip: Use mouse wheel to zoom H-R diagram")
        info_label.setStyleSheet("color: #666666; font-size: 9pt;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
    def _apply_stylesheet(self):
        """Apply custom stylesheet."""
        style = """
        QGroupBox {
            font-weight: bold;
            border: 2px solid #3d3d3d;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 10px;
            background-color: #2d2d2d;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #3d3d3d;
            border: 1px solid #5d5d5d;
            border-radius: 4px;
            padding: 6px 12px;
            color: #e0e0e0;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4d4d4d;
            border: 1px solid #6d6d6d;
        }
        QPushButton:pressed {
            background-color: #2d2d2d;
        }
        QSlider::groove:horizontal {
            border: 1px solid #3d3d3d;
            height: 8px;
            background: #2d2d2d;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #00d4ff;
            border: 1px solid #00a0cc;
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #00e4ff;
        }
        QDoubleSpinBox {
            background-color: #2d2d2d;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 4px;
            color: #e0e0e0;
        }
        QLabel {
            color: #e0e0e0;
        }
        """
        self.setStyleSheet(style)
        
    def _set_preset_mass(self, mass):
        """Set preset mass value."""
        self.mass_spinbox.setValue(mass)
        
    def _on_mass_spinbox_changed(self, value):
        """Handle mass spinbox change."""
        self.mass_changed.emit(value)
        
    def _on_time_slider_changed(self, value):
        """Handle time slider change."""
        fraction = value / 1000.0
        self.time_changed.emit(fraction)
        
    def _on_play_pause_clicked(self):
        """Handle play/pause button click."""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_pause_button.setText("⏸ Pause")
        else:
            self.play_pause_button.setText("▶ Play")
        
        self.play_pause_toggled.emit(self.is_playing)
        
    def _on_reset_clicked(self):
        """Handle reset button click."""
        self.time_slider.setValue(0)
        self.reset_clicked.emit()
        
    def set_time_fraction(self, fraction):
        """
        Set time slider position.
        
        Parameters:
        -----------
        fraction : float
            Time fraction (0-1)
        """
        value = int(fraction * 1000)
        self.time_slider.blockSignals(True)
        self.time_slider.setValue(value)
        self.time_slider.blockSignals(False)
        
    def update_display(self, model):
        """
        Update display labels with model data.
        
        Parameters:
        -----------
        model : StellarModel
            Current stellar model
        """
        from physics import solar_mass, solar_radius, solar_luminosity
        
        # Update phase
        self.phase_label.setText(f"Phase: {PHASE_NAMES[model.phase]}")
        
        # Update parameters
        self.mass_label.setText(f"Mass: {solar_mass(model.mass):.3f} M☉")
        self.radius_label.setText(f"Radius: {solar_radius(model.radius):.3f} R☉")
        self.luminosity_label.setText(f"Luminosity: {solar_luminosity(model.luminosity):.3f} L☉")
        self.temperature_label.setText(f"Temperature: {model.T_eff:.0f} K")
        self.spectral_label.setText(f"Spectral Class: {model.spectral_class}")
        
        # Update time display
        age_gyr = model.age / (1e9 * 3.15576e7)
        self.time_display.setText(f"{age_gyr:.3f} Gyr")
        
        # Update composition
        self.hydrogen_label.setText(f"Hydrogen (X): {model.X:.4f}")
        self.helium_label.setText(f"Helium (Y): {model.Y:.4f}")
        self.metals_label.setText(f"Metals (Z): {model.Z:.4f}")
