import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import  r2_score
import pickle

# Load preprocessed data
X_train = pd.read_csv('./X_train.csv')
y_train = pd.read_csv('./y_train.csv')
X_test = pd.read_csv('./X_test.csv')
y_test = pd.read_csv('./y_test.csv')

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
rmse = np.sqrt(np.mean((y_test-predictions) ** 2))
r2 = r2_score(y_test, predictions)

print(f"RMSE: {rmse}")
print(f"R²: {r2}")

# Save the trained model
with open('house_price_model.pkl', 'wb') as f:
    pickle.dump(model, f)