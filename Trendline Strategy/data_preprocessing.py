import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('./trendlineTrades.csv')

features = ['SL', 'TrendlineMove']
target = 'MaxMove'

data = data[features +[target]].dropna()

X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)