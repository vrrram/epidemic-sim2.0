# Epidemic Simulation 3.0 - Project Context

## Project Overview
A PyQt5-based particle epidemic simulation implementing a SIR model (Susceptible, Infected, Removed) with spatial dynamics, quarantine mechanics, and real-time visualization.

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the simulation
python epidemic_sim3.py
```

## Current State (Last Updated: 2025-11-04)

### Active Branch
- **Branch**: `claude/update-epidemic-sim3-011CUnSd6Douv1cnUvoKPu8J`
- **Status**: All changes committed and pushed
- **Latest Commit**: `1ee011f` - Add requirements.txt for project dependencies

### Recent Commits
1. `1ee011f` - Add requirements.txt for project dependencies
2. `4f35c3c` - Fix quarantine zone, graph colors, and add 11 presets
3. `90d33ad` - Update epidemic_sim3.py: Add quarantine, patient zero, filled graphs, and parameters

## Key Features Implemented

### 1. Quarantine System
- **Quarantine Zone**: Small top-left corner `(-1.5, -1.15, 0.7, 0.95)`
- **Activation**: Starts on day 10 of simulation
- **Quarantine Trigger**: Particles quarantined after 5 days of infection
- **Asymptomatic Carriers**: 20% of infected don't show symptoms and avoid quarantine
- **Color Coding**:
  - Red particles = Symptomatic infected (get quarantined)
  - Orange particles = Asymptomatic infected (stay in population)

### 2. Filled Graph Areas
- **Stacked Area Chart**: Properly rendered using polygon-based PlotCurveItem
- **Layers** (bottom to top):
  - Gray = Removed/Recovered
  - Red = Infected
  - Cyan = Susceptible
- **Implementation**: Uses polygon points with forward + reverse x/y coordinates for proper filling

### 3. Patient Zero Guarantee
- **All Modes**: Guaranteed at least 1 infected particle in simple/quarantine/community modes
- **Implementation**: `max(1, int(num_particles * fraction_infected_init))`

### 4. Preset System
**11 Presets Available**:
- Educational: Baseline Epidemic, Slow Burn, Fast Outbreak, Highly Contagious
- Interventions: Social Distancing (Weak), Social Distancing (Strong)
- Historical: COVID-19 (Original), COVID-19 (Delta), Spanish Flu (1918), Measles, Ebola

## File Structure

```
/home/user/epidemic-sim2.0/
├── epidemic_sim3.py          # Main simulation (1000+ lines)
├── requirements.txt           # Python dependencies
├── claude.md                  # This file
├── UPDATE_SUMMARY.md          # Initial update documentation
└── README.md                  # Project README
```

## Technical Architecture

### Core Components

#### 1. SimParams (Lines 19-47)
Global parameters object with 10 configurable parameters:
- Infection: `infection_radius`, `prob_infection`, `fraction_infected_init`, `infection_duration`
- Social Distancing: `social_distance_factor`, `social_distance_obedient`
- Quarantine: `quarantine_after`, `start_quarantine`, `prob_no_symptoms`
- Performance: `boxes_to_consider`

#### 2. Particle Class (Lines 114-163)
Individual particle with properties:
- Position: `x`, `y`, `vx`, `vy`
- State: `'susceptible'`, `'infected'`, `'removed'`
- Infection tracking: `days_infected`, `shows_symptoms`, `infection_start_day`
- Social behavior: `quarantined`, `obeys_social_distance`

#### 3. EpidemicSim Class (Lines 165-600)
Main simulation logic:
- **Spatial Grid Optimization**: O(n) infection checking using hash grid
- **Movement**: Boundary reflection, social distancing modulation
- **Infection Logic**: Grid-based neighbor checking, probabilistic infection
- **Quarantine Management**: Conditional quarantine based on symptoms, timing
- **Statistics Tracking**: Daily S/I/R counts

#### 4. MainWindow (Lines 602-1000+)
PyQt5 GUI:
- **Visualization**: Real-time particle rendering + stacked area graph
- **Controls**: 10 parameter sliders + mode selector + preset dropdown
- **Stats Display**: Current counts, peak metrics, day counter
- **Timer**: 16ms refresh (60 FPS target)

### Key Algorithms

#### Spatial Grid Hash (Lines 253-268)
```python
def _grid_hash(self, x, y):
    # Maps continuous coordinates to discrete grid cells
    # Enables O(n) infection checking instead of O(n²)
    cell_x = int((x - self.bounds[0]) / self.cell_size)
    cell_y = int((y - self.bounds[2]) / self.cell_size)
    return (cell_x, cell_y)
```

#### Infection Check (Lines 289-337)
```python
def _check_infections(self):
    # Only checks particles in nearby grid cells
    # Uses boxes_to_consider parameter for range
    for infected in self.infected_particles:
        nearby = self._get_nearby_susceptible(infected)
        for susceptible in nearby:
            distance = math.hypot(infected.x - susceptible.x,
                                 infected.y - susceptible.y)
            if distance < params.infection_radius:
                if random.random() < params.prob_infection:
                    self._infect(susceptible)
```

#### Graph Stacking (Lines 928-961)
```python
def update_stats_display(self, counts):
    # Creates polygon points for proper area filling
    # Bottom layer: removed (gray)
    r_x = days + days[::-1]
    r_y = r_data + [0] * len(days)

    # Middle layer: infected (red), stacked on removed
    i_y_top = [r_data[i] + i_data[i] for i in range(len(days))]
    i_y = i_y_top + r_data[::-1]

    # Top layer: susceptible (cyan), stacked on infected+removed
    s_y = [100] * len(days) + s_y_bottom[::-1]
```

## Parameters Explained

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `infection_radius` | 0.15 | 0.05-0.30 | Distance for infection transmission |
| `prob_infection` | 0.02 | 0.01-0.10 | Probability of infection per contact |
| `fraction_infected_init` | 0.01 | 0.00-0.10 | Initial infected fraction |
| `infection_duration` | 25 | 5-50 | Days infected before recovery |
| `social_distance_factor` | 0.0 | 0.0-1.0 | Speed reduction for distancing |
| `social_distance_obedient` | 1.0 | 0.0-1.0 | Fraction obeying distancing |
| `quarantine_after` | 5 | 1-20 | Days infected before quarantine |
| `start_quarantine` | 10 | 0-50 | Simulation day to activate zone |
| `prob_no_symptoms` | 0.20 | 0.0-1.0 | Asymptomatic carrier rate |
| `boxes_to_consider` | 2 | 1-5 | Grid cells to check for infection |

## Color Scheme

### Particles
- **Cyan** `(0, 191, 255)` - Susceptible
- **Red** `(255, 69, 69)` - Symptomatic infected
- **Orange** `(255, 165, 0)` - Asymptomatic infected
- **Gray** `(100, 100, 100)` - Removed/recovered

### UI Theme
- **Neon Green** `#00ff00` - Text, borders
- **Dark Green** `#003300` - Hover states
- **Black** `#000000` - Background
- **Panel Black** `#0a0a0a` - UI panels

## Known Issues & Limitations

### Fixed Issues
- ✅ Quarantine zone too large (fixed to small corner)
- ✅ Graph colors all light blue (fixed with polygon stacking)
- ✅ Poor default presets (added 11 useful presets)
- ✅ Patient zero not guaranteed (fixed with max(1, ...) logic)

### Current Limitations
- No vaccination mechanics
- No immunity duration (removed = permanently immune)
- No age/vulnerability stratification
- No contact tracing visualization
- Grid-based optimization limits infection to local cells

## Development Notes

### Performance
- **Particle Count**: Tested up to 1000 particles
- **Target FPS**: 60 (16ms timer)
- **Optimization**: Spatial grid reduces infection checks from O(n²) to O(n)

### Design Decisions
1. **Quarantine Position**: Top-left corner avoids main simulation area
2. **Asymptomatic Rate**: 20% balances realism with visual interest
3. **Quarantine Timing**: Day 10 start + day 5 quarantine creates observable effect
4. **Graph Type**: Stacked areas show proportions better than separate lines
5. **Preset Diversity**: Mix of educational, intervention, and historical scenarios

### Future Improvements (Not Implemented)
- Vaccination campaign mechanics
- Contact tracing visualization
- Multiple quarantine zones
- Waning immunity
- Age-structured populations
- Hospital capacity modeling
- Mask effectiveness parameter
- Travel between regions

## Testing Presets

### Educational Use
- **Baseline Epidemic**: Standard parameters for teaching
- **Slow Burn**: Low transmission, long duration
- **Fast Outbreak**: High transmission, quick spread

### Intervention Testing
- **Social Distancing (Weak)**: 50% compliance, 50% speed reduction
- **Social Distancing (Strong)**: 80% compliance, 70% speed reduction

### Historical Comparison
- **COVID-19 (Original)**: R₀ ≈ 2.5, moderate spread
- **COVID-19 (Delta)**: R₀ ≈ 5-8, faster spread
- **Spanish Flu (1918)**: R₀ ≈ 2-3, shorter duration
- **Measles**: R₀ ≈ 12-18, highly contagious
- **Ebola (2014)**: R₀ ≈ 1.5-2.5, low transmission

## Git Workflow

### Current Branch
```bash
git checkout claude/update-epidemic-sim3-011CUnSd6Douv1cnUvoKPu8J
```

### Typical Workflow
```bash
# Make changes to code
git add epidemic_sim3.py
git commit -m "Description of changes"
git push -u origin claude/update-epidemic-sim3-011CUnSd6Douv1cnUvoKPu8J
```

### Retry Logic for Network Issues
If push/fetch fails, retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s).

## Dependencies

```txt
PyQt5>=5.15.0      # GUI framework
pyqtgraph>=0.12.0  # Real-time plotting
numpy>=1.20.0      # Numerical operations
```

## Contact & Support

For issues with the simulation:
1. Check this claude.md for context
2. Review recent commits in git log
3. Test with different presets to isolate issues
4. Check console logs (simulation prints status messages)

## Quick Reference: Important Line Numbers

- **SimParams**: Lines 19-47
- **PRESETS Dictionary**: Lines 51-111
- **Particle Class**: Lines 114-163
- **EpidemicSim.__init__**: Lines 167-209
- **Infection Logic**: Lines 289-337
- **Quarantine Logic**: Lines 382-422
- **UI Setup**: Lines 609-730
- **Preset Loading**: Lines 853-873
- **Graph Rendering**: Lines 928-961

---

**Last Updated**: 2025-11-04
**Session ID**: 011CUnSd6Douv1cnUvoKPu8J
**Status**: All features implemented and working ✅
