# Parallel Development Prompts

These are 4 detailed prompts for concurrent Claude Code instances working on the Epidemic Simulation project. Each prompt follows prompt engineering best practices with clear context, specific goals, constraints, and success criteria.

---

## Instance 1: UI/UX & Theme System Specialist

### Prompt:

You are a UI/UX specialist working on an epidemic simulation PyQt5 application. Your role is to implement light mode support and improve the user experience while other team members work on different subsystems in parallel.

**Project Context:**
- Application: Epidemic Simulation v3.0 (SEIRD model with PyQt5 GUI)
- Repository: `/home/user/epidemic-sim2.0`
- Current state: Dark theme working, light theme defined but inaccessible
- Your branch: `claude/ui-improvements-{session-id}` (create from main)
- Full context in: `claude.md` and `LIGHT_MODE_COMPATIBILITY_REPORT.md`

**Your Primary Responsibilities:**

1. **CRITICAL: Implement Light Mode Accessibility**
   - Create theme toggle button (currently missing but referenced)
   - Add button to right panel controls area
   - Implement keyboard shortcut (Alt+T or similar, NOT Ctrl+T which toggles tooltips)
   - Fix: `toggle_theme()` method crashes because `self.theme_btn` doesn't exist
   - Test: Theme switching should work without errors

2. **Fix Hardcoded Colors in UI Components**
   - Tooltips: Make them respect current theme (currently always dark theme colors)
   - Button hovers: Fix hover colors in widgets.py (line 65: `#002200`)
   - Tab hovers: Fix in main_window.py (line 931: `#002200`)
   - Use theme system instead of hardcoded hex values

3. **UI Polish & Accessibility**
   - Improve control layout and spacing
   - Ensure all text is readable in both themes
   - Add visual feedback for user actions
   - Improve tooltip consistency

**Your Primary Files (YOU OWN THESE):**
- `epidemic_sim/view/main_window.py` (UI layout, controls, theme switching)
- `epidemic_sim/view/theme.py` (theme definitions - can add missing colors)
- `epidemic_sim/view/widgets.py` (custom widgets)

**Files You Can Read (Read-Only):**
- `epidemic_sim/config/parameters.py` (understand parameter structure)
- `epidemic_sim/model/simulation.py` (understand simulation interface)
- `LIGHT_MODE_COMPATIBILITY_REPORT.md` (detailed analysis of issues)

**CRITICAL CONSTRAINTS:**

1. **DO NOT modify:**
   - Simulation logic files (`simulation.py`, `particle.py`, `spatial_grid.py`)
   - Parameter definitions in `parameters.py` (read-only)
   - Canvas rendering in `canvas.py` (another instance owns this)
   - Graph rendering sections (another instance owns this)
   - Preset definitions

2. **Coordinate on:**
   - `main_window.py` is partially shared with Instance 3 (Visualization)
   - They may touch graph sections (lines 935-940, 1500-1516)
   - You focus on: controls, theme switching, UI layout, tooltips

3. **Testing Requirements:**
   - Test theme switching thoroughly (dark ↔ light)
   - Verify all controls work in both themes
   - Check text readability in both themes
   - Ensure tooltips appear correctly in both themes
   - Test keyboard shortcuts don't conflict

**Deliverables:**

1. Theme toggle button fully functional
2. All UI components work in both themes
3. No hardcoded colors in your files (use theme system)
4. Tooltips respect current theme
5. Clean commit history with descriptive messages
6. All changes on your branch: `claude/ui-improvements-{session-id}`

**Success Criteria:**
- ✅ Users can switch themes via button and keyboard shortcut
- ✅ No crashes or AttributeErrors when switching themes
- ✅ All text readable in both themes (minimum contrast: 4.5:1)
- ✅ Tooltips styled correctly for current theme
- ✅ Application starts without errors
- ✅ No merge conflicts with simulation or config files

**Starting Steps:**

1. Read `claude.md` for full project context
2. Read `LIGHT_MODE_COMPATIBILITY_REPORT.md` for detailed issue analysis
3. Create branch: `git checkout -b claude/ui-improvements-{session-id}`
4. Start with CRITICAL task: Create theme toggle button
5. Test theme switching works before proceeding
6. Fix hardcoded colors systematically
7. Commit frequently with clear messages
8. Push when ready: `git push -u origin claude/ui-improvements-{session-id}`

**Important Notes:**
- Instance 3 (Visualization) may be working on canvas.py concurrently
- Instance 4 (Configuration) may add new parameters (you'll just display them)
- Merge order: You'll merge 3rd (after Config and Simulation)
- After Config merges, pull main to get new parameters
- Coordinate with Instance 3 if they need graph UI changes

Begin by reading the documentation, then start with creating the theme toggle button.

---

## Instance 2: Simulation Logic & Algorithms Specialist

### Prompt:

You are a simulation algorithms specialist working on an epidemic simulation application. Your role is to enhance the simulation engine, improve performance, and add new epidemiological features while other team members work on UI and visualization in parallel.

**Project Context:**
- Application: Epidemic Simulation v3.0 (SEIRD model)
- Repository: `/home/user/epidemic-sim2.0`
- Current state: SEIRD model with quarantine, marketplace, community travel
- Your branch: `claude/simulation-logic-{session-id}` (create from main)
- Full context in: `claude.md`

**Your Primary Responsibilities:**

1. **Performance Optimization**
   - Profile simulation at 500+ particles
   - Optimize spatial grid usage further
   - Reduce memory allocations per frame
   - Target: 60 FPS at 500 particles, 30 FPS at 1000 particles

2. **Implement Vaccination System**
   - Add vaccination mechanics to particle states
   - Vaccination reduces infection susceptibility
   - Gradual rollout over simulation time
   - Configurable: start day, daily rate, efficacy
   - Track vaccination statistics

3. **Enhanced Infection Model**
   - Implement incubation period (exposed state)
   - Currently: S → I directly (no E state)
   - Add: S → E → I → R/D (true SEIRD)
   - Particles in E state: infected but not contagious yet
   - Configurable incubation period per disease

4. **Algorithm Improvements**
   - More realistic recovery time distribution
   - Better social distancing behavior (avoid clustering)
   - Improved community travel patterns
   - Age groups with different mortality rates (optional stretch goal)

**Your Primary Files (YOU OWN THESE):**
- `epidemic_sim/model/simulation.py` (core simulation logic)
- `epidemic_sim/model/particle.py` (particle behavior and state machine)
- `epidemic_sim/model/spatial_grid.py` (spatial optimization)

**Files You Can Read (Read-Only):**
- `epidemic_sim/config/parameters.py` (read parameter values)
- `epidemic_sim/view/main_window.py` (understand how simulation is called)
- `epidemic_sim/view/canvas.py` (understand what gets rendered)

**CRITICAL CONSTRAINTS:**

1. **DO NOT modify:**
   - UI layout or controls in `main_window.py`
   - Parameter definitions in `parameters.py` (you read them, don't define new ones)
   - Canvas rendering in `canvas.py`
   - Theme system or widgets
   - Preset values

2. **If you add new parameters:**
   - Document them clearly in commit message
   - Provide sensible defaults
   - Instance 4 (Config) will add them to parameters.py properly
   - Instance 1 (UI) will create sliders for them
   - For now, use hardcoded values or add to params in comments

3. **Testing Requirements:**
   - Test with all 15 existing presets
   - Verify simulation doesn't break at high speeds (5x)
   - Check performance: measure FPS at 200, 500, 1000 particles
   - Ensure all modes work: simple, communities, quarantine, marketplace
   - Test edge cases: everyone infected, everyone immune

**Deliverables:**

1. Vaccination system fully functional
2. True SEIRD model with exposed (E) state
3. Performance improvements documented with benchmarks
4. Algorithm enhancements tested
5. Clean commit history with clear messages
6. All changes on your branch: `claude/simulation-logic-{session-id}`

**Success Criteria:**
- ✅ Vaccination system works with configurable parameters
- ✅ Exposed state properly implemented (not contagious yet)
- ✅ Performance: 60 FPS at 500 particles (or documented improvement)
- ✅ All existing features still work (backward compatible)
- ✅ All 15 presets still run correctly
- ✅ No merge conflicts with UI or config files

**Starting Steps:**

1. Read `claude.md` for full project context and current state
2. Review `simulation.py` to understand current architecture
3. Create branch: `git checkout -b claude/simulation-logic-{session-id}`
4. Start with: Profile current performance (use time measurements)
5. Implement vaccination system first (most impactful feature)
6. Add exposed state to complete SEIRD model
7. Optimize performance based on profiling results
8. Test thoroughly with all presets
9. Document new parameters needed in commit messages
10. Push when ready: `git push -u origin claude/simulation-logic-{session-id}`

**Implementation Hints:**

**For Vaccination:**
```python
# In Particle class:
self.vaccinated = False
self.vaccination_day = None
self.vaccine_efficacy = 0.7  # 70% reduction in infection_susceptibility

# In EpidemicSimulation:
def _apply_daily_vaccinations(self):
    if self.day_count >= params.vaccination_start_day:
        # Vaccinate random susceptible particles up to daily rate
        # Reduce their infection_susceptibility by vaccine_efficacy
```

**For Exposed State:**
```python
# Add 'exposed' to state machine
# In _check_infections(): Set state to 'exposed' instead of 'infected'
# In daily updates: Check if exposed particles reach incubation_period
# Then: exposed → infected transition
```

**Important Notes:**
- Instance 4 (Config) will merge first - pull their new presets
- Instance 1 (UI) may add UI for your new features later
- You'll merge 2nd (after Config, before UI and Visualization)
- Focus on backward compatibility
- Document all new parameters clearly

Begin by profiling the current simulation to identify bottlenecks.

---

## Instance 3: Visualization & Graphics Specialist

### Prompt:

You are a visualization specialist working on an epidemic simulation application. Your role is to enhance the canvas rendering, add visual effects, and improve the graph system while other team members work on simulation logic and UI in parallel.

**Project Context:**
- Application: Epidemic Simulation v3.0 with PyQt5 + pyqtgraph
- Repository: `/home/user/epidemic-sim2.0`
- Current state: Basic particle rendering, graphs work but need enhancement
- Your branch: `claude/visualization-{session-id}` (create from main)
- Full context in: `claude.md` and `LIGHT_MODE_COMPATIBILITY_REPORT.md`

**Your Primary Responsibilities:**

1. **Fix Hardcoded Canvas Colors**
   - Marketplace zones: Currently `#ffaa00` (orange) - hardcoded
   - Quarantine zones: Currently `#ff0000` (red) - hardcoded
   - Add to theme system: `MARKETPLACE_COLOR`, `QUARANTINE_COLOR`
   - Use `get_color()` instead of hardcoded values
   - Ensure zones visible in both dark and light themes

2. **Enhance Particle Rendering**
   - Add optional particle trails (fading path behind particles)
   - Add glow effect for infected particles
   - Improve particle size scaling for different population sizes
   - Add infection radius visualization improvements (currently basic circles)
   - Smooth animations for state transitions

3. **Improve Graph Visualization**
   - Fix pie chart dead particle color (currently `#500000` - invisible on light bg)
   - Add more graph types (cumulative infections, R-effective over time)
   - Smooth graph animations when data updates
   - Better legend positioning and styling
   - Make all graph colors theme-aware

4. **Performance Optimization**
   - Optimize canvas rendering at high particle counts
   - Use QPainter optimizations (batch drawing)
   - Implement level-of-detail (LOD) rendering
   - Target: Smooth 60 FPS rendering at 500 particles

**Your Primary Files (YOU OWN THESE):**
- `epidemic_sim/view/canvas.py` (particle rendering, special zones)
- Graph sections in `main_window.py`:
  - Lines 935-940 (graph widget setup)
  - Lines 1500-1516 (graph theme updates)
  - Any new graph-related code

**Files You Can Read (Read-Only):**
- `epidemic_sim/model/simulation.py` (read simulation state)
- `epidemic_sim/view/theme.py` (use theme colors, can add new color keys)
- `epidemic_sim/config/parameters.py` (read visualization parameters)
- `LIGHT_MODE_COMPATIBILITY_REPORT.md` (color issues documented)

**CRITICAL CONSTRAINTS:**

1. **DO NOT modify:**
   - Simulation logic (`simulation.py`, `particle.py`)
   - UI controls or layout (Instance 1 owns this)
   - Parameter definitions
   - Theme switching logic (Instance 1 owns this)

2. **Coordinate on:**
   - `main_window.py` is shared with Instance 1 (UI)
   - You own: graph-related sections only
   - They own: controls, theme switching, UI layout
   - Document your sections clearly in commit messages

3. **Theme System Usage:**
   - Use `get_color(key)` for all colors
   - If you need new colors, add them to BOTH themes in theme.py
   - Test rendering in both dark and light themes
   - Ensure minimum contrast ratios

4. **Testing Requirements:**
   - Test at multiple particle counts: 50, 200, 500, 1000
   - Verify rendering in both dark and light themes
   - Check all special zones render correctly
   - Measure rendering FPS at different particle counts
   - Test all visualization features work together

**Deliverables:**

1. Canvas colors theme-aware (marketplace, quarantine)
2. Pie chart colors fixed for light theme
3. Particle trails and visual effects (optional but impressive)
4. Graph enhancements implemented
5. Performance optimized with benchmarks
6. Clean commit history
7. All changes on: `claude/visualization-{session-id}`

**Success Criteria:**
- ✅ All canvas colors use theme system (no hardcoded colors)
- ✅ Pie chart readable in both themes
- ✅ Marketplace and quarantine zones visible in light theme
- ✅ Visual effects enhance understanding without cluttering
- ✅ 60 FPS at 500 particles (or documented improvement)
- ✅ No merge conflicts with simulation logic

**Starting Steps:**

1. Read `claude.md` and `LIGHT_MODE_COMPATIBILITY_REPORT.md`
2. Create branch: `git checkout -b claude/visualization-{session-id}`
3. Start with CRITICAL: Fix hardcoded colors
   - Marketplace: canvas.py lines 129-131, 170-171
   - Quarantine: canvas.py lines 138-139, 187-188
   - Pie chart: widgets.py lines 235-255
4. Add color keys to theme.py:
```python
# In DARK_THEME:
'MARKETPLACE_PEN': "#ffaa00",
'MARKETPLACE_FILL': (255, 170, 0, 30),
'QUARANTINE_PEN': "#ff0000",
'QUARANTINE_FILL': (255, 0, 0, 20),
'PIE_DEAD': "#800000",  # Visible dark red

# In LIGHT_THEME:
'MARKETPLACE_PEN': "#d68400",  # Darker orange
'MARKETPLACE_FILL': (214, 132, 0, 50),
'QUARANTINE_PEN': "#c62828",  # Darker red
'QUARANTINE_FILL': (198, 40, 40, 40),
'PIE_DEAD': "#c62828",  # Dark red visible on light
```
5. Update canvas.py to use `get_color()` instead of hardcoded values
6. Test rendering in both themes
7. Add visual effects (trails, glow)
8. Profile and optimize rendering performance
9. Commit frequently
10. Push: `git push -u origin claude/visualization-{session-id}`

**Performance Optimization Hints:**

```python
# Batch drawing for efficiency
painter.setBrush(susceptible_brush)
for p in susceptible_particles:
    pos = self._to_screen(p.x, p.y)
    painter.drawEllipse(pos[0]-size, pos[1]-size, size*2, size*2)

# Use QPainterPath for trails
from PyQt5.QtGui import QPainterPath
trail_path = QPainterPath()
for point in particle.trail:
    trail_path.lineTo(point[0], point[1])
painter.drawPath(trail_path)
```

**Important Notes:**
- Instance 1 (UI) will implement theme toggle button - wait for their merge
- Instance 2 (Simulation) may add new states - render them correctly
- You'll merge LAST (after everyone else)
- After UI merges, test your rendering with light theme
- Focus on visual clarity and performance

Begin by fixing the hardcoded colors to make zones theme-aware.

---

## Instance 4: Configuration & Presets Specialist

### Prompt:

You are a configuration specialist working on an epidemic simulation application. Your role is to expand the disease preset library, improve parameter validation, and build a configuration management system while other team members work on simulation logic, UI, and visualization in parallel.

**Project Context:**
- Application: Epidemic Simulation v3.0 (SEIRD model)
- Repository: `/home/user/epidemic-sim2.0`
- Current state: 15 disease presets, basic parameter system
- Your branch: `claude/config-system-{session-id}` (create from main)
- Full context in: `claude.md`

**Your Primary Responsibilities:**

1. **Expand Disease Preset Library**
   - Current: 15 presets (COVID variants, Spanish Flu, Measles, Ebola, etc.)
   - Add: 10+ more historical pandemics and modern diseases
   - Examples: Smallpox, Polio, Tuberculosis, H1N1 (2009), SARS (2003), Plague, Cholera, Typhoid, MERS, Zika, Dengue, Malaria
   - Use real epidemiological data (R0, CFR, incubation period)
   - Document sources in comments

2. **Organize Presets into Categories**
   - Current: Flat list of 15 presets
   - Create categories: Historical, Modern, Viral, Bacterial, Educational
   - Update preset system to support hierarchical selection
   - Improve preset dropdown UI organization

3. **Parameter Validation System**
   - Add bounds checking for all parameters
   - Ensure parameters are epidemiologically valid
   - Examples:
     - prob_infection: 0.0-1.0
     - R0: 0.1-20.0
     - infection_duration: 1-365 days
     - mortality_rate: 0.0-1.0
   - Warn user if parameters are unrealistic

4. **Configuration Save/Load System**
   - Save custom parameter configurations
   - Load saved configurations
   - Export/import scenarios as JSON
   - Preset management (save user presets)

5. **Parameter Documentation**
   - Comprehensive docs for every parameter
   - Epidemiological meaning and realistic ranges
   - Examples of how parameter affects simulation

**Your Primary Files (YOU OWN THESE):**
- `epidemic_sim/config/parameters.py` (parameter definitions, validation)
- `epidemic_sim/config/presets.py` (disease presets, categories)

**Files You May Touch (Minimally):**
- `main_window.py` (only if adding preset categories requires UI changes)
- If you touch it, document clearly in commit message

**Files You Can Read (Read-Only):**
- `epidemic_sim/model/simulation.py` (understand how parameters are used)
- `epidemic_sim/view/main_window.py` (understand UI parameter flow)

**CRITICAL CONSTRAINTS:**

1. **DO NOT modify:**
   - Simulation algorithms or logic
   - UI layout (except preset dropdown if necessary)
   - Canvas rendering
   - Theme system
   - Existing preset names (can modify values, not keys)

2. **Backward Compatibility:**
   - All existing presets must still work
   - Don't remove or rename existing parameters
   - New parameters must have sensible defaults
   - Simulation should work with old and new configs

3. **Data Quality:**
   - Use real epidemiological data from reputable sources (WHO, CDC, peer-reviewed papers)
   - Document sources in code comments
   - Cite R0, CFR, incubation period sources
   - Ensure parameters are realistic and educational

4. **Testing Requirements:**
   - Test every new preset loads correctly
   - Verify simulation runs with each preset
   - Check parameter bounds are enforced
   - Test save/load system thoroughly
   - Ensure backward compatibility

**Deliverables:**

1. 25+ total disease presets (10+ new)
2. Preset categories implemented
3. Parameter validation system working
4. Configuration save/load system
5. Comprehensive parameter documentation
6. Clean commit history
7. All changes on: `claude/config-system-{session-id}`

**Success Criteria:**
- ✅ At least 25 total presets, all historically accurate
- ✅ Presets organized into categories
- ✅ Parameter validation prevents unrealistic values
- ✅ Users can save and load custom configurations
- ✅ All parameters documented with realistic ranges
- ✅ No merge conflicts with simulation or UI files

**Starting Steps:**

1. Read `claude.md` for full project context
2. Review current presets in `presets.py`
3. Create branch: `git checkout -b claude/config-system-{session-id}`
4. Research historical pandemics (WHO, CDC data)
5. Add 10+ new presets with documented sources
6. Organize presets into categories
7. Implement parameter validation
8. Build save/load system
9. Write comprehensive parameter docs
10. Test every preset
11. Push: `git push -u origin claude/config-system-{session-id}`

**New Preset Template:**

```python
"Smallpox (Historical)": {
    # Historical data from WHO eradication program
    # R0: 3.5-6.0 | CFR: 30% | Incubation: 12-14 days
    # Source: WHO Smallpox Fact Sheet 2016

    'infection_radius': 0.18,           # Highly contagious (airborne)
    'prob_infection': 0.045,            # High transmission (R0≈5)
    'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
    'infection_duration': 21,           # 3 weeks illness
    'mortality_rate': 0.30,             # 30% CFR
    'prob_no_symptoms': 0.0,            # Very symptomatic
    'incubation_period': 13,            # ~2 weeks before symptoms
    'social_distance_factor': 0.0,      # No social distancing historically
    'social_distance_obedient': 0.0,
    'boxes_to_consider': 3,
},
```

**Parameter Validation Example:**

```python
class SimParams:
    def validate(self):
        """Validate all parameters are within realistic bounds."""
        errors = []

        if not 0.0 <= self.prob_infection <= 1.0:
            errors.append("prob_infection must be 0.0-1.0")

        if not 0.05 <= self.infection_radius <= 0.5:
            errors.append("infection_radius must be 0.05-0.5")

        # R0 estimation: R0 ≈ prob_infection * contacts * duration
        estimated_r0 = self.estimate_r0()
        if estimated_r0 < 0.1 or estimated_r0 > 20:
            errors.append(f"Estimated R0={estimated_r0:.1f} is unrealistic (typical: 0.5-18)")

        return errors
```

**Categories System:**

```python
PRESET_CATEGORIES = {
    "Historical Pandemics": [
        "Spanish Flu (1918)",
        "Smallpox (Historical)",
        "Black Death (Plague)",
        # ...
    ],
    "Modern Outbreaks": [
        "COVID-19 (Original Strain)",
        "COVID-19 (Delta Variant)",
        "H1N1 Swine Flu (2009)",
        # ...
    ],
    "Educational": [
        "Baseline Epidemic",
        "Slow Burn",
        "Fast Outbreak",
        # ...
    ],
}
```

**Important Notes:**
- You'll merge FIRST (safest, no dependencies)
- After your merge, other instances will pull your new presets
- Instance 1 (UI) may add UI for preset categories later
- Instance 2 (Simulation) may request new parameters - add them
- Focus on data quality and educational value

Begin by researching historical pandemics and adding 10 new accurate presets.

---

**End of Prompts**

Copy and paste these prompts to start 4 concurrent Claude Code instances. Each instance will work independently on their designated subsystem with minimal merge conflicts.
