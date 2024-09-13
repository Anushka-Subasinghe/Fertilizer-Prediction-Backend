import serial
import requests
import time
from npk_sensor import soil_factors2

# Configuration
serial_port = 'COM4'  # Replace with your serial port
baud_rate = 9600

# URLs for ThingsBoard and Flask backend
thingsboard_url = 'http://demo.thingsboard.io/api/v1/GtfPyFGvlki1NcjX88K3/telemetry'
backend_url = 'http://localhost:5000/serial_data'  # Flask backend URL

# Headers for ThingsBoard and Flask backend
headers = {'Content-Type': 'application/json'}

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate)

def send_data_to_thingsboard(temperature, humidity, soil_moisture, nitrogen, phosphorus, potassium):
    payload = {
        'temperature': temperature,
        'humidity': humidity,
        'soilMoisture': soil_moisture,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium
    }
    response = requests.post(thingsboard_url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Data sent to ThingsBoard successfully')
    else:
        print('Failed to send data to ThingsBoard:', response.text)

def send_serial_data_to_backend(temperature, humidity, soil_moisture):
    payload = {
        'temperature': temperature,
        'humidity': humidity,
        'soilMoisture': soil_moisture,
        'nitrogen': soil_factors2()['nitrogen'],
        'phosphorus': soil_factors2()['phosphorus'],
        'potassium': soil_factors2()['potassium']
    }
    response = requests.post(backend_url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Serial data sent to backend successfully')
    else:
        print('Failed to send serial data to backend:', response.text)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print('Received:', line)
        
        # Parse the received data
        try:
            parts = line.split(',')
            temperature = float(parts[0].split(':')[1])
            humidity = float(parts[1].split(':')[1])
            soil_moisture = int(parts[2].split(':')[1])
            nitrogen = soil_factors2()['nitrogen']
            phosphorus = soil_factors2()['phosphorus']
            potassium = soil_factors2()['potassium']

            # Send data to ThingsBoard
            send_data_to_thingsboard(temperature, humidity, soil_moisture, nitrogen, phosphorus, potassium)

            # Send the serial data to the Flask backend
            send_serial_data_to_backend(temperature, humidity, soil_moisture)
        except Exception as e:
            print('Error parsing data:', e)
        
    time.sleep(2)  # Adjust delay as needed
