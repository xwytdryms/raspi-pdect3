import serial
import time
import struct

# Initialize serial connection to Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # Give time for Arduino to reset
    print("Serial connection established")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

def encode_payload(dbmin, dba, dbmax, arc, status):
    """
    Encodes the payload for transmission to the Arduino.
    - dbmin, dba, dbmax: Floats, scaled to 2 decimal precision
    - arc: Integer value
    - status: String ("low", "medium", "high") converted to corresponding integer
    """
    # Validate and convert status
    status_map = {"low": 1, "medium": 2, "high": 3}
    if status not in status_map:
        raise ValueError(f"Invalid status value: {status}. Must be one of {list(status_map.keys())}.")

    status_value = status_map[status]

    # Scale floats to 2 decimal places and convert to int
    dbmin_int = int(dbmin * 100)
    dba_int = int(dba * 100)
    dbmax_int = int(dbmax * 100)

    # Pack the data into a binary format
    payload = struct.pack(">hhhBB", dbmin_int, dba_int, dbmax_int, arc, status_value)
    return payload

def send_payload(payload):
    """
    Sends the binary payload to the Arduino over serial.
    """
    ser.write(payload)
    print(f"Sent payload: {payload.hex()}")

def read_arduino_response():
    """
    Reads and prints the response from the Arduino.
    """
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Arduino: {response}")
        return response
    return None

try:
    while True:
        # Simulated values (adjust as necessary)
        dbmin = 50.00
        dba = 55.50
        dbmax = 60.00
        arc = 2  # Integer value
        status = "high"  # Must be "low", "medium", or "high"

        try:
            payload = encode_payload(dbmin, dba, dbmax, arc, status)
            send_payload(payload)
        except ValueError as e:
            print(e)
            continue

        while True:
            response = read_arduino_response()
            if response and "Packet queued" in response:
                print("Data has been transmitted to LoRa")
                break

        time.sleep(30)  # Send data every 30 seconds

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()
    print("Serial connection closed")
