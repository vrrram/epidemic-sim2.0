import sys
import numpy as np
import random
import math
from collections import defaultdict
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# =================== DISTRIBUTION FUNCTIONS DOCUMENTATION ===================
"""
This simulation uses THREE different statistical distribution functions as required
for the IHK vocational project (German: "Berufsschule Abschlussprojekt").

1. UNIFORM DISTRIBUTION (Gleichverteilung)
   - Usage: Particle initial positions (x, y) and velocities (vx, vy)
   - Function: random.uniform(a, b)
   - Mathematical basis: f(x) = 1/(b-a) for a ≤ x ≤ b
   - Justification: All positions and movement directions should be equally likely.
                    No inherent bias in spatial distribution or movement patterns.
   - Examples in code:
     * Line ~253: x = random.uniform(self.bounds[0], self.bounds[1])
     * Line ~159: self.vx = random.uniform(-0.2, 0.2)

2. NORMAL DISTRIBUTION / GAUSSIAN (Normalverteilung)
   - Usage: Individual infection susceptibility (biological variation in immune response)
   - Function: np.random.normal(mean=1.0, std=0.2)
   - Mathematical basis: f(x) = (1/σ√(2π)) * e^(-(x-μ)²/(2σ²))
   - Justification: Biological traits follow bell curve - most people have average
                    immune response, few are very susceptible or very resistant.
                    The Central Limit Theorem applies to biological systems.
   - Effect: Multiplies base infection probability (mean=1.0, so average is unchanged)
   - Example: If base prob=2%, person with susceptibility=1.2 has effective prob=2.4%

3. EXPONENTIAL DISTRIBUTION (Exponentialverteilung)
   - Usage: Recovery time variation (modeling disease progression time)
   - Function: np.random.exponential(scale=1.0)
   - Mathematical basis: f(x) = λ * e^(-λx) where λ = 1/scale
   - Justification: Exponential distribution has "memoryless property" - ideal for
                    modeling time until an event occurs (recovery). Used extensively
                    in epidemiology for event timing (infection, recovery, death).
                    Note: Overall epidemic growth IS exponential (SIR model), but this
                    distribution models individual recovery time variation.
   - Effect: Multiplies base infection duration (mean=1.0, so average is unchanged)
   - Example: If base duration=25 days, person with modifier=1.3 recovers in 32.5 days

IMPLEMENTATION NOTE:
All three distributions are used to create natural variation in the simulation while
maintaining the expected average behavior set by the user's parameters.
"""

# =================== THEME SYSTEM ===================
# Support for Dark and Light themes with easy switching

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
}

# Current theme - can be 'dark' or 'light'
current_theme = DARK_THEME  # Default to dark

# Helper functions for theme access
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

# Backwards compatibility - keep old names pointing to theme system
def _update_legacy_colors():
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

# Initialize legacy colors
NEON_GREEN = "#00ff00"
DARK_GREEN = "#003300"
BG_BLACK = "#000000"
PANEL_BLACK = "#0a0a0a"
BORDER_GREEN = "#00aa00"

# =================== SIMULATION PARAMETERS ===================
class SimParams:
    def __init__(self):
        # Infection parameters (BETTER DEFAULTS)
        self.infection_radius = 0.15
        self.prob_infection = 0.15  # Increased significantly for visible spread (15% per contact)
        self.fraction_infected_init = 0.01
        self.infection_duration = 25

        # Social distancing
        self.social_distance_factor = 0.0
        self.social_distance_obedient = 1.0
        self.boxes_to_consider = 2

        # Particle physics
        self.num_particles = 200
        self.particle_size = 6
        self.speed_limit = 0.1
        self.boundary_force = 0.2
        self.time_steps_per_day = 24

        # Quarantine parameters (LESS AGGRESSIVE)
        self.quarantine_enabled = False  # Toggle quarantine on/off
        self.quarantine_after = 5  # Quarantine earlier (5 days)
        self.start_quarantine = 10   # But start later (day 10)
        self.prob_no_symptoms = 0.20  # 20% asymptomatic (more realistic)

        # Mortality (SEIRD-ready)
        self.mortality_rate = 0.0  # 0-1 (0% to 100%)

        # Communities
        self.travel_probability = 0.02
        self.num_per_community = 60
        self.communities_to_infect = 2

        # Marketplace gathering parameters
        self.marketplace_enabled = False
        self.marketplace_interval = 7  # Days between gatherings (weekly)
        self.marketplace_duration = 2  # Time steps particles stay (hours)
        self.marketplace_attendance = 0.6  # 60% of population attends
        self.marketplace_x = 0.0  # Center location (simple/quarantine mode)
        self.marketplace_y = 0.0
        self.marketplace_community_id = 4  # Center tile in 3x3 grid (communities mode)

        # Visualization options
        self.show_infection_radius = False  # Toggle infection radius visualization

params = SimParams()

# =================== PRESETS ===================
PRESETS = {
    # Educational Presets
    "Baseline Epidemic": {
        'infection_radius': 0.15, 'prob_infection': 0.15, 'fraction_infected_init': 0.01,
        'infection_duration': 25, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 5, 'start_quarantine': 10, 'prob_no_symptoms': 0.20
    },
    "Slow Burn": {
        'infection_radius': 0.10, 'prob_infection': 0.01, 'fraction_infected_init': 0.005,
        'infection_duration': 30, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 8, 'start_quarantine': 15, 'prob_no_symptoms': 0.15
    },
    "Fast Outbreak": {
        'infection_radius': 0.30, 'prob_infection': 0.05, 'fraction_infected_init': 0.02,
        'infection_duration': 20, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 3, 'start_quarantine': 5, 'prob_no_symptoms': 0.25
    },
    "Highly Contagious": {
        'infection_radius': 0.25, 'prob_infection': 0.08, 'fraction_infected_init': 0.01,
        'infection_duration': 15, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 3, 'start_quarantine': 7, 'prob_no_symptoms': 0.30
    },
    "Social Distancing (Weak)": {
        'infection_radius': 0.15, 'prob_infection': 0.02, 'fraction_infected_init': 0.01,
        'infection_duration': 25, 'social_distance_factor': 0.5, 'social_distance_obedient': 0.7,
        'boxes_to_consider': 3, 'quarantine_after': 5, 'start_quarantine': 10, 'prob_no_symptoms': 0.20
    },
    "Social Distancing (Strong)": {
        'infection_radius': 0.15, 'prob_infection': 0.02, 'fraction_infected_init': 0.01,
        'infection_duration': 25, 'social_distance_factor': 1.5, 'social_distance_obedient': 0.9,
        'boxes_to_consider': 4, 'quarantine_after': 5, 'start_quarantine': 10, 'prob_no_symptoms': 0.20
    },

    # Historical Disease Presets
    "COVID-19 (Original)": {
        'infection_radius': 0.15, 'prob_infection': 0.025, 'fraction_infected_init': 0.005,
        'infection_duration': 14, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 5, 'start_quarantine': 10, 'prob_no_symptoms': 0.30
    },
    "COVID-19 (Delta)": {
        'infection_radius': 0.20, 'prob_infection': 0.05, 'fraction_infected_init': 0.005,
        'infection_duration': 10, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 4, 'start_quarantine': 8, 'prob_no_symptoms': 0.40
    },
    "Spanish Flu (1918)": {
        'infection_radius': 0.18, 'prob_infection': 0.03, 'fraction_infected_init': 0.01,
        'infection_duration': 7, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 3, 'start_quarantine': 5, 'prob_no_symptoms': 0.15
    },
    "Measles": {
        'infection_radius': 0.30, 'prob_infection': 0.10, 'fraction_infected_init': 0.005,
        'infection_duration': 10, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 3, 'start_quarantine': 5, 'prob_no_symptoms': 0.05
    },
    "Ebola (2014)": {
        'infection_radius': 0.10, 'prob_infection': 0.08, 'fraction_infected_init': 0.005,
        'infection_duration': 14, 'social_distance_factor': 0.0, 'social_distance_obedient': 1.0,
        'boxes_to_consider': 2, 'quarantine_after': 5, 'start_quarantine': 3, 'prob_no_symptoms': 0.10
    },
}

# =================== SPATIAL HASH GRID ===================
class SpatialGrid:
    def __init__(self, cell_size=0.2):
        self.cell_size = cell_size
        self.grid = defaultdict(list)

    def clear(self):
        self.grid.clear()

    def _hash(self, x, y):
        return (int(x / self.cell_size), int(y / self.cell_size))

    def insert(self, particle):
        cell = self._hash(particle.x, particle.y)
        self.grid[cell].append(particle)

    def get_nearby(self, x, y, radius=1):
        cell_x, cell_y = self._hash(x, y)
        nearby = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nearby.extend(self.grid.get((cell_x + dx, cell_y + dy), []))
        return nearby

# =================== PARTICLE CLASS ===================
class Particle:
    def __init__(self, x, y, state='susceptible'):
        # POSITION (initialized with parameters, will use UNIFORM distribution in simulation)
        self.x = x
        self.y = y

        # VELOCITY - UNIFORM DISTRIBUTION (Gleichverteilung)
        # All directions and speeds equally likely - no inherent movement bias
        self.vx = random.uniform(-0.2, 0.2)
        self.vy = random.uniform(-0.2, 0.2)

        self.ax = 0
        self.ay = 0
        self.state = state
        self.days_infected = 0
        self.quarantined = False
        self.shows_symptoms = True
        self.obeys_social_distance = random.random() < params.social_distance_obedient
        self.infection_count = 0

        # DISTRIBUTION 2: NORMAL DISTRIBUTION (Normalverteilung) - Infection Susceptibility
        # Models biological variation in immune response
        # Mean = 1.0 (average person), Std Dev = 0.2 (variation)
        # Result: Most people near average, few very susceptible/resistant
        # Ensures ~68% of population between 0.8-1.2 susceptibility
        # Value is clamped to positive range to avoid negative susceptibility
        self.infection_susceptibility = max(0.1, np.random.normal(1.0, 0.2))

        # DISTRIBUTION 3: EXPONENTIAL DISTRIBUTION (Exponentialverteilung) - Recovery Time
        # Models time until recovery event occurs
        # Scale = 1.0, so mean = 1.0 (average recovery time unchanged)
        # Exponential has "memoryless property" - ideal for event timing
        # Some recover quickly (<1.0x), others take longer (>1.0x)
        # Value is clamped to reasonable range (0.5x to 3.0x base duration)
        self.recovery_time_modifier = np.clip(np.random.exponential(1.0), 0.5, 3.0)

        # Marketplace tracking
        self.at_marketplace = False
        self.marketplace_timer = 0
        self.home_x = x
        self.home_y = y
        self.traveling_to_marketplace = False
        self.returning_home = False
        self.target_x = x
        self.target_y = y

        # Community travel tracking
        self.traveling_between_communities = False
        self.target_community_id = None

        if state == 'infected' and random.random() < params.prob_no_symptoms:
            self.shows_symptoms = False

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)

# =================== EPIDEMIC SIMULATION ===================
class EpidemicSimulation(QObject):
    stats_updated = pyqtSignal(dict)
    log_message = pyqtSignal(str)

    def __init__(self, mode='simple'):
        super().__init__()
        self.mode = mode
        self.bounds = (-1, 1, -1, 1)
        self.particles = []
        self.quarantine_particles = []
        self.communities = {}
        self.spatial_grid = SpatialGrid()

        self.time_count = 0
        self.day_count = 0
        self.time_step = 1.0 / params.time_steps_per_day
        self.last_marketplace_day = -params.marketplace_interval  # Start ready

        self.stats = {
            'susceptible': [100],
            'infected': [0],
            'removed': [0],
            'dead': [0],  # Track deaths separately (SEIRD-ready)
            'day': [0]
        }
        self.initial_population = 0  # Set during initialization

    def log(self, message):
        self.log_message.emit(f"[DAY {self.day_count:03d}] {message}")

    def initialize(self):
        self.particles = []
        self.quarantine_particles = []
        self.communities = {}
        self.time_count = 0
        self.day_count = 0
        self.last_marketplace_day = -params.marketplace_interval  # Reset marketplace
        self.stats = {
            'susceptible': [100],
            'infected': [0],
            'removed': [0],
            'dead': [0],
            'day': [0]
        }
        self.initial_population = 0  # Will be set based on mode

        self.log(f"INITIALIZING {self.mode.upper()} SIMULATION...")

        if self.mode == 'communities':
            self._init_communities()
        else:
            self._init_simple()

        self._update_stats()

    def _init_simple(self):
        num_infected = max(1, int(params.num_particles * params.fraction_infected_init))
        self.log(f"SPAWNING {params.num_particles} PARTICLES ({num_infected} INFECTED)")

        for i in range(params.num_particles):
            # UNIFORM DISTRIBUTION: Particle positions randomly distributed
            # All positions within bounds equally likely - no clustering or bias
            x = random.uniform(self.bounds[0] + 0.15, self.bounds[1] - 0.15)
            y = random.uniform(self.bounds[2] + 0.15, self.bounds[3] - 0.15)
            state = 'infected' if i < num_infected else 'susceptible'
            self.particles.append(Particle(x, y, state))

        self.initial_population = params.num_particles

        if num_infected > 0:
            self.log(f">> PATIENT ZERO INITIALIZED: {num_infected} INITIAL INFECTION(S)")

    def _init_communities(self):
        num_to_infect = max(1, min(params.communities_to_infect, 9))
        infected_communities = random.sample(range(9), num_to_infect)
        self.log(f"CREATING 9 COMMUNITIES (INFECTING: {infected_communities})")

        total_infected = 0
        for i in range(3):
            for j in range(3):
                comm_id = i * 3 + j
                bounds = (-3 + i * 2.2, -1 + i * 2.2, -3 + j * 2.2, -1 + j * 2.2)
                self.communities[comm_id] = {
                    'bounds': bounds,
                    'particles': []
                }

                if comm_id in infected_communities:
                    num_infected = max(1, int(params.num_per_community * params.fraction_infected_init))
                else:
                    num_infected = 0

                total_infected += num_infected

                for k in range(params.num_per_community):
                    # UNIFORM DISTRIBUTION: Particle positions within each community
                    # Ensures equal spatial distribution within community bounds
                    x = random.uniform(bounds[0] + 0.1, bounds[1] - 0.1)
                    y = random.uniform(bounds[2] + 0.1, bounds[3] - 0.1)
                    state = 'infected' if k < num_infected else 'susceptible'
                    self.communities[comm_id]['particles'].append(Particle(x, y, state))

        self.initial_population = params.num_per_community * 9
        self.log(f"TOTAL: {self.initial_population} PARTICLES ({total_infected} INFECTED)")
        self.log(f">> PATIENT ZERO INITIALIZED IN {num_to_infect} COMMUNIT{'Y' if num_to_infect == 1 else 'IES'}")

    def get_all_particles(self):
        if self.mode == 'communities':
            all_p = []
            for comm in self.communities.values():
                all_p.extend(comm['particles'])
            return all_p + self.quarantine_particles
        return self.particles + self.quarantine_particles

    def _clamp_to_bounds(self, particle, bounds):
        margin = 0.05

        if particle.x < bounds[0] + margin:
            particle.x = bounds[0] + margin
            particle.vx = abs(particle.vx) * 0.5
        elif particle.x > bounds[1] - margin:
            particle.x = bounds[1] - margin
            particle.vx = -abs(particle.vx) * 0.5

        if particle.y < bounds[2] + margin:
            particle.y = bounds[2] + margin
            particle.vy = abs(particle.vy) * 0.5
        elif particle.y > bounds[3] - margin:
            particle.y = bounds[3] - margin
            particle.vy = -abs(particle.vy) * 0.5

    def _update_particle_physics(self, particle, bounds, nearby_particles):
        # Handle marketplace movement first (overrides normal physics)
        self._update_marketplace_movement(particle)

        # Skip normal physics if traveling (marketplace or communities)
        # Use overall simulation bounds to allow border crossing
        if particle.traveling_to_marketplace or particle.returning_home or particle.traveling_between_communities:
            particle.x += particle.vx * self.time_step
            particle.y += particle.vy * self.time_step
            self._clamp_to_bounds(particle, self.bounds)  # Use overall bounds for travel

            # Check if particle reached destination community
            if particle.traveling_between_communities:
                dist = math.sqrt((particle.x - particle.target_x)**2 + (particle.y - particle.target_y)**2)
                if dist < 0.1:  # Arrived
                    particle.traveling_between_communities = False
                    particle.vx = random.uniform(-0.2, 0.2)
                    particle.vy = random.uniform(-0.2, 0.2)
            return

        fx, fy = 0, 0
        min_dist = 0.15

        dist_left = particle.x - bounds[0]
        dist_right = bounds[1] - particle.x
        dist_bottom = particle.y - bounds[2]
        dist_top = bounds[3] - particle.y

        if dist_left < min_dist:
            fx += params.boundary_force * (1 - dist_left/min_dist)
        if dist_right < min_dist:
            fx -= params.boundary_force * (1 - dist_right/min_dist)
        if dist_bottom < min_dist:
            fy += params.boundary_force * (1 - dist_bottom/min_dist)
        if dist_top < min_dist:
            fy -= params.boundary_force * (1 - dist_top/min_dist)

        if params.social_distance_factor > 0 and particle.obeys_social_distance:
            sd_radius = params.infection_radius * params.boxes_to_consider
            for other in nearby_particles:
                if other is particle:
                    continue
                dist = particle.distance_to(other)
                if 0.001 < dist < sd_radius:
                    force = params.social_distance_factor / (dist ** 2 + 0.01)
                    dx = particle.x - other.x
                    dy = particle.y - other.y
                    fx += force * dx / (dist + 0.001) / 50
                    fy += force * dy / (dist + 0.001) / 50

        particle.ax = random.uniform(-0.002, 0.002)
        particle.ay = random.uniform(-0.002, 0.002)

        particle.vx += (particle.ax + fx) * self.time_step
        particle.vy += (particle.ay + fy) * self.time_step

        speed = math.sqrt(particle.vx**2 + particle.vy**2)
        max_speed = 0.05 if params.social_distance_factor > 0.3 else params.speed_limit
        if speed > max_speed:
            particle.vx *= max_speed / speed
            particle.vy *= max_speed / speed

        particle.x += particle.vx * self.time_step
        particle.y += particle.vy * self.time_step

        self._clamp_to_bounds(particle, bounds)

    def _check_infections(self, particle_list):
        self.spatial_grid.clear()

        susceptible = [p for p in particle_list if p.state == 'susceptible']
        for p in susceptible:
            self.spatial_grid.insert(p)

        new_infections = 0
        infected_particles = [p for p in particle_list if p.state == 'infected']

        for inf_p in infected_particles:
            nearby = self.spatial_grid.get_nearby(inf_p.x, inf_p.y, radius=2)
            for sus_p in nearby:
                dist = inf_p.distance_to(sus_p)
                if dist < params.infection_radius:
                    # APPLY NORMAL DISTRIBUTION: Infection probability modified by susceptibility
                    # Base probability adjusted by individual's immune response (susceptibility)
                    # Susceptibility from Normal distribution (mean=1.0, std=0.2)
                    # Example: susceptibility=1.2 means 20% more likely to get infected
                    effective_prob = (params.prob_infection / params.time_steps_per_day) * sus_p.infection_susceptibility

                    if random.random() < effective_prob:
                        sus_p.state = 'infected'
                        sus_p.days_infected = 0
                        inf_p.infection_count += 1

                        if random.random() < params.prob_no_symptoms:
                            sus_p.shows_symptoms = False

                        new_infections += 1

        if new_infections > 0:
            self.log(f">> {new_infections} NEW INFECTION(S)")

        return new_infections

    def _update_infections(self, particle_list):
        to_quarantine = []
        to_remove_dead = []  # Particles that died
        recovered = 0
        died = 0

        for p in particle_list:
            if p.state == 'infected':
                p.days_infected += 1

                # APPLY EXPONENTIAL DISTRIBUTION: Recovery time modified by individual variation
                # Base infection duration adjusted by recovery time modifier
                # Modifier from Exponential distribution (scale=1.0, so mean=1.0)
                # Example: modifier=1.3 means recovery takes 30% longer than average
                # Exponential models "time until event" - appropriate for disease progression
                effective_duration = params.infection_duration * p.recovery_time_modifier

                if p.days_infected >= effective_duration:
                    # Infection ends - roll for mortality
                    if random.random() < params.mortality_rate:
                        # Particle dies
                        p.state = 'dead'
                        to_remove_dead.append(p)
                        died += 1
                    else:
                        # Particle recovers
                        p.state = 'removed'
                        recovered += 1

                elif (params.quarantine_enabled and
                      p.days_infected >= params.quarantine_after and
                      self.day_count >= params.start_quarantine and
                      p.shows_symptoms and
                      not p.quarantined):
                    to_quarantine.append(p)

        if recovered > 0:
            self.log(f">> {recovered} RECOVERED")
        if died > 0:
            self.log(f">> {died} DIED (mortality: {params.mortality_rate*100:.1f}%)")

        return to_quarantine, to_remove_dead

    def _move_to_quarantine(self, particle, from_list):
        particle.quarantined = True
        particle.obeys_social_distance = False

        # Smaller quarantine zone (top-left corner)
        particle.x = random.uniform(-1.5, -1.15)
        particle.y = random.uniform(0.7, 0.95)
        particle.vx = random.uniform(-0.05, 0.05)
        particle.vy = random.uniform(-0.05, 0.05)

        from_list.remove(particle)
        self.quarantine_particles.append(particle)

    def _get_marketplace_location(self):
        """Get marketplace center location based on mode"""
        if self.mode == 'communities':
            # Use center community bounds
            center_comm = self.communities[params.marketplace_community_id]
            bounds = center_comm['bounds']
            # Return center of center community
            return (
                (bounds[0] + bounds[1]) / 2,
                (bounds[2] + bounds[3]) / 2
            )
        else:
            # Simple/quarantine mode: use configured location
            return (params.marketplace_x, params.marketplace_y)

    def _handle_marketplace(self, particle_list):
        """Handle marketplace gathering events with smooth movement"""
        if not params.marketplace_enabled:
            return 0

        # Check if it's marketplace day
        days_since_last = self.day_count - self.last_marketplace_day
        if days_since_last >= params.marketplace_interval:
            self._start_marketplace_gathering(particle_list)

        # Update marketplace timers
        self._update_marketplace_timers(particle_list)
        return 0

    def _start_marketplace_gathering(self, particle_list):
        """Start a new marketplace gathering event"""
        self.last_marketplace_day = self.day_count
        market_x, market_y = self._get_marketplace_location()

        attending = 0
        for p in particle_list:
            if (not p.quarantined and
                not p.traveling_to_marketplace and
                not p.at_marketplace and
                random.random() < params.marketplace_attendance):

                p.traveling_to_marketplace = True
                p.marketplace_timer = params.marketplace_duration
                p.home_x = p.x
                p.home_y = p.y
                # Set target location at marketplace
                p.target_x = market_x + random.uniform(-0.15, 0.15)
                p.target_y = market_y + random.uniform(-0.15, 0.15)
                attending += 1

        if attending > 0:
            location_desc = "CENTER TILE" if self.mode == 'communities' else "CENTER"
            self.log(f">> MARKETPLACE @ {location_desc}: {attending} TRAVELING")

    def _update_marketplace_timers(self, particle_list):
        """Update marketplace attendance timers"""
        for p in particle_list:
            if p.at_marketplace:
                p.marketplace_timer -= 1
                if p.marketplace_timer <= 0:
                    # Start returning home
                    p.at_marketplace = False
                    p.returning_home = True
                    p.target_x = p.home_x + random.uniform(-0.1, 0.1)
                    p.target_y = p.home_y + random.uniform(-0.1, 0.1)

    def _update_marketplace_movement(self, particle):
        """Smoothly move particles to/from marketplace"""
        if particle.traveling_to_marketplace:
            # Move toward marketplace
            dx = particle.target_x - particle.x
            dy = particle.target_y - particle.y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < 0.05:  # Arrived
                particle.traveling_to_marketplace = False
                particle.at_marketplace = True
                particle.vx = random.uniform(-0.02, 0.02)
                particle.vy = random.uniform(-0.02, 0.02)
            else:
                # Move at constant speed toward target
                speed = 0.08
                particle.vx = (dx / dist) * speed
                particle.vy = (dy / dist) * speed

        elif particle.returning_home:
            # Move toward home
            dx = particle.target_x - particle.x
            dy = particle.target_y - particle.y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < 0.05:  # Arrived home
                particle.returning_home = False
                particle.vx = random.uniform(-0.02, 0.02)
                particle.vy = random.uniform(-0.02, 0.02)
            else:
                # Move at constant speed toward home
                speed = 0.08
                particle.vx = (dx / dist) * speed
                particle.vy = (dy / dist) * speed

    def step(self):
        if self.mode == 'communities':
            for comm in self.communities.values():
                self.spatial_grid.clear()
                for p in comm['particles']:
                    self.spatial_grid.insert(p)

                for p in comm['particles']:
                    nearby = self.spatial_grid.get_nearby(p.x, p.y, radius=params.boxes_to_consider)
                    self._update_particle_physics(p, comm['bounds'], nearby)
        else:
            self.spatial_grid.clear()
            for p in self.particles:
                self.spatial_grid.insert(p)

            for p in self.particles:
                nearby = self.spatial_grid.get_nearby(p.x, p.y, radius=params.boxes_to_consider)
                self._update_particle_physics(p, self.bounds, nearby)

        if self.quarantine_particles:
            # Smaller quarantine zone
            q_bounds = (-1.5, -1.15, 0.7, 0.95)
            self.spatial_grid.clear()
            for p in self.quarantine_particles:
                self.spatial_grid.insert(p)
            for p in self.quarantine_particles:
                nearby = self.spatial_grid.get_nearby(p.x, p.y, radius=params.boxes_to_consider)
                self._update_particle_physics(p, q_bounds, nearby)

        if self.time_count % params.time_steps_per_day == 0:
            self.log(f"==================== DAY {self.day_count + 1} ====================")

            if self.mode == 'communities':
                total_new_infections = 0
                total_quarantined = 0

                for comm in self.communities.values():
                    total_new_infections += self._check_infections(comm['particles'])
                    to_q, to_dead = self._update_infections(comm['particles'])
                    total_quarantined += len(to_q)
                    for p in to_q:
                        self._move_to_quarantine(p, comm['particles'])
                    # Remove dead particles efficiently (build new list instead of removing)
                    if to_dead:
                        to_dead_set = set(to_dead)
                        comm['particles'] = [p for p in comm['particles'] if p not in to_dead_set]

                if self.quarantine_particles:
                    self._check_infections(self.quarantine_particles)
                    _, to_dead = self._update_infections(self.quarantine_particles)
                    # Remove dead particles from quarantine efficiently
                    if to_dead:
                        to_dead_set = set(to_dead)
                        self.quarantine_particles = [p for p in self.quarantine_particles if p not in to_dead_set]

                if total_quarantined > 0:
                    self.log(f">> {total_quarantined} MOVED TO QUARANTINE")

                if random.random() < 0.3:
                    travelers = self._handle_community_travel()
                    if travelers > 0:
                        self.log(f">> {travelers} TRAVELED BETWEEN COMMUNITIES")

                # Handle marketplace in communities mode - center tile becomes marketplace
                if params.marketplace_enabled:
                    all_comm_particles = []
                    for comm in self.communities.values():
                        all_comm_particles.extend(comm['particles'])
                    self._handle_marketplace(all_comm_particles)

            else:
                self._check_infections(self.particles)
                to_q, to_dead = self._update_infections(self.particles)

                if to_q:
                    self.log(f">> {len(to_q)} MOVED TO QUARANTINE")
                    for p in to_q:
                        self._move_to_quarantine(p, self.particles)

                # Remove dead particles efficiently
                if to_dead:
                    to_dead_set = set(to_dead)
                    self.particles = [p for p in self.particles if p not in to_dead_set]

                if self.quarantine_particles:
                    self._check_infections(self.quarantine_particles)
                    _, to_dead = self._update_infections(self.quarantine_particles)
                    # Remove dead particles from quarantine efficiently
                    if to_dead:
                        to_dead_set = set(to_dead)
                        self.quarantine_particles = [p for p in self.quarantine_particles if p not in to_dead_set]

                # Handle marketplace events (simple/quarantine modes)
                self._handle_marketplace(self.particles)

            self._update_stats()
            self.day_count += 1

        self.time_count += 1

    def _handle_community_travel(self):
        travelers = 0
        for comm_id, comm in self.communities.items():
            to_travel = []
            for p in comm['particles']:
                if not p.quarantined and not p.traveling_between_communities and random.random() < params.travel_probability / params.time_steps_per_day:
                    to_travel.append(p)

            for p in to_travel:
                other_comms = [c for c in range(9) if c != comm_id]
                target_comm_id = random.choice(other_comms)
                target_bounds = self.communities[target_comm_id]['bounds']

                # Set target location in destination community
                p.target_x = random.uniform(target_bounds[0] + 0.1, target_bounds[1] - 0.1)
                p.target_y = random.uniform(target_bounds[2] + 0.1, target_bounds[3] - 0.1)
                p.traveling_between_communities = True
                p.target_community_id = target_comm_id

                # Set velocity towards target
                dx = p.target_x - p.x
                dy = p.target_y - p.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 0:
                    speed = 0.15  # Travel speed
                    p.vx = (dx / dist) * speed
                    p.vy = (dy / dist) * speed

                # Move particle to destination community list
                comm['particles'].remove(p)
                self.communities[target_comm_id]['particles'].append(p)
                travelers += 1

        return travelers

    def _update_stats(self):
        all_p = self.get_all_particles()
        current_population = len(all_p)

        # Calculate deaths as difference from initial population
        deaths = self.initial_population - current_population

        if self.initial_population == 0:
            return

        counts = {'susceptible': 0, 'infected': 0, 'removed': 0, 'dead': deaths}
        for p in all_p:
            counts[p.state] += 1

        # Calculate percentages based on initial population
        for state in ['susceptible', 'infected', 'removed']:
            percent = (counts[state] / self.initial_population) * 100
            self.stats[state].append(percent)

        # Deaths as percentage of initial population
        death_percent = (deaths / self.initial_population) * 100
        self.stats['dead'].append(death_percent)

        self.stats['day'].append(self.day_count)
        self.stats_updated.emit(counts)

# =================== VISUALIZATION ===================
class SimulationCanvas(QWidget):
    def __init__(self, sim):
        super().__init__()
        self.sim = sim
        self.setMinimumSize(900, 900)

    def paintEvent(self, event):
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
        if self.sim.mode == 'communities':
            scale = self.scale / 3.5
            sx = int(self.offset_x + x * scale)
            sy = int(self.offset_y - y * scale)
        else:
            sx = int(self.offset_x + x * self.scale)
            sy = int(self.offset_y - y * self.scale)
        return sx, sy

    def _draw_simple(self, painter):
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

        if params.quarantine_enabled and self.sim.quarantine_particles:
            # Smaller quarantine box (top-left)
            tl = self._to_screen(-1.5, 0.95)
            br = self._to_screen(-1.15, 0.7)
            painter.setPen(QPen(QColor("#ff0000"), 3))
            painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

            for p in self.sim.quarantine_particles:
                self._draw_particle(painter, p)

    def _draw_communities(self, painter):
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

        if params.quarantine_enabled and self.sim.quarantine_particles:
            tl = self._to_screen(-1.5, 0.95)
            br = self._to_screen(-1.15, 0.7)
            painter.setPen(QPen(QColor("#ff0000"), 3))
            painter.drawRect(tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

            for p in self.sim.quarantine_particles:
                self._draw_particle(painter, p)

    def _draw_particle(self, painter, p):
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

# =================== COLLAPSIBLE GROUP BOX ===================
class CollapsibleBox(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.toggle_button = QPushButton(f"▼ {title}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px;
                font-weight: bold;
                border: 2px solid {BORDER_GREEN};
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #002200;
                border-color: {NEON_GREEN};
            }}
        """)
        self.toggle_button.clicked.connect(self.toggle)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(3)
        self.content_area.setLayout(self.content_layout)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 3)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_area)

    def toggle(self):
        checked = self.toggle_button.isChecked()
        self.content_area.setVisible(checked)
        icon = "▼" if checked else "▶"
        current_text = self.toggle_button.text()
        self.toggle_button.setText(f"{icon} {current_text[2:]}")

        # Force the parent to recalculate its size
        if checked:
            self.content_area.setMaximumHeight(16777215)  # QWIDGETSIZE_MAX
        else:
            self.content_area.setMaximumHeight(0)

        # Trigger layout update
        self.updateGeometry()
        if self.parent():
            self.parent().updateGeometry()

    def update_theme(self):
        """Update collapsible box theme colors"""
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px;
                font-weight: bold;
                border: 2px solid {BORDER_GREEN};
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {DARK_GREEN};
                border-color: {NEON_GREEN};
            }}
        """)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        self.content_layout.addLayout(layout)

# =================== PIE CHART WIDGET ===================
class PieChartWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(BG_BLACK)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setStyleSheet(f"background-color: {BG_BLACK};")

    def update_chart(self, counts):
        """Update pie chart with current population counts"""
        self.axes.clear()

        total = sum(counts.values())
        if total == 0:
            return

        # Separate infected into symptomatic and asymptomatic
        infected_total = counts['infected']
        asymptomatic = infected_total * params.prob_no_symptoms
        symptomatic = infected_total * (1 - params.prob_no_symptoms)

        # Prepare data
        labels = []
        sizes = []
        colors = []

        if counts['susceptible'] > 0:
            labels.append('Susceptible')
            sizes.append(counts['susceptible'])
            colors.append('#00bfff')

        if symptomatic > 0.5:
            labels.append('Infected (Symp.)')
            sizes.append(symptomatic)
            colors.append('#ff4545')

        if asymptomatic > 0.5:
            labels.append('Infected (Asymp.)')
            sizes.append(asymptomatic)
            colors.append('#ffa500')

        if counts['removed'] > 0:
            labels.append('Removed')
            sizes.append(counts['removed'])
            colors.append('#787878')

        if counts['dead'] > 0:
            labels.append('Dead')
            sizes.append(counts['dead'])
            colors.append('#500000')  # Dark red/black

        if not sizes:
            return

        # Create pie chart with percentages only (no labels on slices)
        wedges, texts, autotexts = self.axes.pie(
            sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            textprops={'fontsize': 9, 'weight': 'bold'}
        )

        # Style percentage text to be readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)

        # Add legend outside the pie to avoid overlap
        self.axes.legend(
            wedges, labels,
            loc="center left",
            bbox_to_anchor=(0.85, 0, 0.5, 1),
            fontsize=9,
            frameon=True,
            facecolor=BG_BLACK,
            edgecolor=NEON_GREEN,
            labelcolor=NEON_GREEN
        )

        self.axes.set_facecolor(BG_BLACK)
        self.fig.tight_layout()
        self.draw()

# =================== MAIN WINDOW ===================
class EpidemicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EPIDEMIC SIMULATION v3.0 - Enhanced Edition")
        self.setGeometry(50, 50, 1800, 1000)

        # Load saved theme preference
        self.settings = QSettings("EpidemicSimulator", "Theme")
        saved_theme = self.settings.value("theme", "dark")  # Default to dark
        self.load_theme(saved_theme)

        # Load saved font size preference
        self.base_font_size = int(self.settings.value("font_size", 10))

        self.sim = EpidemicSimulation('simple')
        self.sim.stats_updated.connect(self.update_stats_display)
        self.sim.log_message.connect(self.add_log)

        self.speed = 1.0
        self.paused = False
        self.speed_accumulator = 0.0  # For smooth fractional speed

        # Track collapsible boxes for theme updates
        self.collapsible_boxes = []

        # Performance optimization: frame skipping
        self.frame_count = 0
        self.skip_frames = 1  # Render every Nth frame (adjusted dynamically)

        self.setup_ui()
        self.sim.initialize()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # 60 FPS target

    def setup_ui(self):
        """Setup UI: Left params (collapsible) + Center canvas + Right controls"""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === LEFT PANEL: PARAMETERS (COLLAPSIBLE) ===
        self.left_panel = QWidget()
        self.left_panel.setStyleSheet(f"background-color: {BG_BLACK};")
        self.left_panel.setMaximumWidth(350)
        self.left_panel.setMinimumWidth(300)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(self.left_panel)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {BG_BLACK}; border-right: 2px solid {BORDER_GREEN}; }}
            QScrollBar:vertical {{
                background-color: {PANEL_BLACK}; width: 12px;
                border: 1px solid {BORDER_GREEN};
            }}
            QScrollBar::handle:vertical {{
                background-color: {BORDER_GREEN}; min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Collapse button
        collapse_btn = QPushButton("COLLAPSE PARAMETERS <<")
        collapse_btn.clicked.connect(self.toggle_left_panel)
        collapse_btn.setMinimumHeight(30)
        left_layout.addWidget(collapse_btn)
        self.left_collapse_btn = collapse_btn

        # === LEFT PANEL: ALL PARAMETERS ===
        self.sliders = {}

        # DISEASE PARAMETERS
        disease_box = CollapsibleBox("DISEASE PARAMETERS")
        self.collapsible_boxes.append(disease_box)

        # Define tooltips for disease parameters
        disease_tooltips = {
            'infection_radius': """Infection Radius: How far the disease can spread between particles

Recommended: 0.10-0.20
• Smaller (0.05-0.10): Localized outbreaks, slow spread
• Medium (0.10-0.20): Realistic epidemic behavior
• Larger (0.20-0.40): Rapid, aggressive spread

Tip: Combine with infection probability for fine control""",

            'prob_infection': """Infection Probability: Chance of transmission when particles are within infection radius

Recommended: 0.10-0.30
• Low (0.05-0.15): Slow spread, allows time for interventions
• Medium (0.15-0.50): Realistic epidemic dynamics
• High (0.50-1.00): Extremely contagious disease

Tip: Modified by individual susceptibility (Normal distribution)""",

            'infection_duration': """Infection Duration: How many days a particle remains infected

Recommended: 14-28 days
• Short (1-7 days): Quick recovery, rapid turnover
• Medium (7-21 days): Typical viral infection
• Long (21-100 days): Chronic infection

Tip: Modified by recovery time variation (Exponential distribution)""",

            'mortality_rate': """Mortality Rate: Probability that an infected particle dies instead of recovering

Recommended: 0.00-0.05
• 0%: No deaths, pure SIR model
• 1-5%: Realistic mortality for serious diseases
• 5-20%: High-mortality outbreak
• >20%: Extreme scenario

Tip: Deaths remove particles permanently from simulation""",

            'fraction_infected_init': """Initial Infected %: Percentage of population starting as infected (Patient Zero)

Recommended: 0.005-0.02 (0.5%-2%)
• Very Low (0.001-0.005): Single patient zero scenario
• Low (0.005-0.02): Few initial cases
• Medium (0.02-0.05): Multiple outbreak sources

Tip: Lower values show clearer epidemic curve development"""
        }

        disease_params = [
            ('infection_radius', 'Infection Radius', 0.01, 0.4, 0.15),
            ('prob_infection', 'Infection Probability', 0, 1.0, 0.15),
            ('infection_duration', 'Infection Duration (days)', 1, 100, 25),
            ('mortality_rate', 'Mortality Rate', 0, 1.0, 0.0),
            ('fraction_infected_init', 'Initial Infected %', 0, 0.05, 0.01),
        ]
        for param, label, min_val, max_val, default in disease_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 11px; margin-top: 4px;")
            lbl.setToolTip(disease_tooltips.get(param, label))
            disease_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(disease_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            disease_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(disease_box)

        # POPULATION PARAMETERS
        pop_box = CollapsibleBox("POPULATION PARAMETERS")
        self.collapsible_boxes.append(pop_box)

        # Define tooltips for population parameters
        pop_tooltips = {
            'num_particles': """Population Size: Number of particles (people) in the simulation

Recommended: 200-500 for balance of detail and performance
• Small (50-200): Fast, good for testing, less realistic statistics
• Medium (200-500): Balanced performance and statistical validity
• Large (500-1000): More realistic, slower performance

Tip: Requires RESET to apply. Larger populations need more time to show trends""",

            'social_distance_factor': """Social Distancing Strength: Repulsive force between nearby particles

Recommended: 0.5-1.5
• 0: No social distancing, normal behavior
• 0.5-1.0: Moderate distancing, maintaining personal space
• 1.0-2.0: Strong distancing, active avoidance

Tip: Simulates behavior changes during epidemic awareness""",

            'social_distance_obedient': """Social Distance Compliance: Percentage of population following distancing rules

Recommended: 0.5-0.9
• Low (0-0.5): Poor compliance, many ignore rules
• Medium (0.5-0.8): Realistic mixed compliance
• High (0.8-1.0): Excellent public cooperation

Tip: Combine with distance strength to model intervention effectiveness"""
        }

        # Population size slider (integer, requires reset)
        pop_lbl = QLabel(f"Population Size: {params.num_particles} (reset to apply)")
        pop_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 11px; margin-top: 4px;")
        pop_lbl.setToolTip(pop_tooltips['num_particles'])
        pop_box.addWidget(pop_lbl)
        pop_slider = QSlider(Qt.Horizontal)
        pop_slider.setMinimum(50)
        pop_slider.setMaximum(1000)
        pop_slider.setValue(params.num_particles)
        pop_slider.setMinimumHeight(22)
        pop_slider.setToolTip(pop_tooltips['num_particles'])
        pop_slider.valueChanged.connect(
            lambda val: self.update_param('num_particles', val, pop_lbl, 'Population Size', is_int=True)
        )
        pop_box.addWidget(pop_slider)
        self.sliders['num_particles'] = (pop_slider, pop_lbl, 'Population Size')

        # Other population parameters (floats)
        pop_params = [
            ('social_distance_factor', 'Social Distancing Strength', 0, 2, 0),
            ('social_distance_obedient', 'Social Distance Compliance', 0, 1, 1.0),
        ]
        for param, label, min_val, max_val, default in pop_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 11px; margin-top: 4px;")
            lbl.setToolTip(pop_tooltips.get(param, label))
            pop_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(pop_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            pop_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(pop_box)

        # INTERVENTION PARAMETERS
        interv_box = CollapsibleBox("INTERVENTION PARAMETERS")
        self.collapsible_boxes.append(interv_box)

        # Define tooltips for intervention parameters
        interv_tooltips = {
            'boxes_to_consider': """Social Distance Range: How many grid cells away particles check for crowding

Recommended: 1-3
• 1: Only immediate neighbors affect distancing
• 2-3: Moderate awareness of surrounding density
• 4-10: Wide-area crowd avoidance

Tip: Higher values increase computation but more realistic behavior""",

            'quarantine_after': """Quarantine After (days): Days infected before symptomatic particles quarantine

Recommended: 3-7 days
• Short (1-3): Quick isolation, unrealistic early detection
• Medium (3-7): Realistic symptom onset timing
• Long (7-20): Delayed response, more spread before isolation

Tip: Only applies to symptomatic cases (see Asymptomatic Rate)""",

            'start_quarantine': """Quarantine Start Day: Simulation day when quarantine policy begins

Recommended: 10-20 days
• Early (0-10): Proactive intervention before major spread
• Medium (10-20): Reactive after outbreak detected
• Late (20-30): Delayed response, epidemic already advanced

Tip: Set to 0 for immediate quarantine from start""",

            'prob_no_symptoms': """Asymptomatic Rate: Proportion of infected who never show symptoms

Recommended: 0.15-0.30 (15-30%)
• Low (0-0.15): Most infections detectable
• Medium (0.15-0.30): Realistic for many diseases (e.g., COVID-19)
• High (0.30-0.50): Many hidden spreaders

Tip: Asymptomatic particles never quarantine, continuing to spread disease"""
        }

        interv_params = [
            ('boxes_to_consider', 'Social Distance Range', 1, 10, 2),
            ('quarantine_after', 'Quarantine After (days)', 1, 20, 5),
            ('start_quarantine', 'Quarantine Start Day', 0, 30, 10),
            ('prob_no_symptoms', 'Asymptomatic Rate', 0, 0.5, 0.20),
        ]
        for param, label, min_val, max_val, default in interv_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 11px; margin-top: 4px;")
            lbl.setToolTip(interv_tooltips.get(param, label))
            interv_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(interv_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            interv_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(interv_box)

        # PRESETS
        presets_box = CollapsibleBox("PRESETS")
        self.collapsible_boxes.append(presets_box)
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("-- Select Preset --")
        for preset_name in PRESETS.keys():
            self.preset_combo.addItem(preset_name)
        self.preset_combo.currentTextChanged.connect(self.load_preset)
        self.preset_combo.setToolTip("""Preset Scenarios: Pre-configured parameter sets for common epidemic scenarios

Available presets:
• Baseline: No interventions, natural spread
• Lockdown: Strict quarantine measures
• Social Distance: Population-wide distancing
• High Mortality: Severe disease scenario
• Fast Spread: Highly contagious disease
• Communities: Isolated population groups

Tip: Use keyboard shortcuts 1-9 to quickly load presets""")
        presets_box.addWidget(self.preset_combo)
        left_layout.addWidget(presets_box)

        left_layout.addStretch()

        main_layout.addWidget(left_scroll)

        # === CENTER: CANVAS ===
        self.canvas = SimulationCanvas(self.sim)
        main_layout.addWidget(self.canvas, 5)

        # === RIGHT PANEL: CONTROLS ===
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet(f"background-color: {BG_BLACK};")
        self.right_panel.setMaximumWidth(400)
        self.right_panel.setMinimumWidth(350)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(self.right_panel)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        right_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {BG_BLACK}; border-left: 2px solid {BORDER_GREEN}; }}
            QScrollBar:vertical {{
                background-color: {PANEL_BLACK}; width: 12px;
                border: 1px solid {BORDER_GREEN};
            }}
            QScrollBar::handle:vertical {{
                background-color: {BORDER_GREEN}; min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(right_scroll, 2)

        # === TITLE & THEME TOGGLE ===
        title_container = QWidget()
        title_container.setStyleSheet(f"background-color: {PANEL_BLACK}; border: 2px solid {BORDER_GREEN};")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(8, 8, 8, 8)
        title_layout.setSpacing(10)

        title = QLabel("EPIDEMIC SIMULATOR v3.0")
        title.setStyleSheet(f"""
            font-size: 16px; font-weight: bold; color: {NEON_GREEN};
            font-family: 'Courier New', monospace;
            background-color: transparent; border: none;
        """)
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title, 1)

        # Theme toggle button
        # Set correct initial text based on current theme
        initial_text = "☀ LIGHT" if current_theme == DARK_THEME else "🌙 DARK"
        self.theme_btn = QPushButton(initial_text)
        self.theme_btn.setToolTip("Toggle Light/Dark Theme (Keyboard: T)\n\nSwitch between light and dark color schemes.\nPreference is saved between sessions.")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setMinimumHeight(32)
        self.theme_btn.setMaximumWidth(90)
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 5px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: #1a1a1a;
                border-color: #ffffff;
                color: #ffffff;
            }}
        """)
        title_layout.addWidget(self.theme_btn)

        # Font size controls
        font_size_label = QLabel("UI:")
        font_size_label.setStyleSheet(f"color: {NEON_GREEN}; font-size: 10px; margin: 0px;")
        font_size_label.setToolTip("Adjust UI font size for better readability")
        title_layout.addWidget(font_size_label)

        self.font_smaller_btn = QPushButton("A-")
        self.font_smaller_btn.setToolTip("Decrease font size\n\nMake UI text smaller for more content.")
        self.font_smaller_btn.clicked.connect(lambda: self.adjust_font_size(-1))
        self.font_smaller_btn.setMinimumHeight(32)
        self.font_smaller_btn.setMaximumWidth(35)
        self.font_smaller_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 2px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background-color: #1a1a1a;
                border-color: #ffffff;
                color: #ffffff;
            }}
        """)
        title_layout.addWidget(self.font_smaller_btn)

        self.font_larger_btn = QPushButton("A+")
        self.font_larger_btn.setToolTip("Increase font size\n\nMake UI text larger for better readability.")
        self.font_larger_btn.clicked.connect(lambda: self.adjust_font_size(1))
        self.font_larger_btn.setMinimumHeight(32)
        self.font_larger_btn.setMaximumWidth(35)
        self.font_larger_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 2px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background-color: #1a1a1a;
                border-color: #ffffff;
                color: #ffffff;
            }}
        """)
        title_layout.addWidget(self.font_larger_btn)

        right_layout.addWidget(title_container)

        # === CONTROLS ===
        ctrl_group = QWidget()
        ctrl_group.setStyleSheet(f"background-color: {PANEL_BLACK}; border: 2px solid {BORDER_GREEN}; padding: 8px;")
        ctrl_layout = QVBoxLayout(ctrl_group)
        ctrl_layout.setSpacing(8)

        # Control buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(4)

        self.pause_btn = QPushButton("PAUSE")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setMinimumHeight(32)
        self.pause_btn.setToolTip("Pause/Resume simulation (Keyboard: SPACE)\n\nPauses the simulation while keeping all state intact.\nUse to examine current situation or adjust parameters.")
        btn_row.addWidget(self.pause_btn)

        reset_btn = QPushButton("RESET")
        reset_btn.clicked.connect(self.reset_sim)
        reset_btn.setMinimumHeight(32)
        reset_btn.setToolTip("Reset simulation (Keyboard: R)\n\nResets simulation to day 0 with current parameters.\nCreates new particle population with random positions.")
        btn_row.addWidget(reset_btn)

        self.fullscreen_btn = QPushButton("FULL")
        self.fullscreen_btn.setToolTip("Fullscreen mode (Keyboard: F)\n\nToggle fullscreen display.\nPress F or ESC to exit fullscreen.")
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_btn.setMinimumHeight(32)
        self.fullscreen_btn.setMaximumWidth(50)
        btn_row.addWidget(self.fullscreen_btn)

        ctrl_layout.addLayout(btn_row)

        # Speed buttons
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet(f"color: {NEON_GREEN}; font-size: 11px; margin-top: 5px;")
        speed_label.setToolTip("Simulation speed multiplier\n\nControls how fast time progresses.\nDoes not affect physics or disease mechanics.")
        ctrl_layout.addWidget(speed_label)

        speed_row = QHBoxLayout()
        speed_row.setSpacing(4)
        self.speed_btns = QButtonGroup()
        self.speed_btns.setExclusive(True)
        speed_tooltips = {
            0.5: "Half speed (0.5x)\n\nSlow motion for detailed observation.\nIdeal for studying individual interactions.",
            1.0: "Normal speed (1.0x)\n\nDefault simulation speed.\nBalanced between detail and progress.",
            2.0: "Double speed (2.0x)\n\nFaster progression through epidemic stages.\nGood for long-term trend observation.",
            5.0: "5x speed (5.0x)\n\nRapid progression to see full epidemic curve.\nSkips early stages quickly."
        }
        for i, speed in enumerate([0.5, 1.0, 2.0, 5.0]):
            btn = QPushButton(f"{speed}x")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, s=speed: self.set_speed(s))
            btn.setMinimumHeight(28)
            btn.setToolTip(speed_tooltips[speed])
            self.speed_btns.addButton(btn, i)
            speed_row.addWidget(btn)
            if speed == 1.0:
                btn.setChecked(True)
        ctrl_layout.addLayout(speed_row)

        # Population
        pop_label = QLabel("Population:")
        pop_label.setStyleSheet(f"color: {NEON_GREEN}; font-size: 11px; margin-top: 8px;")
        ctrl_layout.addWidget(pop_label)

        pop_row = QHBoxLayout()
        self.population_spin = QSpinBox()
        self.population_spin.setRange(50, 2000)
        self.population_spin.setValue(params.num_particles)
        self.population_spin.setSingleStep(50)
        self.population_spin.setMinimumHeight(28)
        self.population_spin.valueChanged.connect(self.on_population_changed)
        self.population_spin.setToolTip("""Population Size: Number of particles in simulation

Range: 50-2000 particles
• 50-200: Fast, good for testing
• 200-500: Balanced performance
• 500-1000: More realistic statistics
• 1000-2000: Highest detail (slower)

Requires clicking 'Apply' to take effect.""")
        pop_row.addWidget(self.population_spin)

        apply_pop_btn = QPushButton("Apply")
        apply_pop_btn.clicked.connect(self.apply_population)
        apply_pop_btn.setMinimumHeight(28)
        apply_pop_btn.setToolTip("Apply new population size\n\nResets the simulation with the new population.\nAll progress will be lost.")
        pop_row.addWidget(apply_pop_btn)
        ctrl_layout.addLayout(pop_row)

        right_layout.addWidget(ctrl_group)

        # === STATS ===
        stats_container = QWidget()
        stats_container.setStyleSheet(f"""
            background-color: {PANEL_BLACK}; border: 2px solid {NEON_GREEN}; padding: 10px;
        """)
        stats_layout = QVBoxLayout(stats_container)
        self.stats_label = QLabel("DAY: 0\nS: 100.0% | I: 0.0% | R: 0.0%")
        self.stats_label.setStyleSheet(f"""
            font-size: 16px; font-weight: bold; color: {NEON_GREEN};
            font-family: 'Courier New', monospace; background-color: transparent; border: none;
        """)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setToolTip("""Real-time epidemic statistics

DAY: Current simulation day
S (Susceptible): Healthy, can be infected
I (Infected): Currently infectious
R (Removed): Recovered or deceased

These percentages sum to 100% at all times (classic SIR model)""")
        stats_layout.addWidget(self.stats_label)
        right_layout.addWidget(stats_container)

        # === MODE ===
        mode_box = CollapsibleBox("SIMULATION MODE")
        self.collapsible_boxes.append(mode_box)
        self.mode_btns = QButtonGroup()

        mode_tooltips = {
            'simple': """Simple Mode: Single well-mixed population

All particles move freely in one shared space.
No barriers or separation between groups.
Fastest spread dynamics.

Use for: Baseline epidemic behavior, teaching basic SIR model""",

            'quarantine': """Quarantine Mode: Infected particles can be isolated

Symptomatic infected particles move to quarantine zone.
Quarantine zone is on the right side of canvas.
Asymptomatic cases continue spreading.

Use for: Studying intervention effectiveness, isolation strategies""",

            'communities': """Communities Mode: Multiple isolated population groups

Population divided into separate communities.
Occasional travel between communities spreads disease.
Slower inter-community transmission.

Use for: Geographic spread modeling, travel restrictions"""
        }

        for i, mode in enumerate(['simple', 'quarantine', 'communities']):
            btn = QPushButton(mode.upper())
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode: self.change_mode(m))
            btn.setMinimumHeight(34)
            btn.setToolTip(mode_tooltips[mode])
            self.mode_btns.addButton(btn, i)
            mode_box.addWidget(btn)
        self.mode_btns.button(0).setChecked(True)
        right_layout.addWidget(mode_box)

        # === INTERVENTIONS ===
        interv_box = CollapsibleBox("INTERVENTIONS")
        self.collapsible_boxes.append(interv_box)

        self.quarantine_checkbox = QCheckBox("Quarantine Zone")
        self.quarantine_checkbox.setChecked(params.quarantine_enabled)
        self.quarantine_checkbox.stateChanged.connect(self.toggle_quarantine)
        self.quarantine_checkbox.setToolTip("""Quarantine Zone: Enable/disable quarantine isolation (Keyboard: Q)

When enabled:
• Symptomatic infected particles move to right side
• Quarantined particles cannot infect main population
• Asymptomatic cases remain in main population

Use for: Testing isolation effectiveness, intervention strategies""")
        interv_box.addWidget(self.quarantine_checkbox)

        self.marketplace_checkbox = QCheckBox("Marketplace Gatherings")
        self.marketplace_checkbox.setChecked(params.marketplace_enabled)
        self.marketplace_checkbox.stateChanged.connect(self.toggle_marketplace)
        self.marketplace_checkbox.setToolTip("""Marketplace Gatherings: Periodic mass gathering events (Keyboard: M)

When enabled:
• Particles periodically gather at central marketplace
• Dramatically increases contact rate during event
• Models superspreader events (concerts, festivals, etc.)

Use for: Studying impact of mass gatherings on epidemic spread""")
        interv_box.addWidget(self.marketplace_checkbox)

        mp_grid = QGridLayout()
        mp_grid.setSpacing(5)

        interval_label = QLabel("Interval (days):")
        interval_label.setToolTip("Days between marketplace gathering events\n\nLower = more frequent gatherings\nHigher = rare events")
        mp_grid.addWidget(interval_label, 0, 0)
        self.marketplace_interval_spin = QSpinBox()
        self.marketplace_interval_spin.setRange(1, 30)
        self.marketplace_interval_spin.setValue(params.marketplace_interval)
        self.marketplace_interval_spin.valueChanged.connect(lambda v: setattr(params, 'marketplace_interval', v))
        self.marketplace_interval_spin.setToolTip("How often marketplace gatherings occur\n\n1-7: Weekly or more frequent\n7-14: Every 1-2 weeks\n14-30: Rare events")
        mp_grid.addWidget(self.marketplace_interval_spin, 0, 1)

        attendance_label = QLabel("Attendance:")
        attendance_label.setToolTip("Fraction of population attending each marketplace event\n\n0.1 = 10% attend\n0.5 = 50% attend\n1.0 = 100% attend")
        mp_grid.addWidget(attendance_label, 1, 0)
        self.marketplace_attendance_spin = QDoubleSpinBox()
        self.marketplace_attendance_spin.setRange(0.1, 1.0)
        self.marketplace_attendance_spin.setSingleStep(0.1)
        self.marketplace_attendance_spin.setValue(params.marketplace_attendance)
        self.marketplace_attendance_spin.valueChanged.connect(lambda v: setattr(params, 'marketplace_attendance', v))
        self.marketplace_attendance_spin.setToolTip("Percentage of population participating in marketplace\n\nHigher attendance = larger superspreader potential")
        mp_grid.addWidget(self.marketplace_attendance_spin, 1, 1)

        interv_box.addLayout(mp_grid)
        right_layout.addWidget(interv_box)

        # === VISUALIZATIONS ===
        vis_box = CollapsibleBox("VISUALIZATIONS")
        self.collapsible_boxes.append(vis_box)
        # Start expanded (not collapsed) - graphs should be visible!

        # Infection radius visibility toggle
        self.show_radius_checkbox = QCheckBox("Show Infection Radius")
        self.show_radius_checkbox.setChecked(params.show_infection_radius)
        self.show_radius_checkbox.stateChanged.connect(self.toggle_infection_radius)
        self.show_radius_checkbox.setToolTip("Display red circles around infected particles showing infection range")
        vis_box.addWidget(self.show_radius_checkbox)

        vis_tabs = QTabWidget()
        vis_tabs.setMinimumHeight(400)  # Much taller now!
        vis_tabs.setToolTip("Epidemic visualization graphs\n\nTIME SERIES: S/I/R percentages over time\nPIE CHART: Current population distribution")
        vis_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid {BORDER_GREEN}; background-color: {BG_BLACK};
            }}
            QTabBar::tab {{
                background-color: {PANEL_BLACK}; color: {NEON_GREEN};
                border: 1px solid {BORDER_GREEN}; padding: 8px 15px;
                margin-right: 2px; font-family: 'Courier New', monospace; font-size: 11px;
            }}
            QTabBar::tab:selected {{
                background-color: {BORDER_GREEN}; color: {BG_BLACK}; font-weight: bold;
            }}
            QTabBar::tab:hover {{ background-color: #002200; }}
        """)

        # Graph
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground(BG_BLACK)
        self.graph_widget.setLabel('left', '% Population', color=NEON_GREEN)
        self.graph_widget.setLabel('bottom', 'Day', color=NEON_GREEN)
        self.graph_widget.showGrid(x=True, y=True, alpha=0.15)
        self.graph_widget.setYRange(0, 100)
        self.graph_widget.setMinimumHeight(380)  # Much taller!
        self.graph_widget.setToolTip("""Time Series Graph: Track epidemic progression over time

Shows percentage of population in each state:
• Blue (Cyan): Susceptible - healthy, can be infected
• Red: Infected - currently infectious
• Green: Removed - recovered or deceased

Watch for:
• Peak infection rate (epidemic peak)
• Final size (total affected)
• Curve shape (exponential growth, plateau, decline)""")

        for side in ['left', 'bottom', 'right', 'top']:
            axis = self.graph_widget.getAxis(side)
            axis.setPen(pg.mkPen(color=BORDER_GREEN, width=2))
            axis.setTextPen(NEON_GREEN)

        legend = self.graph_widget.addLegend(offset=(10, 10))
        legend.setBrush(pg.mkBrush(color=(10, 10, 10, 200)))
        legend.setPen(pg.mkPen(color=BORDER_GREEN, width=1))

        self.pie_chart = PieChartWidget(parent=self, width=3.8, height=3.8, dpi=80)
        self.pie_chart.setMinimumHeight(250)
        self.pie_chart.setToolTip("""Pie Chart: Current population distribution snapshot

Shows current state of entire population:
• Blue: Susceptible (healthy)
• Red: Infected (currently infectious)
• Green: Removed (recovered/deceased)

Updates in real-time as simulation progresses.""")

        vis_tabs.addTab(self.graph_widget, "TIME SERIES")
        vis_tabs.addTab(self.pie_chart, "PIE CHART")

        vis_box.addWidget(vis_tabs)
        right_layout.addWidget(vis_box)

        # === STATUS ===
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"""
            font-size: 11px; padding: 8px; color: {NEON_GREEN};
            background-color: {PANEL_BLACK}; border: 1px solid {BORDER_GREEN};
            font-family: 'Courier New', monospace;
        """)
        self.status_label.setWordWrap(True)
        right_layout.addWidget(self.status_label)

        # === SHORTCUTS ===
        shortcuts = QLabel(
            "SHORTCUTS: SPACE=Pause | R=Reset | T=Theme | F=Fullscreen\n"
            "Q=Quarantine | M=Marketplace | 1-9=Presets"
        )
        shortcuts.setStyleSheet(f"""
            font-size: 9px; padding: 5px; color: {NEON_GREEN};
            background-color: {BG_BLACK}; border: 1px solid {BORDER_GREEN};
            font-family: 'Courier New', monospace;
        """)
        shortcuts.setWordWrap(True)
        right_layout.addWidget(shortcuts)

        right_layout.addStretch()

        self.apply_theme()

    def toggle_left_panel(self):
        """Toggle left parameter panel visibility"""
        is_visible = self.left_panel.parent().isVisible()
        self.left_panel.parent().setVisible(not is_visible)
        if is_visible:
            self.left_collapse_btn.setText("SHOW PARAMETERS >>")
        else:
            self.left_collapse_btn.setText("COLLAPSE PARAMETERS <<")

    def on_population_changed(self, value):
        """Update status when population changes"""
        self.status_label.setText(f"Population set to {value}. Click 'Apply' to update.")

    def apply_population(self):
        """Apply new population size"""
        new_pop = self.population_spin.value()
        params.num_particles = new_pop
        self.reset_sim()
        self.status_label.setText(f"Population changed to {new_pop}")

    def apply_theme(self):
        # Dynamic hover colors based on theme
        if current_theme == LIGHT_THEME:
            hover_bg = "#e8f5e9"  # Light green tint
            hover_border = "#2e7d32"  # Darker green
            hover_text = "#1b5e20"  # Dark green text
            checked_hover_bg = "#4caf50"  # Brighter green
        else:  # Dark theme
            hover_bg = "#1a1a1a"  # Dark gray
            hover_border = "#ffffff"  # White
            hover_text = "#ffffff"  # White
            checked_hover_bg = "#00dd00"  # Bright green

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_BLACK};
            }}
            QWidget {{
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
            }}
            QScrollArea {{
                border: 2px solid {BORDER_GREEN};
            }}
            QComboBox {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 5px;
                font-size: 12px;
            }}
            QComboBox::drop-down {{
                border: 0px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {NEON_GREEN};
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                selection-background-color: {BORDER_GREEN};
                border: 2px solid {BORDER_GREEN};
            }}
            QGroupBox {{
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                border-radius: 0px;
                margin-top: 10px;
                font-weight: bold;
                font-size: 14px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QPushButton {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                border-color: {hover_border};
                border-width: 2px;
                color: {hover_text};
            }}
            QPushButton:checked {{
                background-color: {NEON_GREEN};
                color: {BG_BLACK};
                border: 2px solid {NEON_GREEN};
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: {BORDER_GREEN};
                border: 2px solid {NEON_GREEN};
                padding: 10px;
            }}
            QPushButton:checked:hover {{
                background-color: {checked_hover_bg};
                border: 2px solid {hover_border};
                color: {BG_BLACK};
            }}
            QLabel {{
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
            }}
            QTextEdit {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {BORDER_GREEN};
                height: 4px;
                background: {BG_BLACK};
            }}
            QSlider::handle:horizontal {{
                background: {NEON_GREEN};
                border: 1px solid {BORDER_GREEN};
                width: 14px;
                margin: -5px 0;
            }}
            QCheckBox {{
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 13px;
                font-weight: bold;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {BORDER_GREEN};
                background-color: {BG_BLACK};
            }}
            QCheckBox::indicator:checked {{
                background-color: {NEON_GREEN};
                border: 2px solid {NEON_GREEN};
            }}
            QCheckBox::indicator:hover {{
                border: 2px solid {NEON_GREEN};
            }}
            QSpinBox, QDoubleSpinBox {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 3px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                background-color: {PANEL_BLACK};
                border-left: 1px solid {BORDER_GREEN};
            }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                background-color: {PANEL_BLACK};
                border-left: 1px solid {BORDER_GREEN};
            }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid {NEON_GREEN};
            }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {NEON_GREEN};
            }}
        """)

    def load_preset(self, preset_name):
        """Load a preset configuration"""
        if preset_name == "-- Select Preset --":
            return

        if preset_name not in PRESETS:
            return

        preset = PRESETS[preset_name]

        # Update all parameters
        for param_name, value in preset.items():
            if param_name in self.sliders:
                slider, label, label_text = self.sliders[param_name]
                slider.setValue(int(value * 100))
                label.setText(f"{label_text}: {value:.2f}")
                setattr(params, param_name, value)

        # Reset simulation with new parameters
        self.reset_sim()
        self.sim.log(f"LOADED PRESET: {preset_name}")
        self.status_label.setText(f"✓ Loaded preset: {preset_name}. Simulation reset with new parameters.")

    def update_param(self, param, value, label, label_text, is_int=False):
        setattr(params, param, value)
        if is_int:
            label.setText(f"{label_text}: {int(value)} (reset to apply)")
            self.status_label.setText(f"⚠ {label_text} changed to {int(value)}. Click RESET to apply.")
        else:
            label.setText(f"{label_text}: {value:.2f}")
            self.status_label.setText(f"✓ {label_text} updated to {value:.2f}")

    def change_mode(self, mode):
        self.sim.mode = mode
        self.reset_sim()
        mode_names = {'simple': 'Simple', 'quarantine': 'Quarantine', 'communities': 'Communities'}
        self.status_label.setText(f"✓ Mode changed to: {mode_names.get(mode, mode)}")

    def toggle_quarantine(self, state):
        """Toggle quarantine on/off"""
        params.quarantine_enabled = bool(state)
        self.status_label.setText(f"Quarantine {'enabled' if state else 'disabled'}")

    def toggle_marketplace(self, state):
        """Toggle marketplace gatherings on/off"""
        params.marketplace_enabled = bool(state)
        self.status_label.setText(f"Marketplace {'enabled' if state else 'disabled'}")

    def toggle_infection_radius(self, state):
        """Toggle infection radius visualization"""
        params.show_infection_radius = bool(state)
        self.canvas.update()  # Force redraw
        self.status_label.setText(f"Infection radius {'visible' if state else 'hidden'}")

    def load_theme(self, theme_name):
        """Load and apply a theme (dark or light)"""
        global current_theme
        if theme_name == "light":
            current_theme = LIGHT_THEME
        else:
            current_theme = DARK_THEME
        _update_legacy_colors()

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        global current_theme
        # Switch theme
        if current_theme == DARK_THEME:
            current_theme = LIGHT_THEME
            theme_name = "light"
            self.theme_btn.setText("🌙 DARK")
        else:
            current_theme = DARK_THEME
            theme_name = "dark"
            self.theme_btn.setText("☀ LIGHT")

        # Update legacy colors
        _update_legacy_colors()

        # Save preference
        self.settings.setValue("theme", theme_name)

        # Apply theme to all UI elements
        self.apply_theme()

        # Update panels with direct stylesheets
        self.left_panel.setStyleSheet(f"background-color: {BG_BLACK};")
        self.right_panel.setStyleSheet(f"background-color: {BG_BLACK};")

        # Update all collapsible boxes
        for box in self.collapsible_boxes:
            box.update_theme()

        # Update canvas background
        self.canvas.update()

        # Update graph colors
        self.graph_widget.setBackground(get_color('GRAPH_BG'))
        graph_grid_color = get_color('GRAPH_GRID')
        self.graph_widget.showGrid(x=True, y=True, alpha=graph_grid_color[3]/255.0)

        # Update all axes colors
        for side in ['left', 'bottom', 'right', 'top']:
            axis = self.graph_widget.getAxis(side)
            axis.setPen(pg.mkPen(color=get_color('BORDER_GRAY') if current_theme == LIGHT_THEME else BORDER_GREEN, width=2))
            axis.setTextPen(get_color('TEXT'))

        # Update pie chart
        self.pie_chart.fig.patch.set_facecolor(get_color('GRAPH_BG'))
        self.pie_chart.setStyleSheet(f"background-color: {get_color('GRAPH_BG')};")
        # Update pie chart axes
        if hasattr(self.pie_chart, 'axes'):
            self.pie_chart.axes.set_facecolor(get_color('GRAPH_BG'))
        self.pie_chart.draw()

        # Force full UI refresh
        self.status_label.setText(f"Theme switched to {theme_name.title()} mode")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode by hiding/showing right panel"""
        self.right_panel.setVisible(not self.right_panel.isVisible())
        if not self.right_panel.isVisible():
            self.fullscreen_btn.setText("[X]")
            self.status_label.setText("Fullscreen mode (Press F to exit)")
        else:
            self.fullscreen_btn.setText("FULL")

    def adjust_font_size(self, delta):
        """Adjust the base font size of the application"""
        if not hasattr(self, 'base_font_size'):
            self.base_font_size = 10  # Default size

        # Adjust size with limits (8-14)
        new_size = max(8, min(14, self.base_font_size + delta))

        if new_size == self.base_font_size:
            if delta > 0:
                self.status_label.setText("⚠ Maximum font size reached (14pt)")
            else:
                self.status_label.setText("⚠ Minimum font size reached (8pt)")
            return

        self.base_font_size = new_size

        # Apply new font to application
        from PyQt5.QtWidgets import QApplication
        font = QFont("Courier New", self.base_font_size)
        QApplication.instance().setFont(font)

        # Save preference
        self.settings.setValue("font_size", self.base_font_size)

        self.status_label.setText(f"✓ Font size: {self.base_font_size}pt")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.setText("RESUME" if self.paused else "PAUSE")
        if self.paused:
            self.status_label.setText(f"⏸ Simulation PAUSED at Day {self.sim.day_count}. Adjust parameters or press SPACE to resume.")
        else:
            self.status_label.setText(f"▶ Simulation RESUMED at {self.speed}x speed.")

    def reset_sim(self):
        self.sim.initialize()
        self.graph_widget.clear()

        # Adaptive performance optimization based on population size
        # More particles = skip more rendering frames
        if params.num_particles <= 200:
            self.skip_frames = 1  # Render every frame (60 FPS)
        elif params.num_particles <= 500:
            self.skip_frames = 2  # Render every 2nd frame (30 FPS)
        else:  # > 500 particles
            self.skip_frames = 3  # Render every 3rd frame (20 FPS)

        self.frame_count = 0
        self.status_label.setText(f"Simulation reset ({params.num_particles} particles, {60//self.skip_frames} FPS)")
        self.paused = False
        self.pause_btn.setText("PAUSE")

    def set_speed(self, speed):
        self.speed = speed
        self.status_label.setText(f"Speed set to {speed}x")
        # Visual feedback - find and check the button
        for i, btn in enumerate(self.speed_btns.buttons()):
            if btn.text() == f"{speed}x":
                btn.setChecked(True)
                break

    def add_log(self, message):
        """Update status bar with important events only"""
        # Filter to show only important events
        important_keywords = ['INITIALIZING', 'PATIENT ZERO', 'PRESET', 'QUARANTINE', 'SPEED']
        if any(keyword in message for keyword in important_keywords):
            self.status_label.setText(message)

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        key = event.key()

        # Space: Pause/Resume
        if key == Qt.Key_Space:
            self.toggle_pause()
            return

        # R: Reset
        if key == Qt.Key_R:
            self.reset_sim()
            return

        # 1-9: Quick preset selection
        if Qt.Key_1 <= key <= Qt.Key_9:
            preset_index = key - Qt.Key_1  # 0-8
            preset_names = list(PRESETS.keys())
            if preset_index < len(preset_names):
                preset_name = preset_names[preset_index]
                self.preset_combo.setCurrentText(preset_name)
            return

        # Q: Toggle quarantine
        if key == Qt.Key_Q:
            new_state = not params.quarantine_enabled
            self.quarantine_checkbox.setChecked(new_state)
            return

        # M: Toggle marketplace
        if key == Qt.Key_M:
            new_state = not params.marketplace_enabled
            self.marketplace_checkbox.setChecked(new_state)
            return

        # T: Toggle theme (Light/Dark)
        if key == Qt.Key_T:
            self.toggle_theme()
            return

        # F: Toggle fullscreen
        if key == Qt.Key_F:
            self.toggle_fullscreen()
            return

        # Pass other events to parent
        super().keyPressEvent(event)

    def update_simulation(self):
        if not self.paused:
            # Accumulate fractional speed for smooth slow speeds (0.5x)
            self.speed_accumulator += self.speed
            steps_to_run = int(self.speed_accumulator)

            for _ in range(steps_to_run):
                self.sim.step()

            # Keep the fractional part for next frame
            self.speed_accumulator -= steps_to_run

        # Adaptive frame skipping for performance with many particles
        self.frame_count += 1
        if self.frame_count >= self.skip_frames:
            self.frame_count = 0
            self.canvas.update()  # Only update canvas every Nth frame

    def update_stats_display(self, counts):
        """Update stats display, graph, and pie chart"""
        # Use initial population for percentages
        initial = self.sim.initial_population
        if initial == 0:
            return

        s_pct = counts['susceptible']/initial*100
        i_pct = counts['infected']/initial*100
        r_pct = counts['removed']/initial*100
        d_pct = counts['dead']/initial*100

        text = f"DAY: {self.sim.day_count:03d}\n"
        text += f"S: {s_pct:5.1f}% | I: {i_pct:5.1f}% | R: {r_pct:5.1f}%"
        if counts['dead'] > 0:
            text += f" | D: {d_pct:5.1f}%"
        self.stats_label.setText(text)

        # Update pie chart only every 5 days to reduce stuttering
        if self.sim.day_count % 5 == 0 or self.sim.day_count == 0:
            self.pie_chart.update_chart(counts)

        # Update graph with clear separate lines
        if len(self.sim.stats['day']) > 1:
            self.graph_widget.clear()

            days = self.sim.stats['day']
            s_data = self.sim.stats['susceptible']
            i_data = self.sim.stats['infected']
            r_data = self.sim.stats['removed']
            d_data = self.sim.stats['dead']

            # Plot as separate, clear lines (NO fill!)
            # Susceptible - Cyan line
            s_curve = pg.PlotDataItem(
                days, s_data,
                pen=pg.mkPen(color=(0, 191, 255), width=3),
                brush=None,  # NO FILL
                fillLevel=None,
                name='Susceptible'
            )
            self.graph_widget.addItem(s_curve)

            # Infected - Red line
            i_curve = pg.PlotDataItem(
                days, i_data,
                pen=pg.mkPen(color=(255, 69, 69), width=3),
                brush=None,  # NO FILL
                fillLevel=None,
                name='Infected'
            )
            self.graph_widget.addItem(i_curve)

            # Removed - Gray line
            r_curve = pg.PlotDataItem(
                days, r_data,
                pen=pg.mkPen(color=(120, 120, 120), width=3),
                brush=None,  # NO FILL
                fillLevel=None,
                name='Removed'
            )
            self.graph_widget.addItem(r_curve)

            # Dead - Dark red/black line
            if max(d_data) > 0:  # Only show if there are deaths
                d_curve = pg.PlotDataItem(
                    days, d_data,
                    pen=pg.mkPen(color=(80, 0, 0), width=3),
                    brush=None,  # NO FILL
                    fillLevel=None,
                    name='Dead'
                )
                self.graph_widget.addItem(d_curve)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    font = QFont("Courier New", 10)
    app.setFont(font)

    window = EpidemicApp()
    window.show()
    sys.exit(app.exec_())
