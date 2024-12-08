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
    # Prepare the data string
    data_str = f"{dbmin:.2f} {dba:.2f} {dbmax:.2f} {arc:.2f} {status}\n"
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
        dbmin = 50.00
        dba = 45.50
        dbmax = 60.00
        arc = 20.00
        status = "medium"  # Can be "low", "medium", or "high"

        send_data(dbmin, dba, dbmax, arc, status)

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
