"""
Preset configurations for different epidemic scenarios
Based on real-world disease data with accurate epidemiological parameters

All presets include:
- infection_radius: Transmission range (airborne > droplet > contact)
- prob_infection: Contagiousness per contact (derived from R0)
- fraction_infected_init: Patient Zero (always > 0)
- infection_duration: Disease course in days
- mortality_rate: Case fatality rate
- prob_no_symptoms: Asymptomatic carrier rate
- quarantine_after: Based on incubation period
- start_quarantine: When intervention begins
- social_distance_factor: Intervention strength (0 = none)
- social_distance_obedient: Compliance rate
- boxes_to_consider: Infection spread range
"""

PRESETS = {
    # === REAL DISEASE PRESETS (Based on actual epidemiological data) ===

    "COVID-19 (Original Strain)": {
        # R0: 2.5-3.0 | CFR: 1-2% | Incubation: 5-6 days | Asymptomatic: 30-40%
        'infection_radius': 0.15,
        'prob_infection': 0.03,  # Moderate contagiousness
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 14,  # 14-day disease course
        'mortality_rate': 0.015,  # 1.5% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 5,  # After incubation
        'start_quarantine': 10,  # Delayed response
        'prob_no_symptoms': 0.35,  # 35% asymptomatic
    },

    "COVID-19 (Delta Variant)": {
        # R0: 5-6 | CFR: 0.5-1% | Incubation: 4 days | Asymptomatic: 40%
        'infection_radius': 0.20,  # More airborne
        'prob_infection': 0.05,  # Highly contagious
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 10,  # Shorter course
        'mortality_rate': 0.008,  # 0.8% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 4,  # Shorter incubation
        'start_quarantine': 8,
        'prob_no_symptoms': 0.40,  # 40% asymptomatic
    },

    "COVID-19 (Omicron Variant)": {
        # R0: 7-10 | CFR: 0.1-0.3% | Incubation: 3 days | Asymptomatic: 50%
        'infection_radius': 0.22,  # Highly airborne
        'prob_infection': 0.07,  # Extremely contagious
        'fraction_infected_init': 0.01,  # Patient Zero: 1%
        'infection_duration': 7,  # Much shorter course
        'mortality_rate': 0.002,  # 0.2% CFR (much lower)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 3,  # Very short incubation
        'start_quarantine': 5,
        'prob_no_symptoms': 0.50,  # 50% asymptomatic
    },

    "Spanish Flu (1918)": {
        # R0: 1.8-2.0 | CFR: 2-10% | Incubation: 1-4 days | Asymptomatic: 15%
        'infection_radius': 0.18,
        'prob_infection': 0.025,  # Moderate contagiousness
        'fraction_infected_init': 0.01,  # Patient Zero: 1%
        'infection_duration': 7,  # Acute phase
        'mortality_rate': 0.05,  # 5% CFR (devastating)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 2,  # Short incubation
        'start_quarantine': 5,  # Limited early response (1918)
        'prob_no_symptoms': 0.15,  # 15% asymptomatic
    },

    "Measles": {
        # R0: 12-18 (most contagious known) | CFR: 0.2% | Incubation: 10-12 days | Asymptomatic: 5%
        'infection_radius': 0.30,  # Highly airborne (can spread rooms away)
        'prob_infection': 0.12,  # Extremely contagious
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 10,
        'mortality_rate': 0.002,  # 0.2% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 3,  # Longer range
        'quarantine_after': 3,  # Early quarantine needed
        'start_quarantine': 5,
        'prob_no_symptoms': 0.05,  # 5% asymptomatic (rash visible)
    },

    "Ebola (2014 Outbreak)": {
        # R0: 1.5-2.5 | CFR: 50% | Incubation: 8-10 days | Asymptomatic: 10%
        'infection_radius': 0.10,  # Close contact/bodily fluids
        'prob_infection': 0.08,  # High contact infection rate
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 14,  # 2-3 week illness
        'mortality_rate': 0.50,  # 50% CFR (deadly)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 1,  # Requires very close contact
        'quarantine_after': 5,
        'start_quarantine': 3,  # Rapid response needed
        'prob_no_symptoms': 0.10,  # 10% asymptomatic
    },

    "Influenza (Seasonal)": {
        # R0: 1.3-1.8 | CFR: 0.1% | Incubation: 1-4 days | Asymptomatic: 20%
        'infection_radius': 0.15,
        'prob_infection': 0.018,  # Moderate contagiousness
        'fraction_infected_init': 0.01,  # Patient Zero: 1%
        'infection_duration': 7,  # Week-long illness
        'mortality_rate': 0.001,  # 0.1% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 3,
        'start_quarantine': 7,
        'prob_no_symptoms': 0.20,  # 20% asymptomatic
    },

    "Common Cold (Rhinovirus)": {
        # R0: 2-3 | CFR: 0% | Incubation: 2-3 days | Asymptomatic: 25%
        'infection_radius': 0.15,
        'prob_infection': 0.025,  # Moderate contagiousness
        'fraction_infected_init': 0.02,  # Patient Zero: 2%
        'infection_duration': 7,  # Week-long symptoms
        'mortality_rate': 0.0,  # No mortality
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 5,  # Usually no quarantine
        'start_quarantine': 30,  # No intervention (cold)
        'prob_no_symptoms': 0.25,  # 25% asymptomatic
    },

    "SARS (2003)": {
        # R0: 2-3 | CFR: 10% | Incubation: 4-6 days | Asymptomatic: 10%
        'infection_radius': 0.18,
        'prob_infection': 0.03,  # Moderate contagiousness
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 14,
        'mortality_rate': 0.10,  # 10% CFR (severe)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 4,
        'start_quarantine': 3,  # Aggressive response
        'prob_no_symptoms': 0.10,  # 10% asymptomatic
    },

    "MERS (Coronavirus)": {
        # R0: 0.6-0.9 (low transmission) | CFR: 35% | Incubation: 5-6 days | Asymptomatic: 10%
        'infection_radius': 0.12,  # Close contact mainly
        'prob_infection': 0.015,  # Lower contagiousness
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 14,
        'mortality_rate': 0.35,  # 35% CFR (very deadly)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 5,
        'start_quarantine': 3,
        'prob_no_symptoms': 0.10,  # 10% asymptomatic
    },

    # === EDUCATIONAL PRESETS (For teaching/comparison) ===

    "Baseline Epidemic": {
        # Generic moderate epidemic for teaching
        'infection_radius': 0.15,
        'prob_infection': 0.15,  # High visibility
        'fraction_infected_init': 0.01,  # Patient Zero: 1%
        'infection_duration': 25,
        'mortality_rate': 0.02,  # 2% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 5,
        'start_quarantine': 10,
        'prob_no_symptoms': 0.20,
    },

    "Slow Burn": {
        # Low R0, long duration epidemic
        'infection_radius': 0.10,
        'prob_infection': 0.01,  # Very slow spread
        'fraction_infected_init': 0.005,  # Patient Zero: 0.5%
        'infection_duration': 30,  # Long illness
        'mortality_rate': 0.01,  # 1% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 8,
        'start_quarantine': 15,
        'prob_no_symptoms': 0.15,
    },

    "Fast Outbreak": {
        # High R0, rapid spread
        'infection_radius': 0.30,
        'prob_infection': 0.05,  # Fast spread
        'fraction_infected_init': 0.02,  # Patient Zero: 2%
        'infection_duration': 20,
        'mortality_rate': 0.03,  # 3% CFR
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 3,
        'start_quarantine': 5,
        'prob_no_symptoms': 0.25,
    },

    "Social Distancing (Weak)": {
        # Teaching intervention effectiveness
        'infection_radius': 0.15,
        'prob_infection': 0.02,
        'fraction_infected_init': 0.01,  # Patient Zero: 1%
        'infection_duration': 25,
        'mortality_rate': 0.02,  # 2% CFR
        'social_distance_factor': 0.5,  # Weak intervention
        'social_distance_obedient': 0.7,  # 70% compliance
        'boxes_to_consider': 3,
        'quarantine_after': 5,
        'start_quarantine': 10,
        'prob_no_symptoms': 0.20,
    },

    "Social Distancing (Strong)": {
        # Teaching strong intervention
        'infection_radius': 0.15,
        'prob_infection': 0.02,
        'fraction_infected_init': 0.01,  # Patient Zero: 1%
        'infection_duration': 25,
        'mortality_rate': 0.02,  # 2% CFR
        'social_distance_factor': 1.5,  # Strong intervention
        'social_distance_obedient': 0.9,  # 90% compliance
        'boxes_to_consider': 4,
        'quarantine_after': 5,
        'start_quarantine': 10,
        'prob_no_symptoms': 0.20,
    },
}
