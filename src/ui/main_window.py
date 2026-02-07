"""
Main Window
===========
Main application window with all UI components.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QStatusBar, QMenuBar, QMenu,
    QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence

from .hr_diagram_widget import HRDiagramWidget
from .star_cross_section_widget import StarCrossSectionWidget
from .control_panel import ControlPanel

from physics import StellarEvolutionTrack

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CosmicStudio - Stellar Evolution Simulator")
        self.setGeometry(100, 100, 1600, 900)
        
        # Current evolution track
        self.current_track = None
        self.current_model_index = 0
        
        # Setup UI
        self._setup_ui()
        self._setup_menubar()
        self._setup_statusbar()
        self._apply_stylesheet()
        
        # Initialize with Sun-like star
        self.load_evolution_track(1.0)
        
    def _setup_ui(self):
        """Setup main UI layout."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Control panel
        self.control_panel = ControlPanel()
        self.control_panel.setMinimumWidth(300)
        self.control_panel.setMaximumWidth(400)
        
        # Right panel: Visualization area
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        
        # Create visualization splitter (top/bottom)
        viz_splitter = QSplitter(Qt.Vertical)
        
        # Top: H-R Diagram
        self.hr_diagram = HRDiagramWidget()
        self.hr_diagram.setMinimumHeight(400)
        
        # Bottom: Star Cross Section
        self.star_view = StarCrossSectionWidget()
        self.star_view.setMinimumHeight(300)
        
        viz_splitter.addWidget(self.hr_diagram)
        viz_splitter.addWidget(self.star_view)
        viz_splitter.setSizes([500, 400])
        
        right_layout.addWidget(viz_splitter)
        
        # Add to main splitter
        splitter.addWidget(self.control_panel)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 1300])
        
        main_layout.addWidget(splitter)
        
        # Connect signals
        self.control_panel.mass_changed.connect(self.on_mass_changed)
        self.control_panel.time_changed.connect(self.on_time_changed)
        self.control_panel.play_pause_toggled.connect(self.on_play_pause)
        self.control_panel.reset_clicked.connect(self.on_reset)
        
    def _setup_menubar(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        export_action = QAction("&Export Track...", self)
        export_action.setShortcut(QKeySequence.Save)
        export_action.triggered.connect(self.export_track)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        reset_zoom_action = QAction("&Reset Zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.hr_diagram.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def _setup_statusbar(self):
        """Setup status bar."""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.status_label = QLabel("Ready")
        self.statusBar.addWidget(self.status_label)
        
    def _apply_stylesheet(self):
        """Apply dark theme stylesheet."""
        style = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        QWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        QMenuBar {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border-bottom: 1px solid #3d3d3d;
        }
        QMenuBar::item:selected {
            background-color: #3d3d3d;
        }
        QMenu {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: 1px solid #3d3d3d;
        }
        QMenu::item:selected {
            background-color: #3d3d3d;
        }
        QStatusBar {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border-top: 1px solid #3d3d3d;
        }
        QSplitter::handle {
            background-color: #3d3d3d;
        }
        """
        self.setStyleSheet(style)
        
    def load_evolution_track(self, mass_solar):
        """
        Load evolution track for given mass.
        
        Parameters:
        -----------
        mass_solar : float
            Stellar mass in solar masses
        """
        self.status_label.setText(f"Calculating evolution for {mass_solar:.1f} M☉...")
        QApplication.processEvents()
        
        # Create new track
        self.current_track = StellarEvolutionTrack(M_initial=mass_solar)
        
        # Calculate evolution
        self.current_track.calculate_main_sequence_evolution(n_steps=100)
        self.current_track.calculate_post_main_sequence(n_steps=100)
        
        # Update displays
        self.hr_diagram.set_evolution_track(self.current_track)
        
        # Reset to start
        self.current_model_index = 0
        self.update_current_model()
        
        self.status_label.setText(f"Evolution calculated: {len(self.current_track.models)} models")
        
    def update_current_model(self):
        """Update display with current model."""
        if self.current_track is None or len(self.current_track.models) == 0:
            return
        
        # Get current model
        model = self.current_track.models[self.current_model_index]
        
        # Update HR diagram cursor
        self.hr_diagram.set_current_point(self.current_model_index)
        
        # Update star view
        self.star_view.set_model(model)
        
        # Update control panel display
        self.control_panel.update_display(model)
        
    def on_mass_changed(self, mass_solar):
        """Handle mass change."""
        self.load_evolution_track(mass_solar)
        
    def on_time_changed(self, time_fraction):
        """Handle time slider change."""
        if self.current_track is None:
            return
        
        # Convert fraction to model index
        n_models = len(self.current_track.models)
        self.current_model_index = int(time_fraction * (n_models - 1))
        self.update_current_model()
        
    def on_play_pause(self, is_playing):
        """Handle play/pause toggle."""
        if is_playing:
            # Start animation
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self.advance_time)
            self.animation_timer.start(50)  # 20 FPS
        else:
            # Stop animation
            if hasattr(self, 'animation_timer'):
                self.animation_timer.stop()
                
    def advance_time(self):
        """Advance time by one step."""
        if self.current_track is None:
            return
        
        # Advance index
        self.current_model_index += 1
        
        # Wrap around at end
        if self.current_model_index >= len(self.current_track.models):
            self.current_model_index = 0
        
        # Update display
        self.update_current_model()
        
        # Update control panel time slider
        time_fraction = self.current_model_index / (len(self.current_track.models) - 1)
        self.control_panel.set_time_fraction(time_fraction)
        
    def on_reset(self):
        """Reset to beginning."""
        self.current_model_index = 0
        self.update_current_model()
        self.control_panel.set_time_fraction(0.0)
        
    def export_track(self):
        """Export current evolution track to JSON."""
        if self.current_track is None:
            QMessageBox.warning(self, "No Track", "No evolution track to export.")
            return
        
        from PySide6.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Evolution Track",
            f"evolution_{self.current_track.M_initial_solar:.1f}Msun.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            self.current_track.save_to_json(filename)
            self.status_label.setText(f"Exported to {filename}")
            
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About CosmicStudio",
            "<h3>CosmicStudio v1.0.0</h3>"
            "<p>Stellar Evolution Simulator</p>"
            "<p>Interactive visualization of stellar life cycles using "
            "stellar structure physics and evolution models.</p>"
            "<p><b>Author:</b> Bayram</p>"
            "<p><b>License:</b> MIT</p>"
        )
