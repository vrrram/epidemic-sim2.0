# Testing Guide: Button Styling & Ctrl+T Feature

## Prerequisites
Please ensure you have the latest code:
```bash
git pull origin claude/start-project-implementation-011CUpUPAGWL6PGL6gXbY45B
```

## Feature 1: Green Background for Checked Buttons

### Expected Behavior:
When you click a button (Speed buttons or Mode buttons), the button should:
- **Dark Theme:** Show NEON GREEN background (#00ff00) with BLACK text (#000000)
- **Light Theme:** Show LIGHT GREEN background (#66bb6a) with BLACK text (#000000)

### How to Test:
1. Run the simulation: `python epidemic_sim3.py`
2. Click one of the Speed buttons (1x, 2x, 4x, 8x)
3. The selected button should have a **green background** with **black text**
4. Press **Shift+T** to toggle theme
5. In light mode, the selected button should have **light green background** with **black text**

### Code Location:
- **Line 2020:** `checked_bg = "#00ff00"` (dark theme)
- **Line 2008:** `checked_bg = "#66bb6a"` (light theme)
- **Lines 2103-2108:** QPushButton:checked stylesheet

### If Not Working:
The checked button styling is controlled by these variables in `apply_theme()` method:
- `checked_bg` - background color
- `checked_text` - text color (always #000000 black)
- `checked_border` - border color

---

## Feature 2: Ctrl+T Parameter Overview Dialog

### Expected Behavior:
Press **Ctrl+T** and a dialog window should appear showing:
- Disease Parameters
- Population Parameters
- Intervention Parameters
- Community Parameters (if in Communities mode)
- Marketplace Parameters (if marketplace enabled)
- Simulation Parameters

The dialog has:
- Beautiful ASCII-art box formatting
- Theme-consistent colors (neon green on black in dark mode)
- All current parameter values
- Close button

### How to Test:
1. Run the simulation: `python epidemic_sim3.py`
2. Hold **Ctrl** and press **T**
3. A dialog titled "Parameter Overview (All Modes)" should appear
4. Press ESC or click Close to dismiss

### Code Location:
- **Lines 2390-2495:** `show_parameter_overview()` method implementation
- **Line 2574:** Keyboard handler that calls `self.show_parameter_overview()`
- **Lines 2570-2581:** Key_T handler with Ctrl/Shift modifier detection

### Keyboard Shortcuts Reminder:
- **T** alone = Toggle tooltips
- **Shift+T** = Toggle theme (light/dark)
- **Ctrl+T** = Show parameter overview

### If Not Working:
Check that:
1. You're holding **Ctrl** (not just T alone)
2. The keyPressEvent is not being blocked by another widget having focus
3. The dialog isn't opening behind the main window (check taskbar)

---

## Debugging Steps

### If you don't see either feature:

1. **Verify you have latest commit:**
   ```bash
   git log --oneline -5
   ```
   You should see:
   - `a599f68` Add .gitignore and remove Python cache files
   - `3e3a300` Fix button text visibility and tooltip flickering
   - `eaea92c` Fix critical AttributeError
   - `571e5fc` Fix UI/UX issues: button styling, Ctrl+T overview

2. **Verify the code contains the features:**
   ```bash
   grep -n "checked_bg.*#00ff00" epidemic_sim3.py
   grep -n "def show_parameter_overview" epidemic_sim3.py
   ```
   Should show:
   - Line 2020: checked_bg = "#00ff00"
   - Line 2390: def show_parameter_overview(self):

3. **Restart the application completely** (don't just reload, close and restart)

4. **Check for Python syntax errors:**
   ```bash
   python -m py_compile epidemic_sim3.py
   ```
   Should complete without errors

---

## Expected Visual Result

### Button (Dark Theme - CHECKED):
```
┌────────────────────┐
│       2x           │  <- Black text
│                    │  <- Neon green background (#00ff00)
└────────────────────┘
```

### Button (Light Theme - CHECKED):
```
┌────────────────────┐
│       2x           │  <- Black text
│                    │  <- Light green background (#66bb6a)
└────────────────────┘
```

### Ctrl+T Dialog:
```
╔══════════════════════════════════════════════╗
║   EPIDEMIC SIMULATOR - PARAMETER OVERVIEW    ║
║            Current Mode: SIMPLE              ║
╚══════════════════════════════════════════════╝

📊 DISEASE PARAMETERS (All Modes):
┌──────────────────────────────────────────────┐
│ Infection Radius:        0.150               │
│ Infection Probability:   0.300 (30.0%)       │
│ Infection Duration:      21.0 days           │
...
```

---

## Contact
If features still don't work after pulling latest code and restarting, please provide:
1. Git commit hash you're running: `git rev-parse HEAD`
2. Any error messages in console
3. Screenshot of what you see vs what's expected
