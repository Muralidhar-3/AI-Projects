import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Load dataset
df = pd.read_csv("./data/country_wise_latest.csv")
df.head()

# Check for missing values
print(df.isnull().sum())

# Fill or drop missing values
df.fillna(0, inplace=True)  # Example

print(df.describe())
print(df.info())

sns.lineplot(data=df, x="Confirmed last week", y="Confirmed")
plt.show()

fig = px.line(df, x="Confirmed last week", y="Confirmed", title="Cases Over Time")
fig.show()

# Drop rows with missing values in relevant columns
df = df.dropna(subset=["Confirmed", "Confirmed last week"])

# Convert Date to datetime format if it's not already
# df['Date'] = pd.to_datetime(df['Date'])


app = Dash(__name__)

# Example figure
fig = px.line(df, x="Confirmed last week", y="Confirmed", title="Cases Over Time")

app.layout = html.Div([
    html.H1("Interactive Dashboard"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Confirmed', 'value': 'Confirmed'},
            {'label': 'Deaths', 'value': 'Deaths'}
        ],
        value='Confirmed'
    ),
    dcc.Graph(id='line-graph')
])

@app.callback(
    Output('line-graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_metric):
    return px.line(df, x="Confirmed last week", y=selected_metric, title=f"{selected_metric} Over Time")


if __name__ == '__main__':
    app.run_server(debug=True)