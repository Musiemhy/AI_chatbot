import { createContext, useState } from "react";

export const CharacterContext = createContext();

export const CharacterProvider = ({ children }) => {
  const [characters, setCharacters] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [userId, setUserId] = useState();
  const [loading, setLoading] = useState(false);

  return (
    <CharacterContext.Provider
      value={{
        characters,
        setCharacters,
        userId,
        setUserId,
        loading,
        setLoading,
        chatHistory,
        setChatHistory,
      }}
    >
      {children}
    </CharacterContext.Provider>
  );
};
