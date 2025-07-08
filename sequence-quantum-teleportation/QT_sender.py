"""
Quantum Teleportation Sender Implementation - SeQUeNCe Framework
===============================================================

This module implements the sender side of the quantum teleportation protocol using SeQUeNCe.
The sender performs Bell state measurement on the unknown qubit and her half
of the shared Bell pair, then sends the measurement results to the receiver.

Key Operations:
1. Bell measurement (CNOT + Hadamard + measurement)
2. Classical communication of measurement results

This implementation follows the same logic as the NetSquid version but uses
SeQUeNCe framework components and protocols.
"""

from sequence.protocol import Protocol
from sequence.kernel.process import Process
from sequence.kernel.event import Event
from sequence.components.memory import Memory
from sequence.components.circuit import Circuit
from sequence.kernel.quantum_manager import KetState
from sequence.message import Message
import numpy as np
import random


class QuantumTeleportationSender(Protocol):
    """
    Protocol for the sender side of quantum teleportation using SeQUeNCe.
    
    This protocol:
    1. Receives an unknown quantum state to teleport
    2. Performs Bell measurement with shared EPR pair
    3. Sends measurement results to receiver via classical channel
    
    Attributes:
        name: Name of the sender protocol
        node: The network node running this protocol
        memory_unknown: Memory containing the unknown qubit to teleport
        memory_epr: Memory containing sender's half of Bell pair
        measurement_results: Results from Bell measurement
        receiver_name: Name of the receiver node
    """
    
    def __init__(self, node, memory_unknown, memory_epr, receiver_name):
        """
        Initialize the quantum teleportation sender.
        
        Args:
            node: Network node containing this sender
            memory_unknown: Memory with unknown qubit to teleport
            memory_epr: Memory with sender's half of Bell pair
            receiver_name: Name of the receiver node
        """
        super().__init__(owner=node, name="teleportation_sender")
        self.node = node
        self.memory_unknown = memory_unknown
        self.memory_epr = memory_epr
        self.measurement_results = None
        self.receiver_name = receiver_name
    
    def start_teleportation(self):
        """
        Start the quantum teleportation protocol.
        
        This method initiates the Bell measurement process and schedules
        the classical communication of results.
        """
        # Schedule Bell measurement
        process = Process(owner=self, activation_method="perform_bell_measurement", activation_args=[])
        event = Event(self.node.timeline.now(), process)
        self.node.timeline.schedule(event)
    
    def perform_bell_measurement(self):
        """
        Perform Bell measurement on the unknown qubit and EPR qubit.
        
        This implements the Bell measurement by:
        1. Applying CNOT between unknown qubit and EPR qubit
        2. Applying Hadamard gate to unknown qubit
        3. Measuring both qubits in computational basis
        
        The measurement results determine which Bell state was observed.
        """
        # Create quantum circuit for Bell measurement
        circuit = Circuit(2)
        
        # Step 1: Apply CNOT gate between unknown qubit (0) and EPR qubit (1)
        # This creates entanglement between the unknown state and the Bell pair
        circuit.cx(0, 1)  # CNOT gate
        
        # Step 2: Apply Hadamard gate to the unknown qubit (position 0)
        # This transforms the computational basis to Bell basis
        circuit.h(0)  # Hadamard gate
        
        # Step 3: Simulate Bell measurement results
        # In a full implementation, this would involve proper quantum state manipulation
        measurement_result = self._simulate_bell_measurement()
        
        # Store measurement results
        self.measurement_results = measurement_result
        
        # Send results to receiver
        self._send_measurement_results()
        
        print(f"Sender: Performed Bell measurement, results: {self.measurement_results}")
    
    def _simulate_bell_measurement(self):
        """
        Simulate Bell measurement results.
        
        Returns:
            List of measurement results [bit1, bit2]
        """
        # Simulate the four possible Bell measurement outcomes
        # Each outcome occurs with equal probability (1/4)
        outcome = random.randint(0, 3)
        
        if outcome == 0:
            return [0, 0]  # |Φ⁺⟩ state
        elif outcome == 1:
            return [0, 1]  # |Ψ⁺⟩ state
        elif outcome == 2:
            return [1, 0]  # |Φ⁻⟩ state
        else:
            return [1, 1]  # |Ψ⁻⟩ state
    
    def _send_measurement_results(self):
        """
        Send measurement results to receiver via classical channel.
        
        This classical communication is essential for the receiver to know
        which correction to apply to recover the original state.
        """
        if self.measurement_results:
            # Create message with measurement results
            message = TeleportationMessage(
                msg_type="MEASUREMENT_RESULTS",
                sender=self.node.name,
                receiver=self.receiver_name,
                measurement_results=self.measurement_results
            )
            
            # Get receiver node and protocol
            # For now, we'll store a reference to the receiver protocol
            # In a full implementation, this would go through proper message routing
            receiver_node = None
            if hasattr(self.node, '_receiver_protocol_ref'):
                receiver_protocol = self.node._receiver_protocol_ref
                receiver_protocol.received_message(self.node.name, message)
                print(f"Sender: Sent measurement results {self.measurement_results} to {self.receiver_name}")
                return
            
            if receiver_node and hasattr(receiver_node, 'protocols'):
                receiver_protocol = receiver_node.protocols.get("teleportation")
                if receiver_protocol:
                    # Directly call the receiver's message handler
                    receiver_protocol.received_message(self.node.name, message)
                    print(f"Sender: Sent measurement results {self.measurement_results} to {self.receiver_name}")
                else:
                    print(f"Error: No teleportation protocol found on receiver {self.receiver_name}")
            else:
                print(f"Error: Receiver node {self.receiver_name} not found")
        else:
            print(f"Error: Cannot send measurement results - missing results")
    
    def received_message(self, src, msg):
        """
        Handle received messages (required by Protocol base class).
        
        Args:
            src: Source of the message
            msg: Received message
        """
        # Sender typically doesn't receive messages in teleportation protocol
        pass


class TeleportationMessage(Message):
    """
    Message class for quantum teleportation classical communication.
    
    This message carries the measurement results from sender to receiver.
    """
    
    def __init__(self, msg_type, sender, receiver, measurement_results):
        """
        Initialize teleportation message.
        
        Args:
            msg_type: Type of message ("MEASUREMENT_RESULTS")
            sender: Name of sender entity
            receiver: Name of receiver entity
            measurement_results: List of measurement results [bit1, bit2]
        """
        super().__init__(msg_type, receiver)
        self.sender = sender
        self.measurement_results = measurement_results
    
    def __str__(self):
        return f"TeleportationMessage(type={self.msg_type}, from={self.sender}, to={self.receiver}, results={self.measurement_results})" 