"""
Quantum Teleportation Main Implementation - SeQUeNCe Framework
============================================================

This module implements the main simulation setup for quantum teleportation using SeQUeNCe.
It creates the network topology, initializes quantum states, and coordinates the
teleportation protocol between sender and receiver.

Key Components:
1. Network topology with sender and receiver nodes
2. Quantum state preparation and Bell state creation
3. Protocol coordination and simulation execution

This implementation follows the same logic as the NetSquid version but uses
SeQUeNCe framework components and simulation infrastructure.
"""

from sequence.kernel.timeline import Timeline
from sequence.topology.node import Node
from sequence.components.memory import Memory
from sequence.components.optical_channel import QuantumChannel, ClassicalChannel
from sequence.kernel.quantum_manager import KetState
from sequence.kernel.process import Process
from sequence.kernel.event import Event
from QT_sender import QuantumTeleportationSender
from QT_receiver import QuantumTeleportationReceiver
import numpy as np
import random


class TeleportationNode(Node):
    """
    Custom node class for quantum teleportation simulation.
    
    This node extends the base SeQUeNCe Node to support quantum teleportation
    protocols and quantum state management.
    """
    
    def __init__(self, name, timeline):
        """
        Initialize the teleportation node.
        
        Args:
            name: Name of the node
            timeline: SeQUeNCe timeline for simulation
        """
        super().__init__(name, timeline)
        self.protocols = {}
        self.quantum_memories = {}
        
    def add_protocol(self, protocol_name, protocol):
        """Add a protocol to this node."""
        self.protocols[protocol_name] = protocol
        
    def add_quantum_memory(self, memory_name, memory):
        """Add a quantum memory to this node."""
        self.quantum_memories[memory_name] = memory
        
    def get_protocol(self, protocol_name):
        """Get a protocol by name."""
        return self.protocols.get(protocol_name)
        
    def get_quantum_memory(self, memory_name):
        """Get a quantum memory by name."""
        return self.quantum_memories.get(memory_name)


class SimpleQuantumState:
    """
    Simple quantum state representation for demonstration.
    
    This class provides a basic quantum state interface compatible with
    SeQUeNCe's quantum state management.
    """
    
    def __init__(self, state_vector=None, state_name="|0⟩"):
        """
        Initialize quantum state.
        
        Args:
            state_vector: Complex amplitudes for quantum state
            state_name: Human-readable name for the state
        """
        if state_vector is None:
            # Default to |0⟩ state
            state_vector = np.array([1.0 + 0j, 0.0 + 0j])
        
        self.state_vector = np.array(state_vector)
        self.state_name = state_name
        
    def __str__(self):
        return f"QuantumState({self.state_name})"
        
    def __repr__(self):
        return self.__str__()


class QuantumTeleportationSimulation:
    """
    Main simulation class for quantum teleportation using SeQUeNCe.
    
    This class orchestrates the entire quantum teleportation simulation,
    including network setup, protocol initialization, and execution.
    """
    
    def __init__(self, runtime=1000, bell_state_type=1, delay=0):
        """
        Initialize the quantum teleportation simulation.
        
        Args:
            runtime: Simulation runtime in picoseconds
            bell_state_type: Type of Bell state (1 for |Φ⁺⟩, 3 for |Ψ⁻⟩)
            delay: Optional delay for receiver corrections
        """
        self.runtime = runtime
        self.bell_state_type = bell_state_type
        self.delay = delay
        
        # Initialize timeline
        self.timeline = Timeline(runtime)
        
        # Initialize nodes
        self.sender_node = None
        self.receiver_node = None
        
        # Initialize protocols
        self.sender_protocol = None
        self.receiver_protocol = None
        
        # Initialize quantum states
        self.initial_state = None
        self.bell_state_pair = None
        
    def setup_network(self):
        """
        Set up the network topology for quantum teleportation.
        
        This creates sender and receiver nodes with appropriate quantum
        memories and classical communication channels.
        """
        # Create nodes
        self.sender_node = TeleportationNode("sender", self.timeline)
        self.receiver_node = TeleportationNode("receiver", self.timeline)
        
        # Set random seeds for reproducibility
        self.sender_node.set_seed(42)
        self.receiver_node.set_seed(43)
        
        # Create quantum memories
        sender_memory_unknown = Memory("sender_unknown", self.timeline, 
                                     fidelity=0.9, frequency=1e6, efficiency=0.8, 
                                     coherence_time=1e-3, wavelength=1550)
        sender_memory_epr = Memory("sender_epr", self.timeline,
                                 fidelity=0.9, frequency=1e6, efficiency=0.8,
                                 coherence_time=1e-3, wavelength=1550)
        receiver_memory_epr = Memory("receiver_epr", self.timeline,
                                   fidelity=0.9, frequency=1e6, efficiency=0.8,
                                   coherence_time=1e-3, wavelength=1550)
        
        # Add memories to nodes
        self.sender_node.add_quantum_memory("unknown", sender_memory_unknown)
        self.sender_node.add_quantum_memory("epr", sender_memory_epr)
        self.receiver_node.add_quantum_memory("epr", receiver_memory_epr)
        
        # Create classical channel for communication
        classical_channel = ClassicalChannel("classical_channel", self.timeline, distance=1e3)
        classical_channel.set_ends(self.sender_node, self.receiver_node.name)
        
        print(f"Network setup complete: {self.sender_node.name} ↔ {self.receiver_node.name}")
        
    def prepare_quantum_states(self, initial_state_name="|0⟩"):
        """
        Prepare quantum states for teleportation.
        
        This method:
        1. Creates the unknown quantum state to be teleported
        2. Creates the Bell state pair shared between sender and receiver
        3. Assigns states to appropriate quantum memories
        
        Args:
            initial_state_name: Name of the initial state to teleport
        """
        # Create the unknown quantum state to teleport
        if initial_state_name == "|0⟩":
            self.initial_state = SimpleQuantumState(
                state_vector=np.array([1.0 + 0j, 0.0 + 0j]),
                state_name="|0⟩"
            )
        elif initial_state_name == "|1⟩":
            self.initial_state = SimpleQuantumState(
                state_vector=np.array([0.0 + 0j, 1.0 + 0j]),
                state_name="|1⟩"
            )
        elif initial_state_name == "|+⟩":
            self.initial_state = SimpleQuantumState(
                state_vector=np.array([1/np.sqrt(2) + 0j, 1/np.sqrt(2) + 0j]),
                state_name="|+⟩"
            )
        else:
            # Default to |0⟩
            self.initial_state = SimpleQuantumState(
                state_vector=np.array([1.0 + 0j, 0.0 + 0j]),
                state_name="|0⟩"
            )
        
        # Create Bell state pair
        self.bell_state_pair = self._create_bell_state_pair(self.bell_state_type)
        
        # Assign states to memories
        sender_memory_unknown = self.sender_node.get_quantum_memory("unknown")
        sender_memory_epr = self.sender_node.get_quantum_memory("epr")
        receiver_memory_epr = self.receiver_node.get_quantum_memory("epr")
        
        # Set quantum states in memories
        sender_memory_unknown.quantum_state = self.initial_state
        sender_memory_epr.quantum_state = self.bell_state_pair[0]
        receiver_memory_epr.quantum_state = self.bell_state_pair[1]
        
        print(f"Quantum states prepared:")
        print(f"  Initial state: {self.initial_state}")
        print(f"  Bell state type: {self.bell_state_type}")
        print(f"  Bell pair: {self.bell_state_pair}")
        
    def _create_bell_state_pair(self, bell_state_type):
        """
        Create a Bell state pair for quantum teleportation.
        
        Args:
            bell_state_type: Type of Bell state (1 for |Φ⁺⟩, 3 for |Ψ⁻⟩)
            
        Returns:
            Tuple of quantum states representing the Bell pair
        """
        if bell_state_type == 1:
            # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
            state_name = "|Φ⁺⟩"
            # For simplicity, represent as individual qubit states
            sender_state = SimpleQuantumState(
                state_vector=np.array([1/np.sqrt(2) + 0j, 1/np.sqrt(2) + 0j]),
                state_name=f"{state_name}_sender"
            )
            receiver_state = SimpleQuantumState(
                state_vector=np.array([1/np.sqrt(2) + 0j, 1/np.sqrt(2) + 0j]),
                state_name=f"{state_name}_receiver"
            )
        elif bell_state_type == 3:
            # |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
            state_name = "|Ψ⁻⟩"
            sender_state = SimpleQuantumState(
                state_vector=np.array([1/np.sqrt(2) + 0j, -1/np.sqrt(2) + 0j]),
                state_name=f"{state_name}_sender"
            )
            receiver_state = SimpleQuantumState(
                state_vector=np.array([1/np.sqrt(2) + 0j, -1/np.sqrt(2) + 0j]),
                state_name=f"{state_name}_receiver"
            )
        else:
            raise ValueError(f"Unsupported Bell state type: {bell_state_type}")
            
        return (sender_state, receiver_state)
        
    def setup_protocols(self):
        """
        Set up quantum teleportation protocols for sender and receiver.
        
        This method creates and configures the teleportation protocols
        that will execute the quantum teleportation procedure.
        """
        # Get quantum memories
        sender_memory_unknown = self.sender_node.get_quantum_memory("unknown")
        sender_memory_epr = self.sender_node.get_quantum_memory("epr")
        receiver_memory_epr = self.receiver_node.get_quantum_memory("epr")
        
        # Create sender protocol
        self.sender_protocol = QuantumTeleportationSender(
            node=self.sender_node,
            memory_unknown=sender_memory_unknown,
            memory_epr=sender_memory_epr,
            receiver_name=self.receiver_node.name
        )
        
        # Create receiver protocol
        self.receiver_protocol = QuantumTeleportationReceiver(
            node=self.receiver_node,
            memory_epr=receiver_memory_epr,
            bell_state_type=self.bell_state_type,
            sender_name=self.sender_node.name,
            delay=self.delay
        )
        
        # Add protocols to nodes
        self.sender_node.add_protocol("teleportation", self.sender_protocol)
        self.receiver_node.add_protocol("teleportation", self.receiver_protocol)
        
        # Register receiver protocol to handle messages
        self.receiver_node.protocols["teleportation"] = self.receiver_protocol
        
        # Set up direct reference for message passing (simplified approach)
        self.sender_node._receiver_protocol_ref = self.receiver_protocol
        
        print(f"Protocols configured:")
        print(f"  Sender protocol: {type(self.sender_protocol).__name__}")
        print(f"  Receiver protocol: {type(self.receiver_protocol).__name__}")
        
    def run_simulation(self):
        """
        Execute the quantum teleportation simulation.
        
        This method initializes the timeline, starts the teleportation
        protocol, and runs the simulation to completion.
        """
        # Initialize timeline
        self.timeline.init()
        
        # Start teleportation protocol
        self.sender_protocol.start_teleportation()
        
        # Run simulation
        print(f"\nStarting quantum teleportation simulation...")
        print(f"Runtime: {self.runtime} picoseconds")
        
        self.timeline.run()
        
        print(f"Simulation completed!")
        
    def show_results(self):
        """
        Display simulation results and verify teleportation success.
        
        This method shows the initial state, measurement results,
        and final teleported state for verification.
        """
        print(f"\n=== Quantum Teleportation Results ===")
        print(f"Initial state: {self.initial_state}")
        print(f"Bell state type: {self.bell_state_type}")
        
        if self.sender_protocol.measurement_results:
            print(f"Measurement results: {self.sender_protocol.measurement_results}")
        else:
            print("No measurement results available")
            
        if self.receiver_protocol.teleported_state:
            print(f"Final teleported state: {self.receiver_protocol.teleported_state}")
        else:
            print("No teleported state available")
            
        # Show receiver final state
        self.receiver_protocol.show_final_state()


def create_quantum_teleportation_simulation(runtime=1000, bell_state_type=1, delay=0, initial_state="|0⟩"):
    """
    Create and configure a quantum teleportation simulation.
    
    Args:
        runtime: Simulation runtime in picoseconds
        bell_state_type: Type of Bell state (1 for |Φ⁺⟩, 3 for |Ψ⁻⟩)
        delay: Optional delay for receiver corrections
        initial_state: Initial quantum state to teleport
        
    Returns:
        Configured QuantumTeleportationSimulation instance
    """
    simulation = QuantumTeleportationSimulation(runtime, bell_state_type, delay)
    simulation.setup_network()
    simulation.prepare_quantum_states(initial_state)
    simulation.setup_protocols()
    return simulation


def create_bell_state_memories(timeline, node1, node2, memory_name_1, memory_name_2):
    """
    Create Bell state between two quantum memories.
    
    Args:
        timeline: SeQUeNCe timeline
        node1: First node
        node2: Second node
        memory_name_1: Name of memory on first node
        memory_name_2: Name of memory on second node
    
    Returns:
        Tuple of (memory1, memory2) with Bell state
    """
    # Create quantum memories
    memory1 = Memory(memory_name_1, timeline, fidelity=1.0, frequency=0,
                     efficiency=1.0, coherence_time=0, wavelength=500)
    memory2 = Memory(memory_name_2, timeline, fidelity=1.0, frequency=0,
                     efficiency=1.0, coherence_time=0, wavelength=500)
    
    # Add memories to nodes
    node1.add_component(memory1)
    node2.add_component(memory2)
    
    # Create Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    # This is a simplified representation
    bell_state_1 = QuantumState()
    bell_state_2 = QuantumState()
    
    # Set up entanglement between memories
    memory1.entangled_memory = {'node_id': node2.name, 'memo_id': memory_name_2}
    memory2.entangled_memory = {'node_id': node1.name, 'memo_id': memory_name_1}
    
    # Set quantum states (simplified)
    memory1.quantum_state = bell_state_1
    memory2.quantum_state = bell_state_2
    
    return memory1, memory2


def create_unknown_state_memory(timeline, node, memory_name, state_type="X"):
    """
    Create quantum memory with unknown state to be teleported.
    
    Args:
        timeline: SeQUeNCe timeline
        node: Node to add memory to
        memory_name: Name of the memory
        state_type: Type of state to create ("X" for |1⟩, "H" for |+⟩)
    
    Returns:
        Memory with unknown quantum state
    """
    memory = Memory(memory_name, timeline, fidelity=1.0, frequency=0,
                    efficiency=1.0, coherence_time=0, wavelength=500)
    
    # Add memory to node
    node.add_component(memory)
    
    # Create unknown quantum state
    unknown_state = QuantumState()
    
    # Set state based on type
    if state_type == "X":
        # Create |1⟩ state (equivalent to applying X gate to |0⟩)
        unknown_state.state = np.array([0, 1], dtype=complex)
    elif state_type == "H":
        # Create |+⟩ state (equivalent to applying H gate to |0⟩)
        unknown_state.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
    else:
        # Default to |0⟩ state
        unknown_state.state = np.array([1, 0], dtype=complex)
    
    memory.quantum_state = unknown_state
    
    return memory


def run_teleportation_sim(runtimes=1, delay=0, bell_state_type=1, state_type="X"):
    """
    Run quantum teleportation simulation with configurable parameters.
    
    This function sets up a complete quantum teleportation experiment including:
    - Network nodes (sender and receiver)
    - Quantum memories for Bell state and unknown state
    - Classical communication channel
    - Protocol execution
    
    Args:
        runtimes: Number of simulation runs (default: 1)
        delay: Classical communication delay in picoseconds (default: 0)
        bell_state_type: Type of Bell state (1 for |Φ⁺⟩, 3 for |Ψ⁻⟩)
        state_type: Type of unknown state to teleport ("X" or "H")
    
    Returns:
        0 on successful completion
    """
    
    for run in range(runtimes):
        print(f"\n=== Quantum Teleportation Simulation Run {run + 1} ===")
        
        # ====================================================================
        # TIMELINE AND NETWORK SETUP
        # ====================================================================
        
        # Create simulation timeline (10 seconds = 10e12 picoseconds)
        timeline = Timeline(10e12)
        
        # Create sender and receiver nodes
        sender_node = TeleportationNode("SenderNode", timeline)
        receiver_node = TeleportationNode("ReceiverNode", timeline)
        
        # Set random seeds for reproducibility
        sender_node.set_seed(0)
        receiver_node.set_seed(1)
        
        print(f"Created nodes: {sender_node.name} and {receiver_node.name}")
        
        # ====================================================================
        # CLASSICAL COMMUNICATION CHANNEL
        # ====================================================================
        
        # Create classical channel for measurement results
        classical_channel = ClassicalChannel("cc_sender_receiver", timeline,
                                            distance=1000,  # 1 km
                                            delay=delay)
        
        # Connect sender to receiver
        classical_channel.set_ends(sender_node, receiver_node.name)
        
        print(f"Created classical channel: {classical_channel.name}")
        
        # ====================================================================
        # QUANTUM MEMORY SETUP
        # ====================================================================
        
        # Create unknown state memory on sender
        unknown_memory = create_unknown_state_memory(timeline, sender_node, 
                                                   "unknown_memory", state_type)
        
        # Create Bell state memories between sender and receiver
        sender_epr_memory, receiver_epr_memory = create_bell_state_memories(
            timeline, sender_node, receiver_node, 
            "sender_epr_memory", "receiver_epr_memory"
        )
        
        print(f"Created quantum memories:")
        print(f"  - Unknown state memory: {unknown_memory.name}")
        print(f"  - Sender EPR memory: {sender_epr_memory.name}")
        print(f"  - Receiver EPR memory: {receiver_epr_memory.name}")
        
        # ====================================================================
        # PROTOCOL INITIALIZATION
        # ====================================================================
        
        # Create sender protocol
        sender_protocol = QuantumTeleportationSender(
            name="teleportation_sender",
            timeline=timeline,
            node=sender_node,
            memory_unknown=unknown_memory,
            memory_epr=sender_epr_memory,
            receiver_name=receiver_node.name
        )
        
        # Create receiver protocol
        receiver_protocol = QuantumTeleportationReceiver(
            name="teleportation_receiver",
            timeline=timeline,
            node=receiver_node,
            memory_epr=receiver_epr_memory,
            bell_state_type=bell_state_type,
            sender_name=sender_node.name,
            delay=delay
        )
        
        # Set up protocols in nodes
        sender_node.teleportation_protocol = sender_protocol
        receiver_node.teleportation_protocol = receiver_protocol
        
        print(f"Initialized teleportation protocols")
        
        # ====================================================================
        # SIMULATION EXECUTION
        # ====================================================================
        
        # Initialize timeline
        timeline.init()
        
        # Start teleportation protocol
        sender_protocol.start_teleportation()
        
        print(f"Starting simulation...")
        
        # Run simulation
        timeline.run()
        
        print(f"Simulation completed at time: {timeline.now()} picoseconds")
        
        # ====================================================================
        # RESULTS DISPLAY
        # ====================================================================
        
        # Show final results
        if receiver_protocol.teleported_state:
            print(f"✓ Teleportation successful!")
            receiver_protocol.show_final_state()
        else:
            print(f"✗ Teleportation failed or incomplete")
        
        print(f"Measurement results: {receiver_protocol.measurement_results}")
        
    return 0


def demonstrate_different_states():
    """
    Demonstrate teleportation with different quantum states.
    
    This function shows how different initial states are teleported
    using the same protocol.
    """
    print("\n" + "="*60)
    print("QUANTUM TELEPORTATION DEMONSTRATION")
    print("="*60)
    
    # Test different initial states
    states_to_test = [
        ("X", "Teleporting |1⟩ state"),
        ("H", "Teleporting |+⟩ state"),
        ("0", "Teleporting |0⟩ state")
    ]
    
    for state_type, description in states_to_test:
        print(f"\n{description}")
        print("-" * len(description))
        run_teleportation_sim(runtimes=1, state_type=state_type)
    
    print(f"\nDemonstration completed!")


if __name__ == '__main__':
    # Run quantum teleportation simulation with default parameters
    run_teleportation_sim()
    
    # Optionally run demonstration with different states
    # demonstrate_different_states() 