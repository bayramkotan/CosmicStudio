"""
Stellar Evolution Engine
=========================
Main stellar evolution calculator using stellar structure equations.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import json
from pathlib import Path

from .stellar_constants import *
from .stellar_equations import *

# ============================================================================
# STELLAR EVOLUTION PHASES
# ============================================================================

class EvolutionPhase:
    """Enum for stellar evolution phases."""
    PRE_MAIN_SEQUENCE = 0
    MAIN_SEQUENCE = 1
    SUBGIANT = 2
    RED_GIANT = 3
    HORIZONTAL_BRANCH = 4
    ASYMPTOTIC_GIANT = 5
    PLANETARY_NEBULA = 6
    WHITE_DWARF = 7
    SUPERNOVA = 8
    NEUTRON_STAR = 9
    BLACK_HOLE = 10

PHASE_NAMES = {
    EvolutionPhase.PRE_MAIN_SEQUENCE: "Pre-Main Sequence",
    EvolutionPhase.MAIN_SEQUENCE: "Main Sequence",
    EvolutionPhase.SUBGIANT: "Subgiant",
    EvolutionPhase.RED_GIANT: "Red Giant",
    EvolutionPhase.HORIZONTAL_BRANCH: "Horizontal Branch",
    EvolutionPhase.ASYMPTOTIC_GIANT: "Asymptotic Giant Branch",
    EvolutionPhase.PLANETARY_NEBULA: "Planetary Nebula",
    EvolutionPhase.WHITE_DWARF: "White Dwarf",
    EvolutionPhase.SUPERNOVA: "Supernova",
    EvolutionPhase.NEUTRON_STAR: "Neutron Star",
    EvolutionPhase.BLACK_HOLE: "Black Hole",
}

# ============================================================================
# STELLAR MODEL
# ============================================================================

class StellarModel:
    """
    Represents a stellar model at a given evolutionary time.
    """
    
    def __init__(self, mass, radius, luminosity, T_eff, age, phase,
                 X=X_SUN, Y=Y_SUN, Z=Z_SUN):
        """
        Parameters:
        -----------
        mass : float
            Stellar mass (kg)
        radius : float
            Stellar radius (m)
        luminosity : float
            Luminosity (W)
        T_eff : float
            Effective temperature (K)
        age : float
            Age (s)
        phase : int
            Evolution phase
        X, Y, Z : float
            Chemical composition
        """
        self.mass = mass
        self.radius = radius
        self.luminosity = luminosity
        self.T_eff = T_eff
        self.age = age
        self.phase = phase
        self.X = X
        self.Y = Y
        self.Z = Z
        
        # Derived quantities
        self.spectral_class = get_spectral_class(T_eff)
        self.color = temperature_to_hex(T_eff)
        
    def to_solar_units(self):
        """Return parameters in solar units."""
        return {
            'M': solar_mass(self.mass),
            'R': solar_radius(self.radius),
            'L': solar_luminosity(self.luminosity),
            'T_eff': self.T_eff,
            'age_Gyr': years(self.age) / 1e9,
            'phase': PHASE_NAMES[self.phase],
            'spectral_class': self.spectral_class,
        }
    
    def __repr__(self):
        solar = self.to_solar_units()
        return (f"StellarModel(M={solar['M']:.2f} M☉, "
                f"R={solar['R']:.2f} R☉, "
                f"L={solar['L']:.2f} L☉, "
                f"T={solar['T_eff']:.0f} K, "
                f"age={solar['age_Gyr']:.2f} Gyr, "
                f"phase={solar['phase']})")

# ============================================================================
# INITIAL CONDITIONS
# ============================================================================

def zero_age_main_sequence_model(M, X=X_SUN, Y=Y_SUN, Z=Z_SUN):
    """
    Create a Zero Age Main Sequence (ZAMS) model.
    
    Uses scaling relations for initial estimate.
    
    Parameters:
    -----------
    M : float
        Stellar mass (kg)
    X, Y, Z : float
        Chemical composition
        
    Returns:
    --------
    StellarModel : ZAMS model
    """
    # Use scaling relations
    L = main_sequence_luminosity(M)
    R = main_sequence_radius(M)
    T_eff = main_sequence_temperature(L, R)
    
    return StellarModel(
        mass=M,
        radius=R,
        luminosity=L,
        T_eff=T_eff,
        age=0.0,
        phase=EvolutionPhase.MAIN_SEQUENCE,
        X=X, Y=Y, Z=Z
    )

# ============================================================================
# STELLAR STRUCTURE INTEGRATION
# ============================================================================

def integrate_stellar_structure(M, L_core, T_c, X=X_SUN, Y=Y_SUN, Z=Z_SUN):
    """
    Integrate stellar structure equations from center to surface.
    
    This is a simplified integration for demonstration.
    Full stellar evolution would require iterative shooting method.
    
    Parameters:
    -----------
    M : float
        Total stellar mass (kg)
    L_core : float
        Core luminosity (W)
    T_c : float
        Central temperature (K)
    X, Y, Z : float
        Composition
        
    Returns:
    --------
    dict : Stellar structure profile
    """
    # Initial conditions at center
    r0 = R_CENTER
    M0 = 4.0/3.0 * np.pi * r0**3 * 1.6e5  # Small central mass
    
    # Estimate central pressure from virial theorem
    # P_c ≈ GM²/(R⁴) (rough approximation)
    R_estimate = main_sequence_radius(M)
    P_c = 0.5 * G * M**2 / R_estimate**4
    
    L0 = L_core
    T0 = T_c
    
    y0 = np.array([M0, P_c, L0, T0])
    
    # Integration span
    r_span = (r0, 10 * R_estimate)  # Integrate to large radius
    
    # Event to stop at surface (when P drops to surface pressure)
    def surface_event(r, y):
        return y[1] - P_SURFACE
    surface_event.terminal = True
    surface_event.direction = -1
    
    # Solve ODEs
    try:
        solution = solve_ivp(
            lambda r, y: stellar_structure_equations(r, y, X, Y, Z),
            r_span,
            y0,
            method='Radau',
            events=surface_event,
            dense_output=True,
            rtol=RTOL,
            atol=ATOL,
            max_step=R_estimate/100
        )
        
        if solution.success:
            # Extract final radius (surface)
            R_surface = solution.t[-1]
            M_final, P_final, L_final, T_final = solution.y[:, -1]
            
            return {
                'success': True,
                'radius': R_surface,
                'mass': M_final,
                'luminosity': L_final,
                'T_surface': T_final,
                'profile': {
                    'r': solution.t,
                    'M': solution.y[0],
                    'P': solution.y[1],
                    'L': solution.y[2],
                    'T': solution.y[3],
                }
            }
        else:
            return {'success': False, 'message': solution.message}
            
    except Exception as e:
        return {'success': False, 'message': str(e)}

# ============================================================================
# EVOLUTIONARY TRACK CALCULATOR
# ============================================================================

class StellarEvolutionTrack:
    """
    Calculate and store stellar evolution track.
    """
    
    def __init__(self, M_initial, X=X_SUN, Y=Y_SUN, Z=Z_SUN):
        """
        Parameters:
        -----------
        M_initial : float
            Initial stellar mass (solar masses)
        X, Y, Z : float
            Chemical composition
        """
        self.M_initial_solar = M_initial
        self.M_initial = M_initial * M_SUN
        self.X = X
        self.Y = Y
        self.Z = Z
        
        self.models = []
        self.time_points = []
        
    def calculate_main_sequence_evolution(self, n_steps=100):
        """
        Calculate main sequence evolution using parametric approach.
        
        This is a simplified model that uses scaling relations.
        For full physics, we would integrate stellar structure equations
        at each timestep with changing composition.
        
        Parameters:
        -----------
        n_steps : int
            Number of time steps
        """
        # Get ZAMS model
        zams = zero_age_main_sequence_model(self.M_initial, self.X, self.Y, self.Z)
        
        # Main sequence lifetime
        t_ms = main_sequence_lifetime(self.M_initial)
        
        # Time array (logarithmic spacing)
        times = np.logspace(-3, 0, n_steps) * t_ms  # From 0.001 to 1.0 t_MS
        
        models = []
        
        for t in times:
            # Parametric evolution on main sequence
            # As star ages: L increases, R increases slightly, T_eff increases
            
            age_fraction = t / t_ms
            
            # Luminosity increases as H is depleted
            L = zams.luminosity * (1.0 + 0.5 * age_fraction)
            
            # Radius increases slightly
            R = zams.radius * (1.0 + 0.1 * age_fraction)
            
            # Temperature from L and R
            T_eff = main_sequence_temperature(L, R)
            
            # Composition changes (simplified)
            X_current = self.X * (1.0 - 0.5 * age_fraction)
            Y_current = self.Y + 0.5 * (self.X - X_current)
            
            model = StellarModel(
                mass=self.M_initial,
                radius=R,
                luminosity=L,
                T_eff=T_eff,
                age=t,
                phase=EvolutionPhase.MAIN_SEQUENCE,
                X=X_current,
                Y=Y_current,
                Z=self.Z
            )
            
            models.append(model)
        
        self.models.extend(models)
        self.time_points.extend(times)
        
        return models
    
    def calculate_post_main_sequence(self, n_steps=50):
        """
        Calculate post-main sequence evolution (RGB, HB, AGB).
        
        Simplified parametric model.
        """
        if len(self.models) == 0:
            self.calculate_main_sequence_evolution()
        
        last_ms_model = self.models[-1]
        t_start = last_ms_model.age
        
        # Post-MS evolution depends on mass
        M_solar = self.M_initial_solar
        
        if M_solar < 0.5:
            # Low mass stars: very long MS, become white dwarfs
            return self._evolve_low_mass(last_ms_model, t_start, n_steps)
        elif M_solar < 8.0:
            # Intermediate mass: RGB → HB → AGB → Planetary Nebula → WD
            return self._evolve_intermediate_mass(last_ms_model, t_start, n_steps)
        else:
            # High mass: Supergiant → Supernova → NS/BH
            return self._evolve_high_mass(last_ms_model, t_start, n_steps)
    
    def _evolve_low_mass(self, model, t_start, n_steps):
        """Low mass star evolution (<0.5 M☉)."""
        # Very slow evolution, essentially stays on MS for universe age
        return []
    
    def _evolve_intermediate_mass(self, model, t_start, n_steps):
        """Intermediate mass evolution (0.5 - 8 M☉)."""
        models = []
        
        # Post-MS timescale (much shorter than MS)
        t_post_ms = 0.1 * main_sequence_lifetime(self.M_initial)
        
        times = np.linspace(0, t_post_ms, n_steps)
        
        for i, dt in enumerate(times):
            t = t_start + dt
            progress = dt / t_post_ms
            
            # Subgiant phase (0-20%)
            if progress < 0.2:
                phase = EvolutionPhase.SUBGIANT
                L = model.luminosity * (1.0 + progress * 10)
                R = model.radius * (1.0 + progress * 5)
            
            # Red Giant Branch (20-60%)
            elif progress < 0.6:
                phase = EvolutionPhase.RED_GIANT
                rgb_progress = (progress - 0.2) / 0.4
                L = model.luminosity * (3.0 + rgb_progress * 100)
                R = model.radius * (5.0 + rgb_progress * 50)
            
            # Horizontal Branch (60-75%)
            elif progress < 0.75:
                phase = EvolutionPhase.HORIZONTAL_BRANCH
                L = model.luminosity * 50
                R = model.radius * 10
            
            # AGB (75-95%)
            elif progress < 0.95:
                phase = EvolutionPhase.ASYMPTOTIC_GIANT
                agb_progress = (progress - 0.75) / 0.2
                L = model.luminosity * (50 + agb_progress * 1000)
                R = model.radius * (10 + agb_progress * 200)
            
            # White Dwarf (95-100%)
            else:
                phase = EvolutionPhase.WHITE_DWARF
                L = model.luminosity * 0.001
                R = 0.01 * R_SUN  # Earth-sized
            
            T_eff = main_sequence_temperature(L, R)
            
            new_model = StellarModel(
                mass=self.M_initial * 0.6,  # Mass loss
                radius=R,
                luminosity=L,
                T_eff=T_eff,
                age=t,
                phase=phase,
                X=0.0,  # No H left
                Y=0.98,
                Z=self.Z
            )
            
            models.append(new_model)
        
        self.models.extend(models)
        self.time_points.extend([t_start + dt for dt in times])
        
        return models
    
    def _evolve_high_mass(self, model, t_start, n_steps):
        """High mass evolution (>8 M☉)."""
        models = []
        
        # Very rapid post-MS evolution
        t_post_ms = 0.01 * main_sequence_lifetime(self.M_initial)
        
        times = np.linspace(0, t_post_ms, n_steps)
        
        for i, dt in enumerate(times):
            t = t_start + dt
            progress = dt / t_post_ms
            
            # Red Supergiant
            if progress < 0.9:
                phase = EvolutionPhase.RED_GIANT
                L = model.luminosity * (10 + progress * 1000)
                R = model.radius * (10 + progress * 100)
            
            # Supernova
            else:
                phase = EvolutionPhase.SUPERNOVA
                L = model.luminosity * 1e6  # Extremely bright
                R = model.radius * 1000
            
            T_eff = main_sequence_temperature(L, R)
            
            new_model = StellarModel(
                mass=self.M_initial,
                radius=R,
                luminosity=L,
                T_eff=T_eff,
                age=t,
                phase=phase,
                X=0.0,
                Y=0.0,
                Z=0.98  # Mostly iron
            )
            
            models.append(new_model)
        
        self.models.extend(models)
        self.time_points.extend([t_start + dt for dt in times])
        
        # Add final remnant
        if self.M_initial_solar > 25:
            final_phase = EvolutionPhase.BLACK_HOLE
        else:
            final_phase = EvolutionPhase.NEUTRON_STAR
        
        remnant = StellarModel(
            mass=self.M_initial * 0.3,
            radius=10000,  # 10 km
            luminosity=1e20,  # Very faint
            T_eff=1e6,
            age=t_start + t_post_ms,
            phase=final_phase,
            X=0.0, Y=0.0, Z=0.0
        )
        
        self.models.append(remnant)
        self.time_points.append(t_start + t_post_ms)
        
        return models
    
    def get_hr_track(self):
        """
        Get H-R diagram track (log L vs log T_eff).
        
        Returns:
        --------
        tuple : (log_T_eff, log_L)
        """
        if len(self.models) == 0:
            return np.array([]), np.array([])
        
        log_T = np.array([np.log10(m.T_eff) for m in self.models])
        log_L = np.array([np.log10(solar_luminosity(m.luminosity)) for m in self.models])
        
        return log_T, log_L
    
    def get_model_at_age(self, age):
        """
        Get stellar model at specific age using interpolation.
        
        Parameters:
        -----------
        age : float
            Age in seconds
            
        Returns:
        --------
        StellarModel : Interpolated model
        """
        if len(self.models) == 0:
            return None
        
        if age <= self.time_points[0]:
            return self.models[0]
        if age >= self.time_points[-1]:
            return self.models[-1]
        
        # Find bracketing indices
        idx = np.searchsorted(self.time_points, age)
        
        # Linear interpolation
        t0, t1 = self.time_points[idx-1], self.time_points[idx]
        m0, m1 = self.models[idx-1], self.models[idx]
        
        fraction = (age - t0) / (t1 - t0)
        
        # Interpolate parameters
        mass = m0.mass + fraction * (m1.mass - m0.mass)
        radius = m0.radius + fraction * (m1.radius - m0.radius)
        luminosity = m0.luminosity + fraction * (m1.luminosity - m0.luminosity)
        T_eff = m0.T_eff + fraction * (m1.T_eff - m0.T_eff)
        
        return StellarModel(
            mass=mass,
            radius=radius,
            luminosity=luminosity,
            T_eff=T_eff,
            age=age,
            phase=m0.phase,
            X=m0.X,
            Y=m0.Y,
            Z=m0.Z
        )
    
    def save_to_json(self, filename):
        """Save evolution track to JSON file."""
        data = {
            'M_initial': self.M_initial_solar,
            'X': self.X,
            'Y': self.Y,
            'Z': self.Z,
            'models': []
        }
        
        for model in self.models:
            data['models'].append({
                'age': years(model.age),
                'M': solar_mass(model.mass),
                'R': solar_radius(model.radius),
                'L': solar_luminosity(model.luminosity),
                'T_eff': model.T_eff,
                'phase': PHASE_NAMES[model.phase],
                'X': model.X,
                'Y': model.Y,
                'Z': model.Z,
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_json(cls, filename):
        """Load evolution track from JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        track = cls(data['M_initial'], data['X'], data['Y'], data['Z'])
        
        # Reconstruct models
        for model_data in data['models']:
            model = StellarModel(
                mass=model_data['M'] * M_SUN,
                radius=model_data['R'] * R_SUN,
                luminosity=model_data['L'] * L_SUN,
                T_eff=model_data['T_eff'],
                age=model_data['age'] * YEAR,
                phase=[k for k, v in PHASE_NAMES.items() if v == model_data['phase']][0],
                X=model_data['X'],
                Y=model_data['Y'],
                Z=model_data['Z']
            )
            track.models.append(model)
            track.time_points.append(model.age)
        
        return track

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("STELLAR EVOLUTION ENGINE TEST")
    print("=" * 70)
    
    # Test evolution track for Sun-like star
    print("\nCalculating evolution track for 1.0 M☉ star...")
    track = StellarEvolutionTrack(M_initial=1.0)
    
    # Calculate MS evolution
    ms_models = track.calculate_main_sequence_evolution(n_steps=50)
    print(f"  Main Sequence: {len(ms_models)} models calculated")
    print(f"  ZAMS: {ms_models[0]}")
    print(f"  TAMS: {ms_models[-1]}")
    
    # Calculate post-MS
    post_ms = track.calculate_post_main_sequence(n_steps=50)
    print(f"  Post-Main Sequence: {len(post_ms)} models calculated")
    if len(post_ms) > 0:
        print(f"  Final: {post_ms[-1]}")
    
    # Get H-R track
    log_T, log_L = track.get_hr_track()
    print(f"\n  H-R Track: {len(log_T)} points")
    print(f"  log T range: {log_T.min():.2f} - {log_T.max():.2f}")
    print(f"  log L range: {log_L.min():.2f} - {log_L.max():.2f}")
    
    # Test different masses
    print("\n" + "=" * 70)
    print("MASS COMPARISON")
    print("=" * 70)
    
    for M_init in [0.5, 1.0, 2.0, 5.0, 10.0]:
        track = StellarEvolutionTrack(M_initial=M_init)
        track.calculate_main_sequence_evolution(n_steps=20)
        
        zams = track.models[0]
        tams = track.models[-1]
        
        print(f"\n{M_init} M☉:")
        print(f"  ZAMS: L={solar_luminosity(zams.luminosity):.2f} L☉, "
              f"T={zams.T_eff:.0f} K, Class {zams.spectral_class}")
        print(f"  MS lifetime: {years(main_sequence_lifetime(M_init*M_SUN))/1e9:.2f} Gyr")
    
    print("=" * 70)
