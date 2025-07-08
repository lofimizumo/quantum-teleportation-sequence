# Quantum Teleportation Protocol - SeQUeNCe Framework Implementation

Author: AI Assistant  
Framework: SeQUeNCe (Simulator of QUantum Network Communication)

## Overview

This project implements the quantum teleportation protocol using the SeQUeNCe framework, following the exact same structure and logic as the original NetSquid implementation. The quantum teleportation protocol enables the transfer of an unknown quantum state from one location to another using shared entanglement and classical communication.

## Status

**Framework**: SeQUeNCe (Compatible with SeQUeNCe v0.6+)  
**Implementation Date**: December 2024  
**Based on**: NetSquid QuantumTeleportation implementation

## Project Structure

```
sequence-quantum-teleportation/
├── QT_sender.py          # Sender protocol implementation
├── QT_receiver.py        # Receiver protocol implementation  
├── QT_main.py           # Main simulation setup
├── QT_run.py            # Run script with parameters
└── README.md            # This documentation
```

## Files Description

### QT_sender.py
- **QuantumTeleportationSender**: Main sender protocol class
- **TeleportationMessage**: Message class for classical communication
- Implements Bell measurement (CNOT + Hadamard + measurement)
- Sends measurement results via classical channel

### QT_receiver.py  
- **QuantumTeleportationReceiver**: Main receiver protocol class
- **TeleportationMessageHandler**: Helper for message processing
- Applies conditional corrections based on measurement results
- Supports different Bell state types (|Φ⁺⟩ and |Ψ⁻⟩)

### QT_main.py
- Complete simulation setup with SeQUeNCe components
- **TeleportationNode**: Custom node class for teleportation
- Bell state preparation and quantum memory management
- Timeline and network initialization

### QT_run.py
- Main entry point for running simulations
- **SimpleQuantumState**: Basic quantum state representation
- Configurable parameters and demonstration scenarios
- Results analysis and statistics

## How to Use

### Basic Usage

```bash
python QT_run.py
```

### Advanced Usage

```python
from QT_run import run_teleportation_sim

# Run with custom parameters
run_teleportation_sim(
    runtimes=5,           # Number of simulation runs
    delay=1000,           # Classical communication delay (ps)
    bell_state_type=1,    # Bell state type (1 or 3)
    state_type="H"        # Unknown state type ("X", "H", "0")
)
```

### Demonstration Mode

```python
from QT_run import demonstrate_teleportation_scenarios

# Run comprehensive demonstration
demonstrate_teleportation_scenarios()
```

## Protocol Implementation

### Bell State Corrections

The implementation supports two Bell state types with different correction rules:

#### Bell State |Φ⁺⟩ (bell_state_type = 1)
- Measurement 00: No correction
- Measurement 01: Apply X gate  
- Measurement 10: Apply Z gate
- Measurement 11: Apply X and Z gates

#### Bell State |Ψ⁻⟩ (bell_state_type = 3)  
- Measurement 00: Apply X gate
- Measurement 01: No correction
- Measurement 10: Apply X and Z gates
- Measurement 11: Apply Z gate

### Quantum States Supported

- **|0⟩ state**: Default computational basis state
- **|1⟩ state**: X-rotated state (state_type="X")  
- **|+⟩ state**: Hadamard-rotated state (state_type="H")

## Key Features

### Framework Adaptation
- **SeQUeNCe Integration**: Uses SeQUeNCe Timeline, Node, and Memory components
- **Event-Driven**: Leverages SeQUeNCe's discrete event simulation
- **Classical Communication**: Implements classical channels for measurement results
- **Quantum Memory**: Uses SeQUeNCe memory components for quantum state storage

### Protocol Fidelity
- **Exact Logic**: Follows the same protocol steps as NetSquid implementation
- **Bell Measurement**: CNOT + Hadamard + measurement sequence
- **Conditional Corrections**: Same correction rules for different Bell states
- **State Preparation**: Identical quantum state initialization

### Simulation Features
- **Configurable Parameters**: Runtime, delay, Bell state type, initial state
- **Multiple Scenarios**: Demonstration mode with different configurations
- **Results Analysis**: Detailed output and statistics
- **Error Handling**: Robust error checking and reporting

## Differences from NetSquid Version

### Framework Components
| NetSquid | SeQUeNCe | Purpose |
|----------|----------|---------|
| `NodeProtocol` | `Entity` | Base protocol class |
| `QuantumProgram` | `Circuit` | Quantum operations |
| `ClassicalChannel` | `ClassicalChannel` | Classical communication |
| `QuantumProcessor` | `Memory` | Quantum state storage |

### Implementation Adaptations
1. **Quantum State Management**: Simplified quantum state representation
2. **Message Handling**: Custom message classes for classical communication  
3. **Event Scheduling**: Uses SeQUeNCe's Process and Event system
4. **Node Architecture**: Extended Node class for teleportation functionality

### Maintained Features
- ✅ Same protocol logic and flow
- ✅ Identical Bell measurement sequence
- ✅ Same correction rules for different Bell states
- ✅ Compatible parameter configuration
- ✅ Equivalent simulation output

## Mathematical Foundation

The implementation follows the standard quantum teleportation protocol:

1. **Initial State**: Unknown state |ψ⟩ = α|0⟩ + β|1⟩
2. **Bell State**: Shared entanglement |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
3. **Bell Measurement**: CNOT + Hadamard + computational basis measurement
4. **Classical Communication**: 2-bit measurement results
5. **Conditional Correction**: Unitary operations based on measurement results

## Performance Characteristics

- **Simulation Time**: ~10 seconds timeline (configurable)
- **Memory Usage**: Minimal quantum memory requirements
- **Scalability**: Single teleportation per simulation run
- **Accuracy**: Deterministic protocol with simulated measurement outcomes

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure SeQUeNCe is properly installed
   ```bash
   pip install sequence-quantum
   ```

2. **Timeline Errors**: Check timeline initialization and event scheduling

3. **Memory Issues**: Verify quantum memory setup and state assignment

4. **Communication Errors**: Ensure classical channel connectivity

### Debug Mode

Enable detailed logging by modifying the timeline:
```python
timeline.show_progress = True
```

## Future Enhancements

### Planned Features
- [ ] Noise model integration
- [ ] Fidelity analysis tools
- [ ] Multi-hop teleportation
- [ ] Performance benchmarking
- [ ] Visualization tools

### Research Extensions
- [ ] Quantum error correction
- [ ] Entanglement purification
- [ ] Network topology effects
- [ ] Realistic hardware models

## References

1. **Original NetSquid Implementation**: QuantumTeleportation folder
2. **SeQUeNCe Documentation**: [SeQUeNCe GitHub](https://github.com/sequence-toolbox/SeQUeNCe)
3. **Quantum Teleportation**: Bennett et al., Physical Review Letters 70.13 (1993)
4. **SeQUeNCe Tutorial**: [Chapter 3: Entanglement Management](https://sequence-rtd-tutorial.readthedocs.io/)

## License

This implementation follows the same licensing terms as the original NetSquid implementation and SeQUeNCe framework.

---

**Note**: This SeQUeNCe implementation maintains complete protocol compatibility with the original NetSquid version while adapting to the SeQUeNCe framework's architecture and components. 