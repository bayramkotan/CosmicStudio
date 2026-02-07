"""
Star Cross Section Widget
==========================
Visualizes internal structure of a star.
"""

import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QFont

from physics import solar_radius, solar_luminosity, solar_mass, PHASE_NAMES

class StarCrossSectionWidget(QWidget):
    """
    Widget showing star's internal structure and properties.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.model = None
        self.setMinimumSize(600, 400)
        
        # Colors for different layers
        self.CORE_COLOR = QColor(255, 200, 100)      # Yellow-white
        self.RADIATIVE_COLOR = QColor(255, 150, 50)  # Orange
        self.CONVECTIVE_COLOR = QColor(255, 100, 100) # Red-orange
        self.SURFACE_COLOR = QColor(255, 80, 80)     # Red
        
    def set_model(self, model):
        """
        Set stellar model to display.
        
        Parameters:
        -----------
        model : StellarModel
            Stellar model
        """
        self.model = model
        
        # Update colors based on temperature
        if model:
            from physics import temperature_to_rgb
            r, g, b = temperature_to_rgb(model.T_eff)
            self.SURFACE_COLOR = QColor(r, g, b)
        
        self.update()
        
    def paintEvent(self, event):
        """Paint the star cross section."""
        if self.model is None:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill background
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        # Calculate center and maximum radius for drawing
        center_x = self.width() // 2
        center_y = self.height() // 2
        max_radius = min(self.width(), self.height()) // 2 - 40
        
        center = QPointF(center_x, center_y)
        
        # Draw star layers (from outside to inside for proper z-order)
        self._draw_star_layers(painter, center, max_radius)
        
        # Draw information panel
        self._draw_info_panel(painter)
        
    def _draw_star_layers(self, painter, center, max_radius):
        """Draw concentric layers representing star's structure."""
        
        # Simplified layer structure
        # Core: 0-25% radius
        # Radiative zone: 25-70% radius (for Sun-like stars)
        # Convective zone: 70-100% radius
        
        # These percentages vary with stellar mass and evolution phase
        # For simplicity, we'll use generic values
        
        core_fraction = 0.25
        radiative_fraction = 0.70
        
        # Adjust based on stellar mass (very simplified)
        M_solar = solar_mass(self.model.mass)
        
        if M_solar > 1.5:
            # Massive stars: convective core, radiative envelope
            core_fraction = 0.30
            radiative_fraction = 0.95
        elif M_solar < 0.5:
            # Low mass: fully convective
            core_fraction = 0.0
            radiative_fraction = 0.0
        
        # Adjust for evolution phase
        from physics import EvolutionPhase
        
        if self.model.phase == EvolutionPhase.RED_GIANT:
            # Red giants: small core, large envelope
            core_fraction = 0.05
            radiative_fraction = 0.20
        elif self.model.phase == EvolutionPhase.WHITE_DWARF:
            # White dwarf: degenerate core, thin atmosphere
            core_fraction = 0.95
            radiative_fraction = 1.0
        
        # Draw surface (outermost layer)
        surface_gradient = QRadialGradient(center, max_radius)
        surface_gradient.setColorAt(0.0, self.SURFACE_COLOR.lighter(120))
        surface_gradient.setColorAt(0.7, self.SURFACE_COLOR)
        surface_gradient.setColorAt(1.0, self.SURFACE_COLOR.darker(150))
        
        painter.setBrush(QBrush(surface_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, max_radius, max_radius)
        
        # Draw convective zone (if present)
        if radiative_fraction < 1.0:
            conv_radius = max_radius * radiative_fraction
            conv_gradient = QRadialGradient(center, conv_radius)
            conv_gradient.setColorAt(0.0, self.CONVECTIVE_COLOR.lighter(130))
            conv_gradient.setColorAt(0.8, self.CONVECTIVE_COLOR)
            conv_gradient.setColorAt(1.0, self.CONVECTIVE_COLOR.darker(120))
            
            painter.setBrush(QBrush(conv_gradient))
            painter.drawEllipse(center, conv_radius, conv_radius)
        
        # Draw radiative zone (if present)
        if radiative_fraction > core_fraction:
            rad_radius = max_radius * core_fraction
            rad_gradient = QRadialGradient(center, rad_radius)
            rad_gradient.setColorAt(0.0, self.RADIATIVE_COLOR.lighter(140))
            rad_gradient.setColorAt(0.7, self.RADIATIVE_COLOR)
            rad_gradient.setColorAt(1.0, self.RADIATIVE_COLOR.darker(110))
            
            painter.setBrush(QBrush(rad_gradient))
            painter.drawEllipse(center, rad_radius, rad_radius)
        
        # Draw core
        if core_fraction > 0:
            core_radius = max_radius * core_fraction
            core_gradient = QRadialGradient(center, core_radius)
            core_gradient.setColorAt(0.0, QColor(255, 255, 255))  # White hot
            core_gradient.setColorAt(0.5, self.CORE_COLOR)
            core_gradient.setColorAt(1.0, self.CORE_COLOR.darker(110))
            
            painter.setBrush(QBrush(core_gradient))
            painter.drawEllipse(center, core_radius, core_radius)
        
        # Draw layer labels
        painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
        font = QFont("Arial", 9)
        painter.setFont(font)
        
        if core_fraction > 0:
            # Core label
            painter.drawText(
                int(center.x() - 30),
                int(center.y()),
                "Core"
            )
        
        # Add reference size indicator
        self._draw_size_reference(painter, center, max_radius)
        
    def _draw_size_reference(self, painter, center, max_radius):
        """Draw size comparison reference."""
        # Draw a small Earth or Sun for size comparison
        
        R_solar = solar_radius(self.model.radius)
        
        # Draw scale bar
        scale_y = center.y() + max_radius + 20
        scale_start = center.x() - 50
        scale_end = center.x() + 50
        
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawLine(int(scale_start), int(scale_y), int(scale_end), int(scale_y))
        
        # Scale text
        painter.setPen(QColor(200, 200, 200))
        font = QFont("Arial", 9)
        painter.setFont(font)
        
        scale_text = f"{R_solar:.2f} R☉"
        text_rect = painter.fontMetrics().boundingRect(scale_text)
        painter.drawText(
            int(center.x() - text_rect.width() // 2),
            int(scale_y + 20),
            scale_text
        )
        
    def _draw_info_panel(self, painter):
        """Draw information panel with stellar parameters."""
        # Info panel on the right side
        panel_x = self.width() - 280
        panel_y = 20
        panel_width = 260
        panel_height = self.height() - 40
        
        # Draw semi-transparent background
        painter.setBrush(QBrush(QColor(40, 40, 40, 220)))
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawRoundedRect(panel_x, panel_y, panel_width, panel_height, 8, 8)
        
        # Draw text information
        text_x = panel_x + 15
        text_y = panel_y + 25
        line_height = 25
        
        # Title
        painter.setPen(QColor(255, 255, 255))
        font_title = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font_title)
        painter.drawText(text_x, text_y, "Stellar Parameters")
        
        text_y += line_height + 10
        
        # Parameters
        font_normal = QFont("Arial", 10)
        painter.setFont(font_normal)
        
        params = [
            ("Phase:", PHASE_NAMES[self.model.phase]),
            ("Mass:", f"{solar_mass(self.model.mass):.3f} M☉"),
            ("Radius:", f"{solar_radius(self.model.radius):.3f} R☉"),
            ("Luminosity:", f"{solar_luminosity(self.model.luminosity):.3f} L☉"),
            ("Temperature:", f"{self.model.T_eff:.0f} K"),
            ("Spectral Class:", self.model.spectral_class),
            ("Age:", f"{self.model.age / (1e9 * 3.15576e7):.3f} Gyr"),
        ]
        
        # Composition
        params.extend([
            ("", ""),  # Empty line
            ("Composition:", ""),
            ("  Hydrogen (X):", f"{self.model.X:.4f}"),
            ("  Helium (Y):", f"{self.model.Y:.4f}"),
            ("  Metals (Z):", f"{self.model.Z:.4f}"),
        ])
        
        for label, value in params:
            painter.setPen(QColor(180, 180, 180))
            painter.drawText(text_x, text_y, label)
            
            if value:
                painter.setPen(QColor(255, 255, 255))
                value_x = text_x + 120
                painter.drawText(value_x, text_y, value)
            
            text_y += line_height
        
        # Color indicator
        text_y += 10
        painter.setPen(QColor(180, 180, 180))
        painter.drawText(text_x, text_y, "Star Color:")
        
        # Draw color circle
        color_x = text_x + 120
        color_y = text_y - 12
        painter.setBrush(QBrush(self.SURFACE_COLOR))
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawEllipse(color_x, color_y, 15, 15)
