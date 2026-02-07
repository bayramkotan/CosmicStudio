"""
UI Module
=========
User interface components for CosmicStudio.
"""

from .main_window import MainWindow
from .hr_diagram_widget import HRDiagramWidget
from .star_cross_section_widget import StarCrossSectionWidget
from .control_panel import ControlPanel

__all__ = [
    'MainWindow',
    'HRDiagramWidget',
    'StarCrossSectionWidget',
    'ControlPanel',
]
