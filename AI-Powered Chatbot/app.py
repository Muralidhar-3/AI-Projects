import cohere
import requests
from datetime import datetime
from flask import Flask, request, jsonify

# Replace with your actual API key
API_KEY = "Cpb1AJIaaXzmvYunK4HR8lM7P3urdwAQmNaYAMP9"
WEATHER_API_KEY = "f6bf5f4ae9064bf5b1f162620252701"

# Initialize Cohere client
co = cohere.Client(API_KEY)

app = Flask(__name__)

def get_weather(city):
    """Fetch current weather for a given city using WeatherAPI."""
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        feels_like = data["current"]["feelslike_c"]
        return (f"The current weather in {city} is {condition} with a temperature of {temp}°C. "
                f"It feels like {feels_like}°C.")
    else:
        return "Sorry, I couldn't fetch the weather information. Please check the city name or try again later."

def get_time_or_date(prompt):
    now = datetime.now()
    if "time" in prompt.lower():
        return f"The current time is {now.strftime('%H:%M %S')}."
    elif "date" in prompt.lower():
        return f"Today's date is {now.strftime('%Y-%m-%d')}."
    else:
        return None

def chat_with_cohere(prompt):
    if prompt.lower() in ["hello", "hi", "hey"]:
        return "Hello! How can I assist you today?"
    elif "time" in prompt.lower() or "date" in prompt.lower():
        return get_time_or_date(prompt)
    elif prompt.lower() in ["bye", "goodbye"]:
        return "Goodbye! Have a great day!"
    # Weather functionality
    elif "weather" in prompt.lower():
        # Extract city name (assumes "weather in [city]" format)
        if "weather in" in prompt.lower():
            city = prompt.lower().split("weather in")[-1].strip()
            return get_weather(city)
        else:
            return "Please specify the city to get the weather information."
    # elif "" in prompt.lower():
    #     return "Please enter a valid input."
    else:
      response = co.generate(
            model='command-xlarge-nightly',  # Choose the desired model
            prompt=prompt,
            max_tokens=300,  # Adjust response length
            temperature=0.7  # Adjust creativity
      )
      return response.generations[0].text.strip()



@app.route('/chat', methods=['POST'])

def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'response': 'Please provide a valid input.'})
    response = chat_with_cohere(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

# Export Flask app for Vercel
def handler(request, context):
    return app(request, context)