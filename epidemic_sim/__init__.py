"""
Epidemic Simulation 3.0 - Modular Architecture

A PyQt5-based particle epidemic simulation implementing a SEIRD model
(Susceptible, Exposed, Infected, Removed, Dead) with spatial dynamics,
quarantine mechanics, and real-time visualization.

This simulation was developed as a 3rd-year apprenticeship project
(Fachinformatiker Anwendungsentwicklung) following IHK standards.

## Module Structure

- config/: Configuration and parameters
- model/: Simulation logic (Particle, Simulation, SpatialGrid)
- view/: User interface (MainWindow, Canvas, Widgets, Theme)
- utils/: Helper functions and utilities

## Usage

Run the simulation:
    python -m epidemic_sim.main

Or use the legacy entry point:
    python epidemic_sim3.py
"""

__version__ = "3.0.0"
__author__ = "IHK Vocational Project"

# Make key classes easily importable
from epidemic_sim.config.parameters import SimParams, params
from epidemic_sim.config.presets import PRESETS
from epidemic_sim.model.particle import Particle
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.model.spatial_grid import SpatialGrid
from epidemic_sim.view.theme import DARK_THEME, LIGHT_THEME, get_color, set_theme

__all__ = [
    'SimParams', 'params', 'PRESETS',
    'Particle', 'EpidemicSimulation', 'SpatialGrid',
    'DARK_THEME', 'LIGHT_THEME', 'get_color', 'set_theme'
]
