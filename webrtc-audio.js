// Demande l'accès au micro
navigator.mediaDevices.getUserMedia({ audio: true, video: false })
  .then(stream => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(stream);

    // Option : visualisation ou traitement du son
    const analyser = audioContext.createAnalyser();
    source.connect(analyser);

    console.log("Micro connecté — présence reçue.");

    // Ici, tu peux connecter à une IA vocale ou streamer à distance
    // ex: sendStreamToServer(stream);
  })
  .catch(err => {
    console.error("Erreur accès micro :", err);
  });

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'fr-FR';
  utterance.pitch = 1.1;
  utterance.rate = 0.92;
  utterance.volume = 1;
  utterance.voice = speechSynthesis.getVoices().find(v => v.name.includes("Google") || v.lang === "fr-FR");
  speechSynthesis.speak(utterance);
}
