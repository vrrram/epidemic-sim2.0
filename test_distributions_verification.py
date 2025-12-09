"""
TICKET-001: Statistical Verification of Three Distribution Functions
IHK Project Requirement: Demonstrate correct implementation of distributions

This test verifies that all three distribution functions are:
1. Correctly implemented
2. Produce statistically valid results
3. Meet the mathematical specifications
"""

import numpy as np
import matplotlib.pyplot as plt
from epidemic_sim.model.particle import Particle


def test_uniform_distribution():
    """
    Test UNIFORM DISTRIBUTION (Gleichverteilung)
    Used for: Particle velocities (vx, vy)

    Mathematical Specification:
    - Range: [-0.2, 0.2]
    - Mean: ~0.0
    - All values equally likely
    """
    print("=" * 60)
    print("TEST 1: UNIFORM DISTRIBUTION (Particle Velocities)")
    print("=" * 60)

    # Create 10000 particles and collect velocity data
    particles = [Particle(0, 0) for _ in range(10000)]
    velocities_x = [p.vx for p in particles]
    velocities_y = [p.vy for p in particles]

    # Statistical tests
    mean_vx = np.mean(velocities_x)
    mean_vy = np.mean(velocities_y)
    min_vx = min(velocities_x)
    max_vx = max(velocities_x)
    min_vy = min(velocities_y)
    max_vy = max(velocities_y)

    print(f"Sample Size: 10,000 particles")
    print(f"\nVelocity X (vx):")
    print(f"  Mean:  {mean_vx:7.4f} (Expected: ~0.0000)")
    print(f"  Range: [{min_vx:6.3f}, {max_vx:6.3f}] (Expected: [-0.2, 0.2])")

    print(f"\nVelocity Y (vy):")
    print(f"  Mean:  {mean_vy:7.4f} (Expected: ~0.0000)")
    print(f"  Range: [{min_vy:6.3f}, {max_vy:6.3f}] (Expected: [-0.2, 0.2])")

    # Validation
    assert abs(mean_vx) < 0.02, "vx mean should be close to 0"
    assert abs(mean_vy) < 0.02, "vy mean should be close to 0"
    assert min_vx >= -0.2 and max_vx <= 0.2, "vx should be in range [-0.2, 0.2]"
    assert min_vy >= -0.2 and max_vy <= 0.2, "vy should be in range [-0.2, 0.2]"

    print("\n✅ UNIFORM DISTRIBUTION: PASSED")
    return velocities_x, velocities_y


def test_normal_distribution():
    """
    Test NORMAL DISTRIBUTION (Normalverteilung)
    Used for: Infection susceptibility variation

    Mathematical Specification:
    - Mean (μ): 1.0
    - Standard Deviation (σ): 0.2
    - ~68% of values should be within [0.8, 1.2]
    - ~95% of values should be within [0.6, 1.4]
    """
    print("\n" + "=" * 60)
    print("TEST 2: NORMAL DISTRIBUTION (Infection Susceptibility)")
    print("=" * 60)

    # Create 10000 particles and collect susceptibility data
    particles = [Particle(0, 0) for _ in range(10000)]
    susceptibilities = [p.infection_susceptibility for p in particles]

    # Statistical tests
    mean = np.mean(susceptibilities)
    std_dev = np.std(susceptibilities)
    min_val = min(susceptibilities)
    max_val = max(susceptibilities)

    # Count percentages within standard deviation ranges
    within_1_sigma = sum(1 for s in susceptibilities if 0.8 <= s <= 1.2)
    within_2_sigma = sum(1 for s in susceptibilities if 0.6 <= s <= 1.4)
    pct_1_sigma = (within_1_sigma / len(susceptibilities)) * 100
    pct_2_sigma = (within_2_sigma / len(susceptibilities)) * 100

    print(f"Sample Size: 10,000 particles")
    print(f"\nMean (μ):    {mean:6.3f} (Expected: ~1.000)")
    print(f"Std Dev (σ): {std_dev:6.3f} (Expected: ~0.200)")
    print(f"Range:       [{min_val:5.3f}, {max_val:5.3f}]")
    print(f"\nDistribution Check:")
    print(f"  Within 1σ [0.8-1.2]: {pct_1_sigma:5.1f}% (Expected: ~68%)")
    print(f"  Within 2σ [0.6-1.4]: {pct_2_sigma:5.1f}% (Expected: ~95%)")

    # Validation
    assert 0.95 < mean < 1.05, f"Mean should be close to 1.0, got {mean}"
    assert 0.18 < std_dev < 0.22, f"Std dev should be close to 0.2, got {std_dev}"
    assert 60 < pct_1_sigma < 75, f"~68% should be within 1σ, got {pct_1_sigma}%"
    assert 92 < pct_2_sigma < 98, f"~95% should be within 2σ, got {pct_2_sigma}%"

    print("\n✅ NORMAL DISTRIBUTION: PASSED")
    return susceptibilities


def test_exponential_distribution():
    """
    Test EXPONENTIAL DISTRIBUTION (Exponentialverteilung)
    Used for: Recovery time variation

    Mathematical Specification:
    - Scale (λ): 1.0
    - Mean: 1.0 (since mean = scale for exponential)
    - Has "memoryless property" - ideal for time-until-event
    - Range clamped to [0.5, 3.0] for realistic recovery times
    """
    print("\n" + "=" * 60)
    print("TEST 3: EXPONENTIAL DISTRIBUTION (Recovery Time Modifier)")
    print("=" * 60)

    # Create 10000 particles and collect recovery time data
    particles = [Particle(0, 0) for _ in range(10000)]
    recovery_modifiers = [p.recovery_time_modifier for p in particles]

    # Statistical tests
    mean = np.mean(recovery_modifiers)
    std_dev = np.std(recovery_modifiers)
    min_val = min(recovery_modifiers)
    max_val = max(recovery_modifiers)
    median = np.median(recovery_modifiers)

    # Count percentage in different time ranges
    fast_recovery = sum(1 for r in recovery_modifiers if r < 0.8)
    normal_recovery = sum(1 for r in recovery_modifiers if 0.8 <= r <= 1.2)
    slow_recovery = sum(1 for r in recovery_modifiers if r > 1.2)

    pct_fast = (fast_recovery / len(recovery_modifiers)) * 100
    pct_normal = (normal_recovery / len(recovery_modifiers)) * 100
    pct_slow = (slow_recovery / len(recovery_modifiers)) * 100

    print(f"Sample Size: 10,000 particles")
    print(f"\nMean:   {mean:6.3f} (Expected: ~1.000)")
    print(f"Median: {median:6.3f} (Expected: <1.0 for exponential)")
    print(f"Std Dev:{std_dev:6.3f}")
    print(f"Range:  [{min_val:5.3f}, {max_val:5.3f}] (Clamped: [0.5, 3.0])")
    print(f"\nRecovery Speed Distribution:")
    print(f"  Fast (<0.8):       {pct_fast:5.1f}%")
    print(f"  Normal (0.8-1.2):  {pct_normal:5.1f}%")
    print(f"  Slow (>1.2):       {pct_slow:5.1f}%")

    # Validation
    assert 0.9 < mean < 1.1, f"Mean should be close to 1.0, got {mean}"
    assert median < mean, "Median should be less than mean (right-skewed exponential)"
    assert min_val >= 0.5, "Minimum should be clamped to 0.5"
    assert max_val <= 3.0, "Maximum should be clamped to 3.0"

    print("\n✅ EXPONENTIAL DISTRIBUTION: PASSED")
    return recovery_modifiers


def plot_distributions(velocities_x, susceptibilities, recovery_modifiers):
    """
    Create visualization of all three distributions for documentation
    """
    print("\n" + "=" * 60)
    print("Generating Distribution Plots...")
    print("=" * 60)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('IHK Project: Three Statistical Distributions', fontsize=14, fontweight='bold')

    # Plot 1: Uniform Distribution (Velocities)
    axes[0].hist(velocities_x, bins=50, color='cyan', alpha=0.7, edgecolor='black')
    axes[0].axvline(0, color='red', linestyle='--', linewidth=2, label='Mean (0.0)')
    axes[0].set_title('1. UNIFORM (Gleichverteilung)\nParticle Velocities', fontweight='bold')
    axes[0].set_xlabel('Velocity (vx)')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Plot 2: Normal Distribution (Susceptibility)
    axes[1].hist(susceptibilities, bins=50, color='lightgreen', alpha=0.7, edgecolor='black')
    axes[1].axvline(1.0, color='red', linestyle='--', linewidth=2, label='Mean (1.0)')
    axes[1].axvline(0.8, color='orange', linestyle=':', linewidth=1.5, label='±1σ')
    axes[1].axvline(1.2, color='orange', linestyle=':', linewidth=1.5)
    axes[1].set_title('2. NORMAL (Normalverteilung)\nInfection Susceptibility', fontweight='bold')
    axes[1].set_xlabel('Susceptibility Factor')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # Plot 3: Exponential Distribution (Recovery Time)
    axes[2].hist(recovery_modifiers, bins=50, color='lightcoral', alpha=0.7, edgecolor='black')
    axes[2].axvline(1.0, color='red', linestyle='--', linewidth=2, label='Mean (1.0)')
    axes[2].set_title('3. EXPONENTIAL (Exponentialverteilung)\nRecovery Time Modifier', fontweight='bold')
    axes[2].set_xlabel('Time Modifier')
    axes[2].set_ylabel('Frequency')
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('distribution_verification.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Plot saved: distribution_verification.png")
    print("   (Include this in your IHK documentation!)")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("EPIDEMIC SIMULATOR - DISTRIBUTION VERIFICATION")
    print("IHK Project Requirement: THREE STATISTICAL DISTRIBUTIONS")
    print("=" * 60)

    try:
        # Run all three distribution tests
        velocities_x, velocities_y = test_uniform_distribution()
        susceptibilities = test_normal_distribution()
        recovery_modifiers = test_exponential_distribution()

        # Generate plots for documentation
        plot_distributions(velocities_x, susceptibilities, recovery_modifiers)

        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY: ALL THREE DISTRIBUTIONS VERIFIED ✅")
        print("=" * 60)
        print("\nDistributions implemented and statistically correct:")
        print("  1. ✅ UNIFORM     - Particle velocities (no bias)")
        print("  2. ✅ NORMAL      - Infection susceptibility (biological variation)")
        print("  3. ✅ EXPONENTIAL - Recovery time (time-until-event)")
        print("\nIHK Requirement: FULFILLED ✅")
        print("\nNext Steps:")
        print("  - Include distribution_verification.png in documentation")
        print("  - Reference this test in Projektdokumentation")
        print("  - Explain mathematical justification in presentation")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
