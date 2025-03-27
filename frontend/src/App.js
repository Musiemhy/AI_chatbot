import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ChatBot from "./pages/ChatBot";
import { CharacterProvider } from "./contexts/CharacterContext";
import "./App.js";

function App() {
  return (
    <CharacterProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat-bot" element={<ChatBot />} />
        </Routes>
      </Router>
    </CharacterProvider>
  );
}

export default App;
