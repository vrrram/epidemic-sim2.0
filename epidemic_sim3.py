"""
Epidemic Simulation v3.0 - Legacy Entry Point

This file maintains backward compatibility for existing users.
For new development, use the modular structure:
    python -m epidemic_sim.main

All core components have been modularized:
- epidemic_sim/config/: Parameters and presets
- epidemic_sim/model/: Simulation engine, particles, spatial grid
- epidemic_sim/view/: UI components, canvas, theme, main window
- epidemic_sim/main.py: New entry point

This file now serves as a compatibility shim that imports from the new structure.

Usage:
    python epidemic_sim3.py     # Still works for backward compatibility
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

# Import from modular structure
from epidemic_sim.view.main_window import EpidemicApp
from epidemic_sim.config.parameters import params
from epidemic_sim.config.presets import PRESETS
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.model.particle import Particle
from epidemic_sim.model.spatial_grid import SpatialGrid
from epidemic_sim.view.canvas import SimulationCanvas
from epidemic_sim.view.widgets import CollapsibleBox, PieChartWidget
from epidemic_sim.view.theme import (
    DARK_THEME, LIGHT_THEME, current_theme, get_color,
    update_legacy_colors, NEON_GREEN, BG_BLACK, PANEL_BLACK, BORDER_GREEN
)

# Legacy compatibility: Keep old imports working
# These are no longer defined here but imported from the modular structure
SimParams = type(params)  # For backward compatibility if anyone imports SimParams


# =================== LEGACY ENTRY POINT ===================
# All implementation has been moved to the modular structure.
# This file now only provides the entry point for backward compatibility.

if __name__ == '__main__':
    app = QApplication(sys.argv)

    font = QFont("Courier New", 10)
    app.setFont(font)

    window = EpidemicApp()
    window.show()
    sys.exit(app.exec_())
