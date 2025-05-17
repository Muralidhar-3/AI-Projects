import cohere
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import os

# Replace with your actual API keys
COHERE_API_KEY = "Cpb1AJIaaXzmvYunK4HR8lM7P3urdwAQmNaYAMP9"
WEATHER_API_KEY = "f6bf5f4ae9064bf5b1f162620252701"

# Initialize Flask, Cohere client, and chat histories dictionary
app = Flask(__name__)
co = cohere.Client(COHERE_API_KEY)
chat_histories = {}

# Initialize embeddings and vector store
embeddings = CohereEmbeddings(
    cohere_api_key=COHERE_API_KEY,
    model="embed-english-v3.0"  # specify the model explicitly
)
vector_store = None

def initialize_vector_store():
    """Initialize FAISS vector store with knowledge base"""
    global vector_store
    
    # Create knowledge base directory if it doesn't exist
    if not os.path.exists('knowledge_base'):
        os.makedirs('knowledge_base')
        
    # Ensure weather knowledge base exists
    weather_kb_path = 'knowledge_base/weather_info.txt'
    if not os.path.exists(weather_kb_path):
        with open(weather_kb_path, 'w', encoding='utf-8') as f:
            f.write(weather_knowledge_base)  # You would need to define this content
    
    # Load and process documents
    documents = []
    for file in os.listdir('knowledge_base'):
        if file.endswith('.txt'):
            loader = TextLoader(f'knowledge_base/{file}', encoding='utf-8')
            documents.extend(loader.load())
    
    # Split documents into smaller chunks for better retrieval
    text_splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separator="\n"
    )
    texts = text_splitter.split_documents(documents)
    
    # Create vector store
    vector_store = FAISS.from_documents(texts, embeddings)
    return vector_store

def search_knowledge_base(query, k=2):
    """Search the vector store for relevant information"""
    if vector_store is None:
        return None
    
    docs = vector_store.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])

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
        return f"The current time is {now.strftime('%H:%M:%S')}."
    elif "date" in prompt.lower():
        return f"Today's date is {now.strftime('%Y-%m-%d')}."
    else:
        return None

def get_or_create_chat_history(session_id):
    """Get or create a new chat history for the session"""
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

def initialize_app():
    """Initialize the vector store"""
    global vector_store
    vector_store = initialize_vector_store()

# Call initialize_app during app startup
initialize_app()

def chat_with_cohere(prompt, session_id=None):
    """Generate a response using Cohere's API with memory and vector search."""
    if not prompt or prompt.strip() == "":
        return "Please provide a valid input. I'm here to help!"

    # Get or create chat history for this session
    if session_id:
        chat_history = get_or_create_chat_history(session_id)
    else:
        chat_history = ChatMessageHistory()

    # Handle weather-related queries with enhanced knowledge
    if "weather" in prompt.lower():
        if "weather in" in prompt.lower():
            # Get current weather data
            city = prompt.lower().split("weather in")[-1].strip()
            current_weather = get_weather(city)
            
            # Search knowledge base for relevant context
            relevant_info = search_knowledge_base(prompt)
            
            # If it's raining, add safety tips
            if "rain" in current_weather.lower():
                safety_context = search_knowledge_base("safety tips during heavy rain")
                return f"{current_weather}\n\nHelpful tips: {safety_context}"
            
            # If it's very hot or cold, add relevant information
            if "temperature" in current_weather.lower():
                temp_info = search_knowledge_base("temperature scales and effects")
                return f"{current_weather}\n\nAdditional Information: {temp_info}"
            
            return current_weather
        else:
            return "Please specify the city to get the weather information."
    
    # Handle specific weather-related questions
    elif any(term in prompt.lower() for term in ["humidity", "precipitation", "forecast", "climate", "storm", "thunder"]):
        relevant_info = search_knowledge_base(prompt)
        return f"Based on my knowledge: {relevant_info}"

    # Handle other queries as before
    elif "time" in prompt.lower() or "date" in prompt.lower():
        return get_time_or_date(prompt)
    elif prompt.lower() in ["hello", "hi", "hey"]:
        return "Hello! How can I assist you today?"
    elif prompt.lower() in ["bye", "goodbye"]:
        return "Goodbye! Have a great day!"
    else:
        # For general queries, include relevant knowledge base information
        relevant_info = search_knowledge_base(prompt)
        
        # Format chat history for Cohere
        cohere_chat_history = []
        for msg in chat_history.messages:
            if isinstance(msg, HumanMessage):
                cohere_chat_history.append({"role": "USER", "message": msg.content})
            elif isinstance(msg, AIMessage):
                cohere_chat_history.append({"role": "CHATBOT", "message": msg.content})

        # Generate response using Cohere with context
        response = co.chat(
            message=f"{prompt}\nContext: {relevant_info}",
            model='command',
            temperature=0.7,
            chat_history=cohere_chat_history
        ).text

    # Save the interaction to chat history
    if session_id:
        chat_history.add_user_message(prompt)
        chat_history.add_ai_message(response)

    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    session_id = request.json.get('session_id', None)
    response = chat_with_cohere(user_message, session_id)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
