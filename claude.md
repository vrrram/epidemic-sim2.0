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

## Planned Future Implementations

### Priority Features

#### 1. UI/UX Improvements
- **Keyboard Usability**: Add keyboard shortcuts for common actions
  - Space: Pause/Resume simulation
  - R: Reset simulation
  - 1-9: Quick preset selection
  - Arrow keys: Adjust parameters
- **Improved Layout**: Better organization of controls and displays
- **Responsive Design**: Better handling of window resizing

#### 2. Graph Display Enhancements
- **Fix Current Graph Issues**: Address any rendering or performance issues
- **Add Pie Chart**: Real-time pie chart showing current population distribution
  - Susceptible (cyan)
  - Infected - Symptomatic (red)
  - Infected - Asymptomatic (orange)
  - Removed (gray)
- **Graph Toggle**: Option to show/hide different visualizations

#### 3. Log Window Removal
- **Remove Console Log**: The current log window doesn't provide useful real-time info
- **Replace with**: More informative stats display or status bar
- **Keep Critical Info**: Show important events (peak infections, quarantine start) in status bar

#### 4. Quarantine Checkbox System
- **Make Quarantine Optional**: Convert from mode-based to checkbox toggle
- **Works in All Modes**: Enable quarantine in simple, community, or any mode
- **Benefits**:
  - Test quarantine effectiveness in different scenarios
  - Compare runs with/without quarantine
  - More flexible experimentation

#### 5. Marketplace Feature
- **Marketplace Checkbox**: Toggle marketplace gathering behavior
- **Behavior**:
  - Particles travel to central location every few days (configurable interval)
  - Creates superspreader events
  - Simulates markets, churches, schools, etc.
- **Parameters to Add**:
  - `marketplace_enabled`: Boolean toggle
  - `marketplace_interval`: Days between gatherings (e.g., 7 for weekly)
  - `marketplace_duration`: Hours particles stay at marketplace
  - `marketplace_attendance`: Fraction of population that attends
  - `marketplace_location`: Coordinates for gathering point
- **Implementation Notes**:
  - Can have multiple marketplace locations for community mode
  - Particles return to original location after marketplace
  - Creates realistic infection hotspots

### Implementation Order (Suggested)

1. **Phase 1** (Quick wins):
   - Remove log window
   - Add quarantine checkbox
   - Basic keyboard shortcuts

2. **Phase 2** (Enhanced visualization):
   - Fix graph display issues
   - Add pie chart
   - Improve UI layout

3. **Phase 3** (New mechanics):
   - Implement marketplace feature
   - Add marketplace parameters
   - Test with various presets

### Technical Considerations

- **Marketplace Implementation**: Store original positions, move particles to marketplace location, return after duration
- **Quarantine Checkbox**: Decouple quarantine logic from mode selection
- **Pie Chart**: Use `matplotlib` or `pyqtgraph` pie chart widget
- **Keyboard Shortcuts**: Use PyQt5 `QShortcut` or `keyPressEvent` overrides

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

## Newly Implemented Features (Session: 011CUni2yWfK1jg17LEpZqhC)

### Phase 1: UI/UX Quick Wins ✅

**1. Status Bar Replacement**
- Removed verbose log window that cluttered the UI
- Added concise status bar showing only important events
- Filters messages for: INITIALIZING, PATIENT ZERO, PRESET, QUARANTINE, SPEED
- Cleaner, more professional interface

**2. Quarantine Checkbox System**
- Decoupled quarantine from simulation mode
- Added "ENABLE QUARANTINE" checkbox in interventions panel
- Works in all modes (simple, quarantine, communities)
- More flexible experimentation and comparison
- Keyboard shortcut: Q

**3. Keyboard Shortcuts**
- SPACE: Pause/Resume simulation
- R: Reset simulation
- Q: Toggle quarantine
- M: Toggle marketplace
- 1-9: Quick preset selection (loads first 9 presets)
- Added keyboard shortcuts reference panel for user guidance

### Phase 2: Enhanced Visualization ✅

**4. Real-Time Pie Chart**
- Added matplotlib dependency
- Implemented pie chart widget showing current population distribution
- Categories:
  - Susceptible (cyan)
  - Infected Symptomatic (red)
  - Infected Asymptomatic (orange)
  - Removed (gray)
- Tabbed interface: "TIME SERIES" and "PIE CHART" views
- Updates in real-time with simulation

**5. Improved UI Layout**
- Increased window size to 1800x1000 for better visibility
- Optimized canvas size to 900x900
- Better spacing and margins in right panel (8px spacing)
- Right panel width: 500-550px with optimized organization
- Slider area: 280-320px height for better fit
- Professional, organized appearance

### Phase 3: Marketplace Feature ✅

**6. Marketplace Gathering Mechanics**
- Simulates superspreader events (markets, churches, schools, etc.)
- Configurable parameters:
  - `marketplace_enabled`: Toggle on/off
  - `marketplace_interval`: Days between gatherings (default: 7)
  - `marketplace_duration`: Time steps particles stay (default: 2)
  - `marketplace_attendance`: Fraction attending (default: 0.6)
  - `marketplace_x`, `marketplace_y`: Location coordinates (default: 0, 0)

**7. Marketplace Implementation**
- Particles track original home positions
- On marketplace day, attending particles gather at central location
- After duration, particles return to home positions
- Visual indicator: Orange dashed circle shows marketplace zone
- Status messages log attendance numbers
- Creates realistic infection hotspots and transmission clusters

**8. Marketplace UI Controls**
- "ENABLE MARKETPLACE GATHERINGS" checkbox
- Interval spinbox (1-30 days range)
- Attendance spinbox (0.1-1.0 range, 10% steps)
- Styled spinboxes matching neon green theme
- Keyboard shortcut: M

### Technical Improvements

**Code Quality**
- Clean separation of concerns
- Atomic commits for each feature
- Comprehensive inline documentation
- Maintainable parameter structure

**UI/UX Enhancements**
- Consistent neon green theme throughout
- Styled all new widgets (checkboxes, spinboxes, tabs)
- Intuitive keyboard shortcuts
- Clear visual feedback for marketplace zones
- Professional tabbed visualization interface

**Performance**
- Efficient marketplace tracking (O(n) per day)
- Minimal overhead from new features
- Real-time pie chart updates without lag

### Updated Dependencies

```txt
PyQt5>=5.15.0
pyqtgraph>=0.12.0
numpy>=1.20.0
matplotlib>=3.3.0  # NEW: For pie chart visualization
```

### Updated Keyboard Shortcuts

```
SPACE  - Pause/Resume simulation
R      - Reset simulation
Q      - Toggle quarantine on/off
M      - Toggle marketplace gatherings on/off
1-9    - Load preset 1-9 (quick access)
```

### Files Modified

- `epidemic_sim3.py`: Main simulation (+300 lines)
  - Added Phase 1: Status bar, quarantine checkbox, keyboard shortcuts
  - Added Phase 2: Pie chart widget, tabbed interface, layout improvements
  - Added Phase 3: Marketplace parameters, gathering logic, UI controls
- `requirements.txt`: Added matplotlib>=3.3.0
- `claude.md`: This file, updated with implementation details

### Testing Recommendations

1. **Quarantine Feature**: Enable in simple mode, verify particles move to red box
2. **Marketplace Feature**: Enable with 7-day interval, 60% attendance, observe gatherings
3. **Keyboard Shortcuts**: Test all shortcuts (Space, R, Q, M, 1-9)
4. **Pie Chart**: Switch between time series and pie chart tabs
5. **Combined**: Enable both quarantine + marketplace for complex scenarios

### Known Limitations

- Marketplace only works in simple/quarantine modes (not communities mode yet)
- Pie chart asymptomatic split is approximation based on prob_no_symptoms
- Marketplace particles don't avoid quarantine while traveling (design choice)

---

**Last Updated**: 2025-11-04
**Session ID**: 011CUni2yWfK1jg17LEpZqhC
**Status**: All planned features implemented and working ✅
**Commits**: 3 atomic commits (Phase 1, 2, and 3)
