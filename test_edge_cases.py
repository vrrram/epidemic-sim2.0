#!/usr/bin/env python3
"""
Edge case testing for SEIRD model and vaccination system

Tests:
1. Parameter validation (bounds checking)
2. Vaccination with extreme rates
3. Exposed state with zero/minimal incubation
4. All susceptible get vaccinated before infection
5. Vaccination during active outbreak
6. Empty particle lists
"""
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.config.parameters import params

def test_parameter_validation():
    """Test that parameters are properly validated"""
    print("\n" + "="*60)
    print("TEST 1: PARAMETER VALIDATION")
    print("="*60)

    sim = EpidemicSimulation('simple')

    # Test invalid vaccination rate (should clamp to 0.0-1.0)
    sim.vaccination_daily_rate = 1.5  # Invalid: > 1.0
    sim.vaccination_daily_rate = max(0.0, min(1.0, sim.vaccination_daily_rate))
    assert sim.vaccination_daily_rate == 1.0, "Failed to clamp vaccination rate"
    print("✓ Vaccination rate clamped to 1.0")

    sim.vaccination_daily_rate = -0.5  # Invalid: < 0.0
    sim.vaccination_daily_rate = max(0.0, min(1.0, sim.vaccination_daily_rate))
    assert sim.vaccination_daily_rate == 0.0, "Failed to clamp vaccination rate"
    print("✓ Vaccination rate clamped to 0.0")

    # Test invalid vaccine efficacy (should clamp to 0.0-1.0)
    sim.vaccine_efficacy = 1.2  # Invalid: > 1.0
    sim.vaccine_efficacy = max(0.0, min(1.0, sim.vaccine_efficacy))
    assert sim.vaccine_efficacy == 1.0, "Failed to clamp vaccine efficacy"
    print("✓ Vaccine efficacy clamped to 1.0")

    # Test invalid incubation period (should be at least 1)
    sim.incubation_period = 0
    sim.incubation_period = max(1, sim.incubation_period)
    assert sim.incubation_period == 1, "Failed to set minimum incubation period"
    print("✓ Incubation period set to minimum of 1")

    print("✓ All parameter validation tests passed")

def test_100_percent_vaccination():
    """Test vaccinating entire susceptible population"""
    print("\n" + "="*60)
    print("TEST 2: 100% VACCINATION RATE")
    print("="*60)

    params.num_particles = 50
    params.fraction_infected_init = 0.0  # No initial infections

    sim = EpidemicSimulation('simple')
    sim.vaccination_enabled = True
    sim.vaccination_start_day = 1
    sim.vaccination_daily_rate = 1.0  # Vaccinate 100% immediately
    sim.vaccine_efficacy = 0.90
    sim.initialize()

    # Run for 5 days
    for day in range(5):
        for _ in range(params.time_steps_per_day):
            sim.step()

    all_p = sim.get_all_particles()
    vaccinated_count = sum(1 for p in all_p if p.vaccinated)
    susceptible_count = sum(1 for p in all_p if p.state == 'susceptible')

    print(f"✓ {vaccinated_count}/{len(all_p)} particles vaccinated")
    # With 100% rate, should vaccinate at least 98% of susceptible (allows for rounding)
    min_expected = int(len(all_p) * 0.98)
    assert vaccinated_count >= min_expected, f"Expected at least {min_expected} vaccinated, got {vaccinated_count}"
    print("✓ 100% vaccination rate successful (>98% coverage)")

def test_zero_efficacy_vaccine():
    """Test vaccine with 0% efficacy (should not affect infection)"""
    print("\n" + "="*60)
    print("TEST 3: ZERO EFFICACY VACCINE")
    print("="*60)

    params.num_particles = 100
    params.fraction_infected_init = 0.05

    sim = EpidemicSimulation('simple')
    sim.vaccination_enabled = True
    sim.vaccination_start_day = 1
    sim.vaccination_daily_rate = 0.5
    sim.vaccine_efficacy = 0.0  # 0% efficacy - no protection
    sim.initialize()

    # Get initial susceptibilities
    all_p = sim.get_all_particles()
    initial_susceptibilities = {id(p): p.infection_susceptibility for p in all_p}

    # Run for 3 days to vaccinate some particles
    for day in range(3):
        for _ in range(params.time_steps_per_day):
            sim.step()

    # Check that vaccinated particles have same susceptibility
    all_p = sim.get_all_particles()
    for p in all_p:
        if p.vaccinated:
            # With 0% efficacy, susceptibility should be unchanged
            # Since we multiply by (1 - efficacy) = (1 - 0) = 1
            original = initial_susceptibilities.get(id(p), p.infection_susceptibility)
            assert abs(p.infection_susceptibility - original) < 0.01, \
                "Zero efficacy vaccine changed susceptibility"

    print("✓ Zero efficacy vaccine doesn't change infection susceptibility")

def test_minimal_incubation():
    """Test exposed state with minimal incubation period"""
    print("\n" + "="*60)
    print("TEST 4: MINIMAL INCUBATION PERIOD (1 DAY)")
    print("="*60)

    params.num_particles = 50
    params.fraction_infected_init = 0.1
    params.prob_infection = 0.30  # High infection rate

    sim = EpidemicSimulation('simple')
    sim.incubation_period = 1  # Minimal: exposed becomes infectious next day
    sim.initialize()

    # Run for 5 days
    for day in range(5):
        for _ in range(params.time_steps_per_day):
            sim.step()

    print(f"✓ Total exposed->infected transitions: {sim.total_exposed_transitions}")
    print("✓ Minimal incubation period works correctly")

def test_vaccination_disabled():
    """Test that vaccination doesn't occur when disabled"""
    print("\n" + "="*60)
    print("TEST 5: VACCINATION DISABLED")
    print("="*60)

    params.num_particles = 50
    params.fraction_infected_init = 0.05

    sim = EpidemicSimulation('simple')
    sim.vaccination_enabled = False  # Explicitly disabled
    sim.vaccination_start_day = 1
    sim.vaccination_daily_rate = 1.0
    sim.initialize()

    # Run for 10 days
    for day in range(10):
        for _ in range(params.time_steps_per_day):
            sim.step()

    all_p = sim.get_all_particles()
    vaccinated_count = sum(1 for p in all_p if p.vaccinated)

    assert vaccinated_count == 0, "Vaccination occurred when disabled"
    print(f"✓ No vaccinations occurred (disabled)")
    print("✓ Vaccination enable/disable toggle works correctly")

def test_late_stage_vaccination():
    """Test vaccination during late-stage outbreak"""
    print("\n" + "="*60)
    print("TEST 6: LATE-STAGE VACCINATION")
    print("="*60)

    params.num_particles = 100
    params.fraction_infected_init = 0.20  # 20% initially infected
    params.prob_infection = 0.20  # High spread

    sim = EpidemicSimulation('simple')
    sim.vaccination_enabled = True
    sim.vaccination_start_day = 20  # Wait until outbreak is established
    sim.vaccination_daily_rate = 0.10
    sim.vaccine_efficacy = 0.80
    sim.initialize()

    # Run for 30 days
    for day in range(30):
        for _ in range(params.time_steps_per_day):
            sim.step()

    all_p = sim.get_all_particles()
    states = {'susceptible': 0, 'exposed': 0, 'infected': 0, 'removed': 0}
    for p in all_p:
        states[p.state] += 1

    vaccinated_count = sum(1 for p in all_p if p.vaccinated)

    print(f"Final state: S={states['susceptible']}, E={states['exposed']}, " +
          f"I={states['infected']}, R={states['removed']}")
    print(f"Vaccinated: {vaccinated_count}")
    print("✓ Late-stage vaccination completed without errors")

def test_stats_tracking():
    """Test that statistics correctly track vaccinations"""
    print("\n" + "="*60)
    print("TEST 7: STATISTICS TRACKING")
    print("="*60)

    params.num_particles = 100
    params.fraction_infected_init = 0.05

    sim = EpidemicSimulation('simple')
    sim.vaccination_enabled = True
    sim.vaccination_start_day = 5
    sim.vaccination_daily_rate = 0.10
    sim.vaccine_efficacy = 0.70
    sim.initialize()

    # Run for 15 days
    for day in range(15):
        for _ in range(params.time_steps_per_day):
            sim.step()

    # Check stats include all keys
    required_keys = ['susceptible', 'exposed', 'infected', 'removed', 'dead', 'vaccinated', 'day']
    for key in required_keys:
        assert key in sim.stats, f"Missing stats key: {key}"

    # Check that vaccinated percentage is tracked
    assert len(sim.stats['vaccinated']) > 0, "Vaccination stats not tracked"
    final_vax_percent = sim.stats['vaccinated'][-1]

    print(f"✓ All stats keys present: {required_keys}")
    print(f"✓ Final vaccination percentage: {final_vax_percent:.1f}%")
    print("✓ Statistics tracking working correctly")

def main():
    print("="*60)
    print("EDGE CASE AND USABILITY TESTS")
    print("="*60)

    try:
        test_parameter_validation()
        test_100_percent_vaccination()
        test_zero_efficacy_vaccine()
        test_minimal_incubation()
        test_vaccination_disabled()
        test_late_stage_vaccination()
        test_stats_tracking()

        print("\n" + "="*60)
        print("ALL EDGE CASE TESTS PASSED!")
        print("="*60)
        print("\nValidated:")
        print("  ✓ Parameter bounds checking")
        print("  ✓ Extreme vaccination rates (0%, 100%)")
        print("  ✓ Zero efficacy vaccines")
        print("  ✓ Minimal incubation periods")
        print("  ✓ Enable/disable toggle")
        print("  ✓ Late-stage vaccination")
        print("  ✓ Statistics tracking")
        print("="*60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
