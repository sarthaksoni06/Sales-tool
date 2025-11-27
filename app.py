from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import categorize_and_recommend

# Note: You must install Flask and flask-cors: pip install Flask Flask-CORS

app = Flask(__name__)
# Enable CORS to allow your local frontend (index.html) to call this API
CORS(app) 

@app.route('/predict_lead', methods=['POST'])
def predict_lead():
    """
    API endpoint to receive lead data and return AI prediction.
    """
    try:
        # Get JSON data sent from the frontend
        data = request.get_json()
        
        # Validate that the necessary keys exist (matching the AI engine features)
        required_keys = ['Email_Opens', 'Website_Visits', 'Time_Spent_Sec', 'Demo_Requested']
        if not all(key in data for key in required_keys):
            return jsonify({"error": "Missing required lead features in request data."}), 400

        # Convert keys to integers, as expected by the AI engine
        lead_data_int = {k: int(v) for k, v in data.items()}
        
        # Call the core AI prediction function
        prediction_result = categorize_and_recommend(lead_data_int)
        
        if "error" in prediction_result:
            return jsonify(prediction_result), 500

        # Return the AI's result to the frontend
        return jsonify({
            "success": True,
            "prediction": prediction_result
        })

    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Ensure you have run ai_engine.py once to create the model file
    print("Starting Flask API. Ensure 'lead_predictor_model.pkl' exists.")
    app.run(debug=True, port=5000)
