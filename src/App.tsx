import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Shield } from 'lucide-react';

export default function App() {
  // Efecto sutil de brillo que sigue al ratón
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
      document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="relative min-h-screen bg-black overflow-x-hidden">
      {/* Capa de textura */}
      <div className="noise-overlay" />

      {/* Brillo del cursor (Sutil) */}
      <div className="fixed inset-0 pointer-events-none z-[9999] mix-blend-screen opacity-50">
        <div 
          className="absolute w-64 h-64 bg-gold/10 blur-[100px] rounded-full -translate-x-1/2 -translate-y-1/2 transition-transform duration-75" 
          style={{ left: 'var(--mouse-x, 50%)', top: 'var(--mouse-y, 50%)' }} 
        />
      </div>

      {/* --- NAVEGACIÓN SUPERIOR --- */}
      <nav className="relative z-50 flex justify-between items-center px-6 md:px-12 py-6 border-b border-white/5 bg-black/50 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="border border-gold text-gold p-1.5 rounded-md">
            <Shield size={20} />
          </div>
          <div className="flex flex-col">
            <span className="font-black tracking-[0.2em] text-sm text-white font-sans">VAULT LOGIC</span>
            <span className="text-[0.45rem] text-[#00ff88] tracking-[0.3em] font-mono mt-1">
              <span className="animate-pulse mr-1">⚡</span>NASA JPL SYNC: ACTIVE
            </span>
          </div>
        </div>
        
        <div className="hidden md:flex gap-12 text-[0.65rem] tracking-[0.2em] text-gray-400 font-bold uppercase font-sans">
          <a href="#sincronizacion" className="hover:text-gold transition-colors">Sincronización</a>
          <a href="#ventaja" className="hover:text-gold transition-colors">Ventaja</a>
          <a href="#operadores" className="hover:text-gold transition-colors">Operadores</a>
        </div>

        <a href="portal.html" className="hidden md:inline-block bg-gold text-black px-6 py-2.5 text-[0.7rem] font-bold tracking-[0.15em] rounded-sm hover:bg-gold-light hover:shadow-[0_0_20px_rgba(212,175,55,0.4)] transition-all uppercase font-sans">
          Autorizar Acceso
        </a>
      </nav>

      {/* --- HERO SECTION --- */}
      <main className="relative z-10 flex flex-col items-center justify-center pt-32 pb-24 px-4 text-center">
        
        {/* Badge NASA */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 border border-gold/20 bg-gold/5 px-5 py-2 rounded-full mb-10"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-[#00ff88] animate-pulse"></div>
          <span className="text-gold text-[0.65rem] tracking-[0.25em] font-mono uppercase">NASA JPL DE441 // Sincronización Activa</span>
        </motion.div>

        {/* Título Masivo */}
        <motion.h1 
          initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2, duration: 0.8 }}
          className="flex flex-col items-center"
        >
          {/* Aquí aplicamos la clase del degradado metálico */}
          <span className="text-gradient-gold text-5xl md:text-8xl font-black tracking-tighter leading-[0.9] uppercase font-sans">
            NO PREDIGA EL MERCADO.
          </span>
          <span className="text-white text-5xl md:text-8xl font-black italic tracking-tighter leading-[1.1] uppercase mt-2 font-sans">
            SINCRONÍCELO.
          </span>
        </motion.h1>

        {/* Subtítulo */}
        <motion.p 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
          className="mt-10 text-gray-400 max-w-2xl text-lg md:text-xl font-light leading-relaxed font-sans"
        >
          Los líderes corporativos no dependen de la intuición.<br/>
          <strong className="text-white font-normal">Vault Logic</strong> convierte matemática orbital en decisiones ejecutivas de alta precisión.
        </motion.p>
      </main>
    </div>
  );
}
