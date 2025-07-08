"""
Plotting Functions for Quantum Teleportation Visualization
=========================================================

This module provides Plotly-based visualization functions for displaying
quantum teleportation simulation results, including charts, graphs, and
interactive visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime


def create_bell_measurement_chart(measurement_results):
    """
    Create a visualization of Bell measurement results.
    
    Args:
        measurement_results: List of measurement results [bit1, bit2]
        
    Returns:
        plotly.graph_objects.Figure: Bell measurement visualization
    """
    if not measurement_results or len(measurement_results) != 2:
        # Default empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No measurement results available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title="Bell Measurement Results",
            xaxis_title="Qubit",
            yaxis_title="Measurement Outcome"
        )
        return fig
    
    # Create measurement results visualization
    qubits = ["Unknown Qubit", "EPR Qubit"]
    results = measurement_results
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=qubits,
            y=results,
            marker_color=['#FF6B6B', '#4ECDC4'],
            text=results,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Bell Measurement Results",
        xaxis_title="Measured Qubits",
        yaxis_title="Measurement Outcome (0 or 1)",
        yaxis=dict(range=[0, 1.2]),
        showlegend=False,
        height=400
    )
    
    # Add annotation with Bell state
    bell_state_map = {
        (0, 0): "|Φ⁺⟩",
        (0, 1): "|Ψ⁺⟩", 
        (1, 0): "|Φ⁻⟩",
        (1, 1): "|Ψ⁻⟩"
    }
    
    bell_state = bell_state_map.get(tuple(results), "Unknown")
    fig.add_annotation(
        text=f"Bell State Detected: {bell_state}",
        xref="paper", yref="paper",
        x=0.5, y=0.9,
        showarrow=False,
        font=dict(size=14, color="blue"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="blue",
        borderwidth=1
    )
    
    return fig


def create_correction_rules_chart(bell_state_type, measurement_results):
    """
    Create a visualization of correction rules applied.
    
    Args:
        bell_state_type: Type of Bell state (1 or 3)
        measurement_results: List of measurement results [bit1, bit2]
        
    Returns:
        plotly.graph_objects.Figure: Correction rules visualization
    """
    # Determine corrections based on Bell state type and measurement
    if bell_state_type == 1:  # |Φ⁺⟩
        correction_map = {
            (0, 0): [],
            (0, 1): ["X"],
            (1, 0): ["Z"],
            (1, 1): ["Z", "X"]
        }
        title_suffix = "|Φ⁺⟩"
    else:  # |Ψ⁻⟩
        correction_map = {
            (0, 0): ["X"],
            (0, 1): [],
            (1, 0): ["Z", "X"],
            (1, 1): ["Z"]
        }
        title_suffix = "|Ψ⁻⟩"
    
    corrections = correction_map.get(tuple(measurement_results), [])
    
    # Create visualization
    fig = go.Figure()
    
    # Show all possible corrections and highlight applied ones
    all_corrections = ["I", "X", "Z", "XZ"]
    correction_labels = ["Identity", "X Gate", "Z Gate", "X & Z Gates"]
    
    applied_corrections = []
    for corr in all_corrections:
        if corr == "I":
            applied_corrections.append(1 if not corrections else 0)
        elif corr == "X":
            applied_corrections.append(1 if "X" in corrections and "Z" not in corrections else 0)
        elif corr == "Z":
            applied_corrections.append(1 if "Z" in corrections and "X" not in corrections else 0)
        elif corr == "XZ":
            applied_corrections.append(1 if "X" in corrections and "Z" in corrections else 0)
    
    colors = ['#FF6B6B' if applied else '#E8E8E8' for applied in applied_corrections]
    
    fig.add_trace(go.Bar(
        x=correction_labels,
        y=applied_corrections,
        marker_color=colors,
        text=["Applied" if applied else "Not Applied" for applied in applied_corrections],
        textposition='auto'
    ))
    
    fig.update_layout(
        title=f"Correction Rules Applied - Bell State {title_suffix}",
        xaxis_title="Correction Gates",
        yaxis_title="Applied",
        yaxis=dict(range=[0, 1.2], tickmode='array', tickvals=[0, 1], ticktext=['No', 'Yes']),
        showlegend=False,
        height=400
    )
    
    # Add measurement info
    fig.add_annotation(
        text=f"Measurement: {measurement_results}",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        font=dict(size=12),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="gray",
        borderwidth=1
    )
    
    return fig


def create_quantum_state_sphere(state_name):
    """
    Create a Bloch sphere visualization of a quantum state.
    
    Args:
        state_name: Name of the quantum state
        
    Returns:
        plotly.graph_objects.Figure: Bloch sphere visualization
    """
    # State vectors on Bloch sphere
    state_coords = {
        "|0⟩": (0, 0, 1),      # North pole
        "|1⟩": (0, 0, -1),     # South pole
        "|+⟩": (1, 0, 0),      # +X axis
        "|-⟩": (-1, 0, 0),     # -X axis
        "|+i⟩": (0, 1, 0),     # +Y axis
        "|-i⟩": (0, -1, 0)     # -Y axis
    }
    
    # Create Bloch sphere
    fig = go.Figure()
    
    # Add sphere surface
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        opacity=0.3,
        colorscale='Blues',
        showscale=False,
        hoverinfo='skip'
    ))
    
    # Add coordinate axes
    axes_data = [
        # X axis
        go.Scatter3d(x=[-1.2, 1.2], y=[0, 0], z=[0, 0], mode='lines', 
                    line=dict(color='red', width=4), name='X', showlegend=False),
        # Y axis  
        go.Scatter3d(x=[0, 0], y=[-1.2, 1.2], z=[0, 0], mode='lines',
                    line=dict(color='green', width=4), name='Y', showlegend=False),
        # Z axis
        go.Scatter3d(x=[0, 0], y=[0, 0], z=[-1.2, 1.2], mode='lines',
                    line=dict(color='blue', width=4), name='Z', showlegend=False)
    ]
    
    for trace in axes_data:
        fig.add_trace(trace)
    
    # Add state vector
    if state_name in state_coords:
        x, y, z = state_coords[state_name]
        
        # State vector arrow
        fig.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            mode='lines+markers',
            line=dict(color='red', width=6),
            marker=dict(size=[0, 8], color='red'),
            name=f'State {state_name}',
            showlegend=True
        ))
        
        # State point
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers',
            marker=dict(size=10, color='red'),
            name=f'{state_name}',
            showlegend=False
        ))
    
    # Add axis labels
    fig.add_trace(go.Scatter3d(
        x=[1.3], y=[0], z=[0], mode='text',
        text=['X'], textfont=dict(size=14, color='red'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[1.3], z=[0], mode='text', 
        text=['Y'], textfont=dict(size=14, color='green'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[1.3], mode='text',
        text=['Z'], textfont=dict(size=14, color='blue'),
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Bloch Sphere - Quantum State {state_name}",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y", 
            zaxis_title="Z",
            aspectmode='cube',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=500,
        showlegend=True
    )
    
    return fig


def create_simulation_timeline(result):
    """
    Create a timeline visualization of the simulation process.
    
    Args:
        result: Simulation result dictionary
        
    Returns:
        plotly.graph_objects.Figure: Timeline visualization
    """
    # Create timeline events
    events = [
        {"time": 0, "event": "Start Simulation", "description": "Initialize quantum states"},
        {"time": 10, "event": "Bell Measurement", "description": "Perform Bell measurement on sender side"},
        {"time": 20, "event": "Classical Communication", "description": "Send measurement results to receiver"},
        {"time": 30 + result.get('delay', 0), "event": "Apply Corrections", "description": "Receiver applies quantum corrections"},
        {"time": 40 + result.get('delay', 0), "event": "Teleportation Complete", "description": "Quantum state successfully teleported"}
    ]
    
    fig = go.Figure()
    
    # Add timeline
    times = [e["time"] for e in events]
    events_text = [e["event"] for e in events]
    
    fig.add_trace(go.Scatter(
        x=times,
        y=[1] * len(times),
        mode='markers+lines',
        marker=dict(size=12, color='blue'),
        line=dict(width=3, color='blue'),
        text=events_text,
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Time: %{x} ps<extra></extra>',
        showlegend=False
    ))
    
    # Add event descriptions
    for i, event in enumerate(events):
        fig.add_annotation(
            x=event["time"],
            y=0.8,
            text=event["description"],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="gray",
            ax=0,
            ay=-30,
            font=dict(size=10)
        )
    
    fig.update_layout(
        title="Quantum Teleportation Timeline",
        xaxis_title="Time (picoseconds)",
        yaxis=dict(range=[0.5, 1.5], showticklabels=False),
        height=300,
        showlegend=False
    )
    
    return fig


def create_statistics_dashboard(results):
    """
    Create a comprehensive statistics dashboard.
    
    Args:
        results: List of simulation results
        
    Returns:
        plotly.graph_objects.Figure: Statistics dashboard
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Measurement Distribution', 'Bell State Usage', 
                       'Initial State Distribution', 'Runtime Analysis'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Measurement distribution
    measurement_counts = {}
    for result in results:
        key = tuple(result['measurement_results'])
        measurement_counts[key] = measurement_counts.get(key, 0) + 1
    
    measurements = list(measurement_counts.keys())
    counts = list(measurement_counts.values())
    
    fig.add_trace(
        go.Bar(x=[str(m) for m in measurements], y=counts, name="Measurements"),
        row=1, col=1
    )
    
    # Bell state usage
    bell_counts = {}
    for result in results:
        bell_type = result['bell_state_type']
        bell_name = "|Φ⁺⟩" if bell_type == 1 else "|Ψ⁻⟩"
        bell_counts[bell_name] = bell_counts.get(bell_name, 0) + 1
    
    fig.add_trace(
        go.Pie(labels=list(bell_counts.keys()), values=list(bell_counts.values()), name="Bell States"),
        row=1, col=2
    )
    
    # Initial state distribution
    state_counts = {}
    for result in results:
        state = result['initial_state']
        state_counts[state] = state_counts.get(state, 0) + 1
    
    fig.add_trace(
        go.Bar(x=list(state_counts.keys()), y=list(state_counts.values()), name="Initial States"),
        row=2, col=1
    )
    
    # Runtime analysis
    runtimes = [result['runtime'] for result in results]
    delays = [result['delay'] for result in results]
    
    fig.add_trace(
        go.Scatter(x=runtimes, y=delays, mode='markers', name="Runtime vs Delay"),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Simulation Statistics Dashboard",
        height=600,
        showlegend=False
    )
    
    return fig


def create_fidelity_comparison_chart(results):
    """
    Create a chart comparing fidelity across different configurations.
    
    Args:
        results: List of simulation results
        
    Returns:
        plotly.graph_objects.Figure: Fidelity comparison chart
    """
    # For now, assume perfect fidelity (theoretical limit)
    # In a real implementation, this would calculate actual fidelity
    
    fig = go.Figure()
    
    # Group results by configuration
    config_groups = {}
    for i, result in enumerate(results):
        config_key = f"{result['initial_state']}, {result['bell_state_type']}"
        if config_key not in config_groups:
            config_groups[config_key] = []
        config_groups[config_key].append(1.0)  # Perfect fidelity
    
    # Create box plot for each configuration
    for config, fidelities in config_groups.items():
        fig.add_trace(go.Box(
            y=fidelities,
            name=config,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8
        ))
    
    fig.update_layout(
        title="Teleportation Fidelity by Configuration",
        xaxis_title="Configuration (Initial State, Bell State Type)",
        yaxis_title="Fidelity",
        yaxis=dict(range=[0.95, 1.05]),
        height=400
    )
    
    return fig


def create_correction_frequency_chart(results):
    """
    Create a chart showing frequency of different corrections.
    
    Args:
        results: List of simulation results
        
    Returns:
        plotly.graph_objects.Figure: Correction frequency chart
    """
    correction_counts = {"None": 0, "X": 0, "Z": 0, "X+Z": 0}
    
    for result in results:
        bell_type = result['bell_state_type']
        measurement = result['measurement_results']
        
        # Determine corrections
        if bell_type == 1:  # |Φ⁺⟩
            if measurement == [0, 0]:
                correction_counts["None"] += 1
            elif measurement == [0, 1]:
                correction_counts["X"] += 1
            elif measurement == [1, 0]:
                correction_counts["Z"] += 1
            elif measurement == [1, 1]:
                correction_counts["X+Z"] += 1
        else:  # |Ψ⁻⟩
            if measurement == [0, 0]:
                correction_counts["X"] += 1
            elif measurement == [0, 1]:
                correction_counts["None"] += 1
            elif measurement == [1, 0]:
                correction_counts["X+Z"] += 1
            elif measurement == [1, 1]:
                correction_counts["Z"] += 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(correction_counts.keys()),
            y=list(correction_counts.values()),
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        )
    ])
    
    fig.update_layout(
        title="Frequency of Quantum Corrections Applied",
        xaxis_title="Correction Type",
        yaxis_title="Frequency",
        height=400
    )
    
    return fig 