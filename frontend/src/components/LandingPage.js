import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';
import logo from '../assets/logo.png'; // Ensure this path is correct

const LandingPage = () => {
  const navigate = useNavigate();
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setLoaded(true), 100);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`landing-wrapper ${loaded ? 'loaded' : ''}`}>
      <div className="landing-inner">
        <div className="left">
          <img src={logo} alt="Medaura Logo" className="logo" />
        </div>

        <div className="vertical-divider" />

        <div className="right">
          <h1 className="headline">
            Empowering your <br /> Health Journey<span className="red-dot">.</span>
          </h1>
          <button className="chatbot-button" onClick={() => navigate('/chat')}>
            Try Chatbot
          </button>
        </div>
      </div>

      <p className="description">
        Analyse symptoms, chat away your medical and health concerns, and summarize your test reports — <br/>all leveraging AI.
      </p>
    </div>
  );
};

export default LandingPage;
