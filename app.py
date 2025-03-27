import os
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from google.api_core.exceptions import ResourceExhausted

# Set your Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    personality = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    parameters = db.Column(db.Text, nullable=True)
    emotional_states = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database inside the application context
with app.app_context():
    db.create_all()

def call_llm_with_retry(prompt, retries=3, delay=10):
    """ Calls LLM with retries if rate limit is hit. """
    for attempt in range(retries):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0.5,
                google_api_key=api_key
            )
            response = llm.invoke(prompt)
            return response
        except ResourceExhausted as e:
            print(f"Quota exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)  # Wait before retrying
    return None  # Return None if it keeps failing

def extract_characters(text):
    prompt = (
        "Extract all characters from the following book text. "
        "Return the result as a valid JSON array of objects. "
        "Each object must have the keys 'name' and 'personality'.\n\n"
        "Text:\n" + text
    )

    response = call_llm_with_retry(prompt)
    
    if response is None:
        return None, "LLM service unavailable due to rate limits."

    if isinstance(response, AIMessage):
        response_text = response.content
    else:
        response_text = str(response)

    if not response_text or response_text.strip() == "":
        return None, "LLM returned an empty response"

    if response_text.startswith("```json"):
        response_text = response_text.strip("```json").strip()

    try:
        characters = json.loads(response_text)
        return characters, None
    except json.JSONDecodeError:
        return None, "Invalid JSON format from LLM"

@app.route('/upload', methods=['POST'])
def upload():
    username = request.form.get('username')

    # Check if the user exists or create a new user
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    # Check if a file is uploaded or text is provided
    text = None
    if 'file' in request.files:
        file = request.files['file']
        text = file.read().decode('utf-8')
    elif 'text' in request.form:
        text = request.form.get('text', '').strip()

    # *User exists and no file or text is provided → Fetch existing data**
    if user and not text:
        characters = Character.query.filter_by(user_id=user.id).all()
        conversations = Conversation.query.filter_by(user_id=user.id).all()

        character_data = [{"id": char.id, "name": char.name, "personality": char.personality} for char in characters]
        conversation_data = [{
            "character_id": conv.character_id,
            "user_message": conv.user_message,
            "bot_response": conv.bot_response
        } for conv in conversations]

        return jsonify({
            "characters": character_data,
            "conversation_history": conversation_data,
            "userId": user.id
        })

    # A file or text is provided → Extract new characters**
    characters_extracted, error = extract_characters(text)
    if error:
        return jsonify({"error": error}), 500

    # Save extracted characters if they don’t exist
    new_characters = []
    for char in characters_extracted:
        existing_char = Character.query.filter_by(user_id=user.id, name=char.get('name', 'Unknown')).first()
        if not existing_char:
            new_character = Character(
                user_id=user.id,
                name=char.get('name', 'Unknown'),
                personality=char.get('personality', '')
            )
            db.session.add(new_character)
            db.session.commit()  # Commit immediately to get the ID
            new_characters.append({
                "id": new_character.id,
                "name": new_character.name,
                "personality": new_character.personality
            })

    return jsonify({
        "characters": new_characters,  # Return only new characters
        "conversation_history": [],  # Empty conversation history
        "userId": user.id
    })

def generate_response(character, personality, user_message, conversation_history, username):
    # Create a string version of the conversation history.
    # Each message is formatted with the sender's name and content.
    history_str = "\n".join([
        f"{msg.role}: {msg.content}" for msg in conversation_history
    ])
    
    psi_prompt = (
        "Dorner's Psi Theory\n"
        "Psi Theory Parameters (1 to 7 scale):\n"
        "1. Valence Level: Measures the spectrum of attraction (appetence) vs. aversion; corresponds to positive vs. negative reinforcement.\n"
        "2. Arousal Level: Reflects the agent's readiness for action, similar to the function of the ascending reticular formation in humans.\n"
        "3. Selection Threshold: Indicates how easily the agent shifts between different intentions or balances multiple goals; reflects the dynamics of motive dominance. A higher selection threshold means the agent shifts less easily.\n"
        "4. Resolution Level: Describes the agent's accuracy in perceiving the world, ranging from detailed cognition to rapid perception.\n"
        "5. Goal-Directedness: Represents the stability of the agent's motives; indicates how strongly the agent prioritizes its goals versus adapting or 'going with the flow.'\n"
        "6. Securing Rate: Refers to the frequency with which the agent checks its environment; involves reflective and orientation behaviors.\n\n"
        "Sample of Five Emotions (1 to 7 scale) According to Psi Theory:\n"
        "1. Anger: Arises when an obstacle (often another agent) clearly prevents the achievement of a relevant goal.\n"
        "2. Sadness: Occurs when all perceived paths to achieving active, relevant goals are blocked, without a specific obstacle.\n"
        "3. Pride: Emerges from a perceived high level of self-competence and internal legitimacy.\n"
        "4. Joy: Characterized by a strong reward signal from fulfilling a demand.\n"
        "5. Bliss: Defined by a high perceived reward signal from fulfilling a demand, generally associated with higher-order cognitive demands.\n"
    )
    
    prompt = (
        psi_prompt +
        "\n\nTask: Generate a response for a chatbot character based on the provided personality and user message. The response should reflect the character's personality traits and emotional states as described in the Psi Theory.\n"
        f"Character Personality: {personality}\n"
        f"Users name: {username}\n"
        f"User Message: {user_message}\n"
        f"Conversation History:\n{history_str}\n\n"
        "Output Format: Return only a JSON object with the following keys:\n"
        "- bot_response: The chatbot's reply to the user message. just write the response, no need to add character says:\n"
        "- parameters: A dictionary of Psi Theory parameters relevant to the response, each ranging from 1 to 7.\n"
        "- emotional_states: A dictionary of emotional states influenced by the conversation, each ranging from 1 to 7.\n"
        "Ensure the JSON object is the only content returned."
    )
    
    response = call_llm_with_retry(prompt)
    
    if response is None:
        return "I'm currently unavailable due to service limits.", {}, {}
    
    # Check and extract the response from the LLM
    if isinstance(response, AIMessage):
        response_text = response.content
    else:
        response_text = str(response)
    
    if not response_text or response_text.strip() == "":
        return "Sorry, I couldn't process your message.", {}, {}
    
    if response_text.startswith("```json"):
        response_text = response_text.strip("```json").strip()
    
    try:
        result = json.loads(response_text)
        bot_response = result.get("bot_response", "")
        parameters = result.get("parameters", {})
        emotional_states = result.get("emotional_states", {})
    except json.JSONDecodeError as e:
        bot_response = f"I received your message but I am busy now, please try again later."
        parameters = {
            "valence": 4,
            "arousal": 4,
            "selection_threshold": 4,
            "resolution_level": 4,
            "goal_directedness": 4,
            "securing_rate": 4
        }
        emotional_states = {
            "anger": 1,
            "sadness": 1,
            "pride": 1,
            "joy": 4,
            "bliss": 1
        }
    
    return bot_response, parameters, emotional_states

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('userId')
    character_name = data.get('character')  # Character name from frontend
    user_message = data.get('message')

    # Find the character based on the name and user ID
    character = Character.query.filter_by(name=character_name, user_id=user_id).first()
    if not character:
        return jsonify({"error": "Character not found."}), 404

    character_id = character.id  # Get the actual ID of the character

    # Retrieve chat history (last 20 messages)
    chat_history = ChatMessageHistory()
    history_records = (
        Conversation.query
        .filter_by(user_id=user_id, character_id=character_id)
        .order_by(Conversation.timestamp.desc())
        .limit(20)
        .all()
    )

    for record in reversed(history_records):
        chat_history.add_ai_message(record.bot_response)
        chat_history.add_user_message(record.user_message)

    # Get the username
    user = User.query.get(user_id)
    username = user.username if user else "Unknown"

    # Generate AI response
    bot_response, parameters, emotional_states = generate_response(
        character, character.personality, user_message, chat_history.messages, username
    )

    # Save new conversation record
    new_conversation = Conversation(
        user_id=user_id,
        character_id=character_id,
        user_message=user_message,
        bot_response=bot_response,
        parameters=json.dumps(parameters),
        emotional_states=json.dumps(emotional_states)
    )
    db.session.add(new_conversation)
    db.session.commit()

    chat_history.add_user_message(user_message)
    chat_history.add_ai_message(bot_response)

    return jsonify({
        "response": bot_response,
        "parameters": parameters,
        "emotional_states": emotional_states
    })

if __name__ == '__main__':
    app.run(debug=True)