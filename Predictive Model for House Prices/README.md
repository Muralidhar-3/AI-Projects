# House Price Predictor

This project predicts house prices using a linear regression model. It includes:
- Data preprocessing using Pandas.
- Model training with Scikit-learn.
- A Flask API for serving predictions.

## How to Run
1. Install dependencies: `pip install pandas numpy scikit-learn flask`.
2. Run `data_preprocessing.py` to preprocess data.
3. Train the model with `model_training.py`.
4. Start the Flask API: `python app.py`.
5. Send POST requests to `/predict` with house features to get predictions.

## Example Request
```bash
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{"OverallQual": 7, "GrLivArea": 1500, "GarageCars": 2, "TotalBsmtSF": 1000, "FullBath": 2, "YearBuilt": 2005}'
