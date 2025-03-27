# AI_chatbot

This is a training task at iCog Labs on creating an AI chatbot system that enables users to extract characters from history or fiction books and engage in conversations with them.

## Table of Contents

1. [System Setup and Installation](#system-setup-and-installation)
2. [User Guide for Interacting with the Chatbot and UI](#user-guide-for-interacting-with-the-chatbot-and-ui)
3. [Explanation of the Emotional Model and Long-term Memory Implementation](#explanation-of-the-emotional-model-and-long-term-memory-implementation)

---

## System Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Node.js and npm

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Musiemhy/AI_chatbot.git
   cd AI_chatbot
   ```

2. **Install Backend Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**

   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

4. **Install Frontend Dependencies**

   ```bash
   cd frontend
   npm install
   ```

5. **Run the Application**

   **Backend**

   ```bash
   flask run --debug
   ```

   **Frontend**

   ```bash
   cd frontend
   npm start
   ```

## User Guide for Interacting with the Chatbot and UI

### Starting the Chatbot

- Launch the backend using the command `flask run --debug`.
- Launch the frontend using `npm start` after `cd frontend`. The chatbot interface will open in your default web browser.

### Interacting with the Chatbot

1. **Username Input**: Type a username that the system can identify you with in the input box.
2. **Upload Story or Provide Text**:
   - **File Input**: Upload a text or PDF story in the file upload section.
   - **Text Input**: Manually type a story in the input box.
3. **Click Upload**: The system will extract characters from the provided story.
4. **Character Selection**: Choose a character from the extracted list.
5. **Chat Interaction**:
   - Type a message in the input field and send it.
   - View responses along with emotional and psychological parameters based on Psi Theory.
6. **Conversation History**: The system retains past conversations and emotional states for contextual replies.

### Features

- **Character Extraction**: Extracts characters from books and assigns personality traits.
- **Chat History Retention**: Stores previous interactions for better contextual responses.
- **Emotion and Personality Simulation**: Implements Dorner’s Psi Theory to simulate emotions and decision-making processes.
- **Retry Mechanism**: Handles API rate limits to ensure smooth interaction with the Google Gemini LLM.

## Explanation of the Emotional Model and Long-term Memory Implementation

### Emotional Model

- The chatbot employs Dorner’s Psi Theory, using a range of psychological parameters to generate responses.
- Emotional states such as **anger, sadness, pride, joy, and bliss** are determined dynamically based on conversation context.
- Psychological parameters (on a scale of 1 to 7) influence chatbot responses:
  1. **Valence Level**: Measures attraction vs. aversion.
  2. **Arousal Level**: Readiness for action.
  3. **Selection Threshold**: Determines how easily the chatbot shifts focus.
  4. **Resolution Level**: Precision of perception and cognitive detail.
  5. **Goal-Directedness**: Stability of motives vs. flexibility.
  6. **Securing Rate**: Frequency of environmental checks.

### Long-term Memory

- Stores interactions in a database to maintain continuity across sessions.
- Users' previous conversations and emotional states are retrieved for personalized responses.
- Memory is stored per user and character, enabling immersive and consistent interactions.

### Backend API Endpoints

1. **Upload Story & Extract Characters**: `/upload` (POST)
2. **Initiate Chat & Get Response**: `/chat` (POST)
