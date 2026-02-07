"""
CosmicStudio - Stellar Evolution Simulator
===========================================
Interactive stellar evolution visualization tool.

Author: Bayram
Version: 1.0.0
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow

def main():
    """Main application entry point."""
    
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("CosmicStudio")
    app.setOrganizationName("Bayram")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
