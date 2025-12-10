"""
Theme system for the epidemic simulation
Supports Dark and Light themes with easy switching
"""

DARK_THEME = {
    'name': 'Dark',
    'NEON_GREEN': "#00ff00",
    'DARK_GREEN': "#003300",
    'BG_BLACK': "#000000",
    'PANEL_BLACK': "#0a0a0a",
    'BORDER_GREEN': "#00aa00",
    'TEXT': "#00ff00",
    'CANVAS_BG': "#000000",
    'GRAPH_BG': "#000000",
    'GRAPH_GRID': (0, 255, 0, 30),  # RGBA for pyqtgraph
    # Particle colors (Dark Mode)
    'PARTICLE_SUSCEPTIBLE': (0, 191, 255),  # Cyan
    'PARTICLE_INFECTED_SYMP': (255, 69, 69),  # Red
    'PARTICLE_INFECTED_ASYMP': (255, 165, 0),  # Orange
    'PARTICLE_REMOVED': (100, 100, 100),  # Gray
    'PARTICLE_DEAD': (80, 0, 0),  # Dark red for dead particles
    # Special zone colors (Dark Mode)
    'MARKETPLACE_PEN': "#ffaa00",  # Orange
    'MARKETPLACE_FILL': (255, 170, 0, 30),  # Orange with alpha
    'QUARANTINE_PEN': "#ff0000",  # Red
    'QUARANTINE_FILL': (255, 0, 0, 20),  # Red with alpha
    # Infection radius visualization
    'INFECTION_RADIUS_PEN': (255, 0, 0, 100),  # Semi-transparent red outline
    'INFECTION_RADIUS_FILL': (255, 0, 0, 30),  # Very transparent red fill
    # UI element hover colors
    'HOVER_BG': "#002200",  # Dark green for hover states
    # Tooltip colors
    'TOOLTIP_BG': "#2b2b2b",  # Dark gray background
    'TOOLTIP_TEXT': "#00ff00",  # Neon green text
    'TOOLTIP_BORDER': "#00ff00",  # Neon green border
    # Pie chart colors (Dark Mode)
    'PIE_SUSCEPTIBLE': "#00bfff",  # Cyan
    'PIE_INFECTED_SYMP': "#ff4545",  # Red
    'PIE_INFECTED_ASYMP': "#ffa500",  # Orange
    'PIE_REMOVED': "#787878",  # Gray
    'PIE_DEAD': "#800000",  # Dark red (visible on dark background)
    'PIE_TEXT': "#ffffff",  # White text for dark mode
}

LIGHT_THEME = {
    'name': 'Light',
    'PRIMARY': "#2e7d32",  # Clean forest green
    'SECONDARY': "#66bb6a",  # Vibrant light green
    'BG_WHITE': "#ffffff",  # Pure white background
    'PANEL_GRAY': "#f5f5f5",  # Light gray for panels
    'BORDER_GRAY': "#9e9e9e",  # Clean gray borders
    'TEXT': "#212121",  # Clean dark text
    'CANVAS_BG': "#fafafa",  # Off-white for canvas
    'GRAPH_BG': "#ffffff",  # Pure white graph background
    'GRAPH_GRID': (158, 158, 158, 60),  # Clean gray grid
    # Particle colors (Light Mode) - vibrant for visibility
    'PARTICLE_SUSCEPTIBLE': (33, 150, 243),  # Bright blue
    'PARTICLE_INFECTED_SYMP': (244, 67, 54),  # Bright red
    'PARTICLE_INFECTED_ASYMP': (255, 152, 0),  # Bright orange
    'PARTICLE_REMOVED': (117, 117, 117),  # Medium gray
    'PARTICLE_DEAD': (183, 28, 28),  # Dark red
    # Special zone colors (Light Mode)
    'MARKETPLACE_PEN': "#ff9800",  # Bright orange
    'MARKETPLACE_FILL': (255, 152, 0, 50),  # Bright orange with alpha
    'QUARANTINE_PEN': "#f44336",  # Bright red
    'QUARANTINE_FILL': (244, 67, 54, 40),  # Bright red with alpha
    # Infection radius visualization (Light Mode)
    'INFECTION_RADIUS_PEN': (244, 67, 54, 120),  # Bright red outline
    'INFECTION_RADIUS_FILL': (244, 67, 54, 40),  # Bright red fill
    # UI element hover colors
    'HOVER_BG': "#e8f5e9",  # Light green hover
    # Tooltip colors
    'TOOLTIP_BG': "#ffffff",  # White background
    'TOOLTIP_TEXT': "#212121",  # Dark text
    'TOOLTIP_BORDER': "#2e7d32",  # Green border
    # Pie chart colors (vibrant for clarity)
    'PIE_SUSCEPTIBLE': "#2196f3",  # Bright blue
    'PIE_INFECTED_SYMP': "#f44336",  # Bright red
    'PIE_INFECTED_ASYMP': "#ff9800",  # Bright orange
    'PIE_REMOVED': "#9e9e9e",  # Medium gray
    'PIE_DEAD': "#d32f2f",  # Dark red
    'PIE_TEXT': "#212121",  # Dark text
}

# Current theme - can be 'dark' or 'light'
current_theme = DARK_THEME  # Default to dark

# Legacy color constants for backwards compatibility
NEON_GREEN = "#00ff00"
DARK_GREEN = "#003300"
BG_BLACK = "#000000"
PANEL_BLACK = "#0a0a0a"
BORDER_GREEN = "#00aa00"


def get_color(key):
    """Get color from current theme, with fallback"""
    # Try current theme first
    if key in current_theme:
        return current_theme[key]
    # Fallback to dark theme if key doesn't exist
    if key in DARK_THEME:
        return DARK_THEME[key]
    # Last resort fallback
    return "#00ff00"


def update_legacy_colors():
    """Update legacy color constants to match current theme"""
    global NEON_GREEN, DARK_GREEN, BG_BLACK, PANEL_BLACK, BORDER_GREEN
    if current_theme == DARK_THEME:
        NEON_GREEN = "#00ff00"
        DARK_GREEN = "#003300"
        BG_BLACK = "#000000"
        PANEL_BLACK = "#0a0a0a"
        BORDER_GREEN = "#00aa00"
    else:  # Light theme
        NEON_GREEN = current_theme['PRIMARY']
        DARK_GREEN = current_theme['SECONDARY']
        BG_BLACK = current_theme['BG_WHITE']
        PANEL_BLACK = current_theme['PANEL_GRAY']
        BORDER_GREEN = current_theme['PRIMARY']  # Use PRIMARY for borders in light mode


def set_theme(theme):
    """Set the current theme (DARK_THEME or LIGHT_THEME)"""
    global current_theme
    current_theme = theme
    update_legacy_colors()
