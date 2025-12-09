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


# Preset categories for organized display
PRESET_CATEGORIES = {
    "Historical Pandemics": [
        "Spanish Flu (1918)",
        "Smallpox (Historical)",
        "Black Death (Plague)",
        "Polio (Pre-Vaccine Era)",
    ],

    "Modern Pandemics (COVID-19)": [
        "COVID-19 (Original Strain)",
        "COVID-19 (Delta Variant)",
        "COVID-19 (Omicron Variant)",
    ],

    "Modern Outbreaks": [
        "H1N1 Swine Flu (2009)",
        "SARS (2003)",
        "MERS (Coronavirus)",
        "Ebola (2014 Outbreak)",
        "Tuberculosis (Modern)",
    ],

    "Highly Contagious Viral": [
        "Measles",
        "Chickenpox (Varicella)",
        "Pertussis (Whooping Cough)",
        "Rubella (German Measles)",
        "Mumps",
    ],

    "Bacterial Diseases": [
        "Cholera (Vibrio cholerae)",
        "Typhoid Fever (Salmonella typhi)",
        "Diphtheria (Corynebacterium diphtheriae)",
    ],

    "Respiratory Viruses": [
        "Influenza (Seasonal)",
        "Common Cold (Rhinovirus)",
    ],

    "Educational Scenarios": [
        "Baseline Epidemic",
        "Slow Burn",
        "Fast Outbreak",
        "Social Distancing (Weak)",
        "Social Distancing (Strong)",
    ],
}


# Flat list of all presets for backward compatibility
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

    # === HISTORICAL PANDEMICS (Pre-20th Century) ===

    "Smallpox (Historical)": {
        # Historical data from WHO eradication program
        # R0: 3.5-6.0 | CFR: 30% | Incubation: 12-14 days | Asymptomatic: 0%
        # Source: WHO Smallpox Fact Sheet, Henderson DA (2009) Smallpox: The Death of a Disease
        'infection_radius': 0.18,           # Airborne transmission (respiratory droplets)
        'prob_infection': 0.045,            # High transmission (R0≈5)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 21,           # 3 weeks illness
        'mortality_rate': 0.30,             # 30% CFR (variola major)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 12,             # After incubation
        'start_quarantine': 3,              # Rapid isolation historically
        'prob_no_symptoms': 0.0,            # Very symptomatic (distinctive rash)
    },

    "Black Death (Plague)": {
        # Bubonic plague (Yersinia pestis) - 14th century pandemic
        # R0: 1.5-3.0 | CFR: 50-90% | Incubation: 2-6 days | Asymptomatic: 0%
        # Source: Benedictow OJ (2004) The Black Death 1346-1353
        'infection_radius': 0.12,           # Flea-borne (close contact for pneumonic)
        'prob_infection': 0.025,            # Moderate transmission (R0≈2)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 7,            # Acute phase 3-7 days
        'mortality_rate': 0.60,             # 60% CFR (without antibiotics)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 4,              # After symptoms appear
        'start_quarantine': 8,              # Limited medieval response
        'prob_no_symptoms': 0.0,            # Highly symptomatic (buboes)
    },

    "Polio (Pre-Vaccine Era)": {
        # Poliovirus - paralytic poliomyelitis
        # R0: 5-7 | CFR: 5-15% (paralytic cases) | Incubation: 6-20 days | Asymptomatic: 90%
        # Source: CDC Pink Book (2021), Paul JR (1971) A History of Poliomyelitis
        'infection_radius': 0.20,           # Fecal-oral transmission (high contact)
        'prob_infection': 0.055,            # High transmission (R0≈6)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 14,           # 2 weeks acute phase
        'mortality_rate': 0.10,             # 10% CFR (paralytic cases)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 10,             # After incubation
        'start_quarantine': 7,
        'prob_no_symptoms': 0.90,           # 90% asymptomatic or mild
    },

    # === MODERN PANDEMICS (20th-21st Century) ===

    "H1N1 Swine Flu (2009)": {
        # 2009 H1N1 influenza pandemic
        # R0: 1.4-1.6 | CFR: 0.02% | Incubation: 1-4 days | Asymptomatic: 20%
        # Source: WHO (2010), CDC 2009 H1N1 Final Estimates
        'infection_radius': 0.16,           # Respiratory droplets
        'prob_infection': 0.022,            # Moderate contagiousness (R0≈1.5)
        'fraction_infected_init': 0.01,     # Patient Zero: 1%
        'infection_duration': 7,            # Week-long illness
        'mortality_rate': 0.0002,           # 0.02% CFR (very low)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 3,              # Short incubation
        'start_quarantine': 10,             # Delayed response
        'prob_no_symptoms': 0.20,           # 20% asymptomatic
    },

    "Tuberculosis (Modern)": {
        # Mycobacterium tuberculosis - active pulmonary TB
        # R0: 1-4 | CFR: 15-45% (untreated) | Incubation: weeks-months | Asymptomatic: 10%
        # Source: WHO TB Report 2023, CDC TB Fact Sheet
        'infection_radius': 0.15,           # Airborne (prolonged exposure)
        'prob_infection': 0.03,             # Requires prolonged contact (R0≈2.5)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 60,           # Chronic disease (months)
        'mortality_rate': 0.30,             # 30% CFR (untreated)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 14,             # After diagnosis
        'start_quarantine': 20,             # Slow diagnosis historically
        'prob_no_symptoms': 0.10,           # 10% asymptomatic carriers
    },

    # === HIGHLY CONTAGIOUS VIRAL DISEASES ===

    "Chickenpox (Varicella)": {
        # Varicella-zoster virus
        # R0: 10-12 | CFR: 0.001% | Incubation: 10-21 days | Asymptomatic: 5%
        # Source: CDC Chickenpox Fact Sheet, Marin M et al (2016)
        'infection_radius': 0.28,           # Highly airborne (can spread through ventilation)
        'prob_infection': 0.10,             # Extremely contagious (R0≈11)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 10,           # 10 days of rash
        'mortality_rate': 0.00001,          # 0.001% CFR (very low)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 3,             # Long range transmission
        'quarantine_after': 5,              # Early quarantine needed
        'start_quarantine': 7,
        'prob_no_symptoms': 0.05,           # 5% asymptomatic (rash usually visible)
    },

    "Pertussis (Whooping Cough)": {
        # Bordetella pertussis
        # R0: 12-17 | CFR: 1-2% (infants) | Incubation: 7-10 days | Asymptomatic: 10%
        # Source: CDC Pertussis Surveillance, Cherry JD (2012)
        'infection_radius': 0.20,           # Respiratory droplets (close contact)
        'prob_infection': 0.13,             # Extremely contagious (R0≈15)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 21,           # 3 weeks (catarrhal + paroxysmal phase)
        'mortality_rate': 0.015,            # 1.5% CFR (mainly infants)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 7,
        'start_quarantine': 10,
        'prob_no_symptoms': 0.10,           # 10% asymptomatic
    },

    "Mumps": {
        # Mumps virus (paramyxovirus)
        # R0: 4-7 | CFR: <0.01% | Incubation: 16-18 days | Asymptomatic: 20%
        # Source: CDC Pink Book, Rubin S et al (2015)
        'infection_radius': 0.18,           # Respiratory droplets
        'prob_infection': 0.05,             # High contagiousness (R0≈5.5)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 14,           # 2 weeks illness
        'mortality_rate': 0.00005,          # <0.01% CFR (very low)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 16,             # After incubation
        'start_quarantine': 10,
        'prob_no_symptoms': 0.20,           # 20% asymptomatic
    },

    "Rubella (German Measles)": {
        # Rubella virus
        # R0: 5-7 | CFR: <0.01% | Incubation: 14-21 days | Asymptomatic: 25-50%
        # Source: CDC Pink Book, Lambert N et al (2015)
        'infection_radius': 0.17,           # Respiratory droplets
        'prob_infection': 0.055,            # High contagiousness (R0≈6)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 10,           # 10 days rash
        'mortality_rate': 0.00001,          # <0.01% CFR (very low)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 14,             # After incubation
        'start_quarantine': 7,
        'prob_no_symptoms': 0.35,           # 35% asymptomatic (avg of 25-50%)
    },

    # === BACTERIAL DISEASES ===

    "Cholera (Vibrio cholerae)": {
        # Vibrio cholerae - epidemic cholera
        # R0: 1.5-3.0 | CFR: 50% (untreated), 1% (treated) | Incubation: 1-3 days | Asymptomatic: 75%
        # Source: WHO Cholera Fact Sheet, Ali M et al (2015)
        'infection_radius': 0.10,           # Fecal-oral (contaminated water/food)
        'prob_infection': 0.025,            # Moderate transmission (R0≈2)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 7,            # 3-7 days acute diarrhea
        'mortality_rate': 0.25,             # 25% CFR (limited treatment scenario)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 1,             # Close contact/sanitation
        'quarantine_after': 2,              # Rapid onset
        'start_quarantine': 5,
        'prob_no_symptoms': 0.75,           # 75% asymptomatic or mild
    },

    "Typhoid Fever (Salmonella typhi)": {
        # Salmonella typhi
        # R0: 3-21 (varies by sanitation) | CFR: 10-20% (untreated) | Incubation: 6-30 days | Asymptomatic: 10%
        # Source: WHO Typhoid Fact Sheet, Crump JA et al (2015)
        'infection_radius': 0.12,           # Fecal-oral transmission
        'prob_infection': 0.08,             # High transmission in poor sanitation (R0≈10)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 21,           # 3-4 weeks illness
        'mortality_rate': 0.15,             # 15% CFR (untreated)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 10,             # After symptoms appear
        'start_quarantine': 8,
        'prob_no_symptoms': 0.10,           # 10% asymptomatic carriers
    },

    "Diphtheria (Corynebacterium diphtheriae)": {
        # Corynebacterium diphtheriae
        # R0: 6-7 | CFR: 5-10% | Incubation: 2-5 days | Asymptomatic: 5%
        # Source: CDC Pink Book, Truelove SA et al (2020)
        'infection_radius': 0.17,           # Respiratory droplets (close contact)
        'prob_infection': 0.06,             # High contagiousness (R0≈6.5)
        'fraction_infected_init': 0.005,    # Patient Zero: 0.5%
        'infection_duration': 14,           # 2 weeks illness
        'mortality_rate': 0.075,            # 7.5% CFR (without antitoxin)
        'social_distance_factor': 0.0,
        'social_distance_obedient': 1.0,
        'boxes_to_consider': 2,
        'quarantine_after': 4,              # After symptoms appear
        'start_quarantine': 5,
        'prob_no_symptoms': 0.05,           # 5% asymptomatic carriers
    },
}
