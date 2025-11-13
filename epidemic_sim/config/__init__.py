"""
Configuration package for epidemic simulation

Contains parameters and preset configurations
"""

from epidemic_sim.config.parameters import SimParams, params
from epidemic_sim.config.presets import PRESETS

__all__ = ['SimParams', 'params', 'PRESETS']
