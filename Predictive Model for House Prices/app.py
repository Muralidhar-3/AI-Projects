from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('house_price_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Parse input JSON
    data = request.json
    df = pd.DataFrame([data])
    prediction = model.predict(df)

    # Convert the prediction to a Python float
    predicted_price = float(prediction[0])

    return jsonify({'predicted_price': predicted_price})

if __name__ == '__main__':
    app.run(debug=True)
