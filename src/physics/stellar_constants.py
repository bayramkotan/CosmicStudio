"""
Stellar Constants and Physical Parameters
==========================================
All physical constants and unit conversions for stellar physics calculations.
"""

import numpy as np

# ============================================================================
# FUNDAMENTAL PHYSICAL CONSTANTS (SI Units)
# ============================================================================

# Gravitational constant
G = 6.67430e-11  # m³ kg⁻¹ s⁻²

# Speed of light
C = 2.99792458e8  # m/s

# Stefan-Boltzmann constant
SIGMA_SB = 5.670374419e-8  # W m⁻² K⁻⁴

# Boltzmann constant
K_B = 1.380649e-23  # J K⁻¹

# Radiation constant
A_RAD = 4 * SIGMA_SB / C  # 7.5657e-16 J m⁻³ K⁻⁴

# Proton mass
M_PROTON = 1.6726219e-27  # kg

# Atomic mass unit
M_U = 1.66053906660e-27  # kg

# Gas constant
R_GAS = 8.314462618  # J mol⁻¹ K⁻¹

# Avogadro's number
N_A = 6.02214076e23  # mol⁻¹

# ============================================================================
# ASTRONOMICAL CONSTANTS
# ============================================================================

# Solar mass
M_SUN = 1.98847e30  # kg

# Solar radius
R_SUN = 6.96340e8  # m

# Solar luminosity
L_SUN = 3.828e26  # W

# Solar effective temperature
T_SUN = 5772  # K

# Astronomical Unit
AU = 1.495978707e11  # m

# Parsec
PC = 3.0857e16  # m

# Year (in seconds)
YEAR = 3.15576e7  # s

# ============================================================================
# COMPOSITION PARAMETERS
# ============================================================================

# Solar metallicity (mass fraction)
Z_SUN = 0.0142

# Solar hydrogen mass fraction
X_SUN = 0.7381

# Solar helium mass fraction
Y_SUN = 0.2477

# Mean molecular weight for fully ionized gas
MU_E = 2.0  # electrons (pure hydrogen)
MU_ION = 0.5  # ions (pure hydrogen)
MU = 0.61  # mean molecular weight (solar composition)

# ============================================================================
# NUCLEAR REACTION PARAMETERS
# ============================================================================

# PP-chain energy per reaction
Q_PP = 26.731e6 * 1.60218e-19  # J (26.731 MeV in Joules)

# CNO cycle energy per reaction
Q_CNO = 25.0e6 * 1.60218e-19  # J (25.0 MeV in Joules)

# Triple-alpha process energy
Q_3ALPHA = 7.275e6 * 1.60218e-19  # J (7.275 MeV in Joules)

# ============================================================================
# OPACITY PARAMETERS (Kramers opacity approximation)
# ============================================================================

# Kramers opacity coefficient
KAPPA_0 = 4.34e25  # m² kg⁻¹ (in SI units)

# Electron scattering opacity
KAPPA_ES = 0.02 * (1 + X_SUN)  # m² kg⁻¹

# ============================================================================
# POLYTROPIC INDICES
# ============================================================================

# Common polytropic indices for stellar modeling
GAMMA_ADIABATIC = 5.0 / 3.0  # Monatomic ideal gas
GAMMA_RADIATION = 4.0 / 3.0  # Radiation dominated

# Polytropic indices for different stellar zones
N_CORE = 3.0  # Convective core
N_ENVELOPE = 1.5  # Radiative envelope

# ============================================================================
# STELLAR EVOLUTION PARAMETERS
# ============================================================================

# Main sequence lifetime coefficient (approximate)
# t_MS ≈ 10^10 * (M/M_sun)^-2.5 years
T_MS_COEFF = 1.0e10 * YEAR  # s

# Mass-luminosity relation exponent (main sequence)
ALPHA_ML = 3.5  # L ∝ M^α

# Mass-radius relation exponent (main sequence)
BETA_MR = 0.8  # R ∝ M^β

# ============================================================================
# BOUNDARY CONDITIONS
# ============================================================================

# Central boundary conditions (small radius)
R_CENTER = 1.0e-6 * R_SUN  # Small but non-zero

# Surface boundary conditions
P_SURFACE = 1.0e3  # Pa (low pressure at surface)
T_SURFACE_MIN = 3000  # K (minimum surface temperature)

# ============================================================================
# NUMERICAL PARAMETERS
# ============================================================================

# Integration tolerances
RTOL = 1.0e-6  # Relative tolerance
ATOL = 1.0e-9  # Absolute tolerance

# Maximum number of zones for stellar structure
N_ZONES = 1000

# ============================================================================
# UNIT CONVERSION FUNCTIONS
# ============================================================================

def solar_mass(mass_kg):
    """Convert mass in kg to solar masses."""
    return mass_kg / M_SUN

def solar_radius(radius_m):
    """Convert radius in m to solar radii."""
    return radius_m / R_SUN

def solar_luminosity(luminosity_w):
    """Convert luminosity in W to solar luminosities."""
    return luminosity_w / L_SUN

def years(time_s):
    """Convert time in seconds to years."""
    return time_s / YEAR

def seconds(time_yr):
    """Convert time in years to seconds."""
    return time_yr * YEAR

def kelvin_to_log_T(T):
    """Convert temperature to log10(T)."""
    return np.log10(T)

def log_T_to_kelvin(log_T):
    """Convert log10(T) to temperature."""
    return 10.0 ** log_T

# ============================================================================
# COLOR TEMPERATURE MAPPING
# ============================================================================

def temperature_to_rgb(T):
    """
    Convert stellar temperature to approximate RGB color.
    Based on blackbody radiation color approximation.
    
    Parameters:
    -----------
    T : float
        Temperature in Kelvin
        
    Returns:
    --------
    tuple : (R, G, B) values in range [0, 255]
    """
    # Normalize temperature (1000K - 40000K)
    T = np.clip(T, 1000, 40000)
    T = T / 100.0
    
    # Red channel
    if T <= 66:
        R = 255
    else:
        R = T - 60
        R = 329.698727446 * (R ** -0.1332047592)
        R = np.clip(R, 0, 255)
    
    # Green channel
    if T <= 66:
        G = T
        G = 99.4708025861 * np.log(G) - 161.1195681661
        G = np.clip(G, 0, 255)
    else:
        G = T - 60
        G = 288.1221695283 * (G ** -0.0755148492)
        G = np.clip(G, 0, 255)
    
    # Blue channel
    if T >= 66:
        B = 255
    elif T <= 19:
        B = 0
    else:
        B = T - 10
        B = 138.5177312231 * np.log(B) - 305.0447927307
        B = np.clip(B, 0, 255)
    
    return (int(R), int(G), int(B))

def temperature_to_hex(T):
    """Convert temperature to hex color string."""
    r, g, b = temperature_to_rgb(T)
    return f"#{r:02x}{g:02x}{b:02x}"

# ============================================================================
# STELLAR CLASSIFICATION
# ============================================================================

SPECTRAL_CLASSES = {
    'O': {'T_range': (30000, 60000), 'color': '#9bb0ff'},
    'B': {'T_range': (10000, 30000), 'color': '#aabfff'},
    'A': {'T_range': (7500, 10000), 'color': '#cad7ff'},
    'F': {'T_range': (6000, 7500), 'color': '#f8f7ff'},
    'G': {'T_range': (5200, 6000), 'color': '#fff4ea'},
    'K': {'T_range': (3700, 5200), 'color': '#ffd2a1'},
    'M': {'T_range': (2400, 3700), 'color': '#ffcc6f'},
}

def get_spectral_class(T_eff):
    """
    Get spectral class from effective temperature.
    
    Parameters:
    -----------
    T_eff : float
        Effective temperature in Kelvin
        
    Returns:
    --------
    str : Spectral class (O, B, A, F, G, K, M)
    """
    for spec_class, data in SPECTRAL_CLASSES.items():
        T_min, T_max = data['T_range']
        if T_min <= T_eff <= T_max:
            return spec_class
    
    if T_eff > 30000:
        return 'O'
    else:
        return 'M'

# ============================================================================
# INFORMATION
# ============================================================================

def print_constants():
    """Print all physical constants for verification."""
    print("=" * 70)
    print("STELLAR PHYSICS CONSTANTS")
    print("=" * 70)
    print(f"\nFundamental Constants:")
    print(f"  G = {G:.6e} m³ kg⁻¹ s⁻²")
    print(f"  c = {C:.6e} m/s")
    print(f"  σ = {SIGMA_SB:.6e} W m⁻² K⁻⁴")
    print(f"  k_B = {K_B:.6e} J K⁻¹")
    
    print(f"\nSolar Parameters:")
    print(f"  M_☉ = {M_SUN:.6e} kg")
    print(f"  R_☉ = {R_SUN:.6e} m")
    print(f"  L_☉ = {L_SUN:.6e} W")
    print(f"  T_☉ = {T_SUN} K")
    
    print(f"\nSolar Composition:")
    print(f"  X (H) = {X_SUN:.4f}")
    print(f"  Y (He) = {Y_SUN:.4f}")
    print(f"  Z (metals) = {Z_SUN:.4f}")
    print("=" * 70)

if __name__ == "__main__":
    print_constants()
    
    # Test color conversion
    print("\nTemperature to Color Conversion:")
    test_temps = [3000, 5772, 10000, 20000, 40000]
    for T in test_temps:
        rgb = temperature_to_rgb(T)
        hex_color = temperature_to_hex(T)
        spec_class = get_spectral_class(T)
        print(f"  {T:5d} K → RGB{rgb} → {hex_color} → Class {spec_class}")
