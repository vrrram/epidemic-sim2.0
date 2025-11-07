"""
View package for epidemic simulation

Contains UI components, widgets, and visualization
"""

from epidemic_sim.view.canvas import SimulationCanvas
from epidemic_sim.view.main_window import EpidemicApp
from epidemic_sim.view.theme import DARK_THEME, LIGHT_THEME, get_color, set_theme, current_theme
from epidemic_sim.view.widgets import CollapsibleBox, PieChartWidget

__all__ = [
    'SimulationCanvas', 'EpidemicApp',
    'DARK_THEME', 'LIGHT_THEME', 'get_color', 'set_theme', 'current_theme',
    'CollapsibleBox', 'PieChartWidget'
]
