import sys
import pytest
import numpy as np


from graph import validate_packet

def test_packet_size():
    """
    Tests that packets of incorrect sizes are rejected.
    """
    packet1 = np.array([1,1,1,1,1], dtype = np.float32)
    assert not validate_packet(packet1)

    packet2 = np.array([1,1,1,1,1,1], dtype = np.float32)
    assert validate_packet(packet2) 

    packet3 = np.array([1,1,1,1,1,1,1], dtype = np.float32)
    assert not validate_packet(packet3) 

def test_bad_values():
    """
    Tests that packets containing values outside the boundary are rejected.
    """
    packet1 = np.array([-1,1,1,1,1,1], dtype = np.float32)
    assert not validate_packet(packet1)

    packet2 = np.array([1,1,1,601,1,1], dtype = np.float32)
    assert not validate_packet(packet2)


