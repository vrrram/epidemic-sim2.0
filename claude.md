# Claude Code - Epidemic Simulation Project Guide

## Project Overview

**Epidemic Simulation v3.0** - Interactive SEIRD (Susceptible-Exposed-Infected-Removed-Dead) epidemic simulation with PyQt5 GUI, featuring community grids, quarantine mechanics, marketplace gatherings, and real-time visualization.

---

## Parallel Development Strategy

### Overview

This project is designed to support **4 concurrent Claude Code instances** working in parallel with minimal merge conflicts. Each instance focuses on a distinct subsystem with minimal file overlap.

### Branch Strategy

**Main Branch:** `main`
- Production-ready code
- All features fully tested and integrated

**Development Branches:**
- `claude/ui-improvements-{session-id}` - Instance 1: UI/UX work
- `claude/simulation-logic-{session-id}` - Instance 2: Simulation algorithms
- `claude/visualization-{session-id}` - Instance 3: Graphics and rendering
- `claude/config-system-{session-id}` - Instance 4: Configuration and presets

**Integration Strategy:**
1. Each instance works on its designated branch
2. Merge to main sequentially (not all at once)
3. After each merge, other instances rebase on latest main
4. Test after each merge to catch integration issues early

---

## Instance Assignments

### Instance 1: UI/UX & Theme System
**Primary Files:**
- `epidemic_sim/view/main_window.py` (UI layout, controls, theme switching)
- `epidemic_sim/view/theme.py` (theme definitions)
- `epidemic_sim/view/widgets.py` (custom widgets)

**Secondary Files (Read-Only):**
- `epidemic_sim/config/parameters.py` (read parameter structure)
- `epidemic_sim/model/simulation.py` (understand simulation interface)

**Responsibilities:**
- Light mode implementation
- Theme toggle button and keyboard shortcuts
- Tooltip improvements
- UI polish and accessibility
- Control panel layout optimization
- User experience enhancements

**Merge Conflict Risk:** 🟢 LOW (isolated UI files)

---

### Instance 2: Simulation Logic & Algorithms
**Primary Files:**
- `epidemic_sim/model/simulation.py` (core simulation logic)
- `epidemic_sim/model/particle.py` (particle behavior)
- `epidemic_sim/model/spatial_grid.py` (spatial optimization)

**Secondary Files (Read-Only):**
- `epidemic_sim/config/parameters.py` (read parameters)
- `epidemic_sim/view/main_window.py` (understand UI interface)

**Responsibilities:**
- Performance optimizations
- New simulation features (e.g., vaccination)
- Algorithm improvements
- State machine enhancements
- Physics simulation refinements
- Infection spread modeling

**Merge Conflict Risk:** 🟢 LOW (isolated model files)

---

### Instance 3: Visualization & Graphics
**Primary Files:**
- `epidemic_sim/view/canvas.py` (particle rendering, zones)
- Graph rendering sections in `main_window.py` (lines 935-940, 1500-1516)

**Secondary Files (Read-Only):**
- `epidemic_sim/model/simulation.py` (read simulation state)
- `epidemic_sim/view/theme.py` (use theme colors)
- `epidemic_sim/config/parameters.py` (read visualization parameters)

**Responsibilities:**
- Canvas rendering improvements
- Visual effects (trails, glow, animations)
- Graph enhancements
- Color palette improvements
- Special zone visualization (marketplace, quarantine)
- Performance optimization for rendering

**Merge Conflict Risk:** 🟡 MEDIUM (canvas.py isolated, but graph code in main_window.py)

---

### Instance 4: Configuration & Presets
**Primary Files:**
- `epidemic_sim/config/parameters.py` (parameter definitions)
- `epidemic_sim/config/presets.py` (disease presets)

**Secondary Files (Minimal Touch):**
- Parameter control creation in `main_window.py` (lines 180-400) - May add new sliders

**Responsibilities:**
- More disease presets (historical pandemics)
- Parameter validation and bounds checking
- Configuration save/load system
- Preset categories and organization
- Parameter documentation
- Default value optimization

**Merge Conflict Risk:** 🟢 LOW (isolated config files)

---

## Merge Order Strategy

**Recommended merge sequence** (lowest to highest conflict risk):

1. **Instance 4** (Configuration) → Merge first
   - Only touches config files
   - Other instances can pull new presets/parameters

2. **Instance 2** (Simulation Logic) → Merge second
   - Core logic changes
   - Others can test with new simulation features

3. **Instance 1** (UI/UX) → Merge third
   - UI changes rarely conflict with visualization
   - Can adapt to new parameters from Instance 4

4. **Instance 3** (Visualization) → Merge last
   - May need to adapt to UI changes
   - Can use new theme system from Instance 1

**After each merge:**
```bash
# Other instances should rebase:
git fetch origin main
git rebase origin/main
# Resolve any conflicts
# Test to ensure integration works
```

---

## File Conflict Matrix

| File | Instance 1 | Instance 2 | Instance 3 | Instance 4 | Conflict Risk |
|------|------------|------------|------------|------------|---------------|
| `main_window.py` | ✍️ WRITE | 👁️ READ | ⚠️ TOUCH (graphs) | ⚠️ TOUCH (controls) | 🟡 MEDIUM |
| `simulation.py` | 👁️ READ | ✍️ WRITE | 👁️ READ | 👁️ READ | 🟢 LOW |
| `canvas.py` | 👁️ READ | - | ✍️ WRITE | 👁️ READ | 🟢 LOW |
| `theme.py` | ✍️ WRITE | - | 👁️ READ | - | 🟢 LOW |
| `widgets.py` | ✍️ WRITE | - | 👁️ READ | - | 🟢 LOW |
| `particle.py` | - | ✍️ WRITE | 👁️ READ | - | 🟢 LOW |
| `spatial_grid.py` | - | ✍️ WRITE | - | - | 🟢 LOW |
| `parameters.py` | 👁️ READ | 👁️ READ | 👁️ READ | ✍️ WRITE | 🟢 LOW |
| `presets.py` | 👁️ READ | 👁️ READ | 👁️ READ | ✍️ WRITE | 🟢 LOW |

**Legend:**
- ✍️ WRITE: Primary owner, makes major changes
- ⚠️ TOUCH: May make minor changes in specific sections
- 👁️ READ: Read-only access
- `-`: No interaction

---

## Conflict Prevention Guidelines

### For All Instances:

1. **Commit frequently** with clear messages
2. **Pull and rebase** from main before starting new features
3. **Test thoroughly** before pushing
4. **Document changes** in commit messages
5. **Communicate** if you need to touch shared files

### For Instance 1 (UI/UX):
- Don't modify simulation logic
- Don't change parameter definitions
- Use existing theme system APIs
- Test with default parameters

### For Instance 2 (Simulation):
- Don't modify UI layout or controls
- Don't change parameter definitions (read-only)
- Use existing visualization interface
- Don't change rendering code

### For Instance 3 (Visualization):
- Coordinate graph changes in main_window.py
- Use theme system colors (don't define new themes)
- Don't modify simulation logic
- Test with existing presets

### For Instance 4 (Configuration):
- Don't modify UI controls (can add new ones if needed)
- Don't change simulation algorithms
- Ensure backward compatibility
- Document all parameter changes

---

## Integration Testing Checklist

After each merge, run these tests:

- [ ] Application starts without errors
- [ ] All presets load correctly
- [ ] Simulation runs at all speeds (0.5x - 5x)
- [ ] Both modes work (simple + communities)
- [ ] Quarantine mode functions
- [ ] Marketplace mode functions
- [ ] Theme switching works (if Instance 1 merged)
- [ ] All graphs render correctly
- [ ] All controls respond properly
- [ ] No console errors or warnings
- [ ] Performance acceptable (>30 FPS with 200 particles)

---

## Communication Protocol

When you need to touch a file owned by another instance:

1. **Check the File Conflict Matrix** above
2. **Minimize changes** to shared sections
3. **Document clearly** in commit message
4. **Test integration** with other systems

Example commit message for touching shared file:
```
feat: Add vaccination parameter controls

TOUCHES SHARED FILE: main_window.py (Instance 1's primary file)
- Added vaccination sliders in parameter section (lines 350-365)
- No changes to existing UI layout or theme system
- Tested with all presets

Coordination needed with Instance 1 for UI polish.
```

---

## Current State (as of 2025-11-13)

### Completed Work:
- ✅ Death implementation (SEIRD model)
- ✅ Mortality rate system
- ✅ Real disease presets (15 presets)
- ✅ Marketplace trickle behavior
- ✅ Infection logic fixes (per-step checking)
- ✅ Performance optimization (spatial grid reuse)
- ✅ Quarantine travel cancellation fixes
- ✅ Tooltip system fixes
- ✅ Light mode compatibility analysis

### Known Issues:
- 🔴 Light mode inaccessible (no toggle button)
- ⚠️ Hardcoded colors in canvas special zones
- ⚠️ Pie chart dead color invisible on light backgrounds
- ⚠️ Tooltips don't respect theme

### Ready for Parallel Development:
- ✅ Stable main branch
- ✅ Clear subsystem boundaries
- ✅ Comprehensive documentation
- ✅ Test suite for logic fixes

---

## Quick Reference

### Repository Structure
```
epidemic-sim2.0/
├── epidemic_sim/
│   ├── model/           # Instance 2 - Simulation Logic
│   │   ├── simulation.py
│   │   ├── particle.py
│   │   └── spatial_grid.py
│   ├── view/            # Instance 1 & 3 - UI & Visualization
│   │   ├── main_window.py  (Shared - coordinate!)
│   │   ├── canvas.py       (Instance 3)
│   │   ├── theme.py        (Instance 1)
│   │   └── widgets.py      (Instance 1)
│   └── config/          # Instance 4 - Configuration
│       ├── parameters.py
│       └── presets.py
└── epidemic_sim3.py     # Main entry point (don't modify)
```

### Running Tests
```bash
# Import test
python3 -c "from epidemic_sim.model.simulation import EpidemicSimulation; print('✓ Import success')"

# Simulation test
python3 -c "from epidemic_sim.model.simulation import EpidemicSimulation; sim = EpidemicSimulation('simple'); sim.initialize(); sim.step(); print('✓ Simulation works')"

# Full application test
python3 epidemic_sim3.py
```

### Key Contacts (File Owners)
- **main_window.py**: Shared between Instance 1 and Instance 3 (coordinate!)
- **simulation.py**: Instance 2 (Simulation Logic)
- **canvas.py**: Instance 3 (Visualization)
- **parameters.py**: Instance 4 (Configuration)

---

## Version History

- **v3.0** (Current) - SEIRD model, death system, real disease presets
- **v2.5** - Community travel, marketplace mechanics
- **v2.0** - Quarantine system, multi-mode support
- **v1.0** - Basic SIR model simulation

---

**Last Updated:** 2025-11-13
**Maintained By:** Claude Code Parallel Development Team
