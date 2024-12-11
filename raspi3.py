import serial
import time

# Initialize serial connection to Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # Give time for Arduino to reset
    print("Serial connection established")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

def send_data(dbmin, dba, dbmax, arc, status):
    # Format the data as a single string with space-separated values
    data_str = f"{dbmin:.3f} {dba:.3f} {dbmax:.3f} {arc} {status}\n"
    ser.write(data_str.encode())
    print(f"Sent data: {data_str.strip()}")

def read_arduino_response():
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Arduino: {response}")
        return response
    return None

try:
    while True:
        # Sample data
        dbmin = 41.234  # Example value for dbmin (float)
        dba = 42.567    # Example value for dba (float)
        dbmax = 43.890  # Example value for dbmax (float)
        arc = 5         # Example value for arc (integer)
        status = "medium"  # Example value for status (string: low, medium, high)

        # Send data to Arduino
        send_data(dbmin, dba, dbmax, arc, status)

        print(f"Sent dbmin: {dbmin:.3f}, dba: {dba:.3f}, dbmax: {dbmax:.3f}, arc: {arc}, status: {status}")

        # Wait for Arduino's response
        while True:
            response = read_arduino_response()
            if response and "Packet queued" in response:
                print("Data has been transmitted to LoRa")
                break

        time.sleep(10)  # Sending data every 10 seconds

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()
    print("Serial connection closed")
