import { useRef, useEffect } from 'react';

export default function AuraCanvas() {
  const canvasRef = useRef();
  useEffect(() => {
    const canvas = canvasRef.current, ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const particles = Array.from({length:120}).map(()=>({
      x:Math.random()*canvas.width, y:Math.random()*canvas.height,
      r:Math.random()*2+1, dx:(Math.random()-0.5)*0.6, dy:(Math.random()-0.5)*0.6
    }));
    function animate(){
      ctx.clearRect(0,0,canvas.width,canvas.height);
      ctx.fillStyle = '#ffd700';
      particles.forEach(p=> {
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();
        p.x+=p.dx; p.y+=p.dy;
        if(p.x<0||p.x>canvas.width)p.dx*=-1;
        if(p.y<0||p.y>canvas.height)p.dy*=-1;
      });
      requestAnimationFrame(animate);
    }
    animate();
  }, []);
  return <canvas ref={canvasRef} style={{position:'fixed',top:0,left:0,zIndex:-1}} />;
}
