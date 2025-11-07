"""
Simulation parameters configuration
Contains SimParams class with all configurable simulation parameters
"""


class SimParams:
    """
    Global parameters object for epidemic simulation

    Contains all configurable parameters for:
    - Infection dynamics
    - Population behavior
    - Quarantine rules
    - Mortality rates
    - Community and marketplace settings
    """

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


# Global instance
params = SimParams()
