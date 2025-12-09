"""
SimulationCanvas - Visual rendering component for the epidemic simulation

This module contains the SimulationCanvas class which handles all visual rendering
of the simulation state including particles, boundaries, communities, and special zones.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient

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

    Performance optimizations:
    - Batch rendering groups particles by state for fewer QPainter state changes
    - Glow effects only applied when particle size is sufficient (>=6 pixels)
    - Uses QPainter render hints for quality vs speed tradeoffs

    Attributes:
        sim: Reference to the EpidemicSimulation instance
        scale (float): Scaling factor for coordinate transformation
        offset_x (float): X offset for centering the visualization
        offset_y (float): Y offset for centering the visualization
        _use_batch_rendering (bool): Enable batch rendering for performance
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
        # Performance optimization: enable batch rendering for large particle counts
        self._use_batch_rendering = True
        self._batch_threshold = 100  # Use batch rendering when > 100 particles

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

        rgb = get_color('PARTICLE_DEAD')
        self._color_cache['dead'] = QColor(rgb[0], rgb[1], rgb[2])

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

        # Use batch rendering for large particle counts (better performance)
        if self._use_batch_rendering and len(self.sim.particles) > self._batch_threshold:
            self._draw_particles_batch(painter, self.sim.particles)
        else:
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

        # Collect all community particles for batch rendering
        all_particles = []
        for comm in self.sim.communities.values():
            all_particles.extend(comm['particles'])

        # Use batch rendering for large particle counts (better performance)
        if self._use_batch_rendering and len(all_particles) > self._batch_threshold:
            self._draw_particles_batch(painter, all_particles)
        else:
            for p in all_particles:
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
        - Dead: Dark red

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
        size = params.particle_size

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
            if self.enable_glow and size >= 6:
                glow_size = int(size * 2.5)
                painter.setBrush(glow_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(pos[0] - glow_size//2, pos[1] - glow_size//2,
                                  glow_size, glow_size)
        elif p.state == 'dead':
            color = self._color_cache['dead']
        else:  # removed
            color = self._color_cache['removed']

        # Draw main particle
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(pos[0] - size//2, pos[1] - size//2, size, size)

    def _draw_particles_batch(self, painter, particles):
        """
        Draw multiple particles using batch rendering for improved performance.

        Groups particles by state and renders each group with a single brush setup,
        reducing QPainter state changes and improving performance for large particle counts.

        Args:
            painter (QPainter): Qt painter object for drawing
            particles (list): List of Particle objects to draw
        """
        # Local import to avoid circular dependency
        import epidemic_sim3
        params = epidemic_sim3.params
        size = params.particle_size
        half_size = size // 2

        # Group particles by state for batch rendering
        susceptible = []
        infected_symp = []
        infected_asymp = []
        removed = []
        dead = []

        for p in particles:
            pos = self._to_screen(p.x, p.y)
            if p.state == 'susceptible':
                susceptible.append(pos)
            elif p.state == 'infected':
                if p.shows_symptoms:
                    infected_symp.append(pos)
                else:
                    infected_asymp.append(pos)
            elif p.state == 'dead':
                dead.append(pos)
            else:  # removed
                removed.append(pos)

        painter.setPen(Qt.NoPen)

        # Draw susceptible particles
        if susceptible:
            rgb = get_color('PARTICLE_SUSCEPTIBLE')
            painter.setBrush(QColor(rgb[0], rgb[1], rgb[2]))
            for pos in susceptible:
                painter.drawEllipse(pos[0] - half_size, pos[1] - half_size, size, size)

        # Draw removed particles
        if removed:
            rgb = get_color('PARTICLE_REMOVED')
            painter.setBrush(QColor(rgb[0], rgb[1], rgb[2]))
            for pos in removed:
                painter.drawEllipse(pos[0] - half_size, pos[1] - half_size, size, size)

        # Draw dead particles
        if dead:
            rgb = get_color('PARTICLE_DEAD')
            painter.setBrush(QColor(rgb[0], rgb[1], rgb[2]))
            for pos in dead:
                painter.drawEllipse(pos[0] - half_size, pos[1] - half_size, size, size)

        # Draw asymptomatic infected particles
        if infected_asymp:
            rgb = get_color('PARTICLE_INFECTED_ASYMP')
            painter.setBrush(QColor(rgb[0], rgb[1], rgb[2]))
            for pos in infected_asymp:
                painter.drawEllipse(pos[0] - half_size, pos[1] - half_size, size, size)

        # Draw symptomatic infected particles with glow effect
        if infected_symp:
            rgb = get_color('PARTICLE_INFECTED_SYMP')
            # Draw glow effect first (only if particle size is sufficient)
            if size >= 6:
                glow_size = size + 6
                glow_half = glow_size // 2
                for pos in infected_symp:
                    glow_gradient = QRadialGradient(pos[0], pos[1], glow_half)
                    glow_gradient.setColorAt(0.0, QColor(rgb[0], rgb[1], rgb[2], 80))
                    glow_gradient.setColorAt(0.5, QColor(rgb[0], rgb[1], rgb[2], 40))
                    glow_gradient.setColorAt(1.0, QColor(rgb[0], rgb[1], rgb[2], 0))
                    painter.setBrush(QBrush(glow_gradient))
                    painter.drawEllipse(pos[0] - glow_half, pos[1] - glow_half, glow_size, glow_size)
            # Draw main particles
            painter.setBrush(QColor(rgb[0], rgb[1], rgb[2]))
            for pos in infected_symp:
                painter.drawEllipse(pos[0] - half_size, pos[1] - half_size, size, size)

        # Draw infection radius if enabled (do this separately for clarity)
        if params.show_infection_radius:
            radius_pen = get_color('INFECTION_RADIUS_PEN')
            radius_fill = get_color('INFECTION_RADIUS_FILL')
            radius_world = params.infection_radius
            radius_screen = int(radius_world * self.scale)
            painter.setPen(QPen(QColor(radius_pen[0], radius_pen[1], radius_pen[2], radius_pen[3]), 1))
            painter.setBrush(QBrush(QColor(radius_fill[0], radius_fill[1], radius_fill[2], radius_fill[3])))
            # Draw radius for all infected particles
            for p in particles:
                if p.state == 'infected':
                    pos = self._to_screen(p.x, p.y)
                    painter.drawEllipse(pos[0] - radius_screen, pos[1] - radius_screen,
                                      radius_screen * 2, radius_screen * 2)
