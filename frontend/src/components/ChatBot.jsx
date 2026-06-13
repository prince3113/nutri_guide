import { useState, useRef, useEffect } from "react";
import { apiRequest } from "../api";

export default function ChatBot({ showToast }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello! I am your NutriGuide AI Assistant. 🥗 How can I help you with your nutrition or diet today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const SUGGESTIONS = [
    "Can I eat mango during weight loss?",
    "How much protein is in paneer?",
    "Suggest a healthy breakfast.",
  ];

  // Auto scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isOpen]);

  async function sendMessage(text) {
    if (!text.trim()) return;

    const userMessage = { sender: "user", text };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const data = await apiRequest("/chat", {
        method: "POST",
        body: JSON.stringify({ message: text }),
      });

      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: data.response },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "⚠️ " + err.message },
      ]);
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  return (
    <div className="chatbot-wrapper">
      {/* Floating Action Button */}
      <button
        className={`chatbot-toggle-btn ${isOpen ? "open" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="24" height="24">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="24" height="24">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window glass-card animate-scale-in">
          <div className="chatbot-header">
            <div className="chatbot-title-group">
              <span className="chatbot-avatar-dot"></span>
              <div>
                <h4>NutriGuide AI</h4>
                <p>Online • Nutrition Assistant</p>
              </div>
            </div>
            <button className="chatbot-close-inline" onClick={() => setIsOpen(false)}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="16" height="16">
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                <div className="chat-bubble">{msg.text}</div>
              </div>
            ))}
            {loading && (
              <div className="chat-message ai">
                <div className="chat-bubble typing">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {messages.length === 1 && !loading && (
            <div className="chatbot-suggestions">
              <p className="suggestion-title">Ask me about:</p>
              <div className="suggestion-chips">
                {SUGGESTIONS.map((s, i) => (
                  <button key={i} className="suggestion-chip" onClick={() => sendMessage(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="chatbot-input-form">
            <input
              type="text"
              placeholder="Ask anything about nutrition..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" className="chatbot-send-btn" disabled={loading || !input.trim()}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="18" height="18">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
