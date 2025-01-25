from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('trendline_move.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/maxMove', methods=['POST'])
def maxMove():
    # Parse input JSON
    data = request.json
    df = pd.DataFrame([data])
    try:
        maxMove = model.predict(df)  # Predict using the model
        return jsonify({'max_move': maxMove.tolist()[0]})  # Convert NumPy array to list
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)