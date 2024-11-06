import zmq
import numpy as np
import math
import time

# Initialize ZMQ context and sockets
context = zmq.Context()

# Set up a PULL socket for each ZMQ PUSH source from GNURadio
nullPwr_socket1 = context.socket(zmq.PULL)
nullPwr_socket1.connect("tcp://localhost:5555")
sumPwr_socket2 = context.socket(zmq.PULL)
sumPwr_socket2.connect("tcp://localhost:5556")
phaseDiff_socket3 = context.socket(zmq.PULL)
phaseDiff_socket3.connect("tcp://localhost:5557")

# Parameterize the time interval in seconds
AVERAGING_INTERVAL = 1  # Set the averaging interval (in seconds)
start_time = time.time()

# Lists to accumulate data for averaging
nullPwr_accum = []
sumPwr_accum = []
phaseDiff_accum = []

def process_data(mag1, mag2):

    # Check for zero and calculate direction
    if mag2 != 0:
        direction_indicator = mag1 / mag2
    else:
        direction_indicator = float('inf')  # Handle divide by zero

    return direction_indicator

def process_phase(phase_diff):

    # Divided by 2 because value would be out of range. (Probably remove later)
    phase_val = phase_diff / 2
    # Ensure phase_val is within the range [-pi, pi] to avoid math domain errors
    print(phase_val)

    if not -math.pi <= phase_val <= math.pi:
        raise ValueError("Phase difference out of range. It must be within [-pi, pi].")
    
    # Calculate the angle of incidence
    try:
        angle = math.acos(phase_val / math.pi)
    except ValueError:
        # Handle cases where phase_val/pi is out of acos range due to numerical errors
        angle = 0 if phase_val >= math.pi else math.pi

    return angle
    


# Main processing loop
while True:
    # Receive data from each antenna receiver
    nullPwrMag = np.frombuffer(nullPwr_socket1.recv(), dtype=np.float32)
    sumPwrMag = np.frombuffer(sumPwr_socket2.recv(), dtype=np.float32)
    phaseDiff = np.frombuffer(phaseDiff_socket3.recv(), dtype=np.float32)

    # Calculate the average of each received array
    avg_nullPwrMag = np.mean(nullPwrMag)
    avg_sumPwrMag = np.mean(sumPwrMag)
    avg_phaseDiff = np.mean(phaseDiff)

    # Accumulate the averaged values
    nullPwr_accum.append(avg_nullPwrMag)
    sumPwr_accum.append(avg_sumPwrMag)
    phaseDiff_accum.append(avg_phaseDiff)

    # Check if the averaging interval has elapsed
    if time.time() - start_time >= AVERAGING_INTERVAL:
        # Calculate the overall average of accumulated values
        overall_avg_nullPwrMag = np.mean(nullPwr_accum)
        overall_avg_sumPwrMag = np.mean(sumPwr_accum)
        overall_avg_phaseDiff = np.mean(phaseDiff_accum)

        # Process the averaged values
        direction = process_data(overall_avg_nullPwrMag, overall_avg_sumPwrMag)
        incidentAngle = process_phase(overall_avg_phaseDiff)

        # Output results
        print(f"Null Mag: {overall_avg_nullPwrMag}")
        print(f"Sum Mag: {overall_avg_sumPwrMag}")
        # print(f"Direction indicator: {direction}")
        # print(f"Determined Angle: {incidentAngle}")
        incidentDegrees = incidentAngle * 180 / math.pi
        print(f"Transmitter at: {incidentDegrees} deg")

        # Reset accumulation lists and start time for the next interval
        nullPwr_accum.clear()
        sumPwr_accum.clear()
        phaseDiff_accum.clear()
        start_time = time.time()
