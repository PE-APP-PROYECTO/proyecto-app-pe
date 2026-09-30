import React, { useState } from 'react';
import '../home.css';

export default function Home() {
  const [tab, setTab] = useState('perfil');

  return (
    <div className="app-container">
      {/* CONTENIDO PRINCIPAL */}
      <main className="main-content">
        {tab === 'perfil' && (
          <section className="card-section">
            <h2 className="title">MI PERFIL</h2>
            <div className="avatar">👤</div>
            <h3>Alejandro Rivera</h3>
            <p className="email">alejandro.rivera.example@gmail.com</p>
            <button className="btn-secondary">Información Personal (Ver/Editar)</button>
          </section>
        )}

        {tab === 'buscador' && (
          <section className="card-section">
            <h2 className="title">BUSCADOR DE MEDICAMENTOS</h2>
            <input type="text" placeholder="Buscar medicamento por..." className="search-input" />
            <ul className="list">
              <li><span>Acetaminofén (Ver precios)</span></li>
              <li><span>Ibuprofeno 400mg</span></li>
              <li className="item-price"><span>Aspirina 100mg</span> <strong>$1500</strong></li>
              <li className="item-price"><span>Ibuprofeno 400mg</span> <strong>$1500</strong></li>
            </ul>
          </section>
        )}

        {tab === 'chat' && (
          <section className="card-section">
            <h2 className="title">CHATBOT DE AYUDA</h2>
            <div className="chat-box">
              <p className="chat-bubble">¡Hola! Soy tu asistente virtual. ¿Cómo puedo ayudarte?</p>
            </div>
            <button className="btn-option">Buscar medicamento</button>
            <button className="btn-option">Ver mis pedidos</button>
            <button className="btn-option">Contactar soporte</button>
          </section>
        )}

        {tab === 'mapa' && (
          <section className="card-section">
            <h2 className="title">FARMACIAS CERCANAS EN MAPA</h2>
            <div className="map-placeholder">📌 Mapa Interactivo</div>
            <div className="pharmacy-info">
              <h4>Farmacias Cercanas</h4>
              <p>Active To Corazón - Rionegro</p>
            </div>
          </section>
        )}
      </main>

      {/* NAVEGACIÓN INFERIOR (CELULAR) */}
      <nav className="bottom-nav">
        <button className={tab === 'perfil' ? 'active' : ''} onClick={() => setTab('perfil')}>
          👤<span>PERFIL</span>
        </button>
        <button className={tab === 'buscador' ? 'active' : ''} onClick={() => setTab('buscador')}>
          🔍<span>BUSCADOR</span>
        </button>
        <button className={tab === 'chat' ? 'active' : ''} onClick={() => setTab('chat')}>
          💬<span>CHAT</span>
        </button>
        <button className={tab === 'mapa' ? 'active' : ''} onClick={() => setTab('mapa')}>
          📍<span>MAPA</span>
        </button>
      </nav>
    </div>
  );
}