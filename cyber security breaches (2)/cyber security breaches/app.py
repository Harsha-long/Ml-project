import streamlit as st
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the trained model and label encoders
model = joblib.load('random_forest_model.h5')
label_encoders = joblib.load('label_encoders.pkl')
target_le = joblib.load('target_label_encoder.pkl')

# Define the feature names
features = ['Source Port', 'Destination Port', 'Protocol', 'Packet Length', 
            'Packet Type', 'Traffic Type', 'Action Taken', 'Severity Level', 'Log Source']

# Function to encode user inputs using the label encoders
def encode_input(input_data):
    encoded_data = []
    for i, feature in enumerate(features):
        if feature in label_encoders:
            encoded_data.append(label_encoders[feature].transform([input_data[i]])[0])
        else:
            encoded_data.append(input_data[i])
    return encoded_data

# Streamlit app
st.title("Cyber Attack Prediction")

# Create input fields for each feature
input_data = []
for feature in features:
    input_value = st.text_input(f"Enter {feature}:")
    input_data.append(input_value)

# Predict button
if st.button("Predict"):
    if all(input_data):
        # Encode the inputs
        encoded_input = encode_input(input_data)
        
        # Make a prediction
        prediction = model.predict([encoded_input])[0]
        
        # Decode the prediction
        attack_type = target_le.inverse_transform([prediction])[0]
        
        # Display the prediction
        st.write(f"Predicted Attack Type: {attack_type}")
    else:
        st.write("Please enter values for all features.")
