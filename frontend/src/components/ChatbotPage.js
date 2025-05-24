import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import './ChatbotPage.css';
import sendIcon from '../assets/sendbutton.png';
import her from '../assets/her.png';

function ChatbotPage() {
  const [messages, setMessages] = useState([
    { from: 'bot', text: "Hello I'm Medaura!", isInitial: true },
  ]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState(null); 
  const sessionIdRef = useRef(null);

  useEffect(() => {
    sessionIdRef.current = uuidv4();
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userInput = input;
    setInput('');
    const newMessages = [...messages, { from: 'user', text: userInput }];
    setMessages(newMessages);

    try {
      let response;
      if (mode === 'symptoms') {
        response = await axios.post('http://localhost:8000/symptom-analysis/', {
          symptoms: userInput,
          sessionId: sessionIdRef.current,
        });
      } else {
        // Default: chat
        response = await axios.post('http://localhost:8000/chat/', {
          message: userInput,
          sessionId: sessionIdRef.current,
        });
      }

      setMessages([...newMessages, { from: 'bot', text: response.data.diseases || response.data.reply || response.data }]);
    } catch (error) {
      setMessages([...newMessages, { from: 'bot', text: 'Error: Unable to reach server.' }]);
    }

  
    if (mode === 'symptoms' || mode === 'upload') {
      setMode(null);
    }
  };

  const handleOptionSelect = (selectedMode) => {
    setMode(selectedMode);

    let botText = '';
    if (selectedMode === 'chat') {
      botText = "Hello! I'm here to help. How can I assist you with your healthcare question today?";
    } else if (selectedMode === 'symptoms') {
      botText = "Give me a description of your symptoms";
    } else if (selectedMode === 'upload') {
      botText = { isUploadPrompt: true }; // Special case to show upload UI
    }

    const newMessages = [
      ...messages,
      { from: 'user', text: selectedMode.replace(/^\w/, (c) => c.toUpperCase()) },
      { from: 'bot', text: botText }
    ];
    setMessages(newMessages);
  };

  const handleFileUpload = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const newMessages = [...messages, { from: 'user', text: file.name }];
  const confirmationMsg = { from: 'bot', text: '✅ Your document has been received and is being analyzed. Please wait a moment...' };
  setMessages([...newMessages, confirmationMsg]); 

  const formData = new FormData();
  formData.append('file', file);
  formData.append('sessionId', sessionIdRef.current);

  try {
    const res = await axios.post('http://localhost:8000/pdf-summary/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    const summaryMsg = { from: 'bot', text: res.data.summary };
    setMessages(prev => [...prev, summaryMsg]); 
  } catch (error) {
    setMessages(prev => [...prev, { from: 'bot', text: '❌ Error: Document upload failed. Please try again.' }]);
  }

  setMode(null);
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
            <div key={index} className={`message ${msg.from === 'bot' ? 'left' : 'right'}`}>
              {msg.text?.isUploadPrompt ? (
                <div className="upload-container">
                  <label className="upload-label">
                    Upload PDF
                    <input type="file" accept="application/pdf" onChange={handleFileUpload} hidden />
                  </label>
                </div>
              ) : (
                msg.text
              )}
              {msg.isInitial && (
                <div className="initial-options">
                  <button onClick={() => handleOptionSelect('symptoms')}>Analyse Symptoms</button>
                  <button onClick={() => handleOptionSelect('chat')}>Chat with Medical Expert</button>
                  <button onClick={() => handleOptionSelect('upload')}>Upload Medical Document</button>
                </div>
              )}
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
            disabled={mode === 'upload'}
          />
          <button onClick={sendMessage} disabled={mode === 'upload'}>
            <img src={sendIcon} alt="Send" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatbotPage;
