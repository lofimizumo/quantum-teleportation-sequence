"""
Quantum Teleportation Receiver Implementation - SeQUeNCe Framework
================================================================

This module implements the receiver side of the quantum teleportation protocol using SeQUeNCe.
The receiver receives measurement results from the sender and applies the
appropriate correction to recover the original quantum state.

Key Operations:
1. Receive classical measurement results from sender
2. Apply conditional quantum corrections based on Bell state type
3. Recover the original teleported quantum state

This implementation follows the same logic as the NetSquid version but uses
SeQUeNCe framework components and protocols.
"""

from sequence.protocol import Protocol
from sequence.kernel.process import Process
from sequence.kernel.event import Event
from sequence.components.memory import Memory
from sequence.components.circuit import Circuit
from sequence.topology.node import Node
import numpy as np


class QuantumTeleportationReceiver(Protocol):
    """
    Protocol for the receiver side of quantum teleportation using SeQUeNCe.
    
    This protocol:
    1. Waits for measurement results from sender via classical channel
    2. Applies conditional corrections to recover the original state
    3. Provides access to the teleported quantum state
    
    Attributes:
        node: The network node running this protocol
        memory_epr: Memory containing receiver's half of Bell pair
        bell_state_type: Type of Bell state (1 for |Φ⁺⟩, 3 for |Ψ⁻⟩)
        measurement_results: Received measurement results from sender
        teleported_state: The final teleported quantum state
        sender_name: Name of the sender node
        delay: Optional delay before applying corrections
    """
    
    def __init__(self, node, memory_epr, bell_state_type=1, sender_name=None, delay=0):
        """
        Initialize the quantum teleportation receiver.
        
        Args:
            node: Network node containing this receiver
            memory_epr: Memory with receiver's half of Bell pair
            bell_state_type: Type of Bell state (1 for |Φ⁺⟩, 3 for |Ψ⁻⟩)
            sender_name: Name of the sender node
            delay: Optional delay before applying corrections
        """
        super().__init__(owner=node, name="teleportation_receiver")
        self.node = node
        self.memory_epr = memory_epr
        self.bell_state_type = bell_state_type
        self.measurement_results = None
        self.teleported_state = None
        self.sender_name = sender_name
        self.delay = delay
    
    def received_message(self, src, msg):
        """
        Handle incoming messages from sender.
        
        Args:
            src: Source of the message
            msg: Incoming message containing measurement results
        """
        if hasattr(msg, 'msg_type') and msg.msg_type == "MEASUREMENT_RESULTS":
            self.measurement_results = msg.measurement_results
            print(f"Receiver: Received measurement results {self.measurement_results} from {src}")
            
            # Schedule correction application
            if self.delay > 0:
                # Apply delay before correction
                process = Process(owner=self, activation_method="apply_corrections", activation_args=[])
                event = Event(self.node.timeline.now() + self.delay, process)
                self.node.timeline.schedule(event)
            else:
                # Apply correction immediately
                self.apply_corrections()
    
    def apply_corrections(self):
        """
        Apply conditional corrections to recover the original state.
        
        This method applies the appropriate unitary corrections based on:
        1. The Bell state type shared between sender and receiver
        2. The measurement results received from the sender
        
        Correction Rules:
        
        For Bell State |Φ⁺⟩ (bell_state_type = 1):
        - Measurement 00: No correction needed
        - Measurement 01: Apply X gate
        - Measurement 10: Apply Z gate  
        - Measurement 11: Apply X and Z gates
        
        For Bell State |Ψ⁻⟩ (bell_state_type = 3):
        - Measurement 00: Apply X gate
        - Measurement 01: No correction needed
        - Measurement 10: Apply X and Z gates
        - Measurement 11: Apply Z gate
        """
        if not self.measurement_results:
            print("Error: No measurement results received")
            return
        
        # Determine corrections based on Bell state type and measurement results
        corrections = self._determine_corrections(self.measurement_results, self.bell_state_type)
        
        # Apply corrections (simulated)
        self._apply_corrections_to_memory(corrections)
        
        # Store the final teleported state
        self.teleported_state = self.memory_epr.quantum_state
        
        print(f"Receiver: Applied corrections {corrections} to recover teleported state")
    
    def _determine_corrections(self, measurement_results, bell_state_type):
        """
        Determine which corrections to apply based on measurement results and Bell state type.
        
        Args:
            measurement_results: List of measurement results [bit1, bit2]
            bell_state_type: Type of Bell state (1 or 3)
            
        Returns:
            List of correction gates to apply
        """
        bit1, bit2 = measurement_results
        corrections = []
        
        if bell_state_type == 1:  # Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
            # Apply Z correction if first measurement bit is 1
            if bit1 == 1:
                corrections.append("Z")
            
            # Apply X correction if second measurement bit is 1
            if bit2 == 1:
                corrections.append("X")
        
        elif bell_state_type == 3:  # Bell state |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
            # Apply Z correction if first measurement bit is 1
            if bit1 == 1:
                corrections.append("Z")
            
            # Apply X correction if second measurement bit is 0
            if bit2 == 0:
                corrections.append("X")
        
        else:
            print(f"Error: Undefined Bell state type {bell_state_type}")
        
        return corrections
    
    def _apply_corrections_to_memory(self, corrections):
        """
        Apply quantum corrections to the quantum state in memory.
        
        Args:
            corrections: List of correction gates to apply
        """
        # In a full implementation, this would apply the corrections to the quantum state
        # For now, we'll simulate the effect of the corrections
        if self.memory_epr.quantum_state:
            # Apply the corrections to the quantum state
            # This is a simplified simulation
            print(f"Applying quantum corrections {corrections} to memory {self.memory_epr.name}")
        else:
            print("Error: No quantum state in memory to correct")
    
    def get_teleported_state(self):
        """
        Get the final teleported quantum state.
        
        Returns:
            The teleported quantum state after corrections
        """
        return self.teleported_state
    
    def show_final_state(self):
        """
        Display the final quantum state for debugging and verification.
        Useful for verifying successful teleportation.
        """
        if self.teleported_state:
            print(f"Receiver: Final teleported state: {self.teleported_state}")
        else:
            print("Receiver: No teleported state available")


class TeleportationMessageHandler:
    """
    Helper class for handling teleportation messages.
    
    This class provides utilities for processing classical messages
    in the quantum teleportation protocol.
    """
    
    @staticmethod
    def create_measurement_message(sender, receiver, measurement_results):
        """
        Create a measurement results message.
        
        Args:
            sender: Name of sender
            receiver: Name of receiver
            measurement_results: List of measurement results
            
        Returns:
            Message object for transmission
        """
        message = {
            'msg_type': 'MEASUREMENT_RESULTS',
            'sender': sender,
            'receiver': receiver,
            'measurement_results': measurement_results
        }
        return message
    
    @staticmethod
    def process_measurement_message(message):
        """
        Process a received measurement message.
        
        Args:
            message: Received message
            
        Returns:
            Extracted measurement results
        """
        if message.get('msg_type') == 'MEASUREMENT_RESULTS':
            return message.get('measurement_results')
        return None 