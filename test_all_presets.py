#!/usr/bin/env python3
"""
Test script to verify all 15 presets work correctly with new SEIRD features
"""
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.config.parameters import params
from epidemic_sim.config.presets import PRESETS

def test_preset(preset_name, preset_config):
    """Test a single preset"""
    print(f"\nTesting: {preset_name}")

    # Apply preset
    for key, value in preset_config.items():
        if hasattr(params, key):
            setattr(params, key, value)

    # Set to simple mode with fewer particles for faster testing
    params.num_particles = 50

    try:
        # Create and initialize simulation
        sim = EpidemicSimulation('simple')
        sim.initialize()

        # Run for 10 days
        for day in range(10):
            for _ in range(params.time_steps_per_day):
                sim.step()

        # Check that simulation didn't crash and has valid states
        all_p = sim.get_all_particles()
        if len(all_p) == 0:
            print(f"  ✗ FAILED: No particles remaining")
            return False

        states = {'susceptible': 0, 'exposed': 0, 'infected': 0, 'removed': 0}
        for p in all_p:
            if p.state in states:
                states[p.state] += 1
            else:
                print(f"  ✗ FAILED: Invalid state '{p.state}'")
                return False

        print(f"  ✓ PASSED (S={states['susceptible']}, E={states['exposed']}, I={states['infected']}, R={states['removed']})")
        return True

    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*60)
    print("TESTING ALL PRESETS WITH NEW SEIRD FEATURES")
    print("="*60)

    results = []
    for preset_name, preset_config in PRESETS.items():
        success = test_preset(preset_name, preset_config)
        results.append((preset_name, success))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for preset_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {preset_name}")

    print(f"\n{passed}/{total} presets passed")

    if passed == total:
        print("\n✓ ALL PRESETS WORK CORRECTLY!")
        return 0
    else:
        print(f"\n✗ {total - passed} presets failed")
        return 1

if __name__ == '__main__':
    exit(main())
