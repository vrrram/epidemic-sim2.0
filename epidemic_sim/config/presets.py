"""
Preset configurations for different epidemic scenarios
Educational, intervention, and historical disease presets
"""

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
