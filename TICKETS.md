# PROJECT TICKETS - EPIDEMIC SIMULATOR (REVISED)
## German Vocational School Requirements (3rd Year)

**Project:** Epidemic Simulation with Distribution Functions
**Target Grade:** 1 (Excellent - "Above and Beyond")
**Deadline:** 06.02.2025

**REVISED STRATEGY:** Focus on Application Quality First, Documentation Second
**RATIONALE:** Polish the application first, then document the polished result

---

## 🚀 PRIORITY 1: APPLICATION QUALITY (WEEKS 1-3)

**NEW IMPLEMENTATION ORDER:**
1. TICKET-001: Distribution Functions (CRITICAL REQUIREMENT)
2. TICKET-007: Light Mode Theme (LOOK & FEEL)
3. TICKET-008: ISO 9241-110 Compliance (UI/UX POLISH)
4. TICKET-011: Performance Optimization (PERFORMANCE)
5. TICKET-006: Code Modularization (CODE QUALITY)
6. TICKET-009: Comprehensive Error Handling (BEHAVIOR)

**Note:** TICKET-002 (.exe creation) deprioritized - user will handle
**Note:** TICKET-003, 004, 005 (documentation) moved to Priority 3 - do AFTER app is polished

---

### TICKET-001: Implement 3 Distribution Functions ⚠️ HIGHEST PRIORITY
**Estimated Time:** 2 days (reduced - simplified scope)
**Dependencies:** None
**Status:** TODO
**Priority:** 🔴 CRITICAL - Start here!

**Description:**
Add three different statistical distributions to the simulation as required:

1. **UNIFORM DISTRIBUTION** (already used)
   - **Where:** Particle initial positions (x, y)
   - **Where:** Particle velocities (vx, vy)
   - **Where:** Random travel decisions
   - **Why:** All values equally likely - no inherent bias in space/movement
   - **Code:** `random.uniform(a, b)`

2. **NORMAL DISTRIBUTION (Gaussian)** ⚠️ TO ADD
   - **Where:** Individual infection susceptibility (biological variation)
   - **Why:** Most people have average immune response, few are very susceptible/resistant
   - **Mean:** 1.0 (average), **Std Dev:** 0.2 (variation)
   - **Effect:** Multiply infection probability by this factor
   - **Code:** `np.random.normal(1.0, 0.2)`
   - **Math Justification:** Bell curve models natural biological variation

3. **EXPONENTIAL DISTRIBUTION** ⚠️ TO ADD
   - **Where:** Recovery time variation (memoryless property)
   - **Why:** Exponential growth/decay is fundamental to epidemiology
   - **Lambda:** 1.0 (mean = 1/lambda)
   - **Effect:** Multiply infection_duration by this factor
   - **Code:** `np.random.exponential(1.0)`
   - **Math Justification:** Models time until event (recovery) - memoryless property fits disease progression

   **NOTE:** The overall epidemic growth IS exponential (SIR model behavior), but this distribution models individual recovery time variation!

**Acceptance Criteria:**
- [ ] Particle class has `infection_susceptibility` attribute (Normal dist)
- [ ] Particle class has `recovery_time_modifier` attribute (Exponential dist)
- [ ] Infection logic uses susceptibility in calculation
- [ ] Recovery logic uses time modifier
- [ ] Code comments clearly mark which distribution is used where
- [ ] Mathematical justification documented in code comments
- [ ] All three distributions tested and verified

**Files to Modify:**
- `epidemic_sim3.py` (Particle class, infection logic)
- Later: `models/particle.py` (after modularization)

**German Documentation Section:**
```
Auswahl und Begründung der Verteilungsfunktionen:
1. Gleichverteilung: Räumliche Positionen und Bewegungen
2. Normalverteilung: Biologische Eigenschaften (Immunantwort)
3. Exponentialverteilung: Zeitliche Ereignisse (Genesungsdauer)
```

---

### TICKET-002: Create Windows Executable (.exe)
**Estimated Time:** 2 days
**Dependencies:** TICKET-001 (should include all features)
**Status:** TODO

**Description:**
Package the Python application as a standalone Windows executable for school computers.

**Requirements:**
- Single-file executable (no external dependencies)
- Includes all PyQt5, NumPy, Matplotlib libraries
- Window-mode (not console)
- Icon file
- Tested on Windows 10/11

**Implementation Steps:**
1. Install PyInstaller: `pip install pyinstaller`
2. Create icon.ico (optional but professional)
3. Build command:
   ```bash
   pyinstaller --onefile \
               --windowed \
               --add-data "requirements.txt:." \
               --icon=resources/icon.ico \
               --name "EpidemicSimulator" \
               epidemic_sim3.py
   ```
4. Test on Windows machine
5. Document file size, startup time
6. Create installation instructions

**Acceptance Criteria:**
- [ ] EpidemicSimulator.exe created
- [ ] File size < 150MB
- [ ] Runs on Windows 10/11 without Python installed
- [ ] All features functional
- [ ] No console window appears
- [ ] Startup time < 5 seconds
- [ ] Installation instructions written (German)

**Deliverables:**
- `dist/EpidemicSimulator.exe`
- `docs/Installationsanleitung.pdf`

---

### TICKET-003: German Project Documentation (IHK Standard)
**Estimated Time:** 5 days
**Dependencies:** TICKET-001, TICKET-002
**Status:** TODO

**Description:**
Write comprehensive German documentation following IHK vocational standards.

**Structure (6+ pages, excluding appendix):**

**1. PROJEKTZIELE UND KUNDENWÜNSCHE (1 page)**
- Educational goals: Understanding epidemic dynamics
- Target audience: Students, teachers, general public
- Functional goals: Interactive parameter experimentation
- Success criteria

**2. VORGEHENSMODELL (1 page)**
- Chosen: Agile/Iterative approach
- Justification: Rapid feedback, incremental features
- Phases: Planning → Implementation → Testing → Review
- Why not Waterfall: Requirements evolved during development

**3. RESSOURCEN- UND ABLAUFPLANUNG (1 page)**
- Timeline: 9 weeks breakdown
- Resources: Development tools (all free/open-source)
- Personnel: Solo development
- Milestones and deadlines

**4. KOSTENPLANUNG (0.5 pages)**
- Development costs: 0€ (open source tools)
- Operating costs: 0€ (no servers/licenses)
- Total: 0€ (ideal for educational project)

**5. RISIKOANALYSE (0.5 pages)**
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|--------|-------------------|------------|---------------|
| Zeitdruck | Hoch | Hoch | Frühstart, Priorisierung |
| Performance | Mittel | Mittel | Profiling, Tests |
| .exe Probleme | Mittel | Hoch | Frühtests, Alternativen |

**6. AUSWAHL VERTEILUNGSFUNKTIONEN (1 page)**
- Gleichverteilung: Mathematische Definition, Anwendung, Begründung
- Normalverteilung: Mathematische Definition, Anwendung, Begründung
- Exponentialverteilung: Mathematische Definition, Anwendung, Begründung
- Why these three: Complementary properties for different phenomena

**7. TECHNOLOGIEAUSWAHL (0.5 pages)**
- **Python:** Easy to learn, powerful libraries, cross-platform
- **PyQt5:** Professional GUI framework, mature, well-documented
- **NumPy:** Scientific computing, distribution functions
- **Matplotlib/PyQtGraph:** Publication-quality visualizations
- **Alternativen:** Java/JavaFX (rejected: verbose), C#/WPF (rejected: Windows-only)

**8. PLANUNG BENUTZERSCHNITTSTELLE (0.5 pages)**
- Three-panel layout concept
- Left: Parameters (collapsible)
- Center: Simulation canvas
- Right: Controls and graphs
- Justification: Separation of concerns, optimal screen usage

**9. PLANUNG DES TESTENS (0.5 pages)**
- Unit Tests: Individual functions (Particle, distributions)
- Integration Tests: Full simulation runs
- UI Tests: User interactions
- Performance Tests: Large populations (50-2000 particles)
- Test tools: pytest, manual testing

**10. UMSETZUNG DES PROJEKTS (1 page)**
- Development phases executed
- Key challenges encountered and solutions
- Code structure (modular architecture)
- Notable implementation decisions

**Acceptance Criteria:**
- [ ] Minimum 6 pages (excluding appendix)
- [ ] All sections complete
- [ ] Professional formatting
- [ ] Correct German grammar/spelling
- [ ] Includes diagrams/screenshots
- [ ] IHK standard followed

**Deliverables:**
- `docs/Projektdokumentation.pdf`

---

### TICKET-004: Test Protocols (Excel/PDF)
**Estimated Time:** 2 days
**Dependencies:** TICKET-001, TICKET-002
**Status:** TODO

**Description:**
Create formal test protocols documenting all testing performed.

**Test Categories:**

**1. Functional Tests**
| Test-ID | Beschreibung | Erwartetes Ergebnis | Tatsächliches Ergebnis | Status | Datum |
|---------|--------------|---------------------|------------------------|--------|-------|
| F001 | Infektion Radius ändern | Slider bewegt sich, Wert ändert sich | ✓ | Pass | TBD |
| F002 | Simulation pausieren | Animation stoppt sofort | ✓ | Pass | TBD |
| F003 | Modus wechseln | Simulation resettet, neuer Modus aktiv | ✓ | Pass | TBD |
| ... | ... | ... | ... | ... | ... |

**2. Distribution Tests**
| Test-ID | Beschreibung | Erwartetes Ergebnis | Statistik | Status |
|---------|--------------|---------------------|-----------|--------|
| D001 | Gleichverteilung Position | 0 ≤ x ≤ bounds | Mean ≈ bounds/2 | Pass |
| D002 | Normalverteilung Suszeptibilität | Mean = 1.0, σ = 0.2 | μ = 0.99, σ = 0.21 | Pass |
| D003 | Exponentialverteilung Genesungszeit | λ = 1.0, Mean = 1.0 | μ = 1.02 | Pass |

**3. UI/UX Tests**
| Test-ID | Beschreibung | Erwartetes Ergebnis | Status |
|---------|--------------|---------------------|--------|
| U001 | Linkes Panel zusammenklappen | Canvas erweitert sich | Pass |
| U002 | Grafiken sichtbar | Mindestens 380px Höhe | Pass |
| U003 | Tastenkombinationen | Space pausiert, R resettet | Pass |

**4. Performance Tests**
| Test-ID | Population | FPS | Memory | Status |
|---------|-----------|-----|---------|--------|
| P001 | 50 | 60 | 150MB | Pass |
| P002 | 500 | 45 | 400MB | Pass |
| P003 | 2000 | 25 | 1.2GB | Pass |

**Acceptance Criteria:**
- [ ] Minimum 2 pages in appendix
- [ ] All test categories covered
- [ ] At least 30 test cases documented
- [ ] Pass/fail status for each
- [ ] Statistical validation for distributions
- [ ] Dates recorded
- [ ] Professional formatting

**Deliverables:**
- `docs/Testprotokolle.xlsx`
- `docs/Testprotokolle.pdf` (exported for appendix)

---

### TICKET-005: User Manual (German)
**Estimated Time:** 3 days
**Dependencies:** TICKET-001, TICKET-002
**Status:** TODO

**Description:**
Create comprehensive user manual in German for end users (non-technical).

**Structure:**

**1. EINFÜHRUNG**
- Was ist eine Epidemie-Simulation?
- Zweck dieser Anwendung
- Lernziele

**2. INSTALLATION**
- Systemanforderungen: Windows 10/11, 4GB RAM, 200MB Speicher
- Schritt-für-Schritt Installation
- Erste Schritte

**3. BENUTZEROBERFLÄCHE**
- Übersicht der drei Bereiche
- Linkes Panel: Parameter-Einstellungen
- Mitte: Simulations-Animation
- Rechts: Steuerung und Diagramme

**4. BEDIENUNG**
- Simulation starten/pausieren
- Parameter anpassen
  - Was bedeutet "Infektionsradius"?
  - Was bedeutet "Mortalitätsrate"?
  - Etc. für alle 11 Parameter
- Modi wechseln (Einfach, Quarantäne, Gemeinschaften)
- Geschwindigkeit ändern
- Ergebnisse interpretieren

**5. BEISPIEL-SZENARIEN**
- **Szenario 1:** Baseline-Epidemie (keine Interventionen)
  - Erwartetes Ergebnis
  - Lernziel
- **Szenario 2:** Mit Quarantäne
  - Parameter-Einstellungen
  - Erwartetes Ergebnis
- **Szenario 3:** Mit Social Distancing
  - Parameter-Einstellungen
  - Erwartetes Ergebnis
- **Szenario 4:** Gemeinschaften mit Reisebeschränkungen

**6. TASTENKOMBINATIONEN**
- LEERTASTE: Pausieren/Fortsetzen
- R: Zurücksetzen
- F: Vollbild
- Q: Quarantäne an/aus
- M: Marktplatz an/aus
- 1-9: Voreinstellungen

**7. HÄUFIGE FRAGEN (FAQ)**
- Warum verschwinden Partikel?
- Was bedeuten die Farben?
- Wie interpretiere ich das Diagramm?
- Wie speichere ich Ergebnisse?

**8. FEHLERBEHEBUNG**
- Anwendung startet nicht
- Simulation ist langsam
- Grafiken werden nicht angezeigt

**Acceptance Criteria:**
- [ ] 8+ pages with screenshots
- [ ] All features explained
- [ ] German language (correct grammar)
- [ ] Non-technical language (for students)
- [ ] Screenshots with annotations
- [ ] PDF format
- [ ] Professional layout

**Deliverables:**
- `docs/Benutzerhandbuch.pdf`

---

## 🟡 IMPORTANT - FOR GRADE 1 ("ABOVE AND BEYOND")

### TICKET-006: Code Modularization
**Estimated Time:** 3 days
**Dependencies:** TICKET-001 completed
**Status:** TODO

**Description:**
Refactor monolithic 1856-line file into clean modular architecture.

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
│   └── themes.py                # Color themes (dark/light)
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

**Refactoring Tasks:**
1. Create directory structure
2. Extract `Particle` class → `models/particle.py`
3. Extract `SpatialGrid` → `models/spatial_grid.py`
4. Extract `EpidemicSimulation` → `models/simulation.py`
5. Extract `SimParams` → `config/parameters.py`
6. Extract `EpidemicApp` → `ui/main_window.py`
7. Extract `SimulationCanvas` → `ui/canvas.py`
8. Extract `PieChartWidget` → `ui/charts.py`
9. Extract `CollapsibleBox` → `ui/collapsible_box.py`
10. Create `ui/parameters_panel.py` for left panel
11. Create `utils/distributions.py` for distribution helpers
12. Create `utils/constants.py` for theme colors
13. Extract PRESETS → `config/presets.py`
14. Update all imports
15. Test everything still works

**Acceptance Criteria:**
- [ ] Each file < 300 lines
- [ ] Clear separation of concerns
- [ ] All imports working correctly
- [ ] All functionality preserved
- [ ] Tests pass
- [ ] No duplicate code
- [ ] Clean Code principles followed

**Clean Code Principles Applied:**
- Single Responsibility Principle (each module one purpose)
- DRY (Don't Repeat Yourself)
- Clear naming conventions
- Proper encapsulation
- Minimal coupling between modules

---

### TICKET-007: Light Mode Theme
**Estimated Time:** 2 days
**Dependencies:** TICKET-006 (themes.py module)
**Status:** TODO

**Description:**
Implement light theme as alternative to dark theme for accessibility.

**Implementation:**
1. Create `ui/themes.py`:
   ```python
   DARK_THEME = {
       'NEON_GREEN': "#00ff00",
       'DARK_GREEN': "#003300",
       'BG_BLACK': "#000000",
       'PANEL_BLACK': "#0a0a0a",
       'BORDER_GREEN': "#00aa00",
   }

   LIGHT_THEME = {
       'PRIMARY': "#2e7d32",
       'SECONDARY': "#66bb6a",
       'BG_WHITE': "#ffffff",
       'PANEL_GRAY': "#f5f5f5",
       'BORDER_GRAY': "#bdbdbd",
       'TEXT_BLACK': "#212121",
   }
   ```

2. Add theme toggle button (top-right corner)
3. Implement `apply_theme(theme_name)` method
4. Save theme preference with QSettings
5. Update all stylesheets dynamically
6. Ensure graphs readable in both themes

**Acceptance Criteria:**
- [ ] Toggle button visible and functional
- [ ] Both themes look professional
- [ ] All text readable in both themes
- [ ] Graphs/charts work in both themes
- [ ] Theme preference persists between sessions
- [ ] Smooth transition (no flicker)

---

### TICKET-008: ISO 9241-110 Compliance
**Estimated Time:** 2 days
**Dependencies:** TICKET-001, TICKET-007
**Status:** TODO

**Description:**
Verify and document compliance with ISO 9241-110 interaction principles.

**Seven Dialogue Principles:**

**1. Suitability for the Task**
- [x] Users can run simulations without unnecessary steps
- [x] All needed controls accessible
- [ ] Add: Quick preset buttons for common scenarios
- [ ] Add: One-click export results

**2. Self-Descriptiveness**
- [x] Labels are clear
- [ ] Add: Tooltips for ALL parameters with explanations
- [ ] Add: Help button (?) with context-sensitive help
- [ ] Add: Status messages explain what's happening

**3. Conformity with User Expectations**
- [x] Standard controls (buttons, sliders)
- [x] Familiar layout patterns
- [ ] Add: Undo/Redo for parameter changes
- [ ] Add: Confirmation dialogs for destructive actions

**4. Suitability for Learning**
- [ ] Add: Tutorial mode on first launch
- [ ] Add: Interactive walkthrough
- [ ] Add: Example scenarios with explanations
- [ ] Add: Hints system

**5. Controllability**
- [x] Users can pause, reset, adjust speed
- [x] Collapsible panels
- [ ] Add: Save/Load simulation states
- [ ] Add: Export graphs as images
- [ ] Add: Export data as CSV

**6. Error Tolerance**
- [ ] Add: Input validation with helpful error messages
- [ ] Add: Confirmation for "Reset" action
- [ ] Add: Auto-save feature
- [ ] Add: "Are you sure?" dialogs

**7. Suitability for Individualization**
- [x] 11 adjustable parameters
- [x] Multiple modes
- [x] Theme choice (after TICKET-007)
- [ ] Add: Save custom presets
- [ ] Add: Adjustable font size
- [ ] Add: Layout customization

**Acceptance Criteria:**
- [ ] All 7 principles addressed
- [ ] Checklist document created
- [ ] Evidence screenshots for each principle
- [ ] Documented in German
- [ ] Included in project documentation

**Deliverables:**
- `docs/ISO_9241-110_Compliance.pdf`

---

### TICKET-009: Comprehensive Error Handling
**Estimated Time:** 2 days
**Dependencies:** TICKET-006
**Status:** TODO

**Description:**
Add robust error handling throughout the application.

**Areas to Cover:**

**1. Parameter Validation**
```python
def validate_params(self):
    if not 50 <= self.num_particles <= 2000:
        raise ValueError("Population must be between 50 and 2000")
    if not 0.0 <= self.mortality_rate <= 1.0:
        raise ValueError("Mortality rate must be 0-100%")
    if not 0.01 <= self.infection_radius <= 0.4:
        raise ValueError("Infection radius must be 0.01-0.40")
    # ... etc for all 11 parameters
```

**2. Simulation Safety**
```python
try:
    self.sim.step()
except Exception as e:
    self.show_error_dialog(f"Simulation error: {e}")
    self.pause()
    logging.error(f"Simulation error: {e}", exc_info=True)
```

**3. File Operations**
```python
try:
    self.save_state(filename)
except IOError as e:
    self.show_error_dialog(f"Could not save file: {e}")
except Exception as e:
    self.show_error_dialog(f"Unexpected error: {e}")
```

**4. Graceful Degradation**
- If graph update fails, continue simulation
- If pie chart update fails, continue simulation
- If distribution generation fails, use fallback

**5. User-Friendly Error Messages**
- Show dialog with clear explanation
- Suggest fix if possible
- Log technical details for debugging

**Acceptance Criteria:**
- [ ] Try-catch blocks around all risky operations
- [ ] Parameter validation on all inputs
- [ ] User-friendly error dialogs
- [ ] Logging system implemented
- [ ] No unhandled exceptions
- [ ] Graceful degradation where possible

---

### TICKET-010: Unit Testing Suite
**Estimated Time:** 2 days
**Dependencies:** TICKET-006
**Status:** TODO

**Description:**
Create comprehensive unit tests using pytest.

**Test Coverage Goals:** >80%

**Test Files:**

**1. `tests/test_particle.py`**
```python
def test_particle_creation():
    p = Particle(0, 0, 'susceptible')
    assert p.state == 'susceptible'
    assert p.x == 0 and p.y == 0

def test_particle_infection():
    p = Particle(0, 0, 'susceptible')
    p.state = 'infected'
    assert p.days_infected == 0

def test_particle_distance():
    p1 = Particle(0, 0)
    p2 = Particle(3, 4)
    assert p1.distance_to(p2) == 5.0

def test_particle_susceptibility():
    # Test normal distribution attribute
    particles = [Particle(0, 0) for _ in range(1000)]
    susceptibilities = [p.infection_susceptibility for p in particles]
    mean = np.mean(susceptibilities)
    std = np.std(susceptibilities)
    assert 0.95 < mean < 1.05  # Mean around 1.0
    assert 0.15 < std < 0.25   # Std dev around 0.2
```

**2. `tests/test_distributions.py`**
```python
def test_uniform_distribution():
    values = [random.uniform(0, 1) for _ in range(1000)]
    assert all(0 <= v <= 1 for v in values)
    assert 0.45 < np.mean(values) < 0.55

def test_normal_distribution():
    values = [np.random.normal(50, 10) for _ in range(1000)]
    assert 48 < np.mean(values) < 52
    assert 9 < np.std(values) < 11

def test_exponential_distribution():
    values = [np.random.exponential(5) for _ in range(1000)]
    assert all(v >= 0 for v in values)
    assert 4.5 < np.mean(values) < 5.5
```

**3. `tests/test_simulation.py`**
```python
def test_simulation_initialization():
    sim = EpidemicSimulation('simple')
    sim.initialize()
    assert len(sim.particles) > 0
    assert sim.day_count == 0

def test_simulation_step():
    sim = EpidemicSimulation('simple')
    sim.initialize()
    initial_count = len(sim.particles)
    sim.step()
    assert sim.time_count == 1

def test_infection_spread():
    # Test that infection spreads over time
    sim = EpidemicSimulation('simple')
    sim.initialize()
    initial_infected = sum(1 for p in sim.particles if p.state == 'infected')
    for _ in range(100):
        sim.step()
    final_infected = sum(1 for p in sim.particles if p.state == 'infected')
    assert final_infected > initial_infected
```

**Running Tests:**
```bash
pytest tests/ -v
pytest tests/ --cov=models --cov-report=html
```

**Acceptance Criteria:**
- [ ] >80% code coverage
- [ ] All tests pass
- [ ] Tests for all critical functions
- [ ] Tests for all three distributions
- [ ] Tests run in <5 seconds
- [ ] CI/CD ready (can run automatically)

---

### TICKET-011: Performance Optimization
**Estimated Time:** 2 days
**Dependencies:** TICKET-010 (baseline measurements)
**Status:** TODO

**Description:**
Profile and optimize simulation performance.

**Profiling:**
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run simulation
for _ in range(100 * 24):
    sim.step()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**Optimization Targets:**
1. Spatial grid efficiency (already done)
2. Graph update frequency (already throttled)
3. Memory allocation patterns
4. NumPy vectorization opportunities
5. Particle list operations

**Performance Goals:**
| Population | Target FPS | Target Memory |
|-----------|-----------|---------------|
| 50 | 60 | <100MB |
| 500 | 45 | <300MB |
| 2000 | 30 | <1GB |

**Acceptance Criteria:**
- [ ] Performance goals met
- [ ] Profiling report documented
- [ ] Optimizations documented
- [ ] No functionality broken
- [ ] Tests still pass

---

## 🟢 NICE TO HAVE - POLISH

### TICKET-012: Save/Load Simulation States
**Estimated Time:** 2 days
**Dependencies:** TICKET-006, TICKET-009
**Status:** TODO

**Description:**
Allow users to save and load simulation states.

**Features:**
- Save current simulation state to file (.epidemic format)
- Load previously saved state
- Include all parameters, particle states, statistics
- File dialog for save/load

**File Format (JSON):**
```json
{
  "version": "3.0",
  "timestamp": "2024-12-06T10:30:00",
  "parameters": { ... },
  "day_count": 42,
  "particles": [ ... ],
  "stats": { ... }
}
```

**Acceptance Criteria:**
- [ ] Save button in UI
- [ ] Load button in UI
- [ ] File dialog works
- [ ] Full state restoration
- [ ] Error handling for corrupted files

---

### TICKET-013: Export Functionality
**Estimated Time:** 1 day
**Dependencies:** TICKET-006
**Status:** TODO

**Description:**
Allow exporting graphs and data.

**Features:**
- Export time series graph as PNG
- Export pie chart as PNG
- Export statistics as CSV
- Export all data button

**Acceptance Criteria:**
- [ ] Export buttons in UI
- [ ] High-resolution images
- [ ] CSV format correct
- [ ] File naming sensible

---

### TICKET-014: Tutorial Mode
**Estimated Time:** 2 days
**Dependencies:** TICKET-008
**Status:** TODO

**Description:**
Interactive tutorial for first-time users.

**Steps:**
1. Welcome screen
2. Explain simulation canvas
3. Explain parameters
4. Show how to run simulation
5. Show how to interpret results
6. "Try it yourself" challenge

**Acceptance Criteria:**
- [ ] Launches on first run
- [ ] Can be skipped
- [ ] Can be re-launched from menu
- [ ] German language
- [ ] Interactive (not just text)

---

### TICKET-015: Custom Preset Saving
**Estimated Time:** 1 day
**Dependencies:** TICKET-006, TICKET-012
**Status:** TODO

**Description:**
Allow users to save custom parameter presets.

**Features:**
- "Save as Preset" button
- Name custom preset
- Saved to user config
- Appears in preset dropdown
- Can delete custom presets

**Acceptance Criteria:**
- [ ] UI for saving presets
- [ ] Presets persist between sessions
- [ ] Can delete custom presets
- [ ] Max 20 custom presets

---

## 📊 DOCUMENTATION & PRESENTATION

### TICKET-016: Presentation Slides (German)
**Estimated Time:** 3 days
**Dependencies:** All core tickets complete
**Status:** TODO

**Description:**
Create PowerPoint presentation for 15-20 minute talk.

**Structure:**
1. **Titel** (1 slide)
   - Projekt name, Name, Datum

2. **Agenda** (1 slide)
   - Overview of presentation

3. **Einleitung** (2 slides)
   - Motivation
   - Zielsetzung
   - Bedeutung von Epidemie-Simulationen

4. **Anforderungsanalyse** (2 slides)
   - Funktionale Anforderungen
   - Nichtfunktionale Anforderungen
   - Besondere Herausforderungen

5. **Konzept** (3 slides)
   - Vorgehensmodell
   - Architektur-Entscheidungen
   - Technologie-Stack

6. **Verteilungsfunktionen** (3 slides)
   - Gleichverteilung: Anwendung + Mathematik
   - Normalverteilung: Anwendung + Mathematik
   - Exponentialverteilung: Anwendung + Mathematik

7. **Live-Demonstration** (5-7 minutes)
   - Simulation starten
   - Parameter ändern (zeige Effekt)
   - Modi wechseln
   - Visualisierungen erklären
   - Light/Dark Mode
   - Besondere Features

8. **Technische Umsetzung** (2 slides)
   - Modulare Code-Struktur
   - Clean Code Prinzipien
   - Testing-Strategie

9. **Herausforderungen** (2 slides)
   - Performance-Optimierung
   - Verteilungsfunktionen-Integration
   - UI/UX-Design

10. **Testergebnisse** (1 slide)
    - Test coverage
    - Performance benchmarks

11. **Fazit** (1 slide)
    - Erreichte Ziele (alle + mehr!)
    - Lessons Learned

12. **Ausblick** (1 slide)
    - Mögliche Erweiterungen
    - Anwendungsmöglichkeiten

13. **Danke & Fragen** (1 slide)

**Acceptance Criteria:**
- [ ] 15-20 slides
- [ ] Professional design
- [ ] German language
- [ ] Screenshots included
- [ ] Code examples (short)
- [ ] Rehearsed (< 20 minutes)

**Deliverables:**
- `docs/Praesentation.pptx`

---

### TICKET-017: Defense Q&A Preparation
**Estimated Time:** 2 days
**Dependencies:** TICKET-016
**Status:** TODO

**Description:**
Prepare answers for expected defense questions.

**Expected Questions by Category:**

**Funktionalität:**
- Warum wurden diese drei Verteilungsfunktionen gewählt?
- Wie funktioniert die räumliche Optimierung (SpatialGrid)?
- Erkläre die Implementierung der Sterblichkeitsrate
- Wie wird Community-Travel implementiert?
- Was ist die Zeitkomplexität der Infektionsprüfung?

**User Interface:**
- Warum das drei-Panel-Layout?
- Wie wurde ISO 9241-110 umgesetzt?
- Warum sind Parameter kollabierbar?
- Wie wurde Accessibility berücksichtigt?
- Warum Light/Dark Mode?

**Testing:**
- Wie wurden die Verteilungsfunktionen getestet?
- Welche Performance-Tests wurden durchgeführt?
- Wie hoch ist die Test-Coverage?
- Wie wurde die UI getestet?

**Clean Code:**
- Warum wurde der Code modularisiert?
- Welche Design Patterns wurden verwendet?
- Wie wurde Code-Duplikation vermieden?
- Wie wurde Separation of Concerns erreicht?

**Prepare:**
- [ ] Written answers to 30+ expected questions
- [ ] Code examples ready to show
- [ ] Diagrams to explain architecture
- [ ] Performance data ready
- [ ] Test results ready

---

### TICKET-018: Final Documentation Review
**Estimated Time:** 2 days
**Dependencies:** TICKET-003, TICKET-004, TICKET-005
**Status:** TODO

**Description:**
Review and polish all German documentation.

**Review Checklist:**
- [ ] Grammar and spelling check (German)
- [ ] Consistent formatting
- [ ] All figures/tables numbered
- [ ] All references correct
- [ ] Table of contents generated
- [ ] Page numbers correct
- [ ] Appendix organized
- [ ] Professional appearance
- [ ] PDF export quality
- [ ] File sizes reasonable

**Final Deliverables:**
- [ ] Projektdokumentation.pdf (final)
- [ ] Testprotokolle.pdf (final)
- [ ] Benutzerhandbuch.pdf (final)
- [ ] ISO_9241-110_Compliance.pdf
- [ ] Praesentation.pptx (final)

---

## 📅 RECOMMENDED SEQUENCE

### Week 1-2: Critical Path (Grade 2 Requirements)
```
Day 1-3:   TICKET-001 (Distribution Functions) ⚠️ CRITICAL
Day 4-5:   TICKET-002 (.exe Creation) ⚠️ CRITICAL
Day 6-10:  TICKET-003 (German Documentation) ⚠️ CRITICAL
Day 11-12: TICKET-004 (Test Protocols) ⚠️ CRITICAL
Day 13-15: TICKET-005 (User Manual) ⚠️ CRITICAL
```

### Week 3: Code Quality (Grade 1 Path)
```
Day 16-18: TICKET-006 (Modularization)
Day 19-20: TICKET-007 (Light Mode)
Day 21:    TICKET-008 (ISO Compliance)
```

### Week 4: Robustness
```
Day 22-23: TICKET-009 (Error Handling)
Day 24-25: TICKET-010 (Unit Tests)
Day 26-27: TICKET-011 (Performance)
```

### Week 5-6: Polish & Documentation
```
Day 28-29: TICKET-012 (Save/Load)
Day 30:    TICKET-013 (Export)
Day 31-32: TICKET-014 (Tutorial)
Day 33:    TICKET-015 (Custom Presets)
Day 34-36: TICKET-018 (Doc Review)
```

### Week 7-8: Presentation
```
Day 37-39: TICKET-016 (Slides)
Day 40-41: TICKET-017 (Defense Prep)
Day 42-44: Practice & Rehearse
```

### Week 9: Final Submission
```
Day 45-47: Final testing, bug fixes
Day 48:    Submit everything
```

---

## 🎯 ACCEPTANCE CRITERIA SUMMARY

**For Grade 2 (Must Complete):**
- ✅ TICKET-001: 3 distribution functions implemented
- ✅ TICKET-002: Windows .exe works
- ✅ TICKET-003: German documentation complete (6+ pages)
- ✅ TICKET-004: Test protocols (2+ pages)
- ✅ TICKET-005: User manual (German)

**For Grade 1 (Above and Beyond):**
- ✅ TICKET-006: Code modularized
- ✅ TICKET-007: Light/dark themes
- ✅ TICKET-008: ISO 9241-110 documented
- ✅ TICKET-009: Comprehensive error handling
- ✅ TICKET-010: >80% test coverage
- ✅ TICKET-011: Performance optimized
- ✅ Plus any of TICKET-012 through TICKET-015

**For Excellent Presentation:**
- ✅ TICKET-016: Professional slides
- ✅ TICKET-017: Defense answers prepared
- ✅ TICKET-018: All docs polished

---

## 🚦 STATUS LEGEND

- **TODO**: Not started
- **IN PROGRESS**: Currently being worked on
- **BLOCKED**: Waiting on dependencies
- **REVIEW**: Awaiting review
- **DONE**: Complete and tested

---

**Last Updated:** 2024-12-06
**Total Tickets:** 18
**Critical Path:** Tickets 1-5 (MUST complete for Grade 2)
**Grade 1 Path:** Tickets 1-11
**Excellence Path:** All tickets

**Start with:** TICKET-001 (Distribution Functions)
