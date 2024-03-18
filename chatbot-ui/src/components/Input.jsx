import React, { useState } from "react";

export default function Input({ onSend }) {
  const [text, setText] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleInputChange = (e) => {
    setText(e.target.value);
  };

  const handleSend = async (e) => {
    e.preventDefault();

    if (isSending) {
      return; // Prevent multiple simultaneous sends
    }

    setIsSending(true);

    try {
      // Simulate an asynchronous operation (e.g., an API call)
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Call the onSend function (simulated asynchronous)
      await onSend(text);
      setText("");
    } catch (error) {
      // Handle any errors that occur during the asynchronous operation
      console.error("An error occurred:", error);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="input">
      <form onSubmit={handleSend}>
        <input
          type="text"
          onChange={handleInputChange}
          value={text}
          placeholder="Enter your message here"
        />
        <button>
          <svg
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 500 500"
          >
            <g>
              <g>
                <polygon points="0,497.25 535.5,267.75 0,38.25 0,216.75 382.5,267.75 0,318.75" />
              </g>
            </g>
          </svg>
        </button>
      </form>
    </div>
  );
}
