#!/usr/bin/env python3

import subprocess
import re
import time

# Attach Sum to Top Serial (3)
# Attach Diff to Bottom Serial (1)

# Define serials for each SDR (update these with your device's serial numbers)
bottom_serial = "1044734c9605000d0e001900deb64fc692"
top_serial = "1044734c9605000cebff2e006fcc4f52b4"

def find_iio_contexts():
    # Run iio_info command to list IIO contexts and capture output
    result = subprocess.run(['iio_info', '-s'], capture_output=True, text=True)
    output = result.stdout
    
    # Assign based on the serial numbers instead of fluctuating USB context
    bottom_uri = None
    top_uri = None
    for match in re.finditer(r"serial=(\w+).*?\[(usb:\d+\.\d+\.\d+)]", output):
        serial, usb_uri = match.groups()
        if serial == bottom_serial:
            bottom_uri = usb_uri
        elif serial == top_serial:
            top_uri = usb_uri

    if bottom_uri and top_uri:
        return bottom_uri, top_uri
    else:
        print("Could not find both IIO contexts. Ensure devices are connected.")
        return None, None

def start_gnuradio_flowgraph(bottom_usb, top_usb):
    # Pass the USB URIs as command-line arguments
    gnuradio_process = subprocess.Popen(['python3', './receiver.py', bottom_usb, top_usb])
    return gnuradio_process

def start_direction_finding_script():
    df_process = subprocess.Popen(['python3', './DirectionFinding.py'])
    return df_process

def main():
    # Get IIO contexts
    bottom_usb, top_usb = find_iio_contexts()
    if not (bottom_usb and top_usb):
        return

    # Start GNURadio and direction-finding programs
    gnuradio_process = start_gnuradio_flowgraph(bottom_usb, top_usb)
    df_process = start_direction_finding_script()

    # Monitor processes
    try:
        while True:
            if gnuradio_process.poll() is not None or df_process.poll() is not None:
                print("A subprocess has stopped unexpectedly. Restarting...")
                gnuradio_process = start_gnuradio_flowgraph(bottom_usb, top_usb)
                df_process = start_direction_finding_script()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping processes...")
        gnuradio_process.terminate()
        df_process.terminate()

if __name__ == "__main__":
    main()
