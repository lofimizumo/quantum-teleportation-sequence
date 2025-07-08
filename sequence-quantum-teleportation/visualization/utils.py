"""
Utility Functions for Quantum Teleportation Visualization
========================================================

This module provides utility functions for data processing, formatting,
and analysis of quantum teleportation simulation results.
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional


def format_quantum_state(state_name: str) -> str:
    """
    Format quantum state name for display.
    
    Args:
        state_name: Raw state name
        
    Returns:
        str: Formatted state name with proper notation
    """
    state_map = {
        "|0>": "|0⟩",
        "|1>": "|1⟩", 
        "|+>": "|+⟩",
        "|->": "|-⟩",
        "|0⟩": "|0⟩",
        "|1⟩": "|1⟩",
        "|+⟩": "|+⟩",
        "|-⟩": "|-⟩"
    }
    
    return state_map.get(state_name, state_name)


def calculate_simulation_metrics(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate various metrics from a simulation result.
    
    Args:
        result: Simulation result dictionary
        
    Returns:
        dict: Dictionary containing calculated metrics
    """
    metrics = {}
    
    # Basic metrics
    metrics['initial_state'] = result.get('initial_state', 'Unknown')
    metrics['bell_state_type'] = result.get('bell_state_type', 'Unknown')
    metrics['measurement_results'] = result.get('measurement_results', [])
    
    # Timing metrics
    metrics['runtime'] = result.get('runtime', 0)
    metrics['delay'] = result.get('delay', 0)
    metrics['total_time'] = metrics['runtime'] + metrics['delay']
    
    # Correction analysis
    bell_type = result.get('bell_state_type', 1)
    measurement = result.get('measurement_results', [0, 0])
    
    if bell_type == 1:  # |Φ⁺⟩
        correction_map = {
            (0, 0): [],
            (0, 1): ["X"],
            (1, 0): ["Z"],
            (1, 1): ["X", "Z"]
        }
    else:  # |Ψ⁻⟩
        correction_map = {
            (0, 0): ["X"],
            (0, 1): [],
            (1, 0): ["X", "Z"],
            (1, 1): ["Z"]
        }
    
    corrections = correction_map.get(tuple(measurement), [])
    metrics['corrections'] = corrections
    metrics['correction_count'] = len(corrections)
    
    # Success metrics (always successful in ideal case)
    metrics['success'] = True
    metrics['fidelity'] = 1.0  # Perfect fidelity in ideal case
    
    return metrics


def analyze_measurement_distribution(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze the distribution of Bell measurement results.
    
    Args:
        results: List of simulation results
        
    Returns:
        dict: Analysis of measurement distribution
    """
    if not results:
        return {}
    
    # Count measurement outcomes
    measurement_counts = {}
    total_measurements = len(results)
    
    for result in results:
        measurement = tuple(result.get('measurement_results', [0, 0]))
        measurement_counts[measurement] = measurement_counts.get(measurement, 0) + 1
    
    # Calculate percentages
    measurement_percentages = {}
    for measurement, count in measurement_counts.items():
        measurement_percentages[measurement] = (count / total_measurements) * 100
    
    # Expected distribution (25% each in ideal case)
    expected_percentage = 25.0
    
    # Calculate deviation from expected
    deviations = {}
    for measurement in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        actual = measurement_percentages.get(measurement, 0)
        deviations[measurement] = abs(actual - expected_percentage)
    
    return {
        'counts': measurement_counts,
        'percentages': measurement_percentages,
        'total_measurements': total_measurements,
        'expected_percentage': expected_percentage,
        'deviations': deviations,
        'max_deviation': max(deviations.values()) if deviations else 0
    }


def analyze_correction_patterns(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze patterns in quantum corrections applied.
    
    Args:
        results: List of simulation results
        
    Returns:
        dict: Analysis of correction patterns
    """
    if not results:
        return {}
    
    correction_counts = {"None": 0, "X": 0, "Z": 0, "X+Z": 0}
    bell_state_analysis = {1: {"None": 0, "X": 0, "Z": 0, "X+Z": 0},
                          3: {"None": 0, "X": 0, "Z": 0, "X+Z": 0}}
    
    for result in results:
        bell_type = result.get('bell_state_type', 1)
        measurement = result.get('measurement_results', [0, 0])
        
        # Determine corrections
        if bell_type == 1:  # |Φ⁺⟩
            if measurement == [0, 0]:
                correction = "None"
            elif measurement == [0, 1]:
                correction = "X"
            elif measurement == [1, 0]:
                correction = "Z"
            elif measurement == [1, 1]:
                correction = "X+Z"
            else:
                correction = "None"
        else:  # |Ψ⁻⟩
            if measurement == [0, 0]:
                correction = "X"
            elif measurement == [0, 1]:
                correction = "None"
            elif measurement == [1, 0]:
                correction = "X+Z"
            elif measurement == [1, 1]:
                correction = "Z"
            else:
                correction = "None"
        
        correction_counts[correction] += 1
        bell_state_analysis[bell_type][correction] += 1
    
    # Calculate percentages
    total_results = len(results)
    correction_percentages = {}
    for correction, count in correction_counts.items():
        correction_percentages[correction] = (count / total_results) * 100
    
    return {
        'counts': correction_counts,
        'percentages': correction_percentages,
        'by_bell_state': bell_state_analysis,
        'total_results': total_results
    }


def export_results_to_json(results: List[Dict[str, Any]]) -> str:
    """
    Export simulation results to JSON format.
    
    Args:
        results: List of simulation results
        
    Returns:
        str: JSON string of formatted results
    """
    if not results:
        return json.dumps({"error": "No results to export"}, indent=2)
    
    # Helper function to convert tuple keys to strings
    def convert_tuple_keys(obj):
        if isinstance(obj, dict):
            return {str(k) if isinstance(k, tuple) else k: convert_tuple_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_tuple_keys(item) for item in obj]
        else:
            return obj
    
    # Prepare export data
    measurement_dist = analyze_measurement_distribution(results)
    correction_patterns = analyze_correction_patterns(results)
    
    export_data = {
        "export_info": {
            "timestamp": datetime.now().isoformat(),
            "total_results": len(results),
            "version": "1.0.0"
        },
        "summary": {
            "measurement_distribution": convert_tuple_keys(measurement_dist),
            "correction_patterns": convert_tuple_keys(correction_patterns)
        },
        "results": []
    }
    
    # Process each result
    for i, result in enumerate(results):
        processed_result = {
            "run_id": i + 1,
            "timestamp": result.get('timestamp', datetime.now()).isoformat(),
            "configuration": {
                "initial_state": result.get('initial_state', 'Unknown'),
                "bell_state_type": result.get('bell_state_type', 1),
                "runtime": result.get('runtime', 0),
                "delay": result.get('delay', 0)
            },
            "results": {
                "measurement_results": result.get('measurement_results', []),
                "final_state": result.get('final_state', 'Unknown'),
                "corrections_applied": result.get('corrections_applied', [])
            },
            "metrics": calculate_simulation_metrics(result)
        }
        
        export_data["results"].append(processed_result)
    
    return json.dumps(export_data, indent=2, default=str)


def load_simulation_history(file_path: str) -> List[Dict[str, Any]]:
    """
    Load simulation history from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        list: List of simulation results
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if 'results' in data:
            return data['results']
        else:
            return data if isinstance(data, list) else []
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading simulation history: {e}")
        return []


def calculate_statistics_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics summary.
    
    Args:
        results: List of simulation results
        
    Returns:
        dict: Statistics summary
    """
    if not results:
        return {}
    
    # Basic statistics
    total_runs = len(results)
    
    # State distribution
    state_counts = {}
    for result in results:
        state = result.get('initial_state', 'Unknown')
        state_counts[state] = state_counts.get(state, 0) + 1
    
    # Bell state distribution
    bell_counts = {}
    for result in results:
        bell_type = result.get('bell_state_type', 1)
        bell_name = "|Φ⁺⟩" if bell_type == 1 else "|Ψ⁻⟩"
        bell_counts[bell_name] = bell_counts.get(bell_name, 0) + 1
    
    # Timing statistics
    runtimes = [result.get('runtime', 0) for result in results]
    delays = [result.get('delay', 0) for result in results]
    
    timing_stats = {
        'runtime': {
            'mean': np.mean(runtimes),
            'std': np.std(runtimes),
            'min': np.min(runtimes),
            'max': np.max(runtimes)
        },
        'delay': {
            'mean': np.mean(delays),
            'std': np.std(delays),
            'min': np.min(delays),
            'max': np.max(delays)
        }
    }
    
    return {
        'total_runs': total_runs,
        'state_distribution': state_counts,
        'bell_state_distribution': bell_counts,
        'timing_statistics': timing_stats,
        'measurement_analysis': analyze_measurement_distribution(results),
        'correction_analysis': analyze_correction_patterns(results)
    }


def validate_simulation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a simulation result and return validation info.
    
    Args:
        result: Simulation result to validate
        
    Returns:
        dict: Validation results
    """
    validation = {
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Check required fields
    required_fields = ['initial_state', 'bell_state_type', 'measurement_results']
    for field in required_fields:
        if field not in result:
            validation['valid'] = False
            validation['errors'].append(f"Missing required field: {field}")
    
    # Validate measurement results
    measurement = result.get('measurement_results', [])
    if not isinstance(measurement, list) or len(measurement) != 2:
        validation['valid'] = False
        validation['errors'].append("measurement_results must be a list of 2 elements")
    elif not all(m in [0, 1] for m in measurement):
        validation['valid'] = False
        validation['errors'].append("measurement_results must contain only 0 or 1")
    
    # Validate bell state type
    bell_type = result.get('bell_state_type')
    if bell_type not in [1, 3]:
        validation['valid'] = False
        validation['errors'].append("bell_state_type must be 1 or 3")
    
    # Validate initial state
    initial_state = result.get('initial_state')
    valid_states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
    if initial_state not in valid_states:
        validation['warnings'].append(f"Unusual initial state: {initial_state}")
    
    # Validate timing parameters
    runtime = result.get('runtime', 0)
    delay = result.get('delay', 0)
    if runtime < 0 or delay < 0:
        validation['valid'] = False
        validation['errors'].append("Runtime and delay must be non-negative")
    
    return validation


def format_measurement_result(measurement: List[int]) -> str:
    """
    Format measurement result for display.
    
    Args:
        measurement: List of measurement results
        
    Returns:
        str: Formatted measurement string
    """
    if not measurement or len(measurement) != 2:
        return "Invalid"
    
    return f"[{measurement[0]}, {measurement[1]}]"


def get_bell_state_name(bell_type: int) -> str:
    """
    Get the proper name for a Bell state type.
    
    Args:
        bell_type: Bell state type (1 or 3)
        
    Returns:
        str: Bell state name
    """
    bell_names = {
        1: "|Φ⁺⟩",
        3: "|Ψ⁻⟩"
    }
    
    return bell_names.get(bell_type, f"Unknown({bell_type})")


def calculate_theoretical_probabilities() -> Dict[str, float]:
    """
    Calculate theoretical probabilities for Bell measurements.
    
    Returns:
        dict: Theoretical probabilities for each measurement outcome
    """
    # In ideal conditions, each Bell measurement outcome should be equally likely
    return {
        "(0, 0)": 0.25,
        "(0, 1)": 0.25,
        "(1, 0)": 0.25,
        "(1, 1)": 0.25
    }


def compare_with_theory(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare simulation results with theoretical expectations.
    
    Args:
        results: List of simulation results
        
    Returns:
        dict: Comparison with theoretical expectations
    """
    if not results:
        return {}
    
    # Get actual distribution
    actual_analysis = analyze_measurement_distribution(results)
    theoretical_probs = calculate_theoretical_probabilities()
    
    # Calculate chi-square statistic
    chi_square = 0
    expected_count = len(results) * 0.25  # 25% for each outcome
    
    for measurement in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        actual_count = actual_analysis['counts'].get(measurement, 0)
        if expected_count > 0:
            chi_square += ((actual_count - expected_count) ** 2) / expected_count
    
    return {
        'actual_distribution': actual_analysis,
        'theoretical_probabilities': theoretical_probs,
        'chi_square_statistic': chi_square,
        'degrees_of_freedom': 3,  # 4 outcomes - 1
        'sample_size': len(results)
    } 