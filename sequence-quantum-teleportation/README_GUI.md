# Quantum Teleportation Simulator - Streamlit GUI

A beautiful, interactive web interface for quantum teleportation simulation using the SeQUeNCe framework.

## Features

🎮 **Interactive Controls**
- Easy-to-use sidebar configuration
- Real-time parameter adjustment
- One-click simulation execution

📊 **Beautiful Visualizations**
- Bell measurement results charts
- Quantum correction rules visualization
- Bloch sphere representation of quantum states
- Simulation timeline display
- Statistical analysis dashboards

📈 **Comprehensive Analysis**
- Multi-simulation statistical analysis
- Measurement distribution tracking
- Correction pattern analysis
- Export capabilities for results

🔧 **Advanced Configuration**
- Multiple quantum states (|0⟩, |1⟩, |+⟩)
- Different Bell state types (|Φ⁺⟩, |Ψ⁻⟩)
- Configurable timing parameters
- Memory fidelity settings (advanced mode)

## Installation

### Prerequisites

Make sure you have all required packages installed:

```bash
pip install streamlit plotly pandas numpy
```

### Running the GUI

1. Navigate to the project directory:
```bash
cd sequence-quantum-teleportation
```

2. Launch the Streamlit application:
```bash
streamlit run streamlit_app.py
```

3. Open your web browser and go to `http://localhost:8501`

## Usage Guide

### Configuration Panel (Sidebar)

**🔬 Initial Quantum State**
- Select the quantum state to teleport
- Options: |0⟩, |1⟩, |+⟩
- Each state has different measurement probabilities

**🔗 Bell State Configuration**
- Choose between two Bell state types:
  - Type 1: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
  - Type 3: |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
- Different Bell states use different correction rules

**⏱️ Timing Parameters**
- **Runtime**: Total simulation time (100-5000 ps)
- **Delay**: Receiver processing delay (0-1000 ps)

**🔧 Advanced Options**
- **Memory Fidelity**: Quantum memory quality (0.5-1.0)
- **Coherence Time**: Memory coherence duration (0.1-10.0 ms)

### Main Interface

**🎮 Simulation Controls**
- **🚀 Run Simulation**: Execute quantum teleportation
- **🗑️ Clear Results**: Remove all simulation history
- **📊 Export Results**: Download results as JSON

**📊 Results Display**
The results are organized into four tabs:

1. **📋 Summary**: Key metrics and detailed results table
2. **📈 Visualizations**: Charts and graphs
3. **📊 Statistics**: Multi-simulation analysis
4. **🔍 Analysis**: Detailed correction rules explanation

### Visualization Types

**Bell Measurement Chart**
- Shows measurement outcomes for both qubits
- Displays detected Bell state
- Color-coded results

**Correction Rules Chart**
- Visualizes which quantum gates were applied
- Shows correction logic for different Bell states
- Highlights applied vs. not applied corrections

**Bloch Sphere**
- 3D representation of quantum states
- Interactive rotation and zoom
- Shows state vector on sphere surface

**Timeline Visualization**
- Step-by-step simulation process
- Shows timing of events
- Includes delay effects

**Statistics Dashboard**
- Measurement distribution analysis
- Bell state usage patterns
- Runtime vs. delay correlation
- Multi-simulation trends

## Understanding the Results

### Measurement Results
Bell measurements produce four possible outcomes:
- `[0, 0]`: |Φ⁺⟩ state detected
- `[0, 1]`: |Ψ⁺⟩ state detected  
- `[1, 0]`: |Φ⁻⟩ state detected
- `[1, 1]`: |Ψ⁻⟩ state detected

### Correction Rules

**For Bell State |Φ⁺⟩ (Type 1):**
- `[0, 0]`: No correction needed
- `[0, 1]`: Apply X gate
- `[1, 0]`: Apply Z gate
- `[1, 1]`: Apply X and Z gates

**For Bell State |Ψ⁻⟩ (Type 3):**
- `[0, 0]`: Apply X gate
- `[0, 1]`: No correction needed
- `[1, 0]`: Apply X and Z gates
- `[1, 1]`: Apply Z gate

### Statistical Analysis

**Expected Distribution**
In ideal conditions, each measurement outcome should occur ~25% of the time across many simulations.

**Deviation Analysis**
The GUI calculates and displays deviations from theoretical expectations, helping you understand simulation quality.

## File Structure

```
sequence-quantum-teleportation/
├── streamlit_app.py           # Main Streamlit application
├── visualization/             # GUI components module
│   ├── __init__.py           # Module initialization
│   ├── ui_components.py      # UI elements and layouts
│   ├── plotting.py           # Plotly visualization functions
│   └── utils.py              # Utility functions
├── QT_main.py                # Simulation core
├── QT_sender.py              # Sender protocol
├── QT_receiver.py            # Receiver protocol
├── QT_run.py                 # Command-line interface
├── test_streamlit.py         # GUI testing script
└── README_GUI.md             # This file
```

## Code Architecture

The GUI is designed with separation of concerns:

**📱 Presentation Layer** (`streamlit_app.py`)
- Main application logic
- Session state management
- User interaction handling

**🎨 UI Components** (`ui_components.py`)
- Reusable Streamlit components
- Configuration panels
- Result display sections

**📊 Visualization** (`plotting.py`)
- Plotly-based charts and graphs
- Interactive visualizations
- Statistical dashboards

**🔧 Utilities** (`utils.py`)
- Data processing functions
- Analysis algorithms
- Export/import capabilities

**⚙️ Simulation Core** (`QT_*.py`)
- SeQUeNCe-based quantum simulation
- Protocol implementations
- Network setup

## Testing

Run the test suite to verify GUI functionality:

```bash
python test_streamlit.py
```

The test script verifies:
- ✓ Simulation integration
- ✓ Plotting functions
- ✓ Utility functions
- ✓ Multiple simulation scenarios

## Troubleshooting

**Common Issues:**

1. **Import Errors**
   - Ensure all required packages are installed
   - Check Python environment

2. **Visualization Not Loading**
   - Refresh the browser page
   - Check browser console for errors

3. **Simulation Errors**
   - Verify SeQUeNCe framework is properly installed
   - Check simulation parameters are valid

4. **Performance Issues**
   - Reduce number of simultaneous simulations
   - Clear results regularly
   - Close unused browser tabs

## Advanced Features

**Export Functionality**
- Results exported in JSON format
- Includes simulation metadata
- Statistical analysis included
- Timestamp and version information

**Session Management**
- Results persist during browser session
- Configuration remembered between runs
- History tracking for analysis

**Responsive Design**
- Works on desktop and tablet devices
- Adaptive layout for different screen sizes
- Mobile-friendly interface

## Contributing

To extend the GUI:

1. **Adding New Visualizations**
   - Add functions to `plotting.py`
   - Follow existing Plotly patterns
   - Include proper error handling

2. **New UI Components**
   - Add to `ui_components.py`
   - Use consistent styling
   - Include help text and tooltips

3. **Analysis Features**
   - Extend `utils.py` with new functions
   - Maintain JSON serialization compatibility
   - Add comprehensive tests

## License

This project is part of the quantum teleportation simulation suite. See the main project README for license information.

---

**Happy Quantum Teleporting! 🚀⚛️** 