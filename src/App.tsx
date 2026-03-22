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
          transition={{
            duration: p.duration,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      ))}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,_#1a1a1a_0%,_transparent_70%)]" />
    </div>
  );
};

// --- COMPONENTE PRINCIPAL ---
export default function App() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-gold/30 relative overflow-hidden font-sans">
      
      <ParticlesBackground />
      
      {/* Capa de Ruido CSS (De tu index.css) */}
      <div className="noise-overlay"></div>

      {/* --- NAVEGACIÓN SUPERIOR --- */}
      <nav className="relative z-50 flex justify-between items-center px-6 md:px-12 py-6 border-b border-white/5 bg-black/50 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="border border-gold text-gold p-1.5 rounded-md">
            <Shield size={20} />
          </div>
          <div className="flex flex-col">
            <span className="font-black tracking-[0.2em] text-sm text-white">VAULT LOGIC</span>
            <span className="text-[0.45rem] text-[#00ff88] tracking-[0.3em] font-terminal mt-1">
              <span className="animate-pulse mr-1">⚡</span>NASA JPL SYNC: ACTIVE
            </span>
          </div>
        </div>
        
        <div className="hidden md:flex gap-12 text-[0.65rem] tracking-[0.2em] text-gray-400 font-bold uppercase">
          <a href="#sincronizacion" className="hover:text-gold transition-colors">Sincronización</a>
          <a href="#ventaja" className="hover:text-gold transition-colors">Ventaja</a>
          <a href="#operadores" className="hover:text-gold transition-colors">Operadores</a>
        </div>

        <a href="portal.html" className="hidden md:inline-block bg-gold text-black px-6 py-2.5 text-[0.7rem] font-bold tracking-[0.15em] rounded-sm hover:bg-gold-light hover:shadow-[0_0_20px_rgba(212,175,55,0.4)] transition-all uppercase">
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
          <span className="text-gold text-[0.65rem] tracking-[0.25em] font-terminal uppercase">NASA JPL DE441 // Sincronización Activa</span>
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
          <a href="portal.html" className="group bg-gold text-black px-8 py-4 text-sm font-bold tracking-[0.15em] rounded flex items-center gap-3 hover:bg-gold-light transition-all uppercase">
            Autorizar Acceso
            <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
          </a>
          <div className="flex flex-col items-start border-l border-white/10 pl-6">
            <span className="text-white font-black text-xl">+847</span>
            <span className="text-gray-500 text-[0.6rem] tracking-[0.2em] font-terminal uppercase">Terminales activas en 23 países</span>
          </div>
        </motion.div>
      </main>

      {/* --- CARACTERÍSTICAS (TARJETAS) --- */}
      <section className="relative z-10 py-24 px-6 md:px-12 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { icon: Shield, title: "Protección de Capital", desc: "Algoritmos de sincronización diseñados para preservar la liquidez en ventanas de alta volatilidad orbital." },
          { icon: Zap, title: "Ejecución Instantánea", desc: "Conexión directa con los efemérides de la NASA para una precisión de milisegundos en la toma de decisiones." },
          { icon: FileText, title: "Reportes Ejecutivos", desc: "Documentación técnica detallada de cada movimiento, alineada con los estándares de cumplimiento global." }
        ].map((item, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.2 }}
            className="glass-vault p-8 rounded-xl hover:border-gold/50 transition-colors"
          >
            <div className="border border-gold/30 w-12 h-12 flex items-center justify-center rounded-lg mb-6 text-gold">
              <item.icon size={24} />
            </div>
            <h3 className="text-white text-xl font-bold mb-4">{item.title}</h3>
            <p className="text-gray-400 text-sm leading-relaxed">{item.desc}</p>
          </motion.div>
        ))}
      </section>

      {/* --- VENTAJA ASIMÉTRICA --- */}
      <section id="ventaja" className="relative z-10 py-24 px-6 md:px-12 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl md:text-6xl font-black uppercase tracking-tighter mb-16 flex flex-col md:flex-row gap-4">
            <span className="text-white">LA VENTAJA</span>
            <span className="text-gradient-gold">ASIMÉTRICA</span>
          </h2>
          
          <div className="space-y-16">
            <motion.div initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} className="flex gap-8">
              <span className="text-5xl md:text-7xl font-black text-gold/20">10</span>
              <div>
                <h3 className="text-xl md:text-2xl font-bold text-white mb-3 uppercase tracking-wide">Años de Proyección</h3>
                <p className="text-gray-400">Historial calibrado por perfil ejecutivo individual, garantizando una alineación total con su estrategia.</p>
              </div>
            </motion.div>
            <motion.div initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} className="flex gap-8">
              <span className="text-5xl md:text-7xl font-black text-gold/20">01</span>
              <div>
                <h3 className="text-xl md:text-2xl font-bold text-white mb-3 uppercase tracking-wide">Directiva Operativa</h3>
                <p className="text-gray-400">No entregamos datos crudos. Entregamos directivas claras y accionables para su mesa de operaciones.</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* --- COMPARATIVA DE SISTEMA --- */}
      <section className="relative z-10 py-24 px-6 md:px-12 max-w-5xl mx-auto overflow-hidden">
        <Globe className="absolute right-0 top-1/2 -translate-y-1/2 w-96 h-96 text-gold/5 pointer-events-none" strokeWidth={1} />
        <h2 className="text-2xl font-bold text-gold uppercase tracking-[0.2em] mb-12">Comparativa de Sistema</h2>
        
        <div className="w-full border-t border-white/10">
          <div className="grid grid-cols-3 py-4 border-b border-white/10 text-[0.65rem] tracking-[0.2em] text-gray-500 font-terminal uppercase">
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
              <div className="text-gold text-[0.65rem] font-terminal tracking-[0.1em] uppercase mb-4 space-y-2">
                <p>{">"} Operador: C.M. — Director Comercial, México</p>
                <p className="text-gray-500">{">"} Estado: Genesis Activo // 14 Meses</p>
              </div>
              <p className="text-gray-300 italic text-lg">"Cerré la negociación más grande de mi carrera en una ventana de 3 días que el sistema marcó como óptima. Coincidencia o no, fue real."</p>
            </motion.div>

            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }} className="border-l-2 border-gold/30 pl-6 py-2">
              <div className="text-gold text-[0.65rem] font-terminal tracking-[0.1em] uppercase mb-4 space-y-2">
                <p>{">"} Operador: R.V. — Private Equity, Madrid</p>
                <p className="text-gray-500">{">"} Estado: Sincronización Nivel 4</p>
              </div>
              <p className="text-gray-300 italic text-lg">"La precisión en los puntos de inflexión del mercado es aterradora. Vault Logic se ha convertido en mi brújula operativa diaria."</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* --- CTA FINAL --- */}
      <section className="relative z-10 py-32 px-4 text-center">
        <h2 className="text-6xl md:text-9xl font-black uppercase tracking-tighter flex justify-center gap-4 mb-6">
          <span className="text-white">¿ESTÁ</span>
          <span className="text-gradient-gold">LISTO?</span>
        </h2>
        <p className="text-xl md:text-3xl text-gray-400 font-light mb-12">El mercado no espera. La sincronización orbital es ahora.</p>
        <a href="portal.html" className="inline-block bg-white text-black px-12 py-5 text-lg font-black tracking-[0.2em] rounded-xl hover:scale-105 transition-transform uppercase">
          Autorizar Acceso
        </a>
      </section>

      {/* --- FOOTER --- */}
      <footer className="relative z-10 border-t border-white/10 bg-black pt-16 pb-8 px-6 md:px-12">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-2">
            <div className="flex items-center gap-3 mb-6">
              <div className="border border-gold text-gold p-1.5 rounded-md"><Shield size={24} /></div>
              <span className="font-black tracking-[0.2em] text-lg text-white">VAULT LOGIC</span>
            </div>
            <p className="text-gray-400 max-w-sm">Transformando matemática orbital en directivas operativas de alta precisión para el liderazgo global.</p>
          </div>
          
          <div>
            <h4 className="text-gold font-bold tracking-[0.2em] text-sm mb-6 uppercase">Legal</h4>
            <div className="flex flex-col gap-4 text-gray-400">
              <a href="#" className="hover:text-white transition-colors">Privacidad</a>
              <a href="#" className="hover:text-white transition-colors">Términos</a>
              <a href="#" className="hover:text-white transition-colors">Garantía</a>
            </div>
          </div>

          <div>
            <h4 className="text-gold font-bold tracking-[0.2em] text-sm mb-6 uppercase">Sistema</h4>
            <div className="space-y-4 text-[0.7rem] font-terminal text-gray-400 uppercase">
              <p className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#00ff88]"></span>NASA JPL DE441: ONLINE</p>
              <p className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#00ff88]"></span>LATENCIA: 12ms</p>
              <p className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#00ff88]"></span>ENCRIPTACIÓN: AES-256</p>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto border border-gold/20 bg-gold/5 p-6 rounded-lg mb-8 flex items-start gap-4">
          <AlertTriangle className="text-gold shrink-0 mt-1" size={24} />
          <p className="text-[0.65rem] text-gray-400 font-terminal uppercase leading-relaxed">
            <strong className="text-gold">Advertencia de Riesgo:</strong> La sincronización orbital y el uso de efemérides de la NASA JPL DE441 son herramientas de análisis técnico avanzado. El trading de activos financieros implica un riesgo sustancial de pérdida. Vault Logic no garantiza resultados específicos. Opere bajo su propia responsabilidad.
          </p>
        </div>

        <div className="max-w-7xl mx-auto pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4 text-[0.65rem] font-terminal text-gray-500 uppercase">
          <p>© 2026 VAULT LOGIC — TODOS LOS DERECHOS RESERVADOS | SISTEMA: OPERATIVO</p>
          <div className="flex gap-6">
            <p>NASA SYNC: <span className="text-[#00ff88]">ACTIVO</span></p>
            <p>LATENCIA: 12MS</p>
            <p>VERSIÓN: 4.2.1-GENESIS</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
