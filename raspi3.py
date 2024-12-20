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
    # Scale the float values to integers
    dbmin_scaled = int(dbmin * 1000)  # Scale by 1000 to preserve three decimal places
    dba_scaled = int(dba * 1000)
    dbmax_scaled = int(dbmax * 1000)

    # Format the data as a string with space-separated values
    data_str = f"{dbmin_scaled} {dba_scaled} {dbmax_scaled} {arc} {status}\n"
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
        # Example data
        dbmin = 41.234  # Original float value
        dba = 42.567    # Original float value
        dbmax = 43.890  # Original float value
        arc = 5         # Integer
        status = "medium"  # Status string ("low", "medium", "high")

        # Send scaled data to Arduino
        send_data(dbmin, dba, dbmax, arc, status)

        print(f"Sent dbmin: {dbmin}, dba: {dba}, dbmax: {dbmax}, arc: {arc}, status: {status}")

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
