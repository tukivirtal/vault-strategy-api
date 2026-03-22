import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Shield, ChevronRight, Zap, FileText, CheckCircle2, XCircle, Globe, AlertTriangle } from 'lucide-react';

// --- SISTEMA DE PARTÍCULAS DE FONDO ---
const ParticlesBackground = () => {
  const [particles, setParticles] = useState<Array<{ id: number; x: number; y: number; size: number; duration: number }>>([]);

  useEffect(() => {
    const particleCount = 40;
    const newParticles = Array.from({ length: particleCount }).map((_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 3 + 1,
      duration: Math.random() * 20 + 10,
    }));
    setParticles(newParticles);
  }, []);

  return (
    <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none opacity-30">
      {particles.map((p) => (
        <motion.div
          key={p.id}
          className="absolute bg-gold rounded-full"
          style={{ width: p.size, height: p.size, left: `${p.x}%`, top: `${p.y}%` }}
          animate={{
            y: [0, -100, 0],
            x: [0, Math.random() * 50 - 25, 0],
            opacity: [0.1, 0.5, 0.1],
          }}
          transition={{ duration: p.duration, repeat: Infinity, ease: "linear" }}
        />
      ))}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,_#1a1a1a_0%,_transparent_70%)]" />
    </div>
  );
};

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
    <div className="relative min-h-screen bg-black text-white overflow-x-hidden font-sans">
      {/* Capa de textura de AI Studio */}
      <div className="noise-overlay" />
      
      {/* Las partículas originales */}
      <ParticlesBackground />

      {/* Brillo del cursor */}
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
            <span className="font-black tracking-[0.2em] text-sm text-white">VAULT LOGIC</span>
            <span className="text-[0.45rem] text-[#00ff88] tracking-[0.3em] font-mono mt-1">
              <span className="animate-pulse mr-1">⚡</span>NASA JPL SYNC: ACTIVE
            </span>
          </div>
        </div>
        
        <div className="hidden md:flex gap-12 text-[0.65rem] tracking-[0.2em] text-gray-400 font-bold uppercase">
          <a href="#sincronizacion" className="hover:text-gold transition-colors">Sincronización</a>
          <a href="#ventaja" className="hover:text-gold transition-colors">Ventaja</a>
          <a href="#operadores" className="hover:text-gold transition-colors">Operadores</a>
        </div>

        <a href="portal.html" className="hidden md:inline-block bg-gold text-black px-6 py-2.5 text-[0.7rem] font-bold tracking-[0.15em] rounded-sm hover:opacity-80 transition-all uppercase">
          Autorizar Acceso
        </a>
      </nav>

      {/* --- HERO SECTION --- */}
      <main className="relative z-10 flex flex-col items-center justify-center pt-32 pb-24 px-4 text-center">
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 border border-gold/20 bg-gold/5 px-5 py-2 rounded-full mb-10"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-[#00ff88] animate-pulse"></div>
          <span className="text-gold text-[0.65rem] tracking-[0.25em] font-mono uppercase">NASA JPL DE441 // Sincronización Activa</span>
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2, duration: 0.8 }}
          className="flex flex-col items-center"
        >
          <span className="text-gradient-gold text-5xl md:text-8xl font-black tracking-tighter leading-[0.9] uppercase">
            NO PREDIGA EL MERCADO.
          </span>
          <span className="text-white text-5xl md:text-8xl font-black italic tracking-tighter leading-[1.1] uppercase mt-2">
            SINCRONÍCELO.
          </span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
          className="mt-10 text-gray-400 max-w-2xl text-lg md:text-xl font-light leading-relaxed"
        >
          Los líderes corporativos no dependen de la intuición.<br/>
          <strong className="text-white font-normal">Vault Logic</strong> convierte matemática orbital en decisiones ejecutivas de alta precisión.
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }}
          className="mt-12 flex flex-col md:flex-row items-center gap-6"
        >
          <a href="portal.html" className="group bg-gold text-black px-8 py-4 text-sm font-bold tracking-[0.15em] rounded flex items-center gap-3 hover:opacity-80 transition-all uppercase">
            Autorizar Acceso
            <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
          </a>
          <div className="flex flex-col items-start border-l border-white/10 pl-6">
            <span className="text-white font-black text-xl">+847</span>
            <span className="text-gray-500 text-[0.6rem] tracking-[0.2em] font-mono uppercase">Terminales activas</span>
          </div>
        </motion.div>
      </main>

      {/* --- CARACTERÍSTICAS (TARJETAS) --- */}
      <section className="relative z-10 py-24 px-6 md:px-12 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { icon: Shield, title: "Protección de Capital", desc: "Algoritmos diseñados para preservar liquidez en ventanas de volatilidad orbital." },
          { icon: Zap, title: "Ejecución Instantánea", desc: "Conexión directa con NASA JPL para precisión de milisegundos." },
          { icon: FileText, title: "Reportes Ejecutivos", desc: "Documentación técnica alineada con estándares de cumplimiento global." }
        ].map((item, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.2 }}
            className="glass-gold p-8 rounded-xl hover:border-gold/30 transition-colors"
          >
            <div className="border border-gold/30 w-12 h-12 flex items-center justify-center rounded-lg mb-6 text-gold">
              <item.icon size={24} />
            </div>
            <h3 className="text-white text-xl font-bold mb-4">{item.title}</h3>
            <p className="text-gray-400 text-sm leading-relaxed">{item.desc}</p>
          </motion.div>
        ))}
      </section>

      {/* --- COMPARATIVA DE SISTEMA --- */}
      <section className="relative z-10 py-24 px-6 md:px-12 max-w-5xl mx-auto overflow-hidden">
        <h2 className="text-2xl font-bold text-gold uppercase tracking-[0.2em] mb-12 text-center font-mono">Comparativa de Sistema</h2>
        <div className="w-full border-t border-white/10">
          <div className="grid grid-cols-3 py-4 border-b border-white/10 text-[0.65rem] tracking-[0.2em] text-gray-500 font-mono uppercase">
            <div>Métrica</div>
            <div className="text-white">Vault Logic</div>
            <div className="text-right">Tradicional</div>
          </div>
          {[
            { m: "Output", v: "Directiva", t: "Datos" },
            { m: "Interpretación", v: "Automática", t: "Manual" },
            { m: "Perfil Natal", v: "Calibrado", t: "Genérico" },
            { m: "Base de Datos", v: "NASA JPL", t: "Feeds" },
          ].map((row, i) => (
            <motion.div key={i} initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }} className="grid grid-cols-3 py-6 border-b border-white/5 items-center">
              <div className="text-white font-medium">{row.m}</div>
              <div className="text-gold font-bold flex items-center gap-2"><CheckCircle2 size={16} /> {row.v}</div>
              <div className="text-gray-600 flex items-center justify-end gap-2"><XCircle size={16} /> {row.t}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* --- LOGS DE OPERADORES --- */}
      <section id="operadores" className="relative z-10 py-24 px-6 md:px-12 bg-black">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-6xl font-black uppercase tracking-tighter flex gap-4 mb-16">
            <span className="text-white">LOGS DE</span>
            <span className="text-gradient-gold">OPERADORES</span>
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="border-l-2 border-gold/30 pl-6 py-2">
              <div className="text-gold text-[0.65rem] font-mono tracking-[0.1em] uppercase mb-4 space-y-2">
                <p>{">"} Operador: C.M. — Director Comercial</p>
                <p className="text-gray-500">{">"} Estado: Genesis Activo</p>
              </div>
              <p className="text-gray-300 italic text-lg">"Cerré la negociación más grande de mi carrera en una ventana de 3 días que el sistema marcó como óptima."</p>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }} className="border-l-2 border-gold/30 pl-6 py-2">
              <div className="text-gold text-[0.65rem] font-mono tracking-[0.1em] uppercase mb-4 space-y-2">
                <p>{">"} Operador: R.V. — Private Equity</p>
                <p className="text-gray-500">{">"} Estado: Sincronización Nivel 4</p>
              </div>
              <p className="text-gray-300 italic text-lg">"La precisión en los puntos de inflexión del mercado es aterradora. Vault Logic es mi brújula operativa."</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* --- FOOTER --- */}
      <footer className="relative z-10 border-t border-white/10 bg-black pt-16 pb-8 px-6 md:px-12">
        <div className="max-w-7xl mx-auto flex flex-col items-center text-center">
          <div className="flex items-center gap-3 mb-6">
            <div className="border border-gold text-gold p-1.5 rounded-md"><Shield size={24} /></div>
            <span className="font-black tracking-[0.2em] text-lg text-white">VAULT LOGIC</span>
          </div>
          <p className="text-gray-400 text-sm max-w-md mb-8">Transformando matemática orbital en directivas operativas de alta precisión.</p>
          <div className="border border-gold/20 bg-gold/5 p-4 rounded-lg mb-8 max-w-3xl">
            <p className="text-[0.6rem] text-gray-400 font-mono uppercase">
              <strong className="text-gold">Advertencia:</strong> La sincronización orbital y efemérides NASA JPL DE441 son herramientas de análisis. El trading implica riesgo sustancial.
            </p>
          </div>
          <p className="text-[0.65rem] font-mono text-gray-500 uppercase">
            © 2026 VAULT LOGIC — NASA SYNC: <span className="text-[#00ff88]">ACTIVO</span>
          </p>
        </div>
      </footer>
    </div>
  );
}
