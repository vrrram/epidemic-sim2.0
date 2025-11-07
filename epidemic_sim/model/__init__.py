"""
Model package for epidemic simulation

Contains core simulation logic and data structures
"""

from epidemic_sim.model.particle import Particle
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.model.spatial_grid import SpatialGrid

__all__ = ['Particle', 'EpidemicSimulation', 'SpatialGrid']
