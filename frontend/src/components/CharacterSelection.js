import React from "react";

const CharacterSelection = ({ characters, onSelect }) => {
  return (
    <div className="character-selection">
      <h2>Select a Character to Chat With:</h2>
      {characters.length === 0 ? (
        <p>No characters extracted yet.</p>
      ) : (
        <form>
          {characters.map((char, index) => (
            <div key={index}>
              <input
                type="radio"
                id={`character-${index}`}
                name="character"
                value={char.name}
                onChange={() => onSelect(char)}
              />
              <label htmlFor={`character-${index}`}>
                {char.name} - {char.personality}
              </label>
            </div>
          ))}
        </form>
      )}
    </div>
  );
};

export default CharacterSelection;
