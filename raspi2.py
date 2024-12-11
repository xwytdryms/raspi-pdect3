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

def map_status(status_str):
    # Map status string to corresponding integer value
    if status_str == "low":
        return 1
    elif status_str == "medium":
        return 2
    elif status_str == "high":
        return 3
    else:
        raise ValueError("Invalid status value. Use 'low', 'medium', or 'high'.")

def send_data(dbmin, dba, dbmax, arc, status_str):
    try:
        # Map status to integer value
        status = map_status(status_str)
        
        # Prepare the data string
        data_str = f"{dbmin:.2f} {dba:.2f} {dbmax:.2f} {arc} {status}\n"
        ser.write(data_str.encode())
        print(f"Sent data: {data_str.strip()}")
    except ValueError as e:
        print(f"Error: {e}")

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
        status_str = "high"  # "low", "medium", or "high"

        send_data(dbmin, dba, dbmax, arc, status_str)

        while True:
            response = read_arduino_response()
            if response and "Packet queued" in response:
                print("Data has been transmitted to LoRa")
                break

        time.sleep(10)  # Send data every 10 seconds

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()
    print("Serial connection closed")
