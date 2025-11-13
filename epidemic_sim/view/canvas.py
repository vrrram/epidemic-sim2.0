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
            painter.setPen(QPen(QColor("#ffaa00"), 2, Qt.DashLine))
            painter.setBrush(QBrush(QColor(255, 170, 0, 30)))
            painter.drawEllipse(center[0] - radius, center[1] - radius, radius * 2, radius * 2)

        # Draw quarantine zone if enabled (always visible when enabled)
        if params.quarantine_enabled:
            # Quarantine box (lower-left corner)
            tl = self._to_screen(-0.95, -0.6)
            br = self._to_screen(-0.6, -0.95)
            painter.setPen(QPen(QColor("#ff0000"), 3))
            painter.setBrush(QBrush(QColor(255, 0, 0, 20)))  # Semi-transparent red fill
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
                painter.setPen(QPen(QColor("#ffaa00"), 3))  # Orange for marketplace
                painter.setBrush(QBrush(QColor(255, 170, 0, 20)))  # Semi-transparent fill
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
            painter.setPen(QPen(QColor("#ff0000"), 4))  # Thicker red border
            painter.setBrush(QBrush(QColor(255, 0, 0, 30)))  # Semi-transparent red fill
            painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

            # Draw quarantined particles if any
            for p in self.sim.quarantine_particles:
                self._draw_particle(painter, p)

    def _draw_particle(self, painter, p):
        """
        Draw a single particle (individual) on the canvas.

        Particles are colored based on their infection state:
        - Susceptible: Cyan/Blue
        - Infected (symptomatic): Red
        - Infected (asymptomatic): Orange
        - Removed: Gray

        If enabled, also draws the infection radius as a semi-transparent circle
        around infected particles.

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
            # Semi-transparent red circle
            painter.setPen(QPen(QColor(255, 0, 0, 100), 1))
            painter.setBrush(QBrush(QColor(255, 0, 0, 30)))
            painter.drawEllipse(pos[0] - radius_screen, pos[1] - radius_screen,
                              radius_screen * 2, radius_screen * 2)

        # Use theme-aware colors for particles
        if p.state == 'susceptible':
            rgb = get_color('PARTICLE_SUSCEPTIBLE')
            color = QColor(rgb[0], rgb[1], rgb[2])
        elif p.state == 'infected':
            if not p.shows_symptoms:
                rgb = get_color('PARTICLE_INFECTED_ASYMP')
                color = QColor(rgb[0], rgb[1], rgb[2])
            else:
                rgb = get_color('PARTICLE_INFECTED_SYMP')
                color = QColor(rgb[0], rgb[1], rgb[2])
        else:
            rgb = get_color('PARTICLE_REMOVED')
            color = QColor(rgb[0], rgb[1], rgb[2])

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        size = params.particle_size
        painter.drawEllipse(pos[0] - size//2, pos[1] - size//2, size, size)
