"""
Physics Module
==============
Stellar physics calculations and evolution modeling.
"""

from .stellar_constants import *
from .stellar_equations import *
from .stellar_evolution import *

__all__ = [
    # Constants
    'G', 'C', 'SIGMA_SB', 'K_B',
    'M_SUN', 'R_SUN', 'L_SUN', 'T_SUN',
    'X_SUN', 'Y_SUN', 'Z_SUN',
    
    # Unit conversions
    'solar_mass', 'solar_radius', 'solar_luminosity',
    'years', 'seconds',
    
    # Color functions
    'temperature_to_rgb', 'temperature_to_hex',
    'get_spectral_class',
    
    # Equations
    'total_pressure', 'total_opacity',
    'energy_generation_rate',
    'main_sequence_luminosity', 'main_sequence_radius',
    'main_sequence_temperature', 'main_sequence_lifetime',
    
    # Evolution
    'StellarModel', 'StellarEvolutionTrack',
    'EvolutionPhase', 'PHASE_NAMES',
    'zero_age_main_sequence_model',
]
