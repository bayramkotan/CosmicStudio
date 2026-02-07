"""
Stellar Structure Equations
============================
Fundamental equations for stellar physics and evolution.
"""

import numpy as np
from .stellar_constants import *

# ============================================================================
# EQUATION OF STATE
# ============================================================================

def ideal_gas_pressure(rho, T, mu=MU):
    """
    Ideal gas pressure.
    
    P = (ρ k_B T) / (μ m_u)
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    mu : float
        Mean molecular weight
        
    Returns:
    --------
    float : Pressure (Pa)
    """
    return (rho * K_B * T) / (mu * M_U)

def radiation_pressure(T):
    """
    Radiation pressure.
    
    P_rad = (1/3) a T⁴
    
    Parameters:
    -----------
    T : float
        Temperature (K)
        
    Returns:
    --------
    float : Radiation pressure (Pa)
    """
    return (1.0 / 3.0) * A_RAD * T**4

def total_pressure(rho, T, mu=MU):
    """
    Total pressure (gas + radiation).
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    mu : float
        Mean molecular weight
        
    Returns:
    --------
    float : Total pressure (Pa)
    """
    P_gas = ideal_gas_pressure(rho, T, mu)
    P_rad = radiation_pressure(T)
    return P_gas + P_rad

def density_from_pressure(P, T, mu=MU):
    """
    Calculate density from pressure and temperature.
    Iterative solution since P = P_gas + P_rad.
    
    Parameters:
    -----------
    P : float
        Total pressure (Pa)
    T : float
        Temperature (K)
    mu : float
        Mean molecular weight
        
    Returns:
    --------
    float : Density (kg/m³)
    """
    P_rad = radiation_pressure(T)
    P_gas = P - P_rad
    
    if P_gas <= 0:
        P_gas = 0.01 * P  # Prevent negative density
    
    rho = (P_gas * mu * M_U) / (K_B * T)
    return max(rho, 1e-10)  # Prevent zero density

# ============================================================================
# OPACITY
# ============================================================================

def kramers_opacity(rho, T, X=X_SUN, Z=Z_SUN):
    """
    Kramers opacity law for bound-free and free-free absorption.
    
    κ = κ₀ ρ T⁻³·⁵
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    X : float
        Hydrogen mass fraction
    Z : float
        Metal mass fraction
        
    Returns:
    --------
    float : Opacity (m²/kg)
    """
    # Ensure T is not too small
    T = max(T, 1000.0)
    
    kappa_bf_ff = KAPPA_0 * (1 + X) * Z * rho * T**(-3.5)
    return kappa_bf_ff

def electron_scattering_opacity(X=X_SUN):
    """
    Electron scattering opacity (Thomson scattering).
    
    κ_es = 0.02(1 + X) m²/kg
    
    Parameters:
    -----------
    X : float
        Hydrogen mass fraction
        
    Returns:
    --------
    float : Opacity (m²/kg)
    """
    return 0.02 * (1 + X)

def total_opacity(rho, T, X=X_SUN, Z=Z_SUN):
    """
    Total opacity (Kramers + electron scattering).
    Uses harmonic mean approximation.
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    X : float
        Hydrogen mass fraction
    Z : float
        Metal mass fraction
        
    Returns:
    --------
    float : Total opacity (m²/kg)
    """
    kappa_k = kramers_opacity(rho, T, X, Z)
    kappa_es = electron_scattering_opacity(X)
    
    # Rosseland mean approximation
    kappa = 1.0 / (1.0/kappa_k + 1.0/kappa_es)
    
    return max(kappa, 1e-10)  # Prevent zero opacity

# ============================================================================
# ENERGY GENERATION
# ============================================================================

def pp_chain_rate(rho, T, X=X_SUN):
    """
    PP-chain energy generation rate.
    
    ε_pp ∝ ρ X² T⁴
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    X : float
        Hydrogen mass fraction
        
    Returns:
    --------
    float : Energy generation rate (W/kg)
    """
    # PP-chain threshold temperature
    T6 = T / 1e6  # Temperature in millions of Kelvin
    
    if T6 < 4.0:
        return 0.0
    
    # Simplified PP-chain rate
    # ε_pp = 1.07e-7 ρ X² T₆⁴ W/kg (in SI units)
    epsilon_pp = 1.07e-12 * rho * X**2 * T6**4
    
    return epsilon_pp

def cno_cycle_rate(rho, T, X=X_SUN, X_CNO=0.01*Z_SUN):
    """
    CNO cycle energy generation rate.
    
    ε_CNO ∝ ρ X X_CNO T¹⁶
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    X : float
        Hydrogen mass fraction
    X_CNO : float
        CNO mass fraction
        
    Returns:
    --------
    float : Energy generation rate (W/kg)
    """
    T6 = T / 1e6
    
    if T6 < 13.0:
        return 0.0
    
    # Simplified CNO cycle rate
    # ε_CNO = 8.24e-26 ρ X X_CNO T₆¹⁶ W/kg
    epsilon_cno = 8.24e-31 * rho * X * X_CNO * T6**16
    
    return epsilon_cno

def triple_alpha_rate(rho, T, Y=Y_SUN):
    """
    Triple-alpha process energy generation rate (He burning).
    
    ε_3α ∝ ρ² Y³ T⁴⁰
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    Y : float
        Helium mass fraction
        
    Returns:
    --------
    float : Energy generation rate (W/kg)
    """
    T8 = T / 1e8  # Temperature in 100 million K
    
    if T8 < 1.0:
        return 0.0
    
    # Simplified triple-alpha rate
    # ε_3α = 5.09e-11 ρ² Y³ T₈⁴⁰ W/kg
    epsilon_3alpha = 5.09e-17 * rho**2 * Y**3 * T8**40
    
    return epsilon_3alpha

def energy_generation_rate(rho, T, X=X_SUN, Y=Y_SUN, Z=Z_SUN):
    """
    Total nuclear energy generation rate.
    
    Parameters:
    -----------
    rho : float
        Density (kg/m³)
    T : float
        Temperature (K)
    X, Y, Z : float
        Mass fractions
        
    Returns:
    --------
    float : Total energy generation rate (W/kg)
    """
    eps_pp = pp_chain_rate(rho, T, X)
    eps_cno = cno_cycle_rate(rho, T, X)
    eps_3alpha = triple_alpha_rate(rho, T, Y)
    
    return eps_pp + eps_cno + eps_3alpha

# ============================================================================
# CONVECTION CRITERION
# ============================================================================

def radiative_temperature_gradient(P, T, L, M, r, rho, kappa):
    """
    Radiative temperature gradient.
    
    ∇_rad = (3 κ ρ L P) / (16 π a c T⁴ G M r²)
    
    Parameters:
    -----------
    P : float
        Pressure (Pa)
    T : float
        Temperature (K)
    L : float
        Luminosity (W)
    M : float
        Mass interior to r (kg)
    r : float
        Radius (m)
    rho : float
        Density (kg/m³)
    kappa : float
        Opacity (m²/kg)
        
    Returns:
    --------
    float : Radiative gradient (dimensionless)
    """
    if L <= 0 or M <= 0 or r <= 0:
        return 0.0
    
    numerator = 3 * kappa * rho * L * P
    denominator = 16 * np.pi * A_RAD * C * T**4 * G * M * r**2
    
    grad_rad = numerator / denominator
    
    return grad_rad

def adiabatic_temperature_gradient(gamma=GAMMA_ADIABATIC):
    """
    Adiabatic temperature gradient for ideal gas.
    
    ∇_ad = (γ - 1) / γ
    
    Parameters:
    -----------
    gamma : float
        Adiabatic index
        
    Returns:
    --------
    float : Adiabatic gradient (dimensionless)
    """
    return (gamma - 1.0) / gamma

def is_convective(P, T, L, M, r, rho, kappa, gamma=GAMMA_ADIABATIC):
    """
    Check if region is convectively unstable (Schwarzschild criterion).
    
    Convection occurs when ∇_rad > ∇_ad
    
    Returns:
    --------
    bool : True if convective, False if radiative
    """
    grad_rad = radiative_temperature_gradient(P, T, L, M, r, rho, kappa)
    grad_ad = adiabatic_temperature_gradient(gamma)
    
    return grad_rad > grad_ad

# ============================================================================
# STELLAR STRUCTURE DIFFERENTIAL EQUATIONS
# ============================================================================

def stellar_structure_equations(r, y, X=X_SUN, Y=Y_SUN, Z=Z_SUN):
    """
    System of stellar structure differential equations.
    
    dy/dr = f(r, y)
    
    where y = [M, P, L, T]
    
    Parameters:
    -----------
    r : float
        Radius (m)
    y : array
        [M(r), P(r), L(r), T(r)]
    X, Y, Z : float
        Composition
        
    Returns:
    --------
    array : [dM/dr, dP/dr, dL/dr, dT/dr]
    """
    M, P, L, T = y
    
    # Prevent negative/zero values
    r = max(r, R_CENTER)
    M = max(M, 1e20)  # Small mass
    P = max(P, P_SURFACE)
    L = max(L, 1e20)  # Small luminosity
    T = max(T, T_SURFACE_MIN)
    
    # Calculate density from EOS
    mu = 1.0 / (2*X + 0.75*Y + 0.5*Z)
    rho = density_from_pressure(P, T, mu)
    
    # Calculate opacity
    kappa = total_opacity(rho, T, X, Z)
    
    # Calculate energy generation
    epsilon = energy_generation_rate(rho, T, X, Y, Z)
    
    # 1. Mass conservation: dM/dr = 4πr²ρ
    dM_dr = 4 * np.pi * r**2 * rho
    
    # 2. Hydrostatic equilibrium: dP/dr = -GMρ/r²
    dP_dr = -(G * M * rho) / r**2
    
    # 3. Energy generation: dL/dr = 4πr²ρε
    dL_dr = 4 * np.pi * r**2 * rho * epsilon
    
    # 4. Energy transport
    # Check if convective or radiative
    if is_convective(P, T, L, M, r, rho, kappa):
        # Convective: use adiabatic gradient
        grad = adiabatic_temperature_gradient()
        dT_dr = -(P * T * grad) / (r * G * M * rho)
    else:
        # Radiative: dT/dr = -(3κρL)/(16πacT³r²)
        if L > 0 and T > 0:
            dT_dr = -(3 * kappa * rho * L) / (16 * np.pi * A_RAD * C * T**3 * r**2)
        else:
            dT_dr = 0.0
    
    return np.array([dM_dr, dP_dr, dL_dr, dT_dr])

# ============================================================================
# SCALING RELATIONS (for quick estimates)
# ============================================================================

def main_sequence_luminosity(M):
    """
    Mass-luminosity relation for main sequence stars.
    
    L ∝ M^α where α ≈ 3.5
    
    Parameters:
    -----------
    M : float
        Stellar mass (kg)
        
    Returns:
    --------
    float : Luminosity (W)
    """
    M_ratio = M / M_SUN
    L = L_SUN * M_ratio**ALPHA_ML
    return L

def main_sequence_radius(M):
    """
    Mass-radius relation for main sequence stars.
    
    R ∝ M^β where β ≈ 0.8
    
    Parameters:
    -----------
    M : float
        Stellar mass (kg)
        
    Returns:
    --------
    float : Radius (m)
    """
    M_ratio = M / M_SUN
    R = R_SUN * M_ratio**BETA_MR
    return R

def main_sequence_temperature(L, R):
    """
    Effective temperature from Stefan-Boltzmann law.
    
    L = 4πR²σT⁴
    
    Parameters:
    -----------
    L : float
        Luminosity (W)
    R : float
        Radius (m)
        
    Returns:
    --------
    float : Effective temperature (K)
    """
    T_eff = (L / (4 * np.pi * R**2 * SIGMA_SB))**0.25
    return T_eff

def main_sequence_lifetime(M):
    """
    Main sequence lifetime approximation.
    
    t_MS ≈ 10¹⁰ (M/M_☉)^(-2.5) years
    
    Parameters:
    -----------
    M : float
        Stellar mass (kg)
        
    Returns:
    --------
    float : Main sequence lifetime (seconds)
    """
    M_ratio = M / M_SUN
    t_ms = T_MS_COEFF * M_ratio**(-2.5)
    return t_ms

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("STELLAR EQUATIONS TEST")
    print("=" * 70)
    
    # Test for Sun-like conditions
    print("\nSolar Center Conditions (approximate):")
    rho_c = 1.6e5  # kg/m³
    T_c = 1.5e7  # K
    
    P_gas = ideal_gas_pressure(rho_c, T_c)
    P_rad = radiation_pressure(T_c)
    P_total = total_pressure(rho_c, T_c)
    
    print(f"  Density: {rho_c:.2e} kg/m³")
    print(f"  Temperature: {T_c:.2e} K")
    print(f"  Gas Pressure: {P_gas:.2e} Pa")
    print(f"  Radiation Pressure: {P_rad:.2e} Pa")
    print(f"  Total Pressure: {P_total:.2e} Pa")
    print(f"  P_rad/P_total: {P_rad/P_total:.4f}")
    
    kappa = total_opacity(rho_c, T_c)
    print(f"  Opacity: {kappa:.4f} m²/kg")
    
    epsilon = energy_generation_rate(rho_c, T_c)
    print(f"  Energy generation: {epsilon:.2e} W/kg")
    
    # Test scaling relations
    print("\nMain Sequence Scaling Relations:")
    for M_factor in [0.5, 1.0, 2.0, 5.0]:
        M = M_factor * M_SUN
        L = main_sequence_luminosity(M)
        R = main_sequence_radius(M)
        T_eff = main_sequence_temperature(L, R)
        t_ms = main_sequence_lifetime(M)
        
        print(f"\n  {M_factor:.1f} M_☉:")
        print(f"    L = {solar_luminosity(L):.2f} L_☉")
        print(f"    R = {solar_radius(R):.2f} R_☉")
        print(f"    T_eff = {T_eff:.0f} K")
        print(f"    t_MS = {years(t_ms)/1e9:.2f} Gyr")
    
    print("=" * 70)
