import React, { useState, useContext } from "react";
import { CharacterContext } from "../contexts/CharacterContext";

const ChatWindow = ({ chatHistory, setChatHistory, sendMessage }) => {
  const [message, setMessage] = useState("");
  const { loading } = useContext(CharacterContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim()) {
      const userMessage = message;
      setMessage("");
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { user: userMessage, bot: "loading..." },
      ]);
      await sendMessage(userMessage);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-content">
        {chatHistory.map((chat, idx) => (
          <div key={idx} className="chat-message">
            <div className="message-bubble user-message">{chat.user}</div>
            <div className="message-bubble bot-message">{chat.bot}</div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;
