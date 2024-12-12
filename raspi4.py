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
    """
    Sends formatted data to Arduino via serial.
    """
    data_str = f"{dbmin:.2f} {dba:.2f} {dbmax:.2f} {arc:.2f} {status}\n"
    ser.write(data_str.encode())
    print(f"Sent data: {data_str.strip()}")

def read_arduino_response():
    """
    Reads and returns the response from Arduino, if available.
    """
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Arduino: {response}")
        return response
    return None

try:
    while True:
        # Example input values
        dbmin = 4.51
        dba = 15.67
        dbmax = 36.68
        arc = 2.00
        status = "high"  # Status can be "low", "medium", or "high"

        # Send data to Arduino
        send_data(dbmin, dba, dbmax, arc, status)

        # Wait for Arduino to confirm transmission
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
