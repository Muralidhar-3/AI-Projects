import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle

X_train = pd.read_csv('X_train.csv')
y_train = pd.read_csv('y_train.csv')
X_test = pd.read_csv('X_test.csv')
y_test = pd.read_csv('y_test.csv')

model = LinearRegression()
model.fit(X_train, y_train)

maxMove = model.predict(X_test)
rmse = np.sqrt(np.mean((y_test-maxMove) ** 2))
r2 = r2_score(y_test, maxMove)

print(f"RMSE: {rmse}")
print(f"R²: {r2}")

# Save the trained model
with open('trendline_move.pkl', 'wb') as f:
    pickle.dump(model, f)