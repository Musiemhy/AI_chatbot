import React from "react";

const ParameterDisplay = ({ parameters, emotionalStates }) => {
  return (
    <div className="parameter-display">
      <div className="param psychological-parameters">
        <h3>Psychological Parameters</h3>
        <ul>
          {Object.keys(parameters).map((key, idx) => (
            <li key={idx}>
              {key}: {parameters[key]}
            </li>
          ))}
        </ul>
      </div>
      <div className="param emotional-states">
        <h3>Emotional States</h3>
        <ul>
          {Object.keys(emotionalStates).map((key, idx) => (
            <li key={idx}>
              {key}: {emotionalStates[key]}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ParameterDisplay;
