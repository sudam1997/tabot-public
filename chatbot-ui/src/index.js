import React, { useState, useEffect} from "react";
import ReactDOM from "react-dom";

import BotMessage from "./components/BotMessage";
import UserMessage from "./components/UserMessage";
import Messages from "./components/Messages";
import Input from "./components/Input";

import API from "./ChatbotAPI";
import API_initiate from "./InitiateConversationAPI";
import EndConversation  from "./endConversationAPI";

import "./styles.css";
import Header from "./components/Header";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [conversationID, setConversationID] = useState(null);

  // Initiate Session
  const initiateSession = async  () => {
    try {
      const response = await API_initiate.InitiateSession(); // Make the API call to initiate the session
      setConversationID(response.convID); // Set the conversation ID in the state
      console.log("Conversation ID:", response.convID); // Log the conversation ID to the console
    } catch (error) {
      console.error("Error initiating the session:", error);
    }
  }

  useEffect(() => {
    initiateSession();
  }, []); 


// Handle the API call on page unload
useEffect(() => {
  const handleUnload = () => {
    if (conversationID) {
      EndConversation.MakeAPIRequestOnUnload(conversationID);
    }
  };

  window.addEventListener("beforeunload", handleUnload);

  return () => {
    window.removeEventListener("beforeunload", handleUnload);
  };
}, [conversationID])

// Welcome Message
  useEffect(() => {
    async function loadWelcomeMessage() {
      setMessages([
        <BotMessage
          key="0"
          fetchMessage={
            async () =>   {
              const welcomeMessages = [
                "Welcome to the TA BOT!",
                "Hello there!",
                "Greetings! How can I assist you today?",
                // Add more welcome messages here
              ];
              const randomIndex = Math.floor(Math.random() * welcomeMessages.length);
              return welcomeMessages[randomIndex];
            }
          
          
          }
        />
      ]);
    }

    loadWelcomeMessage();
  }, []);

  

  const send = async text => {
    const newMessages = messages.concat(
      <UserMessage key={messages.length + 1} text={text} />,
      <BotMessage
        key={messages.length + 2}
        fetchMessage={async () => await API.GetChatbotResponse(text,conversationID)}
      />
    );
    setMessages(newMessages);
  };

  useEffect(() => {
    const messagesContainer = document.getElementById("messages-container");
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chatbot">
      <Header />
      <div className="conversation-id">
        Conversation ID: <strong>{conversationID}</strong>
      </div>
      <div className="feedback-link">
        Feedback form: <a href="https://forms.gle/Qg4F2XX2PA9g6DCt9" target="_blank" rel="noopener noreferrer">https://forms.gle/Qg4F2XX2PA9g6DCt9</a>
      </div>

      <Messages messages={messages} />
      <Input onSend={send} />
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Chatbot />, rootElement);
