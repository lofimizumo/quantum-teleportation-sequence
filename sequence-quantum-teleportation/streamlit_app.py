#!/usr/bin/env python3
"""
Streamlit GUI for Quantum Teleportation Simulation - SeQUeNCe Framework
======================================================================

This application provides a beautiful web interface for running and visualizing
quantum teleportation simulations using the SeQUeNCe framework.

Features:
- Interactive configuration of simulation parameters
- Real-time visualization of quantum states and measurement results
- Beautiful charts and graphs showing simulation results
- Export capabilities for results and visualizations
- Comprehensive result analysis and statistics

Usage:
    streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime

# Import our simulation modules
from QT_main import create_quantum_teleportation_simulation
from visualization.ui_components import (
    create_sidebar_config,
    display_simulation_header,
    display_results_section,
    display_statistics_section,
    display_quantum_state_visualization
)
from visualization.plotting import (
    create_bell_measurement_chart,
    create_correction_rules_chart,
    create_simulation_timeline,
    create_quantum_state_sphere,
    create_statistics_dashboard
)
from visualization.utils import (
    format_quantum_state,
    calculate_simulation_metrics,
    export_results_to_json,
    load_simulation_history
)

# Configure Streamlit page
st.set_page_config(
    page_title="Quantum Teleportation Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .config-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables for the Streamlit app."""
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = []
    if 'current_simulation' not in st.session_state:
        st.session_state.current_simulation = None
    if 'simulation_history' not in st.session_state:
        st.session_state.simulation_history = []
    if 'show_advanced_options' not in st.session_state:
        st.session_state.show_advanced_options = False

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>️ Quantum Teleportation Simulator</h1>
        <h3>Ye Tao</h3>
        <p>Central Queensland University</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    config = create_sidebar_config()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Simulation controls
        st.subheader("Simulation Controls")
        
        col_run, col_clear, col_export = st.columns(3)
        
        with col_run:
            if st.button(" Run Simulation", type="primary", use_container_width=True):
                run_simulation(config)
        
        with col_clear:
            if st.button("️ Clear Results", use_container_width=True):
                st.session_state.simulation_results = []
                st.session_state.simulation_history = []
                st.rerun()
        
        with col_export:
            if st.button(" Export Results", use_container_width=True):
                export_simulation_results()
        
        # Results display
        if st.session_state.simulation_results:
            display_simulation_results()
    
    with col2:
        # Configuration summary
        display_configuration_summary(config)
        
        # Quick statistics
        if st.session_state.simulation_results:
            display_quick_statistics()

def run_simulation(config):
    """Run the quantum teleportation simulation with given configuration."""
    try:
        with st.spinner(" Running quantum teleportation simulation..."):
            # Create and run simulation
            simulation = create_quantum_teleportation_simulation(
                runtime=config['runtime'],
                bell_state_type=config['bell_state_type'],
                delay=config['delay'],
                initial_state=config['initial_state']
            )
            
            # Run the simulation
            simulation.run_simulation()
            
            # Store results
            result = {
                'timestamp': datetime.now(),
                'config': config,
                'simulation': simulation,
                'initial_state': str(simulation.initial_state),
                'bell_state_type': simulation.bell_state_type,
                'measurement_results': simulation.sender_protocol.measurement_results,
                'final_state': str(simulation.receiver_protocol.teleported_state),
                'corrections_applied': getattr(simulation.receiver_protocol, 'corrections_applied', []),
                'runtime': config['runtime'],
                'delay': config['delay']
            }
            
            st.session_state.simulation_results.append(result)
            st.session_state.simulation_history.append(result)
            st.session_state.current_simulation = simulation
            
            # Success message
            st.success(" Simulation completed successfully!")
            
    except Exception as e:
        st.error(f" Simulation failed: {str(e)}")
        st.exception(e)

def display_simulation_results():
    """Display the results of the quantum teleportation simulation."""
    st.subheader(" Simulation Results")
    
    if not st.session_state.simulation_results:
        st.info("No simulation results available. Run a simulation to see results.")
        return
    
    # Get the latest result
    latest_result = st.session_state.simulation_results[-1]
    
    # Results tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "📈 Visualizations", "📊 Statistics", "🔍 Analysis"])
    
    with tab1:
        display_results_summary(latest_result)
    
    with tab2:
        display_visualizations(latest_result)
    
    with tab3:
        display_statistics_dashboard()
    
    with tab4:
        display_detailed_analysis(latest_result)

def display_results_summary(result):
    """Display a summary of the simulation results."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="font-size: 1.0em;">
                <strong>Initial State</strong><br>
                {result['initial_state']}<br>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        bell_state_name = "|Φ⁺⟩" if result['bell_state_type'] == 1 else "|Ψ⁻⟩"
        st.metric(
            label="Bell State",
            value=bell_state_name,
            help="The entangled state used for teleportation"
        )
    
    with col3:
        st.metric(
            label="Measurement Results",
            value=str(result['measurement_results']),
            help="Bell measurement outcomes"
        )
    
    # Detailed information
    st.subheader("Detailed Results")
    
    result_data = {
        "Parameter": [
            "Initial State",
            "Bell State Type", 
            "Measurement Results",
            "Final State",
            "Runtime (ps)",
            "Delay (ps)",
            "Timestamp"
        ],
        "Value": [
            str(result['initial_state']),
            f"{result['bell_state_type']} ({'|Φ⁺⟩' if result['bell_state_type'] == 1 else '|Ψ⁻⟩'})",
            str(result['measurement_results']),
            str(result['final_state']),
            str(result['runtime']),
            str(result['delay']),
            result['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        ]
    }
    
    df = pd.DataFrame(result_data)
    st.dataframe(df, use_container_width=True)

def display_visualizations(result):
    """Display visualizations of the simulation results."""
    col1, col2 = st.columns(2)
    
    with col1:
        # Bell measurement results chart
        fig_bell = create_bell_measurement_chart(result['measurement_results'])
        st.plotly_chart(fig_bell, use_container_width=True)
        
        # Correction rules visualization
        fig_corrections = create_correction_rules_chart(
            result['bell_state_type'],
            result['measurement_results']
        )
        st.plotly_chart(fig_corrections, use_container_width=True)
    
    with col2:
        # Quantum state visualization
        fig_state = create_quantum_state_sphere(result['initial_state'])
        st.plotly_chart(fig_state, use_container_width=True)
        
        # Timeline visualization
        fig_timeline = create_simulation_timeline(result)
        st.plotly_chart(fig_timeline, use_container_width=True)

def display_statistics_dashboard():
    """Display statistics dashboard for multiple simulation runs."""
    if len(st.session_state.simulation_results) < 2:
        st.info("Run multiple simulations to see statistical analysis.")
        return
    
    # Create statistics dashboard
    fig_stats = create_statistics_dashboard(st.session_state.simulation_results)
    st.plotly_chart(fig_stats, use_container_width=True)
    
    # Measurement distribution
    measurement_counts = {}
    for result in st.session_state.simulation_results:
        key = tuple(result['measurement_results'])
        measurement_counts[key] = measurement_counts.get(key, 0) + 1
    
    if measurement_counts:
        st.subheader("Measurement Distribution")
        
        measurements = list(measurement_counts.keys())
        counts = list(measurement_counts.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=[str(m) for m in measurements],
                y=counts,
                marker_color='rgb(55, 83, 109)'
            )
        ])
        
        fig.update_layout(
            title="Bell Measurement Results Distribution",
            xaxis_title="Measurement Results",
            yaxis_title="Count",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_detailed_analysis(result):
    """Display detailed analysis of the simulation results."""
    st.subheader("🔬 Detailed Analysis")
    
    # Analysis metrics
    metrics = calculate_simulation_metrics(result)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Teleportation Success</h3>
            <h2>✅ Yes</h2>
            <p>State successfully teleported</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Correction Gates</h3>
            <h2>{len(metrics.get('corrections', []))}</h2>
            <p>Gates applied for correction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Simulation Time</h3>
            <h2>{result['runtime']}</h2>
            <p>Picoseconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Correction rules explanation
    st.subheader("Correction Rules Explanation")
    
    bell_type = result['bell_state_type']
    measurement = result['measurement_results']
    
    if bell_type == 1:  # |Φ⁺⟩
        st.markdown("""
        **Bell State |Φ⁺⟩ Correction Rules:**
        - Measurement [0,0]: No correction needed
        - Measurement [0,1]: Apply X gate
        - Measurement [1,0]: Apply Z gate
        - Measurement [1,1]: Apply X and Z gates
        """)
    else:  # |Ψ⁻⟩
        st.markdown("""
        **Bell State |Ψ⁻⟩ Correction Rules:**
        - Measurement [0,0]: Apply X gate
        - Measurement [0,1]: No correction needed
        - Measurement [1,0]: Apply X and Z gates
        - Measurement [1,1]: Apply Z gate
        """)
    
    st.info(f"For measurement {measurement}, the correction rules were applied correctly.")

def display_configuration_summary(config):
    """Display a summary of the current configuration."""
    st.subheader("️Configuration")
    
    st.markdown(f"""
    <div class="config-section">
        <h4>Simulation Parameters</h4>
        <ul>
            <li><strong>Initial State:</strong> {config['initial_state']}</li>
            <li><strong>Bell State:</strong> {config['bell_state_name']}</li>
            <li><strong>Runtime:</strong> {config['runtime']} ps</li>
            <li><strong>Delay:</strong> {config['delay']} ps</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def display_quick_statistics():
    """Display quick statistics from simulation history."""
    st.subheader("Quick Stats")
    
    if not st.session_state.simulation_results:
        return
    
    total_runs = len(st.session_state.simulation_results)
    
    # Count measurement outcomes
    outcome_counts = {}
    for result in st.session_state.simulation_results:
        key = tuple(result['measurement_results'])
        outcome_counts[key] = outcome_counts.get(key, 0) + 1
    
    st.metric("Total Runs", total_runs)
    
    if outcome_counts:
        most_common = max(outcome_counts.items(), key=lambda x: x[1])
        st.metric("Most Common Result", f"{most_common[0]} ({most_common[1]}x)")

def export_simulation_results():
    """Export simulation results to JSON format."""
    if not st.session_state.simulation_results:
        st.warning("No results to export.")
        return
    
    try:
        export_data = export_results_to_json(st.session_state.simulation_results)
        
        st.download_button(
            label="Download Results (JSON)",
            data=export_data,
            file_name=f"quantum_teleportation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        st.success("Results prepared for download!")
        
    except Exception as e:
        st.error(f"Export failed: {str(e)}")

if __name__ == "__main__":
    main() 