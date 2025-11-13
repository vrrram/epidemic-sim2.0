#!/usr/bin/env python3
"""
Performance profiling script for epidemic simulation

Tests simulation performance at different particle counts and measures:
- Average step time
- FPS (frames per second)
- Memory usage
"""
import time
import sys
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.config.parameters import params

def profile_simulation(mode, num_particles, num_steps=100):
    """Profile simulation performance"""
    # Configure parameters
    original_num = params.num_particles
    params.num_particles = num_particles

    # Create and initialize simulation
    print(f"\n{'='*60}")
    print(f"PROFILING: {mode.upper()} mode with {num_particles} particles")
    print(f"{'='*60}")

    sim = EpidemicSimulation(mode)
    sim.initialize()

    # Warm-up (don't count first few steps)
    for _ in range(10):
        sim.step()

    # Measure performance
    start_time = time.time()
    for _ in range(num_steps):
        sim.step()
    end_time = time.time()

    elapsed = end_time - start_time
    avg_step_time = elapsed / num_steps
    fps = 1.0 / avg_step_time if avg_step_time > 0 else 0

    print(f"\nResults:")
    print(f"  Total time: {elapsed:.2f} seconds")
    print(f"  Steps: {num_steps}")
    print(f"  Avg step time: {avg_step_time*1000:.2f} ms")
    print(f"  FPS: {fps:.1f}")

    if fps >= 60:
        status = "✓ EXCELLENT"
    elif fps >= 30:
        status = "✓ GOOD"
    elif fps >= 15:
        status = "⚠ ACCEPTABLE"
    else:
        status = "✗ POOR"

    print(f"  Status: {status}")

    # Restore original parameter
    params.num_particles = original_num

    return fps, avg_step_time

def main():
    print("="*60)
    print("EPIDEMIC SIMULATION PERFORMANCE PROFILER")
    print("="*60)

    # Test configurations
    test_configs = [
        ('simple', 200),
        ('simple', 500),
        ('simple', 1000),
    ]

    results = []
    for mode, num_particles in test_configs:
        fps, step_time = profile_simulation(mode, num_particles, num_steps=100)
        results.append((mode, num_particles, fps, step_time))

    # Summary
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"{'Mode':<12} {'Particles':<12} {'FPS':<12} {'Step Time':<12} {'Status':<12}")
    print(f"{'-'*60}")

    for mode, num_particles, fps, step_time in results:
        if fps >= 60:
            status = "✓ EXCELLENT"
        elif fps >= 30:
            status = "✓ GOOD"
        elif fps >= 15:
            status = "⚠ ACCEPTABLE"
        else:
            status = "✗ POOR"

        print(f"{mode:<12} {num_particles:<12} {fps:>6.1f} FPS   {step_time*1000:>6.2f} ms    {status}")

    print(f"{'='*60}")
    print("\nTarget Performance:")
    print("  - 60 FPS at 500 particles (EXCELLENT)")
    print("  - 30 FPS at 1000 particles (GOOD)")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
