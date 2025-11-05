# EPIDEMIC SIMULATOR - PROJECT PLAN (REVISED)
## Focus: Application Quality First, Documentation Second

---

## CURRENT STATUS ANALYSIS

### ✅ Already Fulfilled Requirements

**Functional:**
- ✓ Time-dependent simulation (day/hour cycle)
- ✓ 11+ input parameters (exceeds requirement of 7)
- ✓ 4 simulation speed levels (exceeds requirement of 3: 0.5x, 1x, 2x, 5x)
- ✓ Visual representation (time series graph, pie chart)
- ✓ Particle animation reflecting simulation
- ✓ GUI with PyQt5
- ✓ Cross-platform (Windows compatible)
- ✓ Three-panel collapsible layout
- ✓ Quarantine mechanics
- ✓ Marketplace gathering mechanics
- ✓ Community-based simulation
- ✓ Keyboard shortcuts
- ✓ Real-time statistics

**Non-functional:**
- ✓ Smooth animations for UX
- ✓ Collapsible panels for flexibility
- ✓ Real-time visual feedback
- ✓ Neon green consistent theme

---

## ❌ PRIORITY REQUIREMENTS

###  Priority 1: APPLICATION QUALITY (FOCUS AREA) 🚀

**1. Distribution Functions** ⚠️ CRITICAL REQUIREMENT
- Status: Only uniform distribution implemented
- Need: Normal (Gaussian) and Exponential distributions
- Impact: CRITICAL - explicit IHK requirement
- **HIGHEST PRIORITY**

**2. Light Mode Theme** 🎨 HIGH - LOOK & FEEL
- Status: Dark mode only
- Need: Light/Dark theme toggle with theme persistence
- Impact: Better visual experience, accessibility, professional appearance

**3. UI/UX Polish (ISO 9241-110)** 💎 HIGH - FEEL & BEHAVIOR
- Status: Basic UI implemented
- Need: Tooltips, help system, better feedback, polish
- Impact: Professional user experience

**4. Performance Optimization** ⚡ HIGH - PERFORMANCE
- Status: Good for small populations
- Need: Profile and optimize for 2000+ particles
- Impact: Smooth experience at all population levels

**5. Error Handling & Validation** 🛡️ HIGH - BEHAVIOR
- Status: Minimal error handling
- Need: Input validation, graceful degradation, user-friendly errors
- Impact: Professional behavior, stability

**6. Code Modularization** 🏗️ HIGH - MAINTAINABILITY
- Status: Monolithic 1856-line file
- Need: Modular architecture, separation of concerns
- Impact: Clean Code requirement, maintainability

### Priority 2: ENHANCED FEATURES 🎁

**7. Save/Load Functionality**
- Add ability to save and restore simulation states
- JSON format with full state preservation

**8. Export Features**
- Export graphs as PNG images
- Export data as CSV
- Export simulation parameters

**9. Tutorial Mode**
- Interactive first-run tutorial
- Contextual help system

**10. Unit Testing Suite**
- Comprehensive test coverage (>80%)
- pytest-based test suite

### Priority 3: DOCUMENTATION 📚
*(After app is polished)*

**11. German Project Documentation** (IHK Standard)
- 6+ page documentation
- **AFTER** app features are finalized

**12. Test Protocols**
- 2+ pages in Excel/PDF
- **AFTER** all testing complete

**13. User Manual** (German)
- Comprehensive end-user documentation
- **AFTER** app features are complete

### Deprioritized ⏸️

**14. Windows Executable (.exe)**
- User will handle with PyInstaller
- Not part of implementation

---

## 📋 REVISED IMPLEMENTATION PLAN

### Week 1-2: Core Quality Improvements

#### TICKET-001: Distribution Functions (2 days) ⚠️
**Files:** `epidemic_sim3.py`

**Implementation:**
```python
# Particle class additions
class Particle:
    def __init__(self, ...):
        # Normal distribution for infection susceptibility
        self.infection_susceptibility = np.random.normal(1.0, 0.2)
        self.infection_susceptibility = max(0.1, min(2.0, self.infection_susceptibility))

        # Exponential distribution for recovery time variation
        self.recovery_time_modifier = np.random.exponential(1.0)
        self.recovery_time_modifier = max(0.5, min(2.0, self.recovery_time_modifier))
```

**Changes:**
- Add numpy import
- Modify infection probability calculation to use susceptibility
- Modify recovery time to use time modifier
- Add comprehensive code comments documenting each distribution usage
- Test distributions statistically

**Deliverables:**
- 3 distributions implemented and documented
- Statistical tests showing correct distribution
- Code comments explaining mathematical justification

---

#### TICKET-007: Light Mode Theme (2 days) 🎨
**Files:** `ui/themes.py` (new), `epidemic_sim3.py`

**Implementation:**
```python
# themes.py
DARK_THEME = {
    'NEON_GREEN': "#00ff00",
    'DARK_GREEN': "#003300",
    'BG_BLACK': "#000000",
    'PANEL_BLACK': "#0a0a0a",
    'BORDER_GREEN': "#00aa00",
    'TEXT': "#00ff00",
    'CANVAS_BG': "#000000"
}

LIGHT_THEME = {
    'PRIMARY': "#2e7d32",      # Professional green
    'SECONDARY': "#66bb6a",    # Light green
    'BG_WHITE': "#ffffff",
    'PANEL_GRAY': "#f5f5f5",
    'BORDER_GRAY': "#bdbdbd",
    'TEXT': "#212121",
    'CANVAS_BG': "#fafafa"
}
```

**Changes:**
- Create theme system with easy switching
- Add theme toggle button (top-right corner)
- Update all stylesheets dynamically
- Persist theme preference with QSettings
- Ensure graphs readable in both themes
- Update particle colors for light mode

**Deliverables:**
- Light and Dark themes fully working
- Theme toggle button
- Theme persistence between sessions
- Professional appearance in both modes

---

#### TICKET-008: UI/UX Polish - ISO 9241-110 (3 days) 💎
**Files:** `epidemic_sim3.py`

**Implementation:**

**1. Tooltips Everywhere:**
```python
slider.setToolTip("""Infection Radius: How far infection can spread
Recommended: 0.10-0.20
Smaller = localized outbreaks
Larger = rapid spread""")
```

**2. Help System:**
- Add "?" button next to each parameter
- Click shows detailed explanation dialog
- Include recommendations and examples

**3. Status Feedback:**
- Loading indicators for heavy operations
- Success messages (non-intrusive)
- Clear error messages with solutions

**4. Input Validation:**
- Real-time validation with visual feedback
- Prevent invalid values
- Helpful error messages

**5. Keyboard Navigation:**
- Optimized tab order
- All functions keyboard accessible
- Keyboard shortcuts hint panel always visible

**6. Accessibility:**
- High contrast mode option
- Font size adjustment (+/- buttons)
- Screen reader friendly labels

**Deliverables:**
- Tooltips on ALL UI elements
- Help system implemented
- Validation with feedback
- ISO 9241-110 compliance checklist document

---

#### TICKET-011: Performance Optimization (2 days) ⚡
**Files:** `epidemic_sim3.py`

**Profiling:**
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run simulation for 100 days
for _ in range(100 * 24):
    sim.step()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**Optimization Targets:**
1. Graph update frequency (throttle based on FPS)
2. Particle list operations (use numpy where possible)
3. Memory allocation patterns
4. Spatial grid cell size optimization
5. Drawing optimization (batch rendering)

**Performance Goals:**
| Population | Target FPS | Target Memory |
|-----------|-----------|---------------|
| 50 | 60 | <100MB |
| 500 | 50 | <300MB |
| 2000 | 35 | <1GB |

**Deliverables:**
- Performance profiling report
- Optimizations implemented
- Performance goals met
- No functionality broken

---

### Week 3: Code Quality & Error Handling

#### TICKET-006: Code Modularization (3 days) 🏗️
**Goal:** Break 1856-line file into clean modular architecture

**New Structure:**
```
epidemic-sim2.0/
├── epidemic_sim.py              # Main entry point (50 lines)
├── config/
│   ├── __init__.py
│   ├── parameters.py            # SimParams class
│   └── presets.py               # PRESETS dictionary
├── models/
│   ├── __init__.py
│   ├── particle.py              # Particle class
│   ├── simulation.py            # EpidemicSimulation class
│   └── spatial_grid.py          # SpatialGrid class
├── ui/
│   ├── __init__.py
│   ├── main_window.py           # EpidemicApp class
│   ├── canvas.py                # SimulationCanvas class
│   ├── controls.py              # Control widgets
│   ├── parameters_panel.py      # Left panel
│   ├── charts.py                # PieChartWidget
│   ├── collapsible_box.py       # CollapsibleBox widget
│   └── themes.py                # Color themes (from TICKET-007)
├── utils/
│   ├── __init__.py
│   ├── distributions.py         # Random distribution helpers
│   └── constants.py             # Global constants
└── tests/
    ├── __init__.py
    ├── test_particle.py
    ├── test_simulation.py
    └── test_distributions.py
```

**Deliverables:**
- Each file < 300 lines
- Clear separation of concerns
- All imports working
- All functionality preserved
- Clean Code principles followed

---

#### TICKET-009: Comprehensive Error Handling (2 days) 🛡️
**Files:** All Python files

**Areas to Cover:**

**1. Parameter Validation:**
```python
def validate_params(self):
    if not 50 <= self.num_particles <= 2000:
        raise ValueError("Population must be between 50 and 2000")
    if not 0.0 <= self.mortality_rate <= 1.0:
        raise ValueError("Mortality rate must be 0-100%")
    # ... etc
```

**2. Simulation Safety:**
```python
try:
    self.sim.step()
except Exception as e:
    self.show_error_dialog(f"Simulation error: {e}")
    self.pause()
    logging.error(f"Simulation error: {e}", exc_info=True)
```

**3. Graceful Degradation:**
- If graph update fails → continue simulation
- If distribution generation fails → use fallback
- Never crash, always recover

**4. User-Friendly Messages:**
- Clear explanation
- Suggest fix if possible
- Log technical details for debugging

**Deliverables:**
- Try-catch blocks around all risky operations
- Input validation on all parameters
- User-friendly error dialogs
- Logging system implemented
- No unhandled exceptions

---

### Week 4: Enhanced Features

#### TICKET-012: Save/Load Functionality (2 days)
**Files:** `epidemic_sim3.py`, `utils/file_io.py`

**Implementation:**
```python
# Save format (JSON)
{
  "version": "3.0",
  "timestamp": "2024-12-06T10:30:00",
  "parameters": { ... },
  "day_count": 42,
  "particles": [ ... ],
  "stats": { ... }
}
```

**Features:**
- Save current state to .epidemic file
- Load previously saved state
- File dialog for save/load
- Recent files menu

**Deliverables:**
- Save button in UI
- Load button in UI
- Full state restoration
- Error handling for corrupted files

---

#### TICKET-013: Export Functionality (1 day)
**Files:** `epidemic_sim3.py`

**Features:**
- Export time series graph as PNG (high-res)
- Export pie chart as PNG (high-res)
- Export statistics as CSV
- Export all data button
- Configurable image resolution

**Deliverables:**
- Export buttons in UI
- High-resolution images (300 DPI)
- CSV format correct
- Sensible file naming

---

#### TICKET-014: Tutorial Mode (2 days)
**Files:** `ui/tutorial.py`, `epidemic_sim3.py`

**Tutorial Steps:**
1. Welcome screen
2. Explain simulation canvas
3. Explain parameters (with examples)
4. Show how to run simulation
5. Show how to interpret results
6. "Try it yourself" challenge

**Features:**
- Launches on first run
- Can be skipped
- Can be re-launched from menu
- German language
- Interactive (not just text)
- Highlights UI elements

**Deliverables:**
- Tutorial system implemented
- German translation
- Can be toggled from menu
- User-friendly and helpful

---

#### TICKET-010: Unit Testing Suite (2 days)
**Files:** `tests/*.py`

**Test Coverage Goals:** >80%

**Test Files:**

**1. `tests/test_particle.py`**
```python
def test_particle_creation():
    p = Particle(0, 0, 'susceptible')
    assert p.state == 'susceptible'

def test_infection_susceptibility_distribution():
    particles = [Particle(0, 0) for _ in range(1000)]
    susceptibilities = [p.infection_susceptibility for p in particles]
    mean = np.mean(susceptibilities)
    std = np.std(susceptibilities)
    assert 0.95 < mean < 1.05  # Mean around 1.0
    assert 0.15 < std < 0.25   # Std dev around 0.2
```

**2. `tests/test_distributions.py`**
```python
def test_normal_distribution():
    values = [np.random.normal(50, 10) for _ in range(1000)]
    assert 48 < np.mean(values) < 52
    assert 9 < np.std(values) < 11
```

**3. `tests/test_simulation.py`**
```python
def test_infection_spread():
    sim = EpidemicSimulation('simple')
    sim.initialize()
    initial_infected = sum(1 for p in sim.particles if p.state == 'infected')
    for _ in range(100):
        sim.step()
    final_infected = sum(1 for p in sim.particles if p.state == 'infected')
    assert final_infected > initial_infected
```

**Deliverables:**
- >80% code coverage
- All tests pass
- Tests for all critical functions
- Tests for all three distributions
- CI/CD ready

---

### Week 5-6: Documentation (After App is Polished)

#### TICKET-003: German Project Documentation (5 days)
**File:** `docs/Projektdokumentation.pdf`

**Structure (IHK Standard, 6+ pages):**

1. **PROJEKTZIELE UND KUNDENWÜNSCHE** (1 page)
   - Educational goals
   - Target audience
   - Success criteria

2. **VORGEHENSMODELL** (1 page)
   - Agile approach chosen
   - Justification
   - Phases executed

3. **RESSOURCEN- UND ABLAUFPLANUNG** (1 page)
   - 6-week timeline breakdown
   - Resources (all open source)
   - Risk analysis and mitigation

4. **AUSWAHL VERTEILUNGSFUNKTIONEN** (1 page)
   - Uniform: Mathematical definition, usage, justification
   - Normal: Mathematical definition, usage, justification
   - Exponential: Mathematical definition, usage, justification
   - Why these three complement each other

5. **TECHNOLOGIEAUSWAHL** (0.5 pages)
   - Python, PyQt5, NumPy, Matplotlib
   - Alternatives considered and rejected
   - Justifications

6. **BENUTZERSCHNITTSTELLE** (0.5 pages)
   - Three-panel layout concept
   - ISO 9241-110 compliance
   - Accessibility features

7. **TESTPLANUNG** (0.5 pages)
   - Unit, integration, UI, performance tests
   - Test tools used

8. **UMSETZUNG DES PROJEKTS** (1 page)
   - Development phases
   - Key challenges and solutions
   - Modular architecture

**Deliverables:**
- Minimum 6 pages (excluding appendix)
- Professional formatting
- Correct German grammar
- Includes diagrams/screenshots
- IHK standard followed

---

#### TICKET-004: Test Protocols (2 days)
**File:** `docs/Testprotokolle.xlsx`

**Test Categories:**

1. **Functional Tests** (30+ test cases)
2. **Distribution Tests** (statistical validation)
3. **UI/UX Tests** (all interactions)
4. **Performance Tests** (50, 500, 2000 particles)

**Format:**
| Test-ID | Beschreibung | Erwartetes Ergebnis | Tatsächliches Ergebnis | Status | Datum |
|---------|--------------|---------------------|------------------------|--------|-------|
| F001 | ... | ... | ... | Pass | ... |

**Deliverables:**
- Minimum 2 pages in appendix
- All test categories covered
- Pass/fail status for each
- Statistical validation for distributions
- Dates recorded
- Professional formatting

---

#### TICKET-005: User Manual (3 days)
**File:** `docs/Benutzerhandbuch.pdf`

**Structure (8+ pages):**

1. **EINFÜHRUNG**
   - What is epidemic simulation?
   - Purpose and learning goals

2. **INSTALLATION**
   - System requirements
   - Step-by-step installation
   - First launch

3. **BENUTZEROBERFLÄCHE**
   - Three-panel overview
   - All UI elements explained

4. **BEDIENUNG**
   - How to start/pause simulation
   - Parameter explanations (all 11)
   - Mode switching
   - Result interpretation

5. **BEISPIEL-SZENARIEN**
   - 4 example scenarios with explanations

6. **TASTENKOMBINATIONEN**
   - All keyboard shortcuts

7. **FAQ**
   - Common questions answered

8. **FEHLERBEHEBUNG**
   - Troubleshooting guide

**Deliverables:**
- 8+ pages with screenshots
- German language (correct grammar)
- Non-technical language
- PDF format
- Professional layout

---

### Week 7-8: Presentation Preparation

#### TICKET-016: Presentation Slides (3 days)
**File:** `docs/Praesentation.pptx`

**Structure (15-20 slides for 15-20 minute talk):**

1. Titel (1 slide)
2. Agenda (1 slide)
3. Einleitung (2 slides)
4. Anforderungsanalyse (2 slides)
5. Konzept (3 slides)
6. Verteilungsfunktionen (3 slides - one per distribution)
7. Live-Demonstration (5-7 minutes)
8. Technische Umsetzung (2 slides)
9. Herausforderungen (2 slides)
10. Testergebnisse (1 slide)
11. Fazit (1 slide)
12. Ausblick (1 slide)
13. Danke & Fragen (1 slide)

**Deliverables:**
- Professional design
- German language
- Screenshots and code examples
- Rehearsed timing (< 20 minutes)

---

#### TICKET-017: Defense Q&A Preparation (2 days)
**File:** `docs/Defense_QA.md`

**Expected Questions by Category:**

**Funktionalität:**
- Why these three distributions?
- How does spatial optimization work?
- Explain mortality implementation
- Time complexity of infection checking

**User Interface:**
- Why three-panel layout?
- How was ISO 9241-110 implemented?
- Why collapsible panels?
- Accessibility considerations

**Testing:**
- How were distributions tested?
- What performance tests were run?
- Test coverage percentage
- How was UI tested?

**Clean Code:**
- Why modularize code?
- Design patterns used?
- How avoid code duplication?
- Separation of concerns

**Deliverables:**
- Written answers to 30+ expected questions
- Code examples ready
- Architecture diagrams
- Performance data ready

---

#### TICKET-018: Final Documentation Review (2 days)
**Files:** All documentation

**Review Checklist:**
- Grammar and spelling (German)
- Consistent formatting
- All figures/tables numbered
- All references correct
- Table of contents generated
- Page numbers correct
- Appendix organized
- Professional appearance
- PDF export quality

**Deliverables:**
- All documentation polished and final
- No errors or inconsistencies
- Professional quality throughout

---

## 📅 REVISED TIMELINE

```
Week 1: Core Quality
├── TICKET-001: Distribution Functions (2d) ⚠️
├── TICKET-007: Light Mode Theme (2d) 🎨
├── TICKET-008: UI/UX Polish (3d) 💎

Week 2: Performance & Quality
├── TICKET-011: Performance Optimization (2d) ⚡
├── TICKET-006: Code Modularization (3d) 🏗️
├── TICKET-009: Error Handling (2d) 🛡️

Week 3-4: Enhanced Features
├── TICKET-012: Save/Load (2d)
├── TICKET-013: Export (1d)
├── TICKET-014: Tutorial Mode (2d)
├── TICKET-010: Unit Tests (2d)

Week 5-6: Documentation
├── TICKET-003: German Documentation (5d)
├── TICKET-004: Test Protocols (2d)
├── TICKET-005: User Manual (3d)
├── TICKET-018: Doc Review (2d)

Week 7-8: Presentation
├── TICKET-016: Slides (3d)
├── TICKET-017: Defense Prep (2d)
└── Final Rehearsals (3d)
```

---

## 🎯 SUCCESS CRITERIA

### For Grade 2 (Minimum):
- ✅ All functional requirements (7+ parameters, 3+ speeds, visualizations)
- ✅ 3 different distribution functions with justification
- ✅ Complete German documentation (6+ pages)
- ✅ Test protocols (2+ pages)
- ✅ User manual (German)
- ✅ Working application (.exe created by user)

### For Grade 1 (Excellence):
- ✅ All Grade 2 requirements
- ✅ Fully modular code architecture
- ✅ Comprehensive test coverage (>80%)
- ✅ Light/Dark mode themes
- ✅ ISO 9241-110 compliance documented
- ✅ Performance optimized
- ✅ Advanced features (save/load, export)
- ✅ Professional look and feel
- ✅ Exceptional presentation quality

---

## 🚀 NEXT STEPS

### Immediate Start (Week 1):
1. **TICKET-001**: Distribution Functions (HIGHEST PRIORITY)
2. **TICKET-007**: Light Mode Theme
3. **TICKET-008**: UI/UX Polish

### Short-term (Week 2):
4. **TICKET-011**: Performance Optimization
5. **TICKET-006**: Code Modularization
6. **TICKET-009**: Error Handling

### Medium-term (Week 3-4):
7. Enhanced features (Save/Load, Export, Tutorial)
8. Unit testing suite

### Long-term (Week 5-8):
9. Documentation (after app is polished)
10. Presentation preparation

---

## 💰 COST ANALYSIS

**Development Costs: 0€**
- Python, PyQt5, NumPy, Matplotlib: All open source
- VS Code IDE: Free
- Git version control: Free

**Operating Costs: 0€**
- No servers, licenses, or cloud services

**Total: 0€** - Ideal for educational project

---

## ⚠️ RISK ANALYSIS

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Time pressure | High | High | Prioritize app quality first |
| Performance issues | Medium | Medium | Profile early, optimize continuously |
| Testing gaps | Low | Medium | Test-driven development |
| UI/UX issues | Low | High | ISO 9241-110 compliance, user feedback |
| Documentation delay | Medium | High | Write after app is complete |

---

**REVISED PLAN SUMMARY:**

**OLD APPROACH:** Documentation first, then polish
**NEW APPROACH:** Polish application first, document the polished result

**RATIONALE:**
- Better to document a polished, complete application
- User can create .exe themselves
- App quality directly impacts grade presentation
- Documentation describes final state, so should come last

**TARGET:** Grade 1 (Excellence) through superior application quality

---

**Last Updated:** 2025-11-05
**Next Action:** Begin TICKET-001 (Distribution Functions)
**Target Grade:** 1 (Excellent)
