# CosmicStudio Quick Reference

## Installation

### Quick Start (Recommended)

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```batch
run.bat
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
cd src
python main.py
```

## Usage Guide

### 1. Select Stellar Mass
- Use spinner: Enter any value from 0.1 to 100 M☉
- Or click preset buttons: 0.5, 1.0, 5.0, 20 M☉

### 2. Explore Evolution
- **Time Slider**: Navigate through stellar lifetime
- **Play Button**: Animate evolution (real-time)
- **Reset Button**: Return to ZAMS (beginning)

### 3. Understand Displays

#### H-R Diagram (Top Right)
- **X-axis**: Temperature (log scale, inverted - hot left, cool right)
- **Y-axis**: Luminosity (log scale - bright top, dim bottom)
- **Colors**: Spectral classes (O=blue, M=red)
- **Markers**:
  - 🟢 Green circle = Start (ZAMS)
  - 🔴 Red square = End state
  - ⭐ Yellow star = Current position

#### Star Cross Section (Bottom Right)
- **White/Yellow**: Core (nuclear fusion)
- **Orange**: Radiative zone
- **Red**: Convective zone / Surface
- **Info Panel**: Real-time parameters

### 4. Interpret Results

#### Stellar Phases
- **Main Sequence**: H → He fusion (90% of lifetime)
- **Red Giant**: Expanding envelope, shell burning
- **White Dwarf**: Dense remnant (M < 8 M☉)
- **Supernova**: Explosive death (M > 8 M☉)

#### Key Parameters
- **Mass**: Total stellar mass
- **Radius**: Physical size
- **Luminosity**: Energy output (brightness)
- **Temperature**: Surface temperature
- **Composition**: H, He, metals (X, Y, Z)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+S` | Export evolution track |
| `Ctrl+0` | Reset H-R diagram zoom |
| `Ctrl+Q` | Quit application |

## Mouse Controls

### H-R Diagram
- **Left Click + Drag**: Pan view
- **Mouse Wheel**: Zoom in/out
- **Right Click**: Context menu (save plot)

## Stellar Mass Regimes

| Mass Range | Main Sequence | Lifetime | Final State |
|-----------|---------------|----------|-------------|
| < 0.5 M☉ | Red Dwarf (M) | > 100 Gyr | White Dwarf |
| 0.5-1.5 M☉ | Yellow (G-K) | 10-50 Gyr | White Dwarf |
| 1.5-8 M☉ | White-Blue (A-F) | 0.1-10 Gyr | White Dwarf + Nebula |
| 8-25 M☉ | Blue (B-O) | 10-100 Myr | Neutron Star |
| > 25 M☉ | Supergiant (O) | < 10 Myr | Black Hole |

## Temperature-Color Guide

| T (K) | Color | Spectral Class |
|-------|-------|----------------|
| > 30,000 | Blue | O |
| 10,000-30,000 | Blue-White | B |
| 7,500-10,000 | White | A |
| 6,000-7,500 | Yellow-White | F |
| 5,200-6,000 | Yellow | G |
| 3,700-5,200 | Orange | K |
| < 3,700 | Red | M |

## Physics Equations (Quick Reference)

### Main Sequence Relations
```
L ∝ M^3.5        (Mass-Luminosity)
R ∝ M^0.8        (Mass-Radius)
t_MS ∝ M^-2.5    (Lifetime)
```

### Stefan-Boltzmann Law
```
L = 4πR²σT⁴
```

### Energy Sources
- **PP Chain**: T > 4×10⁶ K (low mass)
- **CNO Cycle**: T > 1.3×10⁷ K (high mass)
- **Triple-Alpha**: T > 10⁸ K (giants)

## Troubleshooting

### Application won't start
1. Check Python version: `python --version` (need 3.8+)
2. Verify dependencies: `pip list | grep -E "(PySide6|numpy|scipy|matplotlib)"`
3. Try manual installation steps

### Display issues
- Update graphics drivers
- Try different Qt backend: `export QT_QPA_PLATFORM=xcb`

### Slow performance
- Reduce number of evolution steps (edit source)
- Close other applications
- Use lower mass stars (faster calculation)

## Export Features

### Save Evolution Track
1. File → Export Track
2. Choose location
3. Saves as JSON with all parameters

### Export H-R Diagram
1. Right-click on diagram
2. Select "Save Plot"
3. Choose format (PNG, PDF, SVG)

## Tips & Tricks

### For Education
- Compare different masses side-by-side
- Pause at interesting phases
- Export diagrams for presentations

### For Research
- Use custom mass values
- Export tracks for further analysis
- Verify against MESA/STARS codes

### For Fun
- Watch massive star go supernova
- See the Sun's future (red giant!)
- Explore extreme stellar physics

## Support

**Issues/Bugs**: Create GitHub issue
**Questions**: Check README.md
**Physics Background**: See references in README.md

---

**Version**: 1.0.0  
**Author**: Bayram  
**License**: MIT
