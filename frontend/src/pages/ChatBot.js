import React, { useState, useContext, useEffect } from "react";
import axios from "axios";
import CharacterSelection from "../components/CharacterSelection";
import ChatWindow from "../components/ChatWindow";
import ParameterDisplay from "../components/ParameterDisplay";
import { CharacterContext } from "../contexts/CharacterContext";
import { useNavigate } from "react-router-dom";
import "../App.css";

const ChatBot = () => {
  const {
    characters,
    userId,
    loading,
    setLoading,
    chatHistory,
    setChatHistory,
  } = useContext(CharacterContext);

  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [parameters, setParameters] = useState({});
  const [emotionalStates, setEmotionalStates] = useState({});
  const navigate = useNavigate();

  const handleCharacterSelect = (character) => {
    setSelectedCharacter(character);

    setChatHistory(chatHistory[character.id] || []);

    setParameters({});
    setEmotionalStates({});
  };

  const sendMessage = async (message) => {
    if (!selectedCharacter) {
      alert("Please select a character before sending a message.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/chat", {
        userId: userId,
        character: selectedCharacter.name,
        message: message,
      });

      const newMessage = { user: message, bot: res.data.response };

      setChatHistory((prevHistory) => ({
        ...prevHistory,
        [selectedCharacter.id]: [
          ...(prevHistory[selectedCharacter.id] || []),
          newMessage,
        ],
      }));

      setParameters(res.data.parameters);
      setEmotionalStates(res.data.emotional_states);
    } catch (error) {
      console.error("Error sending message:", error);
      alert("Failed to send message. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (characters.length === 0) {
    return (
      <div className="chatbot">
        <div className="no-characters">
          <p>
            No characters available. Please upload a text to extract characters.
          </p>
          <button onClick={() => navigate("/")}>Go Back to Home</button>
        </div>
      </div>
    );
  }

  return (
    <div className="chatbot">
      <CharacterSelection
        characters={characters}
        onSelect={handleCharacterSelect}
        disabled={loading}
      />
      <ChatWindow
        chatHistory={chatHistory[selectedCharacter?.id] || []}
        setChatHistory={setChatHistory}
        sendMessage={sendMessage}
      />
      <ParameterDisplay
        parameters={parameters}
        emotionalStates={emotionalStates}
      />
    </div>
  );
};

export default ChatBot;
