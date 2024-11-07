import zmq
import numpy as np
import math

# Initialize ZMQ context and sockets
context = zmq.Context()

# Set up a PULL socket for each ZMQ PUSH source from GNURadio
nullPwr_socket1 = context.socket(zmq.PULL)
nullPwr_socket1.connect("tcp://localhost:5555")
sumPwr_socket2 = context.socket(zmq.PULL)
sumPwr_socket2.connect("tcp://localhost:5556")
phase0_socket3 = context.socket(zmq.PULL)
phase0_socket3.connect("tcp://localhost:5557")
phase180_socket4 = context.socket(zmq.PULL)
phase180_socket4.connect("tcp://localhost:5558")

def process_data(mag1, mag2):
    # Check for zero and calculate direction
    if mag2 != 0:
        direction_indicator = mag1 / mag2
    else:
        direction_indicator = float('inf')  # Handle divide by zero

    return direction_indicator

def process_phase(phase_diff):
    phase_val = phase_diff / 2
    if not -math.pi <= phase_val <= math.pi:
        raise ValueError("Phase difference out of range. It must be within [-pi, pi].")
    
    # Calculate the angle of incidence
    try:
        angle = math.acos(phase_val / math.pi)
    except ValueError:
        angle = 0 if phase_val >= math.pi else math.pi

    return angle

# Main processing loop
while True:
    # Receive data from each antenna receiver
    nullPwrMag = np.frombuffer(nullPwr_socket1.recv(), dtype=np.float32)
    sumPwrMag = np.frombuffer(sumPwr_socket2.recv(), dtype=np.float32)
    phase0 = np.frombuffer(phase0_socket3.recv(), dtype=np.float32)
    phase180 = np.frombuffer(phase180_socket4.recv(), dtype=np.float32)

    # Process the averaged values directly
    direction = process_data(nullPwrMag[0], sumPwrMag[0])

    # Calculate phase difference
    phase0Degrees = phase0[0] * 180 / math.pi
    phase180Degrees = phase180[0] * 180 / math.pi
    phaseDiff = phase0Degrees - phase180Degrees

    # Output results
    print(f"\n\n Null Mag: {nullPwrMag}")
    print(f"Sum Mag: {sumPwrMag}")
    # print(f"Direction indicator: {direction}")
    print(f"0 Phase: {phase0}")
    print(f"180 Phase: {phase180} \n")
