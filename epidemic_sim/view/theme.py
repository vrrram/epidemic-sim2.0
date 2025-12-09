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
}

LIGHT_THEME = {
    'name': 'Light',
    'PRIMARY': "#1b5e20",  # Dark green for better contrast
    'SECONDARY': "#4caf50",  # Medium green
    'BG_WHITE': "#f5f5f5",  # Light gray (not pure white - easier on eyes)
    'PANEL_GRAY': "#ffffff",  # White panels for contrast
    'BORDER_GRAY': "#616161",  # Darker gray for visible borders
    'TEXT': "#000000",  # Pure black for maximum readability
    'CANVAS_BG': "#e8e8e8",  # Light gray canvas
    'GRAPH_BG': "#ffffff",
    'GRAPH_GRID': (97, 97, 97, 100),  # Gray grid lines (visible but subtle)
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
    'HOVER_BG': "#e8f5e9",  # Light green for hover states
    # Tooltip colors
    'TOOLTIP_BG': "#ffffff",  # White background
    'TOOLTIP_TEXT': "#212121",  # Almost black text
    'TOOLTIP_BORDER': "#2e7d32",  # Professional green border
    # Pie chart colors (adjusted for light background visibility)
    'PIE_SUSCEPTIBLE': "#1976d2",  # Darker blue
    'PIE_INFECTED_SYMP': "#d32f2f",  # Darker red
    'PIE_INFECTED_ASYMP': "#f57c00",  # Darker orange
    'PIE_REMOVED': "#616161",  # Darker gray
    'PIE_DEAD': "#c62828",  # Dark red (visible on light background)
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
