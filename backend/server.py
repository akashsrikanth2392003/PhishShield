from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all requests

# Load model and vectorizer
MODEL_PATH = r'C:\Users\akash\Downloads\MakeUC2024-NewMain\model.joblib'
VECTORIZER_PATH = r'C:\Users\akash\Downloads\MakeUC2024-NewMain\vectorizer.joblib'

try:
    vectorizer = joblib.load('vectorizer.joblib')
    model = joblib.load('logistic_regression_model.joblib')  # Ensure correct model is loaded
    
    # Debug: Print feature count
    print(f"Vectorizer feature size: {len(vectorizer.get_feature_names_out())}")
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")


def log_prediction(email_text, is_phishing): 
    """Logs email predictions with timestamps."""
    with open("predictions.log", "a", encoding="utf-8") as log_file:
        log_entry = f"{datetime.now()} | Email: {email_text[:50]}... | Is Phishing: {is_phishing}\n"
        log_file.write(log_entry)

@app.route('/predict', methods=['POST'])
def predict():
    """Handles phishing email predictions."""
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model or vectorizer not loaded'}), 500

    try:
        print("Received request with headers:", request.headers)
        print("Received request raw data:", request.data)  # Debugging line
        print("Received request JSON:", request.json)  # Debugging line
        
        if not request.is_json:
            return jsonify({'error': 'Invalid content type, expected application/json'}), 400

        email_text = request.json.get('email_text', '')

        if not email_text:
            return jsonify({'error': 'No email text provided'}), 400

        # Transform email text and predict
        transformed_text = vectorizer.transform([email_text])
        prediction = model.predict(transformed_text)
        is_phishing = bool(prediction[0])

        log_prediction(email_text, is_phishing)

        return jsonify({'is_phishing': is_phishing})
    
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': 'Server error occurred'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Running on port 5001
