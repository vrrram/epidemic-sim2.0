"""
Particle class representing individual agents in the epidemic simulation

Each particle has physical properties (position, velocity) and epidemiological
state (susceptible, infected, removed/recovered, or dead).

Uses THREE statistical distributions as required for IHK project:
1. UNIFORM - Initial positions and velocities
2. NORMAL - Individual infection susceptibility variation
3. EXPONENTIAL - Individual recovery time variation
"""
import random
import numpy as np
from epidemic_sim.config.parameters import params


class Particle:
    """
    Individual particle/agent in the epidemic simulation

    Represents a person with:
    - Physical properties: position, velocity, acceleration
    - Epidemiological state: susceptible, infected, removed
    - Individual variation: susceptibility, recovery time
    - Behavior flags: quarantine status, symptom display, social distancing
    """

    def __init__(self, x, y, state='susceptible'):
        """
        Initialize a particle with position and state

        Args:
            x, y: Initial position coordinates
            state: Initial epidemiological state ('susceptible', 'infected', 'removed')
        """
        # POSITION (initialized with parameters, will use UNIFORM distribution in simulation)
        self.x = x
        self.y = y

        # VELOCITY - UNIFORM DISTRIBUTION (Gleichverteilung)
        # All directions and speeds equally likely - no inherent movement bias
        self.vx = random.uniform(-0.2, 0.2)
        self.vy = random.uniform(-0.2, 0.2)

        self.ax = 0  # Acceleration X
        self.ay = 0  # Acceleration Y

        # Epidemiological state
        self.state = state
        self.days_exposed = 0  # Days in exposed state (incubation period)
        self.days_infected = 0
        self.infection_count = 0

        # Behavior and symptoms
        self.quarantined = False
        self.days_in_quarantine = 0  # Track quarantine duration
        self.shows_symptoms = True
        self.obeys_social_distance = random.random() < params.social_distance_obedient

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

        # Vaccination tracking
        self.vaccinated = False
        self.vaccination_day = None
        self.vaccine_efficacy = 0.0  # Will be set when vaccinated

        # Check if particle is asymptomatic infected
        if state == 'infected' and random.random() < params.prob_no_symptoms:
            self.shows_symptoms = False

    def distance_to(self, other):
        """
        Calculate Euclidean distance to another particle

        Args:
            other: Another Particle object

        Returns:
            float: Distance between this particle and the other
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5
