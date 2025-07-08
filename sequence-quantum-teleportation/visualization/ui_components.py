"""
UI Components for Quantum Teleportation Streamlit GUI
====================================================

This module provides reusable UI components for the Streamlit application,
including configuration panels, result displays, and interactive elements.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


def create_sidebar_config():
    """
    Create the sidebar configuration panel for simulation parameters.
    
    Returns:
        dict: Configuration dictionary with simulation parameters
    """
    st.sidebar.header("Simulation Configuration")
    
    # Initial quantum state selection
    st.sidebar.subheader("Initial Quantum State")
    initial_state = st.sidebar.selectbox(
        "Select the quantum state to teleport:",
        options=["|0⟩", "|1⟩", "|+⟩"],
        index=0,
        help="Choose the initial quantum state that will be teleported"
    )
    
    # Bell state type selection
    st.sidebar.subheader("Bell State Configuration")
    bell_state_option = st.sidebar.selectbox(
        "Select Bell state type:",
        options=["Type 1: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2", "Type 3: |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2"],
        index=0,
        help="Choose the Bell state used for entanglement"
    )
    
    bell_state_type = 1 if "Type 1" in bell_state_option else 3
    bell_state_name = "|Φ⁺⟩" if bell_state_type == 1 else "|Ψ⁻⟩"
    
    # Timing parameters
    st.sidebar.subheader("Timing Parameters")
    
    runtime = st.sidebar.slider(
        "Simulation Runtime (picoseconds):",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
        help="Total simulation time in picoseconds"
    )
    
    delay = st.sidebar.slider(
        "Receiver Delay (picoseconds):",
        min_value=0,
        max_value=1000,
        value=0,
        step=50,
        help="Delay before receiver applies corrections"
    )
    
    # Advanced options
    st.sidebar.subheader("Advanced Options")
    
    show_advanced = st.sidebar.checkbox(
        "Show advanced options",
        value=st.session_state.get('show_advanced_options', False)
    )
    
    advanced_config = {}
    if show_advanced:
        st.session_state.show_advanced_options = True
        
        # Memory parameters
        st.sidebar.write("**Memory Configuration:**")
        memory_fidelity = st.sidebar.slider(
            "Memory Fidelity:",
            min_value=0.5,
            max_value=1.0,
            value=0.9,
            step=0.01,
            help="Fidelity of quantum memories"
        )
        
        memory_coherence = st.sidebar.slider(
            "Coherence Time (ms):",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Quantum memory coherence time"
        )
        
        advanced_config = {
            'memory_fidelity': memory_fidelity,
            'memory_coherence': memory_coherence
        }
    else:
        st.session_state.show_advanced_options = False
    
    # Information panel
    st.sidebar.subheader("Information")
    st.sidebar.info(
        "This simulator implements quantum teleportation using the SeQUeNCe framework. "
        "Adjust the parameters above to explore different scenarios."
    )
    
    # Quick reference
    with st.sidebar.expander("Quick Reference"):
        st.write("""
        **Quantum States:**
        - |0⟩: Computational basis state
        - |1⟩: Computational basis state  
        - |+⟩: Superposition state (|0⟩ + |1⟩)/√2
        
        **Bell States:**
        - |Φ⁺⟩: Maximally entangled state
        - |Ψ⁻⟩: Maximally entangled state
        
        **Process:**
        1. Prepare initial state and Bell pair
        2. Perform Bell measurement
        3. Send classical results
        4. Apply quantum corrections
        """)
    
    return {
        'initial_state': initial_state,
        'bell_state_type': bell_state_type,
        'bell_state_name': bell_state_name,
        'runtime': runtime,
        'delay': delay,
        **advanced_config
    }


def display_simulation_header():
    """Display the main application header with branding."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">Quantum Teleportation Simulator</h1>
        <p style="color: white; margin: 0; opacity: 0.9;">Interactive SeQUeNCe Framework Implementation</p>
    </div>
    """, unsafe_allow_html=True)


def display_results_section(results):
    """
    Display simulation results in a formatted section.
    
    Args:
        results: List of simulation results to display
    """
    if not results:
        st.info("No simulation results available. Run a simulation to see results.")
        return
    
    st.subheader("Simulation Results")
    
    # Display latest result
    latest_result = results[-1]
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Initial State",
            value=latest_result['initial_state'],
            help="The quantum state that was teleported"
        )
    
    with col2:
        bell_name = "|Φ⁺⟩" if latest_result['bell_state_type'] == 1 else "|Ψ⁻⟩"
        st.metric(
            label="Bell State",
            value=bell_name,
            help="The entangled state used for teleportation"
        )
    
    with col3:
        st.metric(
            label="Measurement",
            value=str(latest_result['measurement_results']),
            help="Bell measurement outcomes"
        )
    
    with col4:
        st.metric(
            label="Runtime",
            value=f"{latest_result['runtime']} ps",
            help="Simulation runtime in picoseconds"
        )
    
    # Detailed results table
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
            latest_result['initial_state'],
            f"{latest_result['bell_state_type']} ({bell_name})",
            str(latest_result['measurement_results']),
            latest_result['final_state'],
            latest_result['runtime'],
            latest_result['delay'],
            latest_result['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        ]
    }
    
    df = pd.DataFrame(result_data)
    st.dataframe(df, use_container_width=True)


def display_statistics_section(results):
    """
    Display statistics section for multiple simulation runs.
    
    Args:
        results: List of simulation results for analysis
    """
    if len(results) < 2:
        st.info(" Run multiple simulations to see statistical analysis.")
        return
    
    st.subheader("Statistical Analysis")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Runs", len(results))
    
    with col2:
        # Count unique initial states
        initial_states = set(r['initial_state'] for r in results)
        st.metric("States Tested", len(initial_states))
    
    with col3:
        # Count unique Bell states
        bell_states = set(r['bell_state_type'] for r in results)
        st.metric("Bell States Used", len(bell_states))
    
    # Measurement distribution
    measurement_counts = {}
    for result in results:
        key = tuple(result['measurement_results'])
        measurement_counts[key] = measurement_counts.get(key, 0) + 1
    
    if measurement_counts:
        st.subheader("Measurement Distribution")
        
        # Create distribution table
        dist_data = {
            "Measurement Result": [str(k) for k in measurement_counts.keys()],
            "Count": list(measurement_counts.values()),
            "Percentage": [f"{(v/len(results)*100):.1f}%" for v in measurement_counts.values()]
        }
        
        df_dist = pd.DataFrame(dist_data)
        st.dataframe(df_dist, use_container_width=True)
        
        # Expected vs actual
        st.info("💡 In ideal conditions, each measurement outcome should occur ~25% of the time.")


def display_quantum_state_visualization(state_name):
    """
    Display quantum state visualization and information.
    
    Args:
        state_name: Name of the quantum state to visualize
    """
    st.subheader(f"Quantum State: {state_name}")
    
    # State information
    state_info = {
        "|0⟩": {
            "description": "Computational basis state |0⟩",
            "vector": "[1, 0]",
            "probability": "100% |0⟩, 0% |1⟩"
        },
        "|1⟩": {
            "description": "Computational basis state |1⟩",
            "vector": "[0, 1]",
            "probability": "0% |0⟩, 100% |1⟩"
        },
        "|+⟩": {
            "description": "Superposition state (|0⟩ + |1⟩)/√2",
            "vector": "[1/√2, 1/√2]",
            "probability": "50% |0⟩, 50% |1⟩"
        }
    }
    
    if state_name in state_info:
        info = state_info[state_name]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Description:** {info['description']}")
            st.write(f"**State Vector:** {info['vector']}")
            st.write(f"**Measurement Probabilities:** {info['probability']}")
        
        with col2:
            # Simple visualization
            if state_name == "|0⟩":
                st.bar_chart(pd.DataFrame({"Probability": [1.0, 0.0]}, index=["|0⟩", "|1⟩"]))
            elif state_name == "|1⟩":
                st.bar_chart(pd.DataFrame({"Probability": [0.0, 1.0]}, index=["|0⟩", "|1⟩"]))
            elif state_name == "|+⟩":
                st.bar_chart(pd.DataFrame({"Probability": [0.5, 0.5]}, index=["|0⟩", "|1⟩"]))


def create_control_panel():
    """Create the main control panel for simulation actions."""
    st.subheader("Simulation Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        run_button = st.button(
            "Run Simulation",
            type="primary",
            use_container_width=True,
            help="Execute the quantum teleportation simulation"
        )
    
    with col2:
        clear_button = st.button(
            "Clear Results",
            use_container_width=True,
            help="Clear all simulation results and history"
        )
    
    with col3:
        export_button = st.button(
            "📊 Export Results",
            use_container_width=True,
            help="Export simulation results to JSON format"
        )
    
    return {
        'run': run_button,
        'clear': clear_button,
        'export': export_button
    }


def display_progress_indicator(message="Processing..."):
    """Display a progress indicator with message."""
    return st.spinner(message)


def display_success_message(message):
    """Display a success message with styling."""
    st.markdown(f"""
    <div class="success-message">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)


def display_error_message(message):
    """Display an error message with styling."""
    st.markdown(f"""
    <div class="error-message">
        ❌ {message}
    </div>
    """, unsafe_allow_html=True)


def create_info_panel():
    """Create an information panel with helpful tips."""
    with st.expander(" How Quantum Teleportation Works"):
        st.markdown("""
        **Quantum Teleportation Protocol:**
        
        1. **Preparation**: Create an entangled Bell pair shared between sender and receiver
        2. **Bell Measurement**: Sender performs joint measurement on unknown state and her Bell pair qubit
        3. **Classical Communication**: Sender sends measurement results to receiver
        4. **Correction**: Receiver applies appropriate unitary corrections based on measurement results
        5. **Reconstruction**: Original quantum state is reconstructed at receiver's location
        
        **Key Points:**
        - No quantum information travels between nodes
        - Classical communication is required
        - Original state is destroyed at sender
        - Perfect fidelity is theoretically possible
        """)
    
    with st.expander("Configuration Help"):
        st.markdown("""
        **Parameter Descriptions:**
        
        - **Initial State**: The quantum state to be teleported
        - **Bell State**: The entangled state used for teleportation
        - **Runtime**: Total simulation time in picoseconds
        - **Delay**: Time delay before receiver applies corrections
        
        **Recommended Settings:**
        - Start with |0⟩ or |1⟩ for simple cases
        - Use |+⟩ to test superposition teleportation
        - Try both Bell state types to see different correction rules
        """) 