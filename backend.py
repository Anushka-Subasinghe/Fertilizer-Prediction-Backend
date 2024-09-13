from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the saved model and LabelEncoders
clf = joblib.load('fertilizer_model.joblib')
le_soil = joblib.load('soil_label_encoder.joblib')
le_crop = joblib.load('crop_label_encoder.joblib')
le_fertilizer = joblib.load('fertilizer_label_encoder.joblib')

# Global variable to store the latest received serial data
serial_data_store = {}

@app.route('/serial_data', methods=['POST'])
def receive_serial_data():
    global serial_data_store
    # Receive data from the serial device
    serial_data = request.json
    print('Serial Data received:', serial_data)
    
    # Store the received serial data in the global variable
    serial_data_store = serial_data
    
    return jsonify({'message': 'Serial Data received successfully!'}), 200

@app.route('/predict', methods=['POST'])
def predict_fertilizer():
    global serial_data_store

    # Check if serial data is available
    if not serial_data_store:
        return jsonify({'error': 'No serial data available. Please send serial data first.'}), 400
    
    # Get the JSON data from the frontend
    input_data = request.json
    
    # Extract crop type and soil type from input data
    crop_type = input_data.get('Crop Type')
    soil_type = input_data.get('Soil Type')
    
    # Extract other features from the latest serial data
    temperature = serial_data_store.get('temperature')
    humidity = serial_data_store.get('humidity')
    moisture = serial_data_store.get('soilMoisture')
    nitrogen = serial_data_store.get('nitrogen')
    phosphorus = serial_data_store.get('phosphorus')
    potassium = serial_data_store.get('potassium')

    # Ensure that the input categorical features are mapped correctly
    if soil_type not in le_soil.classes_ or crop_type not in le_crop.classes_:
        return jsonify({'error': 'Invalid Soil Type or Crop Type'}), 400
    
    # Encode categorical features
    soil_type_encoded = le_soil.transform([soil_type])[0]
    crop_type_encoded = le_crop.transform([crop_type])[0]

    # Prepare the input data for the model
    model_input = np.array([[temperature, humidity, moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorus]])

    # Get the prediction from the model
    prediction = clf.predict(model_input)

    # Decode the fertilizer name
    fertilizer_name = le_fertilizer.inverse_transform([prediction[0]])[0]

    # Send the prediction back to the frontend
    return jsonify({'Recommended Fertilizer': fertilizer_name}), 200

if __name__ == '__main__':
    app.run(debug=True)
