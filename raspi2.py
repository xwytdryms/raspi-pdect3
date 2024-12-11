import serial
import struct
import time

# Initialize serial connection to Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # Give time for Arduino to reset
    print("Serial connection established")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

def encode_payload(dbmin, dba, dbmax, arc, status):
    # Convert float values to 16-bit integers (scale by 100) and pack into bytes
    dbmin_int = int(dbmin * 100)
    dba_int = int(dba * 100)
    dbmax_int = int(dbmax * 100)
    
    # Create payload using struct packing (big endian)
    payload = struct.pack(">hhhBB", dbmin_int, dba_int, dbmax_int, arc, status)

    # Calculate checksum (XOR of all bytes)
    checksum = 0
    for byte in payload:
        checksum ^= byte

    # Append checksum to the payload
    payload += struct.pack("B", checksum)
    return payload

def send_data(dbmin, dba, dbmax, arc, status):
    # Validate the status
    valid_status = {"low": 0, "medium": 1, "high": 2}
    if status not in valid_status:
        print(f"Error: Invalid status value '{status}'. Must be one of {list(valid_status.keys())}.")
        return

    # Encode the payload
    encoded_payload = encode_payload(dbmin, dba, dbmax, arc, valid_status[status])

    # Send the encoded payload via serial
    ser.write(encoded_payload)
    print(f"Sent payload: {encoded_payload.hex()}")

def read_arduino_response():
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

        send_data(dbmin, dba, dbmax, arc, status)

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
