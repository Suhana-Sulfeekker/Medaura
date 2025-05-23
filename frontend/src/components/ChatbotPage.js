import React, { useState } from 'react';
import axios from 'axios';
import './ChatbotPage.css';
import sendIcon from '../assets/sendbutton.png';
import her from '../assets/her.png';

function ChatbotPage() {
  const [messages, setMessages] = useState([
    { from: 'bot', text: "Hello I'm Medaura!" },
  ]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userInput = input;
    setInput('');
    const newMessages = [...messages, { from: 'user', text: userInput }];
    setMessages(newMessages);

    try {
      const response = await axios.post('http://localhost:8000/chat/', {
        message: userInput,
      });
      setMessages([...newMessages, { from: 'bot', text: response.data.reply }]);
    } catch (error) {
      setMessages([...newMessages, { from: 'bot', text: 'Error: Unable to reach server.' }]);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-left">
        <img src={her} alt="Doctor" className="doctor-image" />
        <div className="chat-bubble">
          Hi! I'm<br />Medaura.
        </div>

        <div className="features-container">
          <h2 className="features-heading">Features:</h2>
          <ul className="features">
            <li>Find possible diseases based on your symptoms</li>
            <li>Chat with a medical and health expert (AI)</li>
            <li>Summarise your medical reports</li>
          </ul>
        </div>
      </div>

      <div className="chatbot-right">
        <div className="chat-window">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.from === 'bot' ? 'left' : 'right'}`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type here"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') sendMessage();
            }}
          />
          <button onClick={sendMessage}>
            <img src={sendIcon} alt="Send" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatbotPage;
