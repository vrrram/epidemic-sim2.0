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
    'PRIMARY': "#5d7a63",  # Muted sage green
    'SECONDARY': "#8fa98e",  # Soft green
    'BG_WHITE': "#e8f0e8",  # Soft pastel green background
    'PANEL_GRAY': "#f5f9f5",  # Very light mint for panels
    'BORDER_GRAY': "#a8b9a8",  # Muted green-gray borders
    'TEXT': "#2d3a2e",  # Dark green-gray text (soft, not harsh black)
    'CANVAS_BG': "#e0e8e0",  # Soft sage background for canvas
    'GRAPH_BG': "#f8fbf8",  # Almost white with hint of green
    'GRAPH_GRID': (141, 160, 141, 80),  # Soft green-gray grid
    # Particle colors (Light Mode) - adjusted for visibility on light background
    'PARTICLE_SUSCEPTIBLE': (25, 118, 210),  # Blue (darker for visibility)
    'PARTICLE_INFECTED_SYMP': (211, 47, 47),  # Dark red
    'PARTICLE_INFECTED_ASYMP': (245, 124, 0),  # Orange
    'PARTICLE_REMOVED': (97, 97, 97),  # Dark gray
    'PARTICLE_DEAD': (139, 0, 0),  # Dark red visible on light bg
    # Special zone colors (Light Mode) - darker for visibility on light background
    'MARKETPLACE_PEN': "#d68400",  # Darker orange
    'MARKETPLACE_FILL': (214, 132, 0, 50),  # Darker orange with alpha
    'QUARANTINE_PEN': "#c62828",  # Darker red
    'QUARANTINE_FILL': (198, 40, 40, 40),  # Darker red with alpha
    # Infection radius visualization (Light Mode)
    'INFECTION_RADIUS_PEN': (198, 40, 40, 120),  # Darker red outline
    'INFECTION_RADIUS_FILL': (198, 40, 40, 40),  # More visible fill
    # UI element hover colors
    'HOVER_BG': "#d5e5d5",  # Soft green-gray hover
    # Tooltip colors
    'TOOLTIP_BG': "#f5f9f5",  # Soft mint background
    'TOOLTIP_TEXT': "#2d3a2e",  # Dark green-gray text
    'TOOLTIP_BORDER': "#8fa98e",  # Soft green border
    # Pie chart colors (adjusted for light background visibility)
    'PIE_SUSCEPTIBLE': "#5b9bd5",  # Soft blue
    'PIE_INFECTED_SYMP': "#c55a5a",  # Muted red
    'PIE_INFECTED_ASYMP': "#e09952",  # Soft orange
    'PIE_REMOVED': "#8a8a8a",  # Medium gray
    'PIE_DEAD': "#a85252",  # Muted dark red
    'PIE_TEXT': "#2d3a2e",  # Dark green-gray for text
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
