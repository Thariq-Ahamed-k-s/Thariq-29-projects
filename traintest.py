from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Step 1: Dataset
texts = [
    "Hi", "Hello", "Hey", "Good morning", "Good evening",
    "Bye", "Goodbye", "See you later", "Catch you later",
    "How are you?", "What's up?", "How's it going?",
    "Thank you", "Thanks", "Much appreciated",
    "What’s the weather like?", "Tell me the weather", "Is it going to rain?",
    "Tell me a joke", "Make me laugh", "Say something funny",
    "What’s your name?", "Who are you?", "Can you tell me your name?"
]

labels = [
    "greeting", "greeting", "greeting", "greeting", "greeting",
    "farewell", "farewell", "farewell", "farewell",
    "question", "question", "question",
    "thanks", "thanks", "thanks",
    "weather", "weather", "weather",
    "joke", "joke", "joke",
    "name", "name", "name"
]

# Step 2: Vectorization and model training
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = DecisionTreeClassifier()
model.fit(X, labels)

# Step 3: Predefined responses
responses = {
    "greeting": "Hello! How can I help you?",
    "farewell": "Goodbye! Have a nice day!",
    "question": "I'm just a simple chatbot, but I'm doing fine. How about you?",
    "thanks": "You're welcome!",
    "weather": "I can't check the weather yet, but it's always a good day to chat with me!",
    "joke": "Why don’t scientists trust atoms? Because they make up everything! 😂",
    "name": "I am ChatBot 1.0, your virtual assistant!"
}

# Step 4: Flask route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({"response": "Please provide a message."})

    user_vector = vectorizer.transform([user_input])
    predicted_intent = model.predict(user_vector)[0]

    bot_response = responses.get(predicted_intent, "Sorry, I don't understand.")

    return jsonify({
        "user_input": user_input,
        "predicted_intent": predicted_intent,  
        "bot_response": bot_response
    })

# Step 5: Run the server
if __name__ == '__main__':
    print("✅ Model trained successfully!")
    print("🚀 Flask chatbot is running on http://127.0.0.1:5000/chat")
    app.run(debug=True)
