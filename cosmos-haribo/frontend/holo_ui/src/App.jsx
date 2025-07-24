import React from 'react';
import AuraCanvas from './auraCanvas.jsx';
import WhisperPlayer from './whisperPlayer.jsx';

export default function App() {
  return (
    <div style={{ background: '#0a0a0a', height: '100vh' }}>
      <AuraCanvas />
      <WhisperPlayer />
      <div style={{
        color: '#ffd700', fontFamily: 'Orbitron', position: 'absolute', bottom: 20, left: 20
      }}>
        HARIBO ÖROM IA est en éveil.
      </div>
    </div>
  );
}
