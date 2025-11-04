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

# =================== NEON GREEN THEME ===================
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
        self.prob_infection = 0.02
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

        # Communities
        self.travel_probability = 0.02
        self.num_per_community = 60
        self.communities_to_infect = 2

        # Marketplace gathering parameters
        self.marketplace_enabled = False
        self.marketplace_interval = 7  # Days between gatherings (weekly)
        self.marketplace_duration = 2  # Time steps particles stay (hours)
        self.marketplace_attendance = 0.6  # 60% of population attends
        self.marketplace_x = 0.0  # Center location
        self.marketplace_y = 0.0

params = SimParams()

# =================== PRESETS ===================
PRESETS = {
    # Educational Presets
    "Baseline Epidemic": {
        'infection_radius': 0.15, 'prob_infection': 0.02, 'fraction_infected_init': 0.01,
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
        self.x = x
        self.y = y
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

        # Marketplace tracking
        self.at_marketplace = False
        self.marketplace_timer = 0
        self.home_x = x
        self.home_y = y

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
            'day': [0]
        }

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
            'day': [0]
        }

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
            x = random.uniform(self.bounds[0] + 0.15, self.bounds[1] - 0.15)
            y = random.uniform(self.bounds[2] + 0.15, self.bounds[3] - 0.15)
            state = 'infected' if i < num_infected else 'susceptible'
            self.particles.append(Particle(x, y, state))

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
                    x = random.uniform(bounds[0] + 0.1, bounds[1] - 0.1)
                    y = random.uniform(bounds[2] + 0.1, bounds[3] - 0.1)
                    state = 'infected' if k < num_infected else 'susceptible'
                    self.communities[comm_id]['particles'].append(Particle(x, y, state))

        self.log(f"TOTAL: {params.num_per_community * 9} PARTICLES ({total_infected} INFECTED)")
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
                    if random.random() < params.prob_infection / params.time_steps_per_day:
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
        recovered = 0

        for p in particle_list:
            if p.state == 'infected':
                p.days_infected += 1

                if p.days_infected >= params.infection_duration:
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

        return to_quarantine

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

    def _handle_marketplace(self, particle_list):
        """Handle marketplace gathering events"""
        if not params.marketplace_enabled:
            return 0

        # Check if it's marketplace day
        days_since_last = self.day_count - self.last_marketplace_day
        if days_since_last >= params.marketplace_interval:
            # Start new gathering
            self.last_marketplace_day = self.day_count
            attending = 0
            for p in particle_list:
                if not p.quarantined and random.random() < params.marketplace_attendance:
                    p.at_marketplace = True
                    p.marketplace_timer = params.marketplace_duration
                    p.home_x = p.x
                    p.home_y = p.y
                    # Move to marketplace with some randomness
                    p.x = params.marketplace_x + random.uniform(-0.2, 0.2)
                    p.y = params.marketplace_y + random.uniform(-0.2, 0.2)
                    p.vx = random.uniform(-0.02, 0.02)
                    p.vy = random.uniform(-0.02, 0.02)
                    attending += 1
            if attending > 0:
                self.log(f">> MARKETPLACE EVENT: {attending} ATTENDING")
            return attending

        # Update marketplace timers
        returning = 0
        for p in particle_list:
            if p.at_marketplace:
                p.marketplace_timer -= 1
                if p.marketplace_timer <= 0:
                    # Return home
                    p.at_marketplace = False
                    p.x = p.home_x + random.uniform(-0.1, 0.1)
                    p.y = p.home_y + random.uniform(-0.1, 0.1)
                    returning += 1

        return 0

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
                    to_q = self._update_infections(comm['particles'])
                    total_quarantined += len(to_q)
                    for p in to_q:
                        self._move_to_quarantine(p, comm['particles'])

                if self.quarantine_particles:
                    self._check_infections(self.quarantine_particles)
                    self._update_infections(self.quarantine_particles)

                if total_quarantined > 0:
                    self.log(f">> {total_quarantined} MOVED TO QUARANTINE")

                if random.random() < 0.3:
                    travelers = self._handle_community_travel()
                    if travelers > 0:
                        self.log(f">> {travelers} TRAVELED BETWEEN COMMUNITIES")

            else:
                self._check_infections(self.particles)
                to_q = self._update_infections(self.particles)

                if to_q:
                    self.log(f">> {len(to_q)} MOVED TO QUARANTINE")
                    for p in to_q:
                        self._move_to_quarantine(p, self.particles)

                if self.quarantine_particles:
                    self._check_infections(self.quarantine_particles)
                    self._update_infections(self.quarantine_particles)

                # Handle marketplace events
                if self.mode != 'communities':  # Simple and quarantine modes
                    self._handle_marketplace(self.particles)

            self._update_stats()
            self.day_count += 1

        self.time_count += 1

    def _handle_community_travel(self):
        travelers = 0
        for comm_id, comm in self.communities.items():
            to_travel = []
            for p in comm['particles']:
                if not p.quarantined and random.random() < params.travel_probability / params.time_steps_per_day:
                    to_travel.append(p)

            for p in to_travel:
                other_comms = [c for c in range(9) if c != comm_id]
                target_comm = random.choice(other_comms)

                comm['particles'].remove(p)
                bounds = self.communities[target_comm]['bounds']
                p.x = random.uniform(bounds[0] + 0.1, bounds[1] - 0.1)
                p.y = random.uniform(bounds[2] + 0.1, bounds[3] - 0.1)
                self.communities[target_comm]['particles'].append(p)
                travelers += 1

        return travelers

    def _update_stats(self):
        all_p = self.get_all_particles()
        total = len(all_p)
        if total == 0:
            return

        counts = {'susceptible': 0, 'infected': 0, 'removed': 0}
        for p in all_p:
            counts[p.state] += 1

        for state in ['susceptible', 'infected', 'removed']:
            percent = (counts[state] / total) * 100
            self.stats[state].append(percent)

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

        painter.fillRect(self.rect(), QColor(BG_BLACK))

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
        for comm in self.sim.communities.values():
            bounds = comm['bounds']
            tl = self._to_screen(bounds[0], bounds[3])
            br = self._to_screen(bounds[1], bounds[2])
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

        if p.state == 'susceptible':
            color = QColor(0, 191, 255)
        elif p.state == 'infected':
            if not p.shows_symptoms:
                color = QColor(255, 165, 0)
            else:
                color = QColor(255, 69, 69)
        else:
            color = QColor(100, 100, 100)

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        size = params.particle_size
        painter.drawEllipse(pos[0] - size//2, pos[1] - size//2, size, size)

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
        # We'll approximate this based on prob_no_symptoms
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
            colors.append('#00bfff')  # Cyan

        if symptomatic > 0.5:  # Only show if > 0.5 to avoid tiny slices
            labels.append('Infected\n(Symptomatic)')
            sizes.append(symptomatic)
            colors.append('#ff4545')  # Red

        if asymptomatic > 0.5:
            labels.append('Infected\n(Asymptomatic)')
            sizes.append(asymptomatic)
            colors.append('#ffa500')  # Orange

        if counts['removed'] > 0:
            labels.append('Removed')
            sizes.append(counts['removed'])
            colors.append('#646464')  # Gray

        if not sizes:
            return

        # Create pie chart
        wedges, texts, autotexts = self.axes.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'color': NEON_GREEN, 'fontsize': 9, 'family': 'monospace'}
        )

        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(8)
            autotext.set_weight('bold')

        self.axes.set_facecolor(BG_BLACK)
        self.fig.tight_layout()
        self.draw()

# =================== MAIN WINDOW ===================
class EpidemicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EPIDEMIC SIMULATION v3.0 - Enhanced Edition")
        self.setGeometry(50, 50, 1800, 1000)

        self.sim = EpidemicSimulation('simple')
        self.sim.stats_updated.connect(self.update_stats_display)
        self.sim.log_message.connect(self.add_log)

        self.speed = 1.0
        self.paused = False

        self.setup_ui()
        self.sim.initialize()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.canvas = SimulationCanvas(self.sim)
        layout.addWidget(self.canvas, 3)

        right_panel = QWidget()
        right_panel.setMaximumWidth(550)
        right_panel.setMinimumWidth(500)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(8)
        right_layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(right_panel, 2)

        # PRESETS DROPDOWN
        preset_group = QGroupBox("[ PRESETS ]")
        preset_layout = QVBoxLayout()

        self.preset_combo = QComboBox()
        self.preset_combo.addItem("-- Select Preset --")
        for preset_name in PRESETS.keys():
            self.preset_combo.addItem(preset_name)
        self.preset_combo.currentTextChanged.connect(self.load_preset)
        preset_layout.addWidget(self.preset_combo)

        preset_group.setLayout(preset_layout)
        right_layout.addWidget(preset_group)

        # Mode buttons
        mode_group = QGroupBox("[ SIMULATION MODE ]")
        mode_layout = QVBoxLayout()
        self.mode_btns = QButtonGroup()

        for i, mode in enumerate(['simple', 'quarantine', 'communities']):
            btn = QPushButton(f"  [{mode.upper()}]")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode: self.change_mode(m))
            self.mode_btns.addButton(btn, i)
            mode_layout.addWidget(btn)

        self.mode_btns.button(0).setChecked(True)
        mode_group.setLayout(mode_layout)
        right_layout.addWidget(mode_group)

        # Intervention controls
        intervention_group = QGroupBox("[ INTERVENTIONS ]")
        intervention_layout = QVBoxLayout()

        self.quarantine_checkbox = QCheckBox("  ENABLE QUARANTINE")
        self.quarantine_checkbox.setChecked(params.quarantine_enabled)
        self.quarantine_checkbox.stateChanged.connect(self.toggle_quarantine)
        intervention_layout.addWidget(self.quarantine_checkbox)

        self.marketplace_checkbox = QCheckBox("  ENABLE MARKETPLACE GATHERINGS")
        self.marketplace_checkbox.setChecked(params.marketplace_enabled)
        self.marketplace_checkbox.stateChanged.connect(self.toggle_marketplace)
        intervention_layout.addWidget(self.marketplace_checkbox)

        # Marketplace parameters (collapsible)
        marketplace_params_layout = QHBoxLayout()

        interval_label = QLabel("Interval (days):")
        interval_label.setStyleSheet("font-size: 10px; padding: 2px;")
        self.marketplace_interval_spin = QSpinBox()
        self.marketplace_interval_spin.setRange(1, 30)
        self.marketplace_interval_spin.setValue(params.marketplace_interval)
        self.marketplace_interval_spin.valueChanged.connect(lambda v: setattr(params, 'marketplace_interval', v))
        self.marketplace_interval_spin.setMaximumWidth(60)
        marketplace_params_layout.addWidget(interval_label)
        marketplace_params_layout.addWidget(self.marketplace_interval_spin)

        attendance_label = QLabel("  Attendance:")
        attendance_label.setStyleSheet("font-size: 10px; padding: 2px;")
        self.marketplace_attendance_spin = QDoubleSpinBox()
        self.marketplace_attendance_spin.setRange(0.1, 1.0)
        self.marketplace_attendance_spin.setSingleStep(0.1)
        self.marketplace_attendance_spin.setValue(params.marketplace_attendance)
        self.marketplace_attendance_spin.valueChanged.connect(lambda v: setattr(params, 'marketplace_attendance', v))
        self.marketplace_attendance_spin.setMaximumWidth(60)
        marketplace_params_layout.addWidget(attendance_label)
        marketplace_params_layout.addWidget(self.marketplace_attendance_spin)

        intervention_layout.addLayout(marketplace_params_layout)

        intervention_group.setLayout(intervention_layout)
        right_layout.addWidget(intervention_group)

        # Control buttons
        controls = QHBoxLayout()
        self.pause_btn = QPushButton("[PAUSE]")
        self.pause_btn.clicked.connect(self.toggle_pause)
        controls.addWidget(self.pause_btn)

        reset_btn = QPushButton("[RESET]")
        reset_btn.clicked.connect(self.reset_sim)
        controls.addWidget(reset_btn)
        right_layout.addLayout(controls)

        # Speed controls
        speed_group = QGroupBox("[ SPEED CONTROL ]")
        speed_layout = QHBoxLayout()

        for speed in [0.5, 1.0, 2.0, 5.0]:
            btn = QPushButton(f"[{speed}x]")
            btn.clicked.connect(lambda checked, s=speed: self.set_speed(s))
            speed_layout.addWidget(btn)

        speed_group.setLayout(speed_layout)
        right_layout.addWidget(speed_group)

        # Stats display
        self.stats_label = QLabel("> DAY: 0\n> S: 100.0%\n> I: 0.0%\n> R: 0.0%")
        self.stats_label.setStyleSheet(f"font-size: 18px; padding: 15px; font-family: 'Courier New'; color: {NEON_GREEN};")
        right_layout.addWidget(self.stats_label)

        # Visualization tabs
        vis_tabs = QTabWidget()
        vis_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid {BORDER_GREEN};
                background-color: {BG_BLACK};
            }}
            QTabBar::tab {{
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 8px 15px;
                font-family: 'Courier New', monospace;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {BORDER_GREEN};
                color: {BG_BLACK};
            }}
        """)

        # Graph (FIXED FILLING)
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground(BG_BLACK)
        self.graph_widget.setLabel('left', '% POPULATION', color=NEON_GREEN)
        self.graph_widget.setLabel('bottom', 'DAY', color=NEON_GREEN)
        self.graph_widget.showGrid(x=True, y=True, alpha=0.2)
        self.graph_widget.setYRange(0, 100)

        axis_pen = pg.mkPen(color=NEON_GREEN, width=2)
        self.graph_widget.getAxis('left').setPen(axis_pen)
        self.graph_widget.getAxis('bottom').setPen(axis_pen)
        self.graph_widget.getAxis('left').setTextPen(NEON_GREEN)
        self.graph_widget.getAxis('bottom').setTextPen(NEON_GREEN)

        # Pie chart
        self.pie_chart = PieChartWidget(parent=self, width=4, height=4, dpi=80)

        # Add both to tabs
        vis_tabs.addTab(self.graph_widget, "TIME SERIES")
        vis_tabs.addTab(self.pie_chart, "PIE CHART")

        right_layout.addWidget(vis_tabs)

        # Parameter sliders
        sliders_scroll = QScrollArea()
        sliders_scroll.setWidgetResizable(True)
        sliders_scroll.setMinimumHeight(280)
        sliders_scroll.setMaximumHeight(320)

        sliders_widget = QWidget()
        sliders_layout = QVBoxLayout(sliders_widget)

        self.sliders = {}
        slider_params = [
            ('infection_radius', 'INFECTION_RADIUS', 0.01, 0.4, 0.15),
            ('prob_infection', 'INFECTION_PROB', 0, 0.1, 0.02),
            ('fraction_infected_init', 'INITIAL_INFECTED_%', 0, 0.05, 0.01),
            ('infection_duration', 'DURATION_DAYS', 1, 100, 25),
            ('social_distance_factor', 'SOCIAL_DISTANCE', 0, 2, 0),
            ('social_distance_obedient', 'SD_OBEDIENT_%', 0, 1, 1.0),
            ('boxes_to_consider', 'SD_RADIUS_MULT', 1, 10, 2),
            ('quarantine_after', 'QUARANTINE_AFTER', 1, 20, 5),
            ('start_quarantine', 'START_Q_DAY', 0, 30, 10),
            ('prob_no_symptoms', 'ASYMPTOMATIC_%', 0, 0.5, 0.20),
        ]

        for param, label, min_val, max_val, default in slider_params:
            hlayout = QHBoxLayout()
            lbl = QLabel(f"{label}: {default:.2f}")
            lbl.setMinimumWidth(200)
            lbl.setStyleSheet("font-size: 11px;")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            hlayout.addWidget(lbl)
            hlayout.addWidget(slider)
            sliders_layout.addLayout(hlayout)
            self.sliders[param] = (slider, lbl, label)

        sliders_scroll.setWidget(sliders_widget)
        right_layout.addWidget(sliders_scroll)

        # Status bar for important events
        status_group = QGroupBox("[ STATUS ]")
        status_layout = QVBoxLayout()
        self.status_label = QLabel("Ready to start simulation")
        self.status_label.setStyleSheet(f"font-size: 12px; padding: 10px; font-family: 'Courier New'; color: {NEON_GREEN};")
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        right_layout.addWidget(status_group)

        # Keyboard shortcuts reference
        shortcuts_group = QGroupBox("[ KEYBOARD SHORTCUTS ]")
        shortcuts_layout = QVBoxLayout()
        shortcuts_text = QLabel(
            "SPACE: Pause/Resume\n"
            "R: Reset Simulation\n"
            "Q: Toggle Quarantine\n"
            "M: Toggle Marketplace\n"
            "1-9: Load Preset (1-9)"
        )
        shortcuts_text.setStyleSheet(f"font-size: 11px; padding: 5px; font-family: 'Courier New'; color: {NEON_GREEN};")
        shortcuts_layout.addWidget(shortcuts_text)
        shortcuts_group.setLayout(shortcuts_layout)
        right_layout.addWidget(shortcuts_group)

        self.apply_theme()

    def apply_theme(self):
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
            }}
            QPushButton:hover {{
                background-color: {DARK_GREEN};
                border: 2px solid {NEON_GREEN};
            }}
            QPushButton:checked {{
                background-color: {BORDER_GREEN};
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

    def update_param(self, param, value, label, label_text):
        setattr(params, param, value)
        label.setText(f"{label_text}: {value:.2f}")

    def change_mode(self, mode):
        self.sim.mode = mode
        self.reset_sim()

    def toggle_quarantine(self, state):
        """Toggle quarantine on/off"""
        params.quarantine_enabled = bool(state)
        status = "ENABLED" if state else "DISABLED"
        self.status_label.setText(f"Quarantine {status}")

    def toggle_marketplace(self, state):
        """Toggle marketplace gatherings on/off"""
        params.marketplace_enabled = bool(state)
        status = "ENABLED" if state else "DISABLED"
        self.status_label.setText(f"Marketplace gatherings {status}")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.setText("[RESUME]" if self.paused else "[PAUSE]")

    def reset_sim(self):
        self.sim.initialize()
        self.graph_widget.clear()
        self.status_label.setText("Simulation reset")
        self.paused = False
        self.pause_btn.setText("[PAUSE]")

    def set_speed(self, speed):
        self.speed = speed
        self.sim.log(f"SPEED SET TO {speed}x")

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

        # Pass other events to parent
        super().keyPressEvent(event)

    def update_simulation(self):
        if not self.paused:
            steps = int(self.speed)
            for _ in range(steps):
                self.sim.step()

        self.canvas.update()

    def update_stats_display(self, counts):
        """Update stats display, graph, and pie chart"""
        total = sum(counts.values())
        if total == 0:
            return

        s_pct = counts['susceptible']/total*100
        i_pct = counts['infected']/total*100
        r_pct = counts['removed']/total*100

        text = f"> DAY: {self.sim.day_count:03d}\n"
        text += f"> SUSCEPTIBLE: {s_pct:5.1f}%\n"
        text += f"> INFECTED:    {i_pct:5.1f}%\n"
        text += f"> REMOVED:     {r_pct:5.1f}%"
        self.stats_label.setText(text)

        # Update pie chart
        self.pie_chart.update_chart(counts)

        if len(self.sim.stats['day']) > 1:
            self.graph_widget.clear()

            days = self.sim.stats['day']
            s_data = self.sim.stats['susceptible']
            i_data = self.sim.stats['infected']
            r_data = self.sim.stats['removed']

            # Create polygon points for filled areas (key fix!)
            # Removed area (bottom)
            r_x = days + days[::-1]
            r_y = r_data + [0] * len(days)
            r_item = pg.PlotCurveItem(r_x, r_y, fillLevel=0,
                                      brush=(100, 100, 100, 180),
                                      pen=pg.mkPen(color=(100, 100, 100), width=2))
            self.graph_widget.addItem(r_item)

            # Infected area (middle) - stack on removed
            i_y_top = [r_data[i] + i_data[i] for i in range(len(days))]
            i_x = days + days[::-1]
            i_y = i_y_top + r_data[::-1]
            i_item = pg.PlotCurveItem(i_x, i_y, fillLevel=0,
                                      brush=(255, 69, 69, 180),
                                      pen=pg.mkPen(color=(255, 69, 69), width=2))
            self.graph_widget.addItem(i_item)

            # Susceptible area (top) - stack on infected+removed
            s_y_bottom = [r_data[i] + i_data[i] for i in range(len(days))]
            s_x = days + days[::-1]
            s_y = [100] * len(days) + s_y_bottom[::-1]
            s_item = pg.PlotCurveItem(s_x, s_y, fillLevel=0,
                                      brush=(0, 191, 255, 180),
                                      pen=pg.mkPen(color=(0, 191, 255), width=2))
            self.graph_widget.addItem(s_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    font = QFont("Courier New", 10)
    app.setFont(font)

    window = EpidemicApp()
    window.show()
    sys.exit(app.exec_())
