"""
Epidemic Simulation Engine Module

This module contains the core EpidemicSimulation class that manages the epidemic
simulation logic, including particle physics, infection spread, quarantine mechanics,
marketplace gatherings, and community travel.

The simulation supports multiple modes:
- Simple mode: All particles in a single space
- Communities mode: 9-tile grid with inter-community travel
- Quarantine mode: Dedicated quarantine zones for infected individuals

Classes:
    EpidemicSimulation: Main simulation engine with SEIRD model implementation
"""

import random
import math
from PyQt5.QtCore import QObject, pyqtSignal

from epidemic_sim.config.parameters import params
from epidemic_sim.model.particle import Particle
from epidemic_sim.model.spatial_grid import SpatialGrid


class EpidemicSimulation(QObject):
    """
    Core epidemic simulation engine implementing SEIRD model with spatial dynamics.

    This class manages the simulation of disease spread among particles in a bounded
    space, with support for quarantine, community travel, and marketplace gathering
    events. The simulation uses a spatial grid for efficient collision detection and
    infection checking.

    Statistical Distributions Used:
        - UNIFORM: Initial positions and velocities (equal probability)
        - NORMAL: Individual infection susceptibility (natural variation)
        - EXPONENTIAL: Recovery time variation (time-to-event modeling)

    Signals:
        stats_updated (dict): Emitted when statistics are updated (daily)
        log_message (str): Emitted for simulation events and status messages

    Attributes:
        mode (str): Simulation mode ('simple' or 'communities')
        bounds (tuple): Simulation space boundaries (xmin, xmax, ymin, ymax)
        particles (list): Main particle list for simple mode
        quarantine_particles (list): Particles in quarantine zone
        communities (dict): Community data for communities mode
        spatial_grid (SpatialGrid): Spatial partitioning for efficient queries
        time_count (int): Current simulation timestep
        day_count (int): Current simulation day
        time_step (float): Time delta per simulation step
        stats (dict): Historical statistics (susceptible, infected, removed, dead, day)
        initial_population (int): Starting population for percentage calculations
    """

    stats_updated = pyqtSignal(dict)
    log_message = pyqtSignal(str)

    def __init__(self, mode='simple'):
        """
        Initialize the epidemic simulation.

        Args:
            mode (str): Simulation mode - 'simple' or 'communities'
        """
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
        """
        Emit a log message with day counter prefix.

        Args:
            message (str): Message to log
        """
        self.log_message.emit(f"[DAY {self.day_count:03d}] {message}")

    def initialize(self):
        """
        Initialize or reset the simulation to starting conditions.

        Creates particles based on the simulation mode, infects initial particles,
        and sets up communities or simple space as needed. Resets all counters and
        statistics.
        """
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
        """
        Initialize simple mode with all particles in a single space.

        Creates particles with uniform random positions and velocities. Infects
        an initial subset based on configuration parameters.
        """
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
        """
        Initialize communities mode with 9 separate communities in a 3x3 grid.

        Creates 9 communities with separate bounds and particle populations. Infects
        particles in a subset of communities based on configuration. If quarantine is
        enabled, reserves community 0 (lower-left tile) as the quarantine zone.
        """
        num_to_infect = max(1, min(params.communities_to_infect, 9))
        infected_communities = random.sample(range(9), num_to_infect)
        self.log(f"CREATING 9 COMMUNITIES (INFECTING: {infected_communities})")

        total_infected = 0
        # Quarantine zone is community 0 (lower-left tile)
        quarantine_comm_id = 0

        for i in range(3):
            for j in range(3):
                comm_id = i * 3 + j
                bounds = (-3 + i * 2.2, -1 + i * 2.2, -3 + j * 2.2, -1 + j * 2.2)
                self.communities[comm_id] = {
                    'bounds': bounds,
                    'particles': []
                }

                # Skip adding initial population to quarantine zone ONLY if quarantine is enabled
                if params.quarantine_enabled and comm_id == quarantine_comm_id:
                    continue  # Keep quarantine zone empty at start when quarantine mode is active

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

        # Adjust initial population count (8 communities if quarantine enabled, 9 otherwise)
        if params.quarantine_enabled:
            self.initial_population = params.num_per_community * 8
            self.log(f"TOTAL: {self.initial_population} PARTICLES ({total_infected} INFECTED)")
            self.log(f">> PATIENT ZERO INITIALIZED IN {num_to_infect} COMMUNIT{'Y' if num_to_infect == 1 else 'IES'}")
            self.log(f">> LOWER-LEFT TILE RESERVED FOR QUARANTINE")
        else:
            self.initial_population = params.num_per_community * 9
            self.log(f"TOTAL: {self.initial_population} PARTICLES ({total_infected} INFECTED)")
            self.log(f">> PATIENT ZERO INITIALIZED IN {num_to_infect} COMMUNIT{'Y' if num_to_infect == 1 else 'IES'}")

    def get_all_particles(self):
        """
        Get a list of all particles in the simulation across all zones.

        Returns:
            list: All active particles (main space + quarantine)
        """
        if self.mode == 'communities':
            all_p = []
            for comm in self.communities.values():
                all_p.extend(comm['particles'])
            return all_p + self.quarantine_particles
        return self.particles + self.quarantine_particles

    def _clamp_to_bounds(self, particle, bounds):
        """
        Keep particle within specified bounds using soft wall collisions.

        When a particle hits a boundary, it bounces back with reduced velocity
        to simulate a soft collision.

        Args:
            particle (Particle): Particle to constrain
            bounds (tuple): Boundaries (xmin, xmax, ymin, ymax)
        """
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
        """
        Update particle position and velocity based on physics simulation.

        Handles multiple movement modes:
        - Normal physics with boundary forces and social distancing
        - Marketplace travel (moving to/from marketplace)
        - Community travel (moving between communities)

        Args:
            particle (Particle): Particle to update
            bounds (tuple): Boundaries to respect
            nearby_particles (list): Nearby particles for social distancing calculations
        """
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
        """
        Check for new infections using spatial grid for efficiency.

        Uses a spatial grid to find nearby susceptible particles for each infected
        particle, then checks infection radius and applies infection probability
        modified by individual susceptibility.

        Args:
            particle_list (list): Particles to check for infections

        Returns:
            int: Number of new infections this check
        """
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
                    #
                    # FIXED: Use prob_infection directly as per-contact probability
                    # No division by time_steps_per_day - the slider shows the actual contact probability
                    effective_prob = params.prob_infection * sus_p.infection_susceptibility

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
        """
        Update infection status for all infected particles (recovery/death/quarantine).

        For each infected particle:
        - Increments days infected
        - Checks for recovery or death based on infection duration
        - Checks for quarantine eligibility (symptomatic particles after threshold)

        Args:
            particle_list (list): Particles to update

        Returns:
            tuple: (particles_to_quarantine, particles_that_died)
        """
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
        """
        Move a particle to the quarantine zone.

        Repositions the particle to the quarantine area (location depends on mode),
        disables social distancing behavior, and transfers to quarantine list.

        Args:
            particle (Particle): Particle to quarantine
            from_list (list): Source list to remove particle from
        """
        particle.quarantined = True
        particle.obeys_social_distance = False

        if self.mode == 'communities':
            # Communities mode: Use lower-left tile (community 0)
            # Bounds: (-3, -1, -3, -1)
            particle.x = random.uniform(-2.9, -1.1)
            particle.y = random.uniform(-2.9, -1.1)
        else:
            # Simple mode: Lower-left corner of main bounds
            particle.x = random.uniform(-0.95, -0.6)
            particle.y = random.uniform(-0.95, -0.6)

        particle.vx = random.uniform(-0.05, 0.05)
        particle.vy = random.uniform(-0.05, 0.05)

        from_list.remove(particle)
        self.quarantine_particles.append(particle)

    def _get_marketplace_location(self):
        """
        Get marketplace center location based on simulation mode.

        Returns:
            tuple: (x, y) coordinates of marketplace center
        """
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
        """
        Handle marketplace gathering events with smooth movement.

        Checks if it's time for a marketplace event and initiates particle travel.
        Updates marketplace timers for particles currently at marketplace.

        Args:
            particle_list (list): Particles that can attend marketplace

        Returns:
            int: Number of particles starting to travel (always 0, kept for compatibility)
        """
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
        """
        Start a new marketplace gathering event.

        Randomly selects particles to attend based on attendance probability,
        sets their travel targets, and logs the event.

        Args:
            particle_list (list): Particles eligible for marketplace attendance
        """
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
        """
        Update marketplace attendance timers.

        Decrements timers for particles at marketplace and initiates return
        journey when timer expires.

        Args:
            particle_list (list): Particles to update timers for
        """
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
        """
        Smoothly move particles to/from marketplace.

        Updates particle velocity to move toward target (marketplace or home)
        at constant speed. Handles arrival detection and state transitions.

        Args:
            particle (Particle): Particle to update movement for
        """
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
        """
        Execute one simulation timestep.

        Updates particle physics, checks for infections, handles recovery/death,
        manages quarantine transfers, and processes daily events (marketplace,
        community travel). Emits statistics updates on day boundaries.
        """
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
            # Quarantine zone bounds - depends on mode
            if self.mode == 'communities':
                q_bounds = (-2.9, -1.1, -2.9, -1.1)  # Lower-left tile
            else:
                q_bounds = (-0.95, -0.6, -0.95, -0.6)  # Lower-left corner
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
        """
        Handle random travel between communities.

        Randomly selects particles from each community to travel to other communities
        based on travel probability. Updates particle targets and velocities for
        inter-community travel.

        Returns:
            int: Number of particles that started traveling
        """
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
        """
        Update simulation statistics and emit stats_updated signal.

        Calculates current counts and percentages for each disease state based on
        initial population. Deaths are calculated as the difference between initial
        and current population. Appends to historical statistics and emits signal
        for UI updates.
        """
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
