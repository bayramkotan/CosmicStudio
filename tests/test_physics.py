#!/usr/bin/env python3
"""
Test script for physics module
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def test_constants():
    """Test physical constants."""
    print("=" * 70)
    print("TESTING STELLAR CONSTANTS")
    print("=" * 70)
    
    from physics.stellar_constants import print_constants, temperature_to_hex
    
    print_constants()
    
    # Test color conversion
    print("\nColor Conversion Test:")
    test_temps = [3000, 5772, 10000, 20000]
    for T in test_temps:
        color = temperature_to_hex(T)
        print(f"  T = {T:5d} K → {color}")
    
    print("\n✓ Constants test passed\n")

def test_equations():
    """Test stellar equations."""
    print("=" * 70)
    print("TESTING STELLAR EQUATIONS")
    print("=" * 70)
    
    from physics.stellar_equations import (
        total_pressure, total_opacity, energy_generation_rate,
        main_sequence_lifetime
    )
    from physics.stellar_constants import M_SUN, years
    
    # Solar center conditions
    rho_c = 1.6e5  # kg/m³
    T_c = 1.5e7    # K
    
    P = total_pressure(rho_c, T_c)
    kappa = total_opacity(rho_c, T_c)
    epsilon = energy_generation_rate(rho_c, T_c)
    
    print(f"\nSolar Core Conditions:")
    print(f"  Density: {rho_c:.2e} kg/m³")
    print(f"  Temperature: {T_c:.2e} K")
    print(f"  Pressure: {P:.2e} Pa")
    print(f"  Opacity: {kappa:.4f} m²/kg")
    print(f"  Energy generation: {epsilon:.2e} W/kg")
    
    # Main sequence lifetimes
    print("\nMain Sequence Lifetimes:")
    for M_factor in [0.5, 1.0, 2.0, 5.0]:
        t_ms = main_sequence_lifetime(M_factor * M_SUN)
        print(f"  {M_factor:.1f} M☉: {years(t_ms)/1e9:.2f} Gyr")
    
    print("\n✓ Equations test passed\n")

def test_evolution():
    """Test stellar evolution."""
    print("=" * 70)
    print("TESTING STELLAR EVOLUTION")
    print("=" * 70)
    
    from physics.stellar_evolution import (
        StellarEvolutionTrack, zero_age_main_sequence_model
    )
    from physics.stellar_constants import M_SUN
    
    # Test ZAMS model
    print("\nZero Age Main Sequence Models:")
    for M_factor in [0.5, 1.0, 2.0, 5.0]:
        zams = zero_age_main_sequence_model(M_factor * M_SUN)
        solar = zams.to_solar_units()
        print(f"\n  {M_factor:.1f} M☉:")
        print(f"    L = {solar['L']:.2f} L☉")
        print(f"    R = {solar['R']:.2f} R☉")
        print(f"    T = {solar['T_eff']:.0f} K")
        print(f"    Class: {solar['spectral_class']}")
    
    # Test evolution track
    print("\n\nEvolution Track for 1.0 M☉:")
    track = StellarEvolutionTrack(M_initial=1.0)
    
    print("  Calculating main sequence...")
    ms_models = track.calculate_main_sequence_evolution(n_steps=50)
    print(f"    Generated {len(ms_models)} models")
    print(f"    ZAMS: {ms_models[0]}")
    print(f"    TAMS: {ms_models[-1]}")
    
    print("  Calculating post-main sequence...")
    post_ms = track.calculate_post_main_sequence(n_steps=50)
    print(f"    Generated {len(post_ms)} models")
    if len(post_ms) > 0:
        print(f"    Final: {post_ms[-1]}")
    
    # Get H-R track
    log_T, log_L = track.get_hr_track()
    print(f"\n  H-R Track Statistics:")
    print(f"    Points: {len(log_T)}")
    print(f"    log T range: {log_T.min():.2f} - {log_T.max():.2f}")
    print(f"    log L range: {log_L.min():.2f} - {log_L.max():.2f}")
    
    print("\n✓ Evolution test passed\n")

def test_all():
    """Run all tests."""
    try:
        test_constants()
        test_equations()
        test_evolution()
        
        print("=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_all()
