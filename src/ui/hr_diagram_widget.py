"""
Hertzsprung-Russell Diagram Widget
===================================
Interactive H-R diagram showing stellar evolution tracks.
"""

import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from physics import (
    solar_luminosity, M_SUN, L_SUN, R_SUN,
    main_sequence_luminosity, main_sequence_radius,
    main_sequence_temperature, SPECTRAL_CLASSES
)

class HRDiagramWidget(QWidget):
    """
    H-R Diagram visualization widget.
    Shows log(L) vs log(T_eff) with evolution track.
    """
    
    point_clicked = Signal(int)  # Emits model index when point is clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.evolution_track = None
        self.current_point_index = 0
        
        self._setup_ui()
        self._plot_empty_hr_diagram()
        
    def _setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 8), facecolor='#1e1e1e')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Create axis
        self.ax = self.figure.add_subplot(111)
        
        # Apply dark theme
        self._apply_style()
        
    def _apply_style(self):
        """Apply dark theme to matplotlib."""
        plt.style.use('dark_background')
        
        self.figure.patch.set_facecolor('#1e1e1e')
        self.ax.set_facecolor('#252525')
        
        # Grid
        self.ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        
    def _plot_empty_hr_diagram(self):
        """Plot empty H-R diagram with reference lines."""
        self.ax.clear()
        
        # Plot main sequence reference line
        masses = np.logspace(-1, 2, 50)  # 0.1 to 100 solar masses
        log_T_ms = []
        log_L_ms = []
        
        for M in masses:
            M_kg = M * M_SUN
            L = main_sequence_luminosity(M_kg)
            R = main_sequence_radius(M_kg)
            T_eff = main_sequence_temperature(L, R)
            
            log_T_ms.append(np.log10(T_eff))
            log_L_ms.append(np.log10(solar_luminosity(L)))
        
        # Plot main sequence
        self.ax.plot(log_T_ms, log_L_ms, '--', 
                    color='#606060', linewidth=2, 
                    label='Main Sequence', alpha=0.5, zorder=1)
        
        # Add spectral class regions
        self._add_spectral_regions()
        
        # Add constant radius lines
        self._add_radius_lines()
        
        # Labels and formatting
        self.ax.set_xlabel('log₁₀(T_eff) [K]', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('log₁₀(L / L☉)', fontsize=12, fontweight='bold')
        self.ax.set_title('Hertzsprung-Russell Diagram', fontsize=14, fontweight='bold', pad=20)
        
        # Invert x-axis (hot stars on left)
        self.ax.invert_xaxis()
        
        # Set reasonable limits
        self.ax.set_xlim(4.8, 3.5)  # ~60,000 K to ~3,000 K
        self.ax.set_ylim(-4, 6)     # 10^-4 to 10^6 L_sun
        
        # Legend
        self.ax.legend(loc='lower left', fontsize=10, framealpha=0.8)
        
        self.canvas.draw()
        
    def _add_spectral_regions(self):
        """Add colored regions for spectral classes."""
        # Get y-axis limits for vertical spans
        y_min, y_max = self.ax.get_ylim()
        
        for spec_class, data in SPECTRAL_CLASSES.items():
            T_min, T_max = data['T_range']
            color = data['color']
            
            log_T_min = np.log10(T_min)
            log_T_max = np.log10(T_max)
            
            # Add vertical span (inverted x-axis, so swap min/max)
            self.ax.axvspan(log_T_max, log_T_min, 
                          alpha=0.05, color=color, zorder=0)
            
            # Add label at top
            log_T_mid = (log_T_min + log_T_max) / 2
            self.ax.text(log_T_mid, 5.5, spec_class, 
                        ha='center', va='center',
                        fontsize=11, fontweight='bold',
                        color=color, alpha=0.6)
    
    def _add_radius_lines(self):
        """Add constant radius lines."""
        # Radius lines: L = 4πR²σT⁴
        # log L = log(4πσ) + 2 log R + 4 log T
        
        radii_solar = [0.01, 0.1, 1.0, 10.0, 100.0]  # Solar radii
        T_range = np.logspace(3.5, 4.8, 100)  # Temperature range
        
        for R_solar in radii_solar:
            R = R_solar * R_SUN
            
            # Calculate luminosity for each temperature
            log_L = []
            log_T = []
            
            for T in T_range:
                from physics import SIGMA_SB
                L = 4 * np.pi * R**2 * SIGMA_SB * T**4
                
                log_L.append(np.log10(solar_luminosity(L)))
                log_T.append(np.log10(T))
            
            # Plot radius line
            self.ax.plot(log_T, log_L, ':', 
                        color='#808080', linewidth=1, 
                        alpha=0.3, zorder=0)
            
            # Add label
            if len(log_T) > 50:
                idx = 50
                self.ax.text(log_T[idx], log_L[idx], 
                           f'{R_solar:g}R☉',
                           fontsize=8, alpha=0.4,
                           rotation=-45)
    
    def set_evolution_track(self, track):
        """
        Set evolution track to display.
        
        Parameters:
        -----------
        track : StellarEvolutionTrack
            Evolution track to plot
        """
        self.evolution_track = track
        self.current_point_index = 0
        
        self._plot_track()
        
    def _plot_track(self):
        """Plot the evolution track."""
        if self.evolution_track is None:
            return
        
        # Clear and replot base diagram
        self._plot_empty_hr_diagram()
        
        # Get track data
        log_T, log_L = self.evolution_track.get_hr_track()
        
        if len(log_T) == 0:
            return
        
        # Plot evolution track
        self.track_line, = self.ax.plot(log_T, log_L, 
                                        color='#00d4ff', linewidth=3, 
                                        label=f'{self.evolution_track.M_initial_solar:.1f} M☉ Evolution',
                                        zorder=5)
        
        # Plot start point (ZAMS)
        self.ax.scatter(log_T[0], log_L[0], 
                       s=150, c='#00ff00', marker='o',
                       edgecolors='white', linewidths=2,
                       label='ZAMS', zorder=10)
        
        # Plot end point
        self.ax.scatter(log_T[-1], log_L[-1], 
                       s=150, c='#ff0000', marker='s',
                       edgecolors='white', linewidths=2,
                       label='Final', zorder=10)
        
        # Current position marker (will be updated)
        self.current_marker, = self.ax.plot(log_T[0], log_L[0],
                                           marker='*', markersize=20,
                                           color='#ffff00',
                                           markeredgecolor='white',
                                           markeredgewidth=1.5,
                                           linestyle='none',
                                           zorder=15)
        
        # Update legend
        self.ax.legend(loc='lower left', fontsize=10, framealpha=0.8)
        
        self.canvas.draw()
        
    def set_current_point(self, index):
        """
        Update current position marker.
        
        Parameters:
        -----------
        index : int
            Model index in evolution track
        """
        if self.evolution_track is None:
            return
        
        log_T, log_L = self.evolution_track.get_hr_track()
        
        if index >= len(log_T):
            return
        
        self.current_point_index = index
        
        # Update marker position
        if hasattr(self, 'current_marker'):
            self.current_marker.set_data([log_T[index]], [log_L[index]])
            self.canvas.draw()
            
    def reset_zoom(self):
        """Reset zoom to default view."""
        self.ax.set_xlim(4.8, 3.5)
        self.ax.set_ylim(-4, 6)
        self.canvas.draw()
        
    def save_plot(self, filename):
        """Save current plot to file."""
        self.figure.savefig(filename, dpi=300, bbox_inches='tight',
                          facecolor='#1e1e1e', edgecolor='none')
