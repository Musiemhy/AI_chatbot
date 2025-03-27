import React, { useState, useContext } from "react";
import { CharacterContext } from "../contexts/CharacterContext";

const ChatWindow = ({ chatHistory, sendMessage }) => {
  const [message, setMessage] = useState("");
  const { loading } = useContext(CharacterContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim()) {
      const userMessage = message;
      setMessage("");
      await sendMessage(userMessage);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-content">
        {chatHistory.length === 0 && (
          <div className="no-messages">
            No messages yet. Start the conversation!
          </div>
        )}
        {chatHistory.map((chat, idx) => (
          <div key={idx} className="chat-message">
            {chat.user && (
              <div className="message-bubble user-message">{chat.user}</div>
            )}
            {chat.bot && (
              <div className="message-bubble bot-message">
                {loading ? "loading..." : chat.bot}
              </div>
            )}
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
