import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { CharacterContext } from "../contexts/CharacterContext";
import "../App.css";

const Home = () => {
  const { setCharacters, setUserId, setChatHistory } =
    useContext(CharacterContext);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");

  const handleUpload = async (e, isContinuing = false) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append("username", username);

    if (!isContinuing) {
      const fileInput = document.getElementById("uploadFile");
      if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
      } else {
        const text = document.getElementById("textInput").value.trim();
        if (text) {
          formData.append("text", text);
        }
      }
    }

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);

      if (res.data.userId) {
        setCharacters(res.data.characters);
        setUserId(res.data.userId);

        // Organize chat history by character ID
        const structuredChatHistory = res.data.conversation_history.reduce(
          (acc, chat) => {
            if (!acc[chat.character_id]) {
              acc[chat.character_id] = [];
            }
            acc[chat.character_id].push({
              user: chat.user_message,
              bot: chat.bot_response,
            });
            return acc;
          },
          {}
        );

        setChatHistory(structuredChatHistory);
        navigate("/chat-bot");
      } else {
        alert("No characters found. Try another text!");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to fetch data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <h1>Interactive Character Chat</h1>
      <form onSubmit={handleUpload}>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
        />
        <br />
        <textarea
          id="textInput"
          placeholder="Paste text here..."
          rows="5"
          cols="50"
          disabled={loading}
        ></textarea>
        <br />
        <input
          type="file"
          id="uploadFile"
          accept=".txt,.pdf"
          disabled={loading}
        />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Upload & Extract Characters"}
        </button>
      </form>
      <br />
      <button onClick={(e) => handleUpload(e, true)} disabled={loading}>
        {loading ? "Loading..." : "Continue Previous Conversation"}
      </button>
    </div>
  );
};

export default Home;
