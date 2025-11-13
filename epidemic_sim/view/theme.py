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
    # Special zone colors (Dark Mode)
    'MARKETPLACE_PEN': "#ffaa00",  # Orange
    'MARKETPLACE_FILL': (255, 170, 0, 30),  # Orange with alpha
    'QUARANTINE_PEN': "#ff0000",  # Red
    'QUARANTINE_FILL': (255, 0, 0, 20),  # Red with alpha
    # Pie chart colors (Dark Mode)
    'PIE_DEAD': "#800000",  # Visible dark red
}

LIGHT_THEME = {
    'name': 'Light',
    'PRIMARY': "#2e7d32",  # Professional green
    'SECONDARY': "#66bb6a",  # Light green accent
    'BG_WHITE': "#ffffff",
    'PANEL_GRAY': "#f5f5f5",
    'BORDER_GRAY': "#bdbdbd",
    'TEXT': "#212121",  # Almost black for text
    'CANVAS_BG': "#fafafa",  # Very light gray
    'GRAPH_BG': "#ffffff",
    'GRAPH_GRID': (33, 125, 50, 50),  # RGBA for pyqtgraph (green-ish)
    # Particle colors (Light Mode) - adjusted for visibility on light background
    'PARTICLE_SUSCEPTIBLE': (25, 118, 210),  # Blue (darker for visibility)
    'PARTICLE_INFECTED_SYMP': (211, 47, 47),  # Dark red
    'PARTICLE_INFECTED_ASYMP': (245, 124, 0),  # Orange
    'PARTICLE_REMOVED': (97, 97, 97),  # Dark gray
    # Special zone colors (Light Mode) - darker for visibility on light background
    'MARKETPLACE_PEN': "#d68400",  # Darker orange
    'MARKETPLACE_FILL': (214, 132, 0, 50),  # Darker orange with alpha
    'QUARANTINE_PEN': "#c62828",  # Darker red
    'QUARANTINE_FILL': (198, 40, 40, 40),  # Darker red with alpha
    # Pie chart colors (Light Mode)
    'PIE_DEAD': "#c62828",  # Dark red visible on light
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
        BORDER_GREEN = current_theme['BORDER_GRAY']


def set_theme(theme):
    """Set the current theme (DARK_THEME or LIGHT_THEME)"""
    global current_theme
    current_theme = theme
    update_legacy_colors()
