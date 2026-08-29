import { useEffect, useRef, useState } from "react";

import { useAuth } from "../context/useAuth";
import { api } from "../services/api";
import "../chatbot.css";

const WELCOME_MESSAGE = {
  id: "welcome",
  role: "assistant",
  content:
    "Hola. Puedo ayudarte a consultar el inventario y el histórico de ventas de demostración.",
};

const SUGGESTIONS = [
  "¿Cuáles son los 3 productos más caros?",
  "¿Qué producto fue el más vendido?",
  "¿Cuánto stock hay por marca?",
];

function ChatIcon({ size = 24 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        d="M5.5 18.5 3 21v-5.2A8 8 0 0 1 4 4.9 10.7 10.7 0 0 1 12 2c5.5 0 10 3.8 10 8.5S17.5 19 12 19c-1.7 0-3.3-.4-4.7-1.1l-1.8.6Z"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M7.5 10.5h.01M12 10.5h.01M16.5 10.5h.01"
        stroke="currentColor"
        strokeWidth="2.6"
        strokeLinecap="round"
      />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        d="m4 4 17 8-17 8 3-8-3-8Z"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M7 12h14" stroke="currentColor" strokeWidth="1.8" />
    </svg>
  );
}

function createMessage(role, content) {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
    role,
    content,
  };
}

function Chatbot() {
  const { token } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [question, setQuestion] = useState("");
  const [error, setError] = useState("");
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [isOpen, isSending, messages]);

  if (!token) return null;

  const sendQuestion = async (rawQuestion) => {
    const cleanQuestion = rawQuestion.trim();
    if (!cleanQuestion || isSending) return;

    const conversation = messages.filter(
      (message) => message.id !== WELCOME_MESSAGE.id,
    );
    const completedConversation =
      conversation.at(-1)?.role === "user"
        ? conversation.slice(0, -1)
        : conversation;
    const history = completedConversation
      .slice(-10)
      .map(({ role, content }) => ({ role, content }));

    setMessages((current) => [
      ...current,
      createMessage("user", cleanQuestion),
    ]);
    setQuestion("");
    setError("");
    setIsSending(true);

    try {
      const response = await api.askChatbot(cleanQuestion);
      setMessages((current) => [
        ...current,
        createMessage("assistant", response.answer),
      ]);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSending(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendQuestion(question);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendQuestion(question);
    }
  };

  const resetConversation = () => {
    setMessages([WELCOME_MESSAGE]);
    setQuestion("");
    setError("");
  };

  return (
    <div className="chatbot-shell">
      {isOpen && (
        <section
          className="chatbot-panel"
          role="dialog"
          aria-label="Asistente de inventario TECAPP"
        >
          <header className="chatbot-header">
            <div className="chatbot-header-icon">
              <ChatIcon size={22} />
            </div>
            <div>
              <h2>Asistente TECAPP</h2>
              <span>Inventario y ventas</span>
            </div>
            <button
              className="chatbot-header-action"
              type="button"
              onClick={resetConversation}
              aria-label="Limpiar conversación"
              title="Limpiar conversación"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M4 7h16M9 7V4h6v3m-8 0 1 13h8l1-13M10 11v5M14 11v5"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
            <button
              className="chatbot-header-action"
              type="button"
              onClick={() => setIsOpen(false)}
              aria-label="Cerrar asistente"
              title="Cerrar"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="m6 6 12 12M18 6 6 18"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          </header>

          <div className="chatbot-messages" aria-live="polite">
            {messages.map((message) => (
              <div
                className={`chatbot-message chatbot-message-${message.role}`}
                key={message.id}
              >
                {message.content}
              </div>
            ))}

            {messages.length === 1 && (
              <div className="chatbot-suggestions">
                {SUGGESTIONS.map((suggestion) => (
                  <button
                    type="button"
                    key={suggestion}
                    onClick={() => sendQuestion(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}

            {isSending && (
              <div className="chatbot-message chatbot-message-assistant chatbot-typing">
                <span />
                <span />
                <span />
                <span className="sr-only">Analizando información</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && <div className="chatbot-error">{error}</div>}

          <form className="chatbot-form" onSubmit={handleSubmit}>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Escribe tu pregunta…"
              aria-label="Pregunta para el asistente"
              maxLength={500}
              rows={1}
              disabled={isSending}
            />
            <button
              type="submit"
              disabled={!question.trim() || isSending}
              aria-label="Enviar pregunta"
            >
              <SendIcon />
            </button>
          </form>
          <p className="chatbot-disclaimer">
            Las ventas corresponden al conjunto de demostración suministrado.
          </p>
        </section>
      )}

      <button
        className="chatbot-launcher"
        type="button"
        onClick={() => setIsOpen((current) => !current)}
        aria-label={isOpen ? "Cerrar asistente" : "Abrir asistente"}
        aria-expanded={isOpen}
      >
        {isOpen ? (
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="m6 6 12 12M18 6 6 18"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            />
          </svg>
        ) : (
          <ChatIcon size={26} />
        )}
      </button>
    </div>
  );
}

export default Chatbot;
