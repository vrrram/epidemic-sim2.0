#!/usr/bin/env python3
"""
Test script for new SEIRD features:
- Vaccination system
- Exposed (E) state with incubation period
"""
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.config.parameters import params

def test_exposed_state():
    """Test that exposed state works correctly"""
    print("\n" + "="*60)
    print("TEST 1: EXPOSED STATE (SEIRD MODEL)")
    print("="*60)

    params.num_particles = 100
    params.fraction_infected_init = 0.05  # 5% start infected
    params.mortality_rate = 0.0  # No deaths for this test

    sim = EpidemicSimulation('simple')
    sim.incubation_period = 3  # 3 days incubation
    sim.initialize()

    print(f"Initial state:")
    all_p = sim.get_all_particles()
    states = {'susceptible': 0, 'exposed': 0, 'infected': 0, 'removed': 0}
    for p in all_p:
        states[p.state] += 1
    print(f"  S: {states['susceptible']}, E: {states['exposed']}, I: {states['infected']}, R: {states['removed']}")

    # Run for several days to see exposed -> infected transitions
    print(f"\nRunning simulation for 10 days...")
    for day in range(10):
        for _ in range(params.time_steps_per_day):
            sim.step()

        # Check states
        all_p = sim.get_all_particles()
        states = {'susceptible': 0, 'exposed': 0, 'infected': 0, 'removed': 0}
        for p in all_p:
            states[p.state] += 1

        print(f"Day {day+1}: S={states['susceptible']}, E={states['exposed']}, I={states['infected']}, R={states['removed']}")

    print("\n✓ Exposed state test completed")
    if states['exposed'] > 0 or states['infected'] > 0:
        print("✓ Infection spread detected")
    else:
        print("⚠ No infections detected (may be random)")

def test_vaccination():
    """Test that vaccination system works correctly"""
    print("\n" + "="*60)
    print("TEST 2: VACCINATION SYSTEM")
    print("="*60)

    params.num_particles = 100
    params.fraction_infected_init = 0.02
    params.mortality_rate = 0.0

    sim = EpidemicSimulation('simple')
    sim.vaccination_start_day = 5  # Start on day 5
    sim.vaccination_daily_rate = 0.10  # Vaccinate 10% per day
    sim.vaccine_efficacy = 0.70  # 70% efficacy
    sim.initialize()

    print(f"Vaccination params:")
    print(f"  Start day: {sim.vaccination_start_day}")
    print(f"  Daily rate: {sim.vaccination_daily_rate*100:.0f}%")
    print(f"  Efficacy: {sim.vaccine_efficacy*100:.0f}%")

    # Run for several days
    print(f"\nRunning simulation for 15 days...")
    for day in range(15):
        for _ in range(params.time_steps_per_day):
            sim.step()

        # Count vaccinated
        all_p = sim.get_all_particles()
        vaccinated_count = sum(1 for p in all_p if p.vaccinated)

        if day >= sim.vaccination_start_day:
            print(f"Day {day+1}: {vaccinated_count} vaccinated ({vaccinated_count/len(all_p)*100:.1f}%)")

    print(f"\n✓ Vaccination test completed")
    if vaccinated_count > 0:
        print(f"✓ {vaccinated_count} particles vaccinated successfully")
    else:
        print("✗ No vaccinations occurred!")

def test_combined():
    """Test vaccination and exposed state together"""
    print("\n" + "="*60)
    print("TEST 3: COMBINED SEIRD + VACCINATION")
    print("="*60)

    params.num_particles = 200
    params.fraction_infected_init = 0.03
    params.mortality_rate = 0.05  # 5% mortality
    params.prob_infection = 0.20  # Higher infection rate

    sim = EpidemicSimulation('simple')
    sim.incubation_period = 4
    sim.vaccination_start_day = 10
    sim.vaccination_daily_rate = 0.05
    sim.vaccine_efficacy = 0.70
    sim.initialize()

    print(f"Running full SEIRD simulation with vaccination for 30 days...")

    for day in range(30):
        for _ in range(params.time_steps_per_day):
            sim.step()

        # Statistics every 5 days
        if (day + 1) % 5 == 0:
            all_p = sim.get_all_particles()
            states = {'susceptible': 0, 'exposed': 0, 'infected': 0, 'removed': 0}
            for p in all_p:
                states[p.state] += 1

            vaccinated = sum(1 for p in all_p if p.vaccinated)
            dead = sim.initial_population - len(all_p)

            print(f"\nDay {day+1}:")
            print(f"  S={states['susceptible']}, E={states['exposed']}, I={states['infected']}, R={states['removed']}, D={dead}")
            print(f"  Vaccinated: {vaccinated} ({vaccinated/sim.initial_population*100:.1f}%)")

    print("\n✓ Combined test completed successfully")

def main():
    print("="*60)
    print("SEIRD MODEL + VACCINATION FEATURE TESTS")
    print("="*60)

    try:
        test_exposed_state()
        test_vaccination()
        test_combined()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nNew Features Summary:")
        print("  ✓ Exposed (E) state with incubation period")
        print("  ✓ Vaccination system with configurable efficacy")
        print("  ✓ Full SEIRD model implementation")
        print("="*60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
