# Light Mode Compatibility Report

**Date:** 2025-11-12
**Analyzed by:** Claude Code
**Status:** ⚠️ PARTIALLY IMPLEMENTED - CRITICAL ISSUES FOUND

---

## Executive Summary

The epidemic simulation has a **light theme defined** but it is **NOT accessible** to users. While the theme system architecture is well-designed, there are critical implementation gaps and hardcoded colors that prevent light mode from working correctly.

**Overall Status:** 🔴 NOT FUNCTIONAL
- Theme system: ✅ Properly designed
- UI accessibility: 🔴 No theme toggle button
- Color consistency: ⚠️ Multiple hardcoded colors
- Canvas rendering: ⚠️ Partial theme support

---

## 1. Theme System Architecture ✅

**Location:** `epidemic_sim/view/theme.py`

**Status:** WELL DESIGNED

The theme system is properly implemented with:
- ✅ Separate `DARK_THEME` and `LIGHT_THEME` dictionaries
- ✅ `get_color(key)` function for theme-aware color retrieval
- ✅ `set_theme()` function to switch themes
- ✅ `update_legacy_colors()` to maintain backwards compatibility
- ✅ Complete color definitions for both themes:
  - Canvas backgrounds
  - Particle colors (adjusted for visibility on light background)
  - Graph colors (including RGBA for pyqtgraph)
  - UI element colors

**Light Theme Colors:**
```python
LIGHT_THEME = {
    'PRIMARY': "#2e7d32",          # Professional green
    'SECONDARY': "#66bb6a",        # Light green accent
    'BG_WHITE': "#ffffff",         # White background
    'PANEL_GRAY': "#f5f5f5",       # Light gray panels
    'BORDER_GRAY': "#bdbdbd",      # Gray borders
    'TEXT': "#212121",             # Almost black text
    'CANVAS_BG': "#fafafa",        # Very light gray canvas
    'PARTICLE_SUSCEPTIBLE': (25, 118, 210),   # Darker blue (visibility)
    'PARTICLE_INFECTED_SYMP': (211, 47, 47),  # Dark red
    'PARTICLE_INFECTED_ASYMP': (245, 124, 0), # Orange
    'PARTICLE_REMOVED': (97, 97, 97),         # Dark gray
}
```

---

## 2. CRITICAL ISSUE: No Theme Toggle Button 🔴

**Problem:** The theme toggle button (`self.theme_btn`) is **referenced but never created**.

**Evidence:**
```python
# epidemic_sim/view/main_window.py:1472, 1476
def toggle_theme(self):
    if theme_module.current_theme == DARK_THEME:
        self.theme_btn.setText("🌙 DARK")  # ❌ AttributeError: no theme_btn
    else:
        self.theme_btn.setText("☀ LIGHT")  # ❌ AttributeError: no theme_btn
```

**Impact:**
- Users **cannot switch to light mode** through the UI
- The `toggle_theme()` method would crash with `AttributeError` if called
- No keyboard shortcut for theme switching

**Current Workaround:**
- Theme can only be set by modifying `theme.py` directly
- Requires code changes to test light mode

---

## 3. Hardcoded Colors (Won't Change with Theme) ⚠️

### 3.1 Main Window (`main_window.py`)

**Tab Hover Color (Line 931):**
```python
QTabBar::tab:hover {{ background-color: #002200; }}  # Dark green - won't work in light mode
```

**Checkable Button Stylesheet (Lines 1028-1069):**
```python
# Light theme colors - HARDCODED
QPushButton:hover {{ background-color: #e8f5e9; }}
QPushButton:checked {{ background-color: #66bb6a; color: #000000; }}

# Dark theme colors - HARDCODED
QPushButton:hover {{ background-color: #1a1a1a; }}
QPushButton:checked {{ background-color: #00ff00; color: #000000; }}
```

**Dynamic Hover Colors (Lines 1096-1118):**
```python
if theme_module.current_theme == LIGHT_THEME:
    hover_bg = "#e8f5e9"       # HARDCODED light green
    hover_border = "#2e7d32"   # HARDCODED dark green
    hover_text = "#1b5e20"     # HARDCODED dark green text
    # ... more hardcoded colors
```

**Impact:** These are actually used dynamically in `apply_theme()`, so they work correctly. However, they're defined inline rather than in the theme dictionary.

### 3.2 Canvas (`canvas.py`)

**Marketplace Zone Colors (Lines 129-130, 170-171):**
```python
painter.setPen(QPen(QColor("#ffaa00"), 2, Qt.DashLine))      # Orange - not theme-aware
painter.setBrush(QBrush(QColor(255, 170, 0, 30)))            # Orange with alpha
```

**Quarantine Zone Colors (Lines 138-139, 187-188):**
```python
painter.setPen(QPen(QColor("#ff0000"), 3))                   # Red - not theme-aware
painter.setBrush(QBrush(QColor(255, 0, 0, 20)))              # Red with alpha
```

**Impact:**
- Marketplace zones will always be orange (might be invisible on light backgrounds)
- Quarantine zones will always be red (might clash with light theme aesthetics)
- These special zones won't adapt to theme changes

### 3.3 Widgets (`widgets.py`)

**CollapsibleBox Hover Color (Line 65):**
```python
QPushButton:hover {{ background-color: #002200; }}  # Dark green - wrong for light mode
```

**PieChartWidget Colors (Lines 235-255):**
```python
colors.append('#00bfff')  # Cyan - Susceptible (might work in both modes)
colors.append('#ff4545')  # Red - Infected symptomatic (might work)
colors.append('#ffa500')  # Orange - Infected asymptomatic (might work)
colors.append('#787878')  # Gray - Removed (might work)
colors.append('#500000')  # Dark red - Dead (invisible on light background!)
```

**Impact:**
- Pie chart colors are hardcoded and don't use theme system
- Dead particle color (`#500000`) is **very dark** and will be **nearly invisible** on light backgrounds

### 3.4 Tooltip Colors

**Tooltip Toggle (Lines 1543-1562):**
```python
# Enabled tooltips - HARDCODED for dark theme
QToolTip {
    background-color: #2b2b2b;  # Dark gray
    color: #00ff00;             # Neon green
    border: 1px solid #00ff00;  # Neon green
}

# Disabled tooltips
QToolTip {
    opacity: 0;
    background-color: transparent;
}
```

**Impact:** Tooltips always use dark theme colors, even in light mode

---

## 4. Theme-Aware Components ✅

### 4.1 Canvas Rendering
**Status:** PARTIAL - Uses `get_color()` for some elements

**Proper usage:**
```python
canvas_bg = get_color('CANVAS_BG')
painter.fillRect(self.rect(), QColor(canvas_bg))

# Particle colors
rgb = get_color('PARTICLE_SUSCEPTIBLE')
color = QColor(rgb[0], rgb[1], rgb[2])
```

**Issues:**
- Marketplace and quarantine zones use hardcoded colors (see 3.2)
- Boundary colors use legacy constants (`NEON_GREEN`, `BORDER_GREEN`)

### 4.2 Main Window
**Status:** GOOD - Uses theme system in most places

**Proper usage:**
```python
from epidemic_sim.view.theme import get_color, BG_BLACK, NEON_GREEN, BORDER_GREEN

self.left_panel.setStyleSheet(f"background-color: {BG_BLACK};")
self.graph_widget.setBackground(get_color('GRAPH_BG'))
```

**Legacy color constants update automatically:**
```python
# When theme switches, these update automatically:
NEON_GREEN -> theme['PRIMARY'] (in light mode)
BG_BLACK -> theme['BG_WHITE'] (in light mode)
```

### 4.3 Graph Widget
**Status:** GOOD - Theme switching properly implemented

```python
def toggle_theme(self):
    # Update graph colors
    self.graph_widget.setBackground(get_color('GRAPH_BG'))
    graph_grid_color = get_color('GRAPH_GRID')
    self.graph_widget.showGrid(x=True, y=True, alpha=graph_grid_color[3]/255.0)

    # Update axes colors
    for side in ['left', 'bottom', 'right', 'top']:
        axis = self.graph_widget.getAxis(side)
        axis.setPen(pg.mkPen(color=get_color('BORDER_GRAY'), width=2))
        axis.setTextPen(get_color('TEXT'))
```

---

## 5. Missing Functionality

### 5.1 Theme Toggle Button
**Status:** 🔴 NOT IMPLEMENTED

**What exists:**
- ✅ `toggle_theme()` method (lines 1465-1526)
- ✅ Theme saving/loading with QSettings
- ✅ Complete theme switching logic
- ❌ **No button in UI**
- ❌ **No keyboard shortcut**

**Expected behavior (from code):**
- Button should show "☀ LIGHT" in dark mode
- Button should show "🌙 DARK" in light mode
- Clicking should toggle theme and save preference

### 5.2 Keyboard Shortcut
**Current shortcuts (lines 1684-1690):**
- SPACE: Pause/Resume
- R: Reset simulation
- F: Fullscreen toggle
- Q: Toggle quarantine
- M: Toggle marketplace
- Ctrl+T: Toggle tooltips (NOT theme!)
- 1-9: Load preset by number

**Missing:** No keyboard shortcut for theme toggle (could be Ctrl+Shift+T or Alt+T)

---

## 6. Testing Status

### Tested:
- ✅ Theme system architecture (properly designed)
- ✅ Color definitions (complete for both themes)
- ✅ `get_color()` function (works correctly with fallbacks)
- ✅ Legacy color updates (work correctly)

### NOT Tested (Cannot test without UI access):
- 🔴 Theme toggle button (doesn't exist)
- 🔴 Light mode rendering (button missing)
- 🔴 Light mode particle visibility (no way to switch)
- 🔴 Light mode graph rendering (no way to switch)
- 🔴 Light mode UI contrast (no way to switch)

---

## 7. Recommendations (Do NOT Implement - Report Only)

### Priority 1: CRITICAL - Make Light Mode Accessible
1. **Create theme toggle button** in the UI (right panel controls area)
2. **Add keyboard shortcut** (suggest: Alt+T or Ctrl+Shift+T)
3. **Test theme switching** thoroughly once button exists

### Priority 2: HIGH - Fix Hardcoded Colors
1. **Canvas special zones** (marketplace, quarantine):
   - Add to theme dictionaries: `MARKETPLACE_COLOR`, `QUARANTINE_COLOR`
   - Use `get_color()` instead of hardcoded values

2. **Pie chart colors**:
   - Add to theme dictionaries: `PIE_SUSCEPTIBLE`, `PIE_INFECTED_SYMP`, etc.
   - Fix dead particle color for light mode visibility

3. **Tooltip colors**:
   - Use theme system instead of hardcoded values in `toggle_tooltips()`
   - Respect current theme when enabling tooltips

### Priority 3: MEDIUM - Improve Color Definitions
1. **Move inline colors to theme dictionary:**
   - Button hover colors (currently in `apply_theme()`)
   - Tab hover colors
   - Tooltip colors

2. **Add missing theme keys:**
   - `MARKETPLACE_PEN_COLOR`
   - `MARKETPLACE_FILL_COLOR`
   - `QUARANTINE_PEN_COLOR`
   - `QUARANTINE_FILL_COLOR`

### Priority 4: LOW - Code Cleanup
1. **Consolidate color definitions:**
   - Move all dynamic color logic from `apply_theme()` to theme dictionaries
   - Reduce code duplication

2. **Add theme preview:**
   - Show example colors before switching
   - Help users understand what will change

---

## 8. Compatibility Matrix

| Component | Dark Theme | Light Theme | Notes |
|-----------|------------|-------------|-------|
| **Main Window** | ✅ Works | ⚠️ Partial | Legacy colors update, but some hardcoded |
| **Canvas Background** | ✅ Works | ✅ Should work | Uses `get_color('CANVAS_BG')` |
| **Particles** | ✅ Works | ✅ Should work | Theme-aware colors defined |
| **Boundaries** | ✅ Works | ✅ Should work | Uses legacy constants (auto-update) |
| **Marketplace Zone** | ✅ Works | 🔴 Hardcoded | Always orange (#ffaa00) |
| **Quarantine Zone** | ✅ Works | 🔴 Hardcoded | Always red (#ff0000) |
| **Graph** | ✅ Works | ✅ Should work | Proper theme switching implemented |
| **Pie Chart** | ✅ Works | ⚠️ Issues | Dead color invisible on light bg |
| **Tooltips** | ✅ Works | 🔴 Wrong colors | Always dark theme colors |
| **Buttons** | ✅ Works | ✅ Should work | Dynamic colors in `apply_theme()` |
| **Sliders** | ✅ Works | ✅ Should work | Uses legacy constants |
| **Text** | ✅ Works | ✅ Should work | Uses `get_color('TEXT')` |

**Legend:**
- ✅ Works: Confirmed working
- ✅ Should work: Theme-aware but untested
- ⚠️ Partial: Some issues, mostly functional
- ⚠️ Issues: Works but with problems
- 🔴 Hardcoded: Won't change with theme
- 🔴 Wrong colors: Uses wrong theme's colors

---

## 9. Code References

### Theme System
- **Theme definitions:** `epidemic_sim/view/theme.py:6-40`
- **get_color() function:** `epidemic_sim/view/theme.py:53-62`
- **set_theme() function:** `epidemic_sim/view/theme.py:82-86`

### Theme Switching Logic
- **toggle_theme() method:** `epidemic_sim/view/main_window.py:1465-1526`
- **apply_theme() method:** `epidemic_sim/view/main_window.py:1092-1260`
- **load_theme() method:** `epidemic_sim/view/main_window.py:1451-1463`

### Hardcoded Colors
- **Canvas marketplace:** `epidemic_sim/view/canvas.py:129-131, 170-171`
- **Canvas quarantine:** `epidemic_sim/view/canvas.py:138-139, 187-188`
- **Pie chart colors:** `epidemic_sim/view/widgets.py:235-255`
- **Tooltip colors:** `epidemic_sim/view/main_window.py:1543-1562`
- **Button hover:** `epidemic_sim/view/widgets.py:65`
- **Tab hover:** `epidemic_sim/view/main_window.py:931`

---

## 10. Conclusion

**Current State:** The light mode is **defined but inaccessible**. The theme system architecture is excellent, but critical implementation gaps prevent users from using light mode.

**Blockers:**
1. 🔴 **CRITICAL:** No theme toggle button (prevents all testing)
2. ⚠️ **HIGH:** Hardcoded special zone colors (marketplace, quarantine)
3. ⚠️ **MEDIUM:** Pie chart dead color invisible on light backgrounds
4. ⚠️ **LOW:** Tooltip colors don't respect theme

**Assessment:** Light mode **cannot be used** without first creating the theme toggle button. Once the button exists, most components should work correctly due to the well-designed theme system, but thorough testing is required to identify visual issues.

**Estimated Work to Full Compatibility:**
- Create theme button: ~30 minutes
- Fix hardcoded colors: ~1-2 hours
- Test and refine: ~2-3 hours
- **Total: 3.5-5.5 hours**

---

**Report Generated:** 2025-11-12
**Analysis Complete** ✅
