import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import joblib

# --- 1. Data Generation and Model Training (Run once to train the initial model) ---

def train_lead_predictor(data_path='lead_data.csv'):
    """
    Loads simulated lead data, trains a Logistic Regression model, 
    and saves the model to a file.
    """
    print("--- Training AI Model ---")
    try:
        # Load or generate data
        try:
            df = pd.read_csv(data_path)
            print(f"Loaded existing data from {data_path}")
        except FileNotFoundError:
            print("Generating simulated lead data...")
            # Simulate features that predict conversion (Target: 'Converted' = 1/0)
            data = {
                'Email_Opens': np.random.randint(0, 50, 500),
                'Website_Visits': np.random.randint(0, 30, 500),
                'Time_Spent_Sec': np.random.randint(5, 600, 500),
                'Demo_Requested': np.random.choice([0, 1], 500, p=[0.8, 0.2]),
                # Create a dependent target variable:
                'Converted': (
                    (np.random.rand(500) < 0.1) + # Baseline conversion
                    (np.random.rand(500) < (0.02 * np.random.randint(0, 50, 500))) + # Opens factor
                    (np.random.rand(500) < (0.05 * np.random.randint(0, 30, 500))) + # Visits factor
                    (np.random.choice([0, 1], 500, p=[0.9, 0.1]) * 0.5) # Demo factor
                ) > 0.5
            }
            df = pd.DataFrame(data).astype(int)
            df.to_csv(data_path, index=False)
            
        # Define features (X) and target (y)
        features = ['Email_Opens', 'Website_Visits', 'Time_Spent_Sec', 'Demo_Requested']
        X = df[features]
        y = df['Converted']

        # Split data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = LogisticRegression(solver='liblinear', random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

        # Save the trained model
        joblib.dump(model, 'lead_predictor_model.pkl')
        print("Model trained and saved successfully as 'lead_predictor_model.pkl'.")
        return features

    except Exception as e:
        print(f"An error occurred during training: {e}")
        return None


# --- 2. Prediction and Recommendation Function (Used by the Back-end API) ---

# Load the trained model globally when the script runs
try:
    LEAD_MODEL = joblib.load('lead_predictor_model.pkl')
    MODEL_FEATURES = ['Email_Opens', 'Website_Visits', 'Time_Spent_Sec', 'Demo_Requested']
    print("\nAI Model loaded successfully.")
except FileNotFoundError:
    print("\nAI Model not found. Running initial training...")
    MODEL_FEATURES = train_lead_predictor()
    if MODEL_FEATURES:
        LEAD_MODEL = joblib.load('lead_predictor_model.pkl')
    else:
        LEAD_MODEL = None


def categorize_and_recommend(lead_data: dict) -> dict:
    """
    Takes raw lead data, predicts conversion probability, categorizes, and suggests an action.
    
    Args:
        lead_data: A dictionary containing feature values for a single lead.
                   e.g., {'Email_Opens': 15, 'Website_Visits': 8, 'Time_Spent_Sec': 120, 'Demo_Requested': 0}
    
    Returns:
        A dictionary with prediction, category, and recommendation.
    """
    if LEAD_MODEL is None:
        return {"error": "Model failed to load or train. Cannot process request."}

    # 1. Prepare data for prediction (must be in the same order as training features)
    try:
        data_point = pd.DataFrame([lead_data], columns=MODEL_FEATURES)
    except KeyError as e:
        return {"error": f"Missing required lead feature: {e}. Required features: {MODEL_FEATURES}"}

    # 2. Predict Probability
    # probability[0][1] is the probability of the positive class (Converted=1)
    probability = LEAD_MODEL.predict_proba(data_point)[0][1]

    # 3. Categorize Lead
    if probability >= 0.75:
        category = "Hot Lead (High Conversion Likelihood)"
        recommendation = "Contact immediately via **Phone Call**. Send personalized case study."
    elif probability >= 0.50:
        category = "Warm Lead (Moderate Conversion Likelihood)"
        recommendation = "Send a follow-up email about a relevant feature. Schedule a **webinar invite**."
    elif probability >= 0.25:
        category = "Cool Lead (Low-Medium Likelihood)"
        recommendation = "Automate a **nurturing email sequence**. Monitor website activity closely."
    else:
        category = "Cold Lead (Low Likelihood)"
        recommendation = "Add to general **long-term newsletter**. No direct sales outreach yet."

    # 4. Return Result
    return {
        "conversion_probability": round(probability * 100, 2),
        "category": category,
        "recommendation": recommendation,
        "raw_data_processed": lead_data
    }


# --- Example Usage (How your back-end would call this function) ---

if __name__ == '__main__':
    # 1. If the model doesn't exist, it trains it.

    # 2. Example Lead Data coming from a CRM/Database
    lead_a = {'Email_Opens': 40, 'Website_Visits': 25, 'Time_Spent_Sec': 450, 'Demo_Requested': 1}
    lead_b = {'Email_Opens': 5, 'Website_Visits': 2, 'Time_Spent_Sec': 60, 'Demo_Requested': 0}
    lead_c = {'Email_Opens': 20, 'Website_Visits': 10, 'Time_Spent_Sec': 200, 'Demo_Requested': 0}

    print("\n--- Processing Lead A ---")
    result_a = categorize_and_recommend(lead_a)
    print(f"Result: {result_a}")

    print("\n--- Processing Lead B ---")
    result_b = categorize_and_recommend(lead_b)
    print(f"Result: {result_b}")
