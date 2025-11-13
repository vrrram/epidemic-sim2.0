"""
SimulationCanvas - Visual rendering component for the epidemic simulation

This module contains the SimulationCanvas class which handles all visual rendering
of the simulation state including particles, boundaries, communities, and special zones.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush

from epidemic_sim.view.theme import get_color, NEON_GREEN, BORDER_GREEN


class SimulationCanvas(QWidget):
    """
    Custom QWidget that renders the epidemic simulation visualization.

    This canvas displays:
    - Particles (individuals) colored by their infection state
    - Community boundaries in community mode
    - Special zones (marketplace, quarantine)
    - Infection radius circles when enabled

    The canvas adapts its rendering based on the simulation mode (simple vs communities)
    and handles coordinate transformations from simulation space to screen space.

    Attributes:
        sim: Reference to the EpidemicSimulation instance
        scale (float): Scaling factor for coordinate transformation
        offset_x (float): X offset for centering the visualization
        offset_y (float): Y offset for centering the visualization
    """

    def __init__(self, sim):
        """
        Initialize the simulation canvas.

        Args:
            sim: The EpidemicSimulation instance to visualize
        """
        super().__init__()
        self.sim = sim
        self.setMinimumSize(900, 900)

        # Visual effects: Store particle position history for trails
        # Dictionary mapping particle id to deque of recent positions
        self.particle_trails = {}
        self.max_trail_length = 10  # Number of trail points to keep
        self.enable_trails = False  # Can be toggled by user
        self.enable_glow = True  # Glow effect for infected particles

        # Performance optimization: Cache color objects to avoid recreating them every frame
        self._color_cache = {}
        self._update_color_cache()

    def _update_color_cache(self):
        """
        Update cached color objects from theme system.

        Performance optimization: Pre-create QColor objects to avoid
        recreating them every frame. Call this when theme changes.
        """
        # Particle colors (RGB tuples -> QColor objects)
        rgb = get_color('PARTICLE_SUSCEPTIBLE')
        self._color_cache['susceptible'] = QColor(rgb[0], rgb[1], rgb[2])

        rgb = get_color('PARTICLE_INFECTED_SYMP')
        self._color_cache['infected_symp'] = QColor(rgb[0], rgb[1], rgb[2])
        self._color_cache['infected_symp_glow'] = QColor(rgb[0], rgb[1], rgb[2], 40)

        rgb = get_color('PARTICLE_INFECTED_ASYMP')
        self._color_cache['infected_asymp'] = QColor(rgb[0], rgb[1], rgb[2])
        self._color_cache['infected_asymp_glow'] = QColor(rgb[0], rgb[1], rgb[2], 40)

        rgb = get_color('PARTICLE_REMOVED')
        self._color_cache['removed'] = QColor(rgb[0], rgb[1], rgb[2])

        # Special zone colors
        self._color_cache['marketplace_pen'] = QColor(get_color('MARKETPLACE_PEN'))
        fill = get_color('MARKETPLACE_FILL')
        self._color_cache['marketplace_fill'] = QColor(fill[0], fill[1], fill[2], fill[3])

        self._color_cache['quarantine_pen'] = QColor(get_color('QUARANTINE_PEN'))
        fill = get_color('QUARANTINE_FILL')
        self._color_cache['quarantine_fill'] = QColor(fill[0], fill[1], fill[2], fill[3])

        # Infection radius colors
        self._color_cache['infection_radius_pen'] = QColor(255, 0, 0, 100)
        self._color_cache['infection_radius_fill'] = QColor(255, 0, 0, 30)

    def paintEvent(self, event):
        """
        Qt paint event handler - renders the entire simulation state.

        This method is called automatically by Qt when the widget needs to be redrawn.
        It handles coordinate scaling, background rendering, and delegates to mode-specific
        drawing methods.

        Args:
            event: QPaintEvent from Qt framework
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Use theme-aware background color
        canvas_bg = get_color('CANVAS_BG')
        painter.fillRect(self.rect(), QColor(canvas_bg))

        w = self.width()
        h = self.height()
        self.scale = min(w, h) / 2.2
        self.offset_x = w / 2
        self.offset_y = h / 2

        if self.sim.mode == 'communities':
            self._draw_communities(painter)
        else:
            self._draw_simple(painter)

    def _to_screen(self, x, y):
        """
        Convert simulation coordinates to screen coordinates.

        Transforms coordinates from the simulation's coordinate system (typically -1 to 1
        or larger for communities) to pixel coordinates on the screen. Handles different
        scaling for simple vs community modes.

        Args:
            x (float): X coordinate in simulation space
            y (float): Y coordinate in simulation space

        Returns:
            tuple: (sx, sy) screen pixel coordinates as integers
        """
        if self.sim.mode == 'communities':
            scale = self.scale / 3.5
            sx = int(self.offset_x + x * scale)
            sy = int(self.offset_y - y * scale)
        else:
            sx = int(self.offset_x + x * self.scale)
            sy = int(self.offset_y - y * self.scale)
        return sx, sy

    def _draw_simple(self, painter):
        """
        Draw the simulation in simple (single boundary) mode.

        Renders:
        - Main boundary box in neon green
        - All active particles
        - Marketplace zone (if enabled)
        - Quarantine zone and quarantined particles (if enabled)

        Args:
            painter (QPainter): Qt painter object for drawing
        """
        # Local import to avoid circular dependency
        import epidemic_sim3
        params = epidemic_sim3.params

        tl = self._to_screen(-1, 1)
        br = self._to_screen(1, -1)
        painter.setPen(QPen(QColor(NEON_GREEN), 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

        for p in self.sim.particles:
            self._draw_particle(painter, p)

        # Draw marketplace zone if enabled
        if params.marketplace_enabled:
            center = self._to_screen(params.marketplace_x, params.marketplace_y)
            radius = int(0.25 * self.scale)  # Marketplace zone radius
            # Use cached colors for better performance
            painter.setPen(QPen(self._color_cache['marketplace_pen'], 2, Qt.DashLine))
            painter.setBrush(QBrush(self._color_cache['marketplace_fill']))
            painter.drawEllipse(center[0] - radius, center[1] - radius, radius * 2, radius * 2)

        # Draw quarantine zone if enabled (always visible when enabled)
        if params.quarantine_enabled:
            # Quarantine box (lower-left corner)
            tl = self._to_screen(-0.95, -0.6)
            br = self._to_screen(-0.6, -0.95)
            # Use cached colors for better performance
            painter.setPen(QPen(self._color_cache['quarantine_pen'], 3))
            painter.setBrush(QBrush(self._color_cache['quarantine_fill']))
            painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

            # Draw quarantined particles if any
            for p in self.sim.quarantine_particles:
                self._draw_particle(painter, p)

    def _draw_communities(self, painter):
        """
        Draw the simulation in communities (grid) mode.

        Renders:
        - All community boundaries
        - Particles within each community
        - Special highlighting for marketplace community (if enabled)
        - Quarantine zone and quarantined particles (if enabled)

        Args:
            painter (QPainter): Qt painter object for drawing
        """
        # Local import to avoid circular dependency
        import epidemic_sim3
        params = epidemic_sim3.params

        for comm_id, comm in self.sim.communities.items():
            bounds = comm['bounds']
            tl = self._to_screen(bounds[0], bounds[3])
            br = self._to_screen(bounds[1], bounds[2])

            # Highlight center tile (marketplace) if marketplace enabled
            if params.marketplace_enabled and comm_id == params.marketplace_community_id:
                # Use cached colors for better performance
                painter.setPen(QPen(self._color_cache['marketplace_pen'], 3))
                painter.setBrush(QBrush(self._color_cache['marketplace_fill']))
            else:
                painter.setPen(QPen(QColor(BORDER_GREEN), 2))
                painter.setBrush(Qt.NoBrush)

            painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

            for p in comm['particles']:
                self._draw_particle(painter, p)

        # Draw quarantine zone if enabled (always visible when enabled)
        if params.quarantine_enabled:
            # Quarantine zone: Lower-left tile (community 0)
            # Highlight with red border and fill
            tl = self._to_screen(-2.9, -1.1)
            br = self._to_screen(-1.1, -2.9)
            # Use cached colors for better performance
            painter.setPen(QPen(self._color_cache['quarantine_pen'], 4))
            painter.setBrush(QBrush(self._color_cache['quarantine_fill']))
            painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

            # Draw quarantined particles if any
            for p in self.sim.quarantine_particles:
                self._draw_particle(painter, p)

    def _draw_particle(self, painter, p):
        """
        Draw a single particle (individual) on the canvas with enhanced visual effects.

        Particles are colored based on their infection state:
        - Susceptible: Cyan/Blue
        - Infected (symptomatic): Red with glow effect
        - Infected (asymptomatic): Orange with glow effect
        - Removed: Gray

        Enhanced features:
        - Glow effect for infected particles (larger semi-transparent halo)
        - Infection radius visualization
        - Cached colors for performance

        Args:
            painter (QPainter): Qt painter object for drawing
            p (Particle): The particle object to draw
        """
        # Local import to avoid circular dependency
        import epidemic_sim3
        params = epidemic_sim3.params
        pos = self._to_screen(p.x, p.y)

        # Draw infection radius circle if enabled and particle is infected
        if params.show_infection_radius and p.state == 'infected':
            radius_world = params.infection_radius
            radius_screen = int(radius_world * self.scale)
            # Use cached colors for better performance
            painter.setPen(QPen(self._color_cache['infection_radius_pen'], 1))
            painter.setBrush(QBrush(self._color_cache['infection_radius_fill']))
            painter.drawEllipse(pos[0] - radius_screen, pos[1] - radius_screen,
                              radius_screen * 2, radius_screen * 2)

        # Use cached colors for particles (major performance improvement)
        if p.state == 'susceptible':
            color = self._color_cache['susceptible']
        elif p.state == 'infected':
            if not p.shows_symptoms:
                color = self._color_cache['infected_asymp']
                glow_color = self._color_cache['infected_asymp_glow']
            else:
                color = self._color_cache['infected_symp']
                glow_color = self._color_cache['infected_symp_glow']

            # Add glow effect for infected particles (visual enhancement)
            if self.enable_glow:
                glow_size = int(params.particle_size * 2.5)
                painter.setBrush(glow_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(pos[0] - glow_size//2, pos[1] - glow_size//2,
                                  glow_size, glow_size)
        else:
            color = self._color_cache['removed']

        # Draw main particle
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        size = params.particle_size
        painter.drawEllipse(pos[0] - size//2, pos[1] - size//2, size, size)
