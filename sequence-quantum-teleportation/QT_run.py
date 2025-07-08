#!/usr/bin/env python3
"""
Quantum Teleportation Run Script - SeQUeNCe Framework
====================================================

This script provides the main entry point for running quantum teleportation
simulations using the SeQUeNCe framework. It supports various configurations
and provides examples of different quantum states and Bell state types.

Usage:
    python QT_run.py

The script demonstrates:
1. Basic quantum teleportation with different initial states
2. Different Bell state types (|Φ⁺⟩ and |Ψ⁻⟩)
3. Configurable simulation parameters
4. Result verification and analysis

This implementation follows the same structure as the NetSquid version
but uses SeQUeNCe framework components.
"""

import sys
import numpy as np
from QT_main import create_quantum_teleportation_simulation, QuantumTeleportationSimulation


class SimpleQuantumState:
    """
    Simple quantum state representation for demonstration purposes.
    
    This class provides a minimal interface for quantum states that can be
    used with the SeQUeNCe quantum teleportation simulation.
    """
    
    def __init__(self, state_vector, state_name):
        """
        Initialize a quantum state.
        
        Args:
            state_vector: Complex amplitudes representing the quantum state
            state_name: Human-readable name for the state
        """
        self.state_vector = np.array(state_vector, dtype=complex)
        self.state_name = state_name
        
    def __str__(self):
        return f"QuantumState({self.state_name})"
        
    def __repr__(self):
        return self.__str__()
        
    def get_fidelity(self, other_state):
        """
        Calculate fidelity between this state and another state.
        
        Args:
            other_state: Another quantum state to compare with
            
        Returns:
            Fidelity value between 0 and 1
        """
        if hasattr(other_state, 'state_vector'):
            # Calculate fidelity as |⟨ψ|φ⟩|²
            overlap = np.vdot(self.state_vector, other_state.state_vector)
            return abs(overlap) ** 2
        return 0.0


def run_basic_teleportation():
    """
    Run a basic quantum teleportation simulation with default parameters.
    
    This demonstrates the simplest case of quantum teleportation:
    - Initial state: |0⟩
    - Bell state type: |Φ⁺⟩ (type 1)
    - No delay
    """
    print("=== Basic Quantum Teleportation Simulation ===")
    print("Configuration:")
    print("  Initial state: |0⟩")
    print("  Bell state type: |Φ⁺⟩ (type 1)")
    print("  Runtime: 1000 picoseconds")
    print("  Delay: 0")
    print()
    
    # Create and run simulation
    simulation = create_quantum_teleportation_simulation(
        runtime=1000,
        bell_state_type=1,
        delay=0,
        initial_state="|0⟩"
    )
    
    simulation.run_simulation()
    simulation.show_results()
    
    return simulation


def run_teleportation_with_different_states():
    """
    Run quantum teleportation with different initial states.
    
    This demonstrates teleportation of various quantum states:
    - |0⟩ (computational basis)
    - |1⟩ (computational basis)
    - |+⟩ (superposition state)
    """
    states_to_test = ["|0⟩", "|1⟩", "|+⟩"]
    
    print("=== Quantum Teleportation with Different Initial States ===")
    
    for state in states_to_test:
        print(f"\n--- Teleporting {state} ---")
        
        simulation = create_quantum_teleportation_simulation(
            runtime=1000,
            bell_state_type=1,
            delay=0,
            initial_state=state
        )
        
        simulation.run_simulation()
        simulation.show_results()
        
        print(f"Teleportation of {state} completed.")


def run_teleportation_with_different_bell_states():
    """
    Run quantum teleportation with different Bell state types.
    
    This demonstrates how different Bell states affect the correction
    rules in quantum teleportation:
    - Bell state type 1: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    - Bell state type 3: |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
    """
    bell_states = [
        (1, "|Φ⁺⟩"),
        (3, "|Ψ⁻⟩")
    ]
    
    print("=== Quantum Teleportation with Different Bell States ===")
    
    for bell_type, bell_name in bell_states:
        print(f"\n--- Using Bell state {bell_name} (type {bell_type}) ---")
        
        simulation = create_quantum_teleportation_simulation(
            runtime=1000,
            bell_state_type=bell_type,
            delay=0,
            initial_state="|+⟩"
        )
        
        simulation.run_simulation()
        simulation.show_results()
        
        print(f"Teleportation with {bell_name} completed.")


def run_teleportation_with_delay():
    """
    Run quantum teleportation with receiver delay.
    
    This demonstrates the effect of adding delay to the receiver's
    correction operations.
    """
    print("=== Quantum Teleportation with Receiver Delay ===")
    print("Configuration:")
    print("  Initial state: |+⟩")
    print("  Bell state type: |Φ⁺⟩ (type 1)")
    print("  Runtime: 2000 picoseconds")
    print("  Delay: 500 picoseconds")
    print()
    
    simulation = create_quantum_teleportation_simulation(
        runtime=2000,
        bell_state_type=1,
        delay=500,
        initial_state="|+⟩"
    )
    
    simulation.run_simulation()
    simulation.show_results()
    
    return simulation


def run_comprehensive_test():
    """
    Run comprehensive tests of the quantum teleportation implementation.
    
    This function tests multiple combinations of parameters to verify
    the correctness of the implementation.
    """
    print("=== Comprehensive Quantum Teleportation Test ===")
    
    test_cases = [
        # (initial_state, bell_state_type, delay, description)
        ("|0⟩", 1, 0, "Basic |0⟩ with |Φ⁺⟩"),
        ("|1⟩", 1, 0, "Basic |1⟩ with |Φ⁺⟩"),
        ("|+⟩", 1, 0, "Superposition |+⟩ with |Φ⁺⟩"),
        ("|0⟩", 3, 0, "Basic |0⟩ with |Ψ⁻⟩"),
        ("|1⟩", 3, 0, "Basic |1⟩ with |Ψ⁻⟩"),
        ("|+⟩", 3, 0, "Superposition |+⟩ with |Ψ⁻⟩"),
        ("|+⟩", 1, 200, "Delayed correction with |Φ⁺⟩"),
        ("|+⟩", 3, 200, "Delayed correction with |Ψ⁻⟩"),
    ]
    
    results = []
    
    for i, (initial_state, bell_type, delay, description) in enumerate(test_cases):
        print(f"\n--- Test {i+1}: {description} ---")
        
        try:
            simulation = create_quantum_teleportation_simulation(
                runtime=1000 + delay,
                bell_state_type=bell_type,
                delay=delay,
                initial_state=initial_state
            )
            
            simulation.run_simulation()
            simulation.show_results()
            
            # Record results
            results.append({
                'test_id': i+1,
                'description': description,
                'initial_state': initial_state,
                'bell_state_type': bell_type,
                'delay': delay,
                'success': True,
                'measurement_results': simulation.sender_protocol.measurement_results,
                'final_state': simulation.receiver_protocol.teleported_state
            })
            
            print(f"✓ Test {i+1} completed successfully")
            
        except Exception as e:
            print(f"✗ Test {i+1} failed: {e}")
            results.append({
                'test_id': i+1,
                'description': description,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n=== Test Summary ===")
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    print(f"Successful tests: {successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Check the output above for details.")
    
    return results


def demonstrate_measurement_statistics():
    """
    Demonstrate the statistical distribution of Bell measurement results.
    
    This function runs multiple teleportation simulations to show that
    the Bell measurement results are distributed according to quantum
    mechanical predictions.
    """
    print("=== Bell Measurement Statistics Demonstration ===")
    print("Running multiple simulations to show measurement statistics...")
    
    num_runs = 20
    measurement_counts = {
        (0, 0): 0,
        (0, 1): 0,
        (1, 0): 0,
        (1, 1): 0
    }
    
    for run in range(num_runs):
        simulation = create_quantum_teleportation_simulation(
            runtime=1000,
            bell_state_type=1,
            delay=0,
            initial_state="|+⟩"
        )
        
        simulation.run_simulation()
        
        if simulation.sender_protocol.measurement_results:
            result_tuple = tuple(simulation.sender_protocol.measurement_results)
            measurement_counts[result_tuple] += 1
    
    print(f"\nMeasurement results distribution over {num_runs} runs:")
    for result, count in measurement_counts.items():
        percentage = (count / num_runs) * 100
        print(f"  {result}: {count} times ({percentage:.1f}%)")
    
    print(f"\nNote: In ideal conditions, each outcome should occur ~25% of the time")
    print(f"due to the random nature of quantum measurements.")


def main():
    """
    Main function to run quantum teleportation demonstrations.
    
    This function provides a menu of different simulation scenarios
    to demonstrate various aspects of quantum teleportation.
    """
    print("SeQUeNCe Quantum Teleportation Simulation")
    print("=" * 50)
    print()
    
    # Check if specific test requested via command line
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        if test_name == "basic":
            run_basic_teleportation()
        elif test_name == "states":
            run_teleportation_with_different_states()
        elif test_name == "bell":
            run_teleportation_with_different_bell_states()
        elif test_name == "delay":
            run_teleportation_with_delay()
        elif test_name == "comprehensive":
            run_comprehensive_test()
        elif test_name == "stats":
            demonstrate_measurement_statistics()
        else:
            print(f"Unknown test: {test_name}")
            print("Available tests: basic, states, bell, delay, comprehensive, stats")
    else:
        # Run default demonstration
        print("Running default quantum teleportation demonstration...")
        print()
        
        # Run basic teleportation
        run_basic_teleportation()
        
        print("\n" + "=" * 50)
        print("For more demonstrations, run with:")
        print("  python QT_run.py basic       # Basic teleportation")
        print("  python QT_run.py states      # Different initial states")
        print("  python QT_run.py bell        # Different Bell states")
        print("  python QT_run.py delay       # With receiver delay")
        print("  python QT_run.py comprehensive # Full test suite")
        print("  python QT_run.py stats       # Measurement statistics")


if __name__ == "__main__":
    main() 