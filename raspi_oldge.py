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

def send_data(voltageS, frequency):
    data_str = f"{voltage:.2f} {frequency:.2f}\n"
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
        high_voltage = 300.00
        high_frequency = 100.00

        send_data(high_voltage, high_frequency)

        print(f"Sent voltage: {high_voltage:.2f} kV, frequency: {high_frequency:.2f} Hz")

        while True:
            response = read_arduino_response()
            if response and "Packet queued" in response:
                print("Data has been transmitted to LoRa")
                break

        time.sleep(0)  # Sending data every 10 seconds

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    ser.close()
    print("Serial connection closed")