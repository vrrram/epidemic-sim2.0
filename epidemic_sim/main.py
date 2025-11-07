"""
Epidemic Simulation - Main Entry Point

This is the main entry point for the epidemic simulation application.
Run this file to start the simulation with the modular architecture.

Usage:
    python -m epidemic_sim.main
    or
    python epidemic_sim/main.py
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from epidemic_sim.view.main_window import EpidemicApp


def main():
    """
    Main entry point for the Epidemic Simulation application.

    Sets up the QApplication, applies default font settings, creates the main
    window, and starts the Qt event loop.

    Returns:
        int: Application exit code
    """
    # Create Qt application
    app = QApplication(sys.argv)

    # Set default monospace font (retro terminal aesthetic)
    font = QFont("Courier New", 10)
    font.setStyleHint(QFont.Monospace)
    app.setFont(font)

    # Create and show main window
    window = EpidemicApp()
    window.show()

    # Start event loop and return exit code
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
