"""
Simulation parameters configuration
Contains SimParams class with all configurable simulation parameters
"""
import json
from typing import List, Dict, Tuple, Any


class ValidationError(Exception):
    """Exception raised when parameter validation fails"""
    pass


class SimParams:
    """
    Global parameters object for epidemic simulation

    Contains all configurable parameters for:
    - Infection dynamics
    - Population behavior
    - Quarantine rules
    - Mortality rates
    - Community and marketplace settings

    PARAMETER REFERENCE:
    ====================

    INFECTION DYNAMICS:
    -------------------
    infection_radius (float: 0.01-0.5)
        Range at which a particle can infect others (world coordinates)
        • Airborne diseases (e.g., Measles): 0.25-0.30
        • Respiratory droplets (e.g., COVID-19): 0.15-0.20
        • Close contact (e.g., Ebola): 0.08-0.12
        • Affects spatial grid efficiency and R0

    prob_infection (float: 0.0-1.0)
        Probability of infection per contact per time step
        • Derived from R0: R0 ≈ prob_infection × contacts × duration
        • Measles (R0≈15): 0.10-0.13
        • COVID-19 (R0≈3): 0.03-0.05
        • Seasonal flu (R0≈1.5): 0.018-0.025
        • Key driver of epidemic speed

    fraction_infected_init (float: 0.0-1.0)
        Initial infected fraction (Patient Zero)
        • Typical: 0.005-0.01 (0.5%-1%)
        • Must be > 0 for epidemic to start
        • Higher values skip early growth phase

    infection_duration (int: 1-365 days)
        Days a particle remains infected before recovery/death
        • Acute diseases (e.g., Flu): 7-10 days
        • Moderate (e.g., COVID-19): 14-21 days
        • Chronic (e.g., TB): 60+ days
        • Directly impacts R0 and peak infections

    mortality_rate (float: 0.0-1.0)
        Probability of death (case fatality rate)
        • Common cold: 0.0
        • COVID-19: 0.01-0.02 (1-2%)
        • Ebola: 0.50 (50%)
        • Black Death: 0.60 (60%)
        • Applied daily during infection

    prob_no_symptoms (float: 0.0-1.0)
        Fraction of infected who are asymptomatic
        • Asymptomatic carriers: mobile, don't quarantine
        • COVID-19: 0.30-0.40 (30-40%)
        • Polio: 0.90 (90%)
        • Smallpox: 0.0 (highly symptomatic)
        • Critical for "silent spread"

    SOCIAL DISTANCING:
    ------------------
    social_distance_factor (float: 0.0-5.0)
        Strength of social distancing intervention
        • 0.0: No intervention
        • 0.5: Weak distancing
        • 1.0-1.5: Strong distancing
        • 2.0+: Lockdown-level restrictions
        • Reduces particle movement and interaction

    social_distance_obedient (float: 0.0-1.0)
        Compliance rate for social distancing
        • 0.0: No one complies
        • 0.7: 70% compliance (typical)
        • 0.9: 90% compliance (high)
        • 1.0: Perfect compliance
        • Multiplies with social_distance_factor

    boxes_to_consider (int: 1-10)
        Number of spatial grid boxes to check for infections
        • 1: Only immediate neighbors (short-range)
        • 2: Standard (balances realism and performance)
        • 3+: Long-range airborne diseases (e.g., Measles)
        • Higher values increase computation but improve accuracy

    PARTICLE PHYSICS:
    -----------------
    num_particles (int: 10-5000)
        Total population size
        • 50-200: Fast, educational
        • 200-500: Standard simulations
        • 500-1000: Detailed analysis
        • 1000+: Performance intensive
        • Affects statistical accuracy

    particle_size (int: 1-20 pixels)
        Visual size of particles on canvas
        • Scaled automatically for visibility
        • No effect on infection dynamics
        • Typical: 6-8 pixels

    speed_limit (float: 0.01-1.0)
        Maximum particle velocity (world units/time step)
        • Typical: 0.1 (moderate movement)
        • Higher: Faster mixing, faster spread
        • Lower: Localized clusters, slower spread
        • Affects contact rate

    boundary_force (float: 0.01-2.0)
        Strength of repulsion from boundaries
        • 0.2: Standard (keeps particles in bounds)
        • Higher: Stronger containment
        • Lower: Particles near edges

    time_steps_per_day (int: 1-100)
        Simulation steps per simulated day
        • 24: Standard (hourly updates)
        • Higher: Smoother animation, more precise
        • Lower: Faster simulation, less smooth
        • Affects daily calculations (quarantine, etc.)

    QUARANTINE SYSTEM:
    ------------------
    quarantine_enabled (bool)
        Enable/disable quarantine system
        • True: Symptomatic particles move to quarantine zone
        • False: No quarantine (free movement)

    quarantine_after (int: 0-365 days)
        Days after infection before quarantine
        • Represents incubation period
        • COVID-19: 5 days
        • Measles: 3 days (early quarantine)
        • 0: Immediate quarantine (unrealistic)

    start_quarantine (int: 0-365 days)
        Simulation day when quarantine begins
        • Represents policy response delay
        • 3-5: Rapid response
        • 10-15: Delayed response
        • 30+: No intervention (educational)

    quarantine_duration (int: 0-365 days)
        Days to stay in quarantine
        • 0: Until recovered (standard)
        • 14: COVID-19 protocol
        • Positive value: Fixed duration

    COMMUNITIES:
    ------------
    travel_probability (float: 0.0-1.0)
        Daily probability of traveling between communities
        • 0.01-0.02: Typical (1-2% daily)
        • 0.0: Isolated communities
        • Higher: Frequent mixing

    num_per_community (int: 1-500)
        Particles per community in grid mode
        • Typical: 60-80
        • Total particles = num_per_community × 9 communities
        • Affects community density

    communities_to_infect (int: 1-9)
        Initial communities with infections
        • 1: Single outbreak origin
        • 2-3: Multiple seeding
        • 9: All communities (worst case)

    MARKETPLACE:
    ------------
    marketplace_enabled (bool)
        Enable marketplace gathering system
        • True: Periodic mass gatherings
        • False: No marketplace events

    marketplace_interval (int: 0-30 days)
        Days between marketplace events
        • 1: Daily market (realistic)
        • 7: Weekly market
        • 0: Continuous gathering

    marketplace_duration (int: 1-200 time steps)
        How long particles stay at marketplace
        • 50: Realistic shopping/work time
        • 100+: Extended gathering
        • Longer = more transmission risk

    marketplace_attendance (float: 0.0-1.0)
        Fraction of population attending marketplace
        • 0.08: Trickle effect (realistic)
        • 0.2-0.5: Major gathering
        • 1.0: Everyone attends (superspreader)

    marketplace_x, marketplace_y (float: -10.0 to 10.0)
        Marketplace location in world coordinates
        • Used in simple/quarantine mode
        • Default: (0, 0) center

    marketplace_community_id (int: 0-8)
        Marketplace community in grid mode
        • Default: 4 (center tile of 3×3 grid)
        • 0-8: Any community can host

    VISUALIZATION:
    --------------
    show_infection_radius (bool)
        Display infection radius circles
        • True: Show visual range indicator
        • False: Clean display
        • Educational tool for understanding transmission range

    METHODS:
    --------
    validate() -> Tuple[bool, List[str]]
        Validate all parameters are within bounds
        Returns (is_valid, error_messages)

    _estimate_r0() -> float
        Estimate basic reproduction number (R0)
        Rough approximation for epidemiological realism

    to_dict() -> Dict[str, Any]
        Export parameters to dictionary

    from_dict(data: Dict[str, Any])
        Import parameters from dictionary

    save_to_file(filename: str)
        Save parameters to JSON file

    load_from_file(filename: str)
        Load parameters from JSON file with validation
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
        self.quarantine_duration = 14  # Days to stay in quarantine (0 = until recovered)
        self.prob_no_symptoms = 0.20  # 20% asymptomatic (more realistic)

        # Mortality (SEIRD-ready)
        self.mortality_rate = 0.0  # 0-1 (0% to 100%)

        # Communities
        self.travel_probability = 0.02
        self.num_per_community = 60
        self.communities_to_infect = 2

        # Marketplace gathering parameters (REALISTIC SETTINGS)
        self.marketplace_enabled = False
        self.marketplace_interval = 1  # Daily marketplace availability
        self.marketplace_duration = 50  # Time steps particles stay (realistic shopping/work time)
        self.marketplace_attendance = 0.08  # 8% attend daily (realistic trickle, not mass gathering)
        self.marketplace_x = 0.0  # Center location (simple/quarantine mode)
        self.marketplace_y = 0.0
        self.marketplace_community_id = 4  # Center tile in 3x3 grid (communities mode)

        # Visualization options
        self.show_infection_radius = False  # Toggle infection radius visualization

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate all parameters are within realistic and safe bounds.

        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_error_messages)
        """
        errors = []
        warnings = []

        # Infection parameters validation
        if not 0.0 <= self.prob_infection <= 1.0:
            errors.append(f"prob_infection must be 0.0-1.0 (got {self.prob_infection})")

        if not 0.01 <= self.infection_radius <= 0.5:
            errors.append(f"infection_radius must be 0.01-0.5 (got {self.infection_radius})")

        if not 0.0 <= self.fraction_infected_init <= 1.0:
            errors.append(f"fraction_infected_init must be 0.0-1.0 (got {self.fraction_infected_init})")
        elif self.fraction_infected_init == 0.0:
            warnings.append("fraction_infected_init is 0.0 - no initial infections")

        if not 1 <= self.infection_duration <= 365:
            errors.append(f"infection_duration must be 1-365 days (got {self.infection_duration})")

        if not 0.0 <= self.mortality_rate <= 1.0:
            errors.append(f"mortality_rate must be 0.0-1.0 (got {self.mortality_rate})")

        if not 0.0 <= self.prob_no_symptoms <= 1.0:
            errors.append(f"prob_no_symptoms must be 0.0-1.0 (got {self.prob_no_symptoms})")

        # Social distancing validation
        if not 0.0 <= self.social_distance_factor <= 5.0:
            errors.append(f"social_distance_factor must be 0.0-5.0 (got {self.social_distance_factor})")

        if not 0.0 <= self.social_distance_obedient <= 1.0:
            errors.append(f"social_distance_obedient must be 0.0-1.0 (got {self.social_distance_obedient})")

        if not 1 <= self.boxes_to_consider <= 10:
            errors.append(f"boxes_to_consider must be 1-10 (got {self.boxes_to_consider})")

        # Particle physics validation
        if not 10 <= self.num_particles <= 5000:
            errors.append(f"num_particles must be 10-5000 (got {self.num_particles})")
        elif self.num_particles > 1000:
            warnings.append(f"num_particles={self.num_particles} may cause performance issues (recommend <1000)")

        if not 1 <= self.particle_size <= 20:
            errors.append(f"particle_size must be 1-20 pixels (got {self.particle_size})")

        if not 0.01 <= self.speed_limit <= 1.0:
            errors.append(f"speed_limit must be 0.01-1.0 (got {self.speed_limit})")

        if not 0.01 <= self.boundary_force <= 2.0:
            errors.append(f"boundary_force must be 0.01-2.0 (got {self.boundary_force})")

        if not 1 <= self.time_steps_per_day <= 100:
            errors.append(f"time_steps_per_day must be 1-100 (got {self.time_steps_per_day})")

        # Quarantine validation
        if not 0 <= self.quarantine_after <= 365:
            errors.append(f"quarantine_after must be 0-365 days (got {self.quarantine_after})")

        if not 0 <= self.start_quarantine <= 365:
            errors.append(f"start_quarantine must be 0-365 days (got {self.start_quarantine})")

        if not 0 <= self.quarantine_duration <= 365:
            errors.append(f"quarantine_duration must be 0-365 days (got {self.quarantine_duration})")

        # Community validation
        if not 0.0 <= self.travel_probability <= 1.0:
            errors.append(f"travel_probability must be 0.0-1.0 (got {self.travel_probability})")

        if not 1 <= self.num_per_community <= 500:
            errors.append(f"num_per_community must be 1-500 (got {self.num_per_community})")

        if not 1 <= self.communities_to_infect <= 9:
            errors.append(f"communities_to_infect must be 1-9 (got {self.communities_to_infect})")

        # Marketplace validation
        if not 0 <= self.marketplace_interval <= 30:
            errors.append(f"marketplace_interval must be 0-30 days (got {self.marketplace_interval})")

        if not 1 <= self.marketplace_duration <= 200:
            errors.append(f"marketplace_duration must be 1-200 time steps (got {self.marketplace_duration})")

        if not 0.0 <= self.marketplace_attendance <= 1.0:
            errors.append(f"marketplace_attendance must be 0.0-1.0 (got {self.marketplace_attendance})")

        # Estimate R0 for epidemiological realism check
        if errors == []:  # Only calculate if basic parameters are valid
            estimated_r0 = self._estimate_r0()
            if estimated_r0 < 0.1 or estimated_r0 > 25:
                warnings.append(f"Estimated R0={estimated_r0:.2f} is unusual (typical: 0.5-20)")

        # Print warnings if any
        if warnings:
            print("\n⚠️  Parameter Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        return (len(errors) == 0, errors)

    def _estimate_r0(self) -> float:
        """
        Estimate basic reproduction number (R0) from parameters.

        This is a rough approximation:
        R0 ≈ prob_infection × average_contacts_per_day × infection_duration

        Returns:
            float: Estimated R0 value
        """
        # Estimate average contacts based on infection radius and boxes
        # This is highly simplified
        contact_factor = (self.infection_radius * 10) * (self.boxes_to_consider ** 2)
        contacts_per_day = contact_factor * (1.0 - self.social_distance_factor * self.social_distance_obedient * 0.3)

        # R0 calculation
        r0 = self.prob_infection * contacts_per_day * self.infection_duration

        return r0

    def to_dict(self) -> Dict[str, Any]:
        """
        Export parameters to dictionary format.

        Returns:
            Dict[str, Any]: Dictionary of all parameters
        """
        return {
            # Infection parameters
            'infection_radius': self.infection_radius,
            'prob_infection': self.prob_infection,
            'fraction_infected_init': self.fraction_infected_init,
            'infection_duration': self.infection_duration,
            'mortality_rate': self.mortality_rate,
            'prob_no_symptoms': self.prob_no_symptoms,

            # Social distancing
            'social_distance_factor': self.social_distance_factor,
            'social_distance_obedient': self.social_distance_obedient,
            'boxes_to_consider': self.boxes_to_consider,

            # Particle physics
            'num_particles': self.num_particles,
            'particle_size': self.particle_size,
            'speed_limit': self.speed_limit,
            'boundary_force': self.boundary_force,
            'time_steps_per_day': self.time_steps_per_day,

            # Quarantine
            'quarantine_enabled': self.quarantine_enabled,
            'quarantine_after': self.quarantine_after,
            'start_quarantine': self.start_quarantine,
            'quarantine_duration': self.quarantine_duration,

            # Communities
            'travel_probability': self.travel_probability,
            'num_per_community': self.num_per_community,
            'communities_to_infect': self.communities_to_infect,

            # Marketplace
            'marketplace_enabled': self.marketplace_enabled,
            'marketplace_interval': self.marketplace_interval,
            'marketplace_duration': self.marketplace_duration,
            'marketplace_attendance': self.marketplace_attendance,
            'marketplace_x': self.marketplace_x,
            'marketplace_y': self.marketplace_y,
            'marketplace_community_id': self.marketplace_community_id,

            # Visualization
            'show_infection_radius': self.show_infection_radius,
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Import parameters from dictionary format.

        Args:
            data: Dictionary containing parameter values
        """
        # Infection parameters
        if 'infection_radius' in data:
            self.infection_radius = data['infection_radius']
        if 'prob_infection' in data:
            self.prob_infection = data['prob_infection']
        if 'fraction_infected_init' in data:
            self.fraction_infected_init = data['fraction_infected_init']
        if 'infection_duration' in data:
            self.infection_duration = data['infection_duration']
        if 'mortality_rate' in data:
            self.mortality_rate = data['mortality_rate']
        if 'prob_no_symptoms' in data:
            self.prob_no_symptoms = data['prob_no_symptoms']

        # Social distancing
        if 'social_distance_factor' in data:
            self.social_distance_factor = data['social_distance_factor']
        if 'social_distance_obedient' in data:
            self.social_distance_obedient = data['social_distance_obedient']
        if 'boxes_to_consider' in data:
            self.boxes_to_consider = data['boxes_to_consider']

        # Particle physics
        if 'num_particles' in data:
            self.num_particles = data['num_particles']
        if 'particle_size' in data:
            self.particle_size = data['particle_size']
        if 'speed_limit' in data:
            self.speed_limit = data['speed_limit']
        if 'boundary_force' in data:
            self.boundary_force = data['boundary_force']
        if 'time_steps_per_day' in data:
            self.time_steps_per_day = data['time_steps_per_day']

        # Quarantine
        if 'quarantine_enabled' in data:
            self.quarantine_enabled = data['quarantine_enabled']
        if 'quarantine_after' in data:
            self.quarantine_after = data['quarantine_after']
        if 'start_quarantine' in data:
            self.start_quarantine = data['start_quarantine']
        if 'quarantine_duration' in data:
            self.quarantine_duration = data['quarantine_duration']

        # Communities
        if 'travel_probability' in data:
            self.travel_probability = data['travel_probability']
        if 'num_per_community' in data:
            self.num_per_community = data['num_per_community']
        if 'communities_to_infect' in data:
            self.communities_to_infect = data['communities_to_infect']

        # Marketplace
        if 'marketplace_enabled' in data:
            self.marketplace_enabled = data['marketplace_enabled']
        if 'marketplace_interval' in data:
            self.marketplace_interval = data['marketplace_interval']
        if 'marketplace_duration' in data:
            self.marketplace_duration = data['marketplace_duration']
        if 'marketplace_attendance' in data:
            self.marketplace_attendance = data['marketplace_attendance']
        if 'marketplace_x' in data:
            self.marketplace_x = data['marketplace_x']
        if 'marketplace_y' in data:
            self.marketplace_y = data['marketplace_y']
        if 'marketplace_community_id' in data:
            self.marketplace_community_id = data['marketplace_community_id']

        # Visualization
        if 'show_infection_radius' in data:
            self.show_infection_radius = data['show_infection_radius']

    def save_to_file(self, filename: str) -> None:
        """
        Save parameters to JSON file.

        Args:
            filename: Path to save file
        """
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"✓ Configuration saved to {filename}")

    def load_from_file(self, filename: str) -> None:
        """
        Load parameters from JSON file.

        Args:
            filename: Path to load file
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        self.from_dict(data)

        # Validate after loading
        is_valid, errors = self.validate()
        if not is_valid:
            raise ValidationError(f"Loaded configuration is invalid:\n" + "\n".join(f"  - {e}" for e in errors))

        print(f"✓ Configuration loaded from {filename}")


# Global instance
params = SimParams()
