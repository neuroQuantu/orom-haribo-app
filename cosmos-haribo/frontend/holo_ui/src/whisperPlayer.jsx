import { useEffect, useRef } from 'react';

export default function WhisperPlayer() {
  const audioRef = useRef();
  useEffect(() => {
    audioRef.current.src = '/assets/whisper.aura.mp3';
  }, []);
  return <audio ref={audioRef} autoPlay loop />;
}
