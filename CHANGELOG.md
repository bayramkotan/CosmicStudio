# Changelog

All notable changes to CosmicStudio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-02-07

### Added
- Initial release of CosmicStudio
- Full stellar physics engine with:
  - Stellar structure equations (mass, pressure, luminosity, temperature)
  - Nuclear reaction rates (PP-chain, CNO cycle, triple-alpha)
  - Equation of state (ideal gas + radiation pressure)
  - Opacity calculations (Kramers + electron scattering)
  - Convection criterion (Schwarzschild)
  
- Stellar evolution calculator:
  - Main sequence evolution (ZAMS to TAMS)
  - Post-main sequence phases (RGB, HB, AGB)
  - Different mass regimes (low, intermediate, high mass)
  - Final states (white dwarf, neutron star, black hole)
  
- Interactive H-R Diagram widget:
  - Evolution track visualization
  - Spectral class regions (O, B, A, F, G, K, M)
  - Constant radius lines
  - Real-time position marker
  - Zoom and pan controls
  
- Star cross-section visualization:
  - Internal structure layers
  - Temperature-based coloring
  - Detailed parameter display
  - Composition tracking
  
- User interface controls:
  - Mass selection (0.1 - 100 M☉)
  - Preset stellar configurations
  - Time slider for navigation
  - Play/pause animation
  - Parameter display panel
  
- Documentation:
  - Comprehensive README
  - Physics background explanations
  - Installation instructions
  - Usage guide
  
- Development tools:
  - Automated test suite
  - Quick start scripts (bash/batch)
  - Example scenarios

### Technical Details
- Python 3.8+ compatibility
- PySide6 for modern Qt6 GUI
- NumPy/SciPy for numerical calculations
- Matplotlib for scientific plotting
- Dark theme UI design

## [Unreleased]

### Planned Features
- Custom composition controls
- Binary star systems
- Stellar rotation effects
- Mass loss modeling
- Nucleosynthesis visualization
- Animation export
- Multiple comparison tracks
- WebGL browser version
