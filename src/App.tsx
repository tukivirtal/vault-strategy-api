import { motion } from "framer-motion";
import { Shield } from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      
      {/* Efecto de fondo radial (Brillo central superior) */}
      <div className="absolute inset-0 z-0 opacity-40 pointer-events-none" 
           style={{ backgroundImage: 'radial-gradient(circle at 50% 0%, #1a1a1a 0%, transparent 60%)' }}>
      </div>

      {/* --- NAVEGACIÓN SUPERIOR --- */}
      <nav className="relative z-50 flex justify-between items-center px-10 py-6 border-b border-white/5 bg-black/40 backdrop-blur-xl">
        <div className="flex items-center gap-4">
          <div className="border border-gold text-gold p-1.5 rounded-md">
            <Shield size={22} />
          </div>
          <div className="flex flex-col">
            <span className="font-black tracking-[0.25em] text-sm text-white">VAULT LOGIC</span>
            <span className="text-[0.48rem] text-[#00ff88] tracking-[0.3em] font-terminal mt-1">
              <span className="animate-pulse mr-1">⚡</span>NASA JPL SYNC: ACTIVE
            </span>
          </div>
        </div>
        
        <div className="hidden md:flex gap-14 text-[0.68rem] tracking-[0.2em] text-gray-400 font-bold uppercase">
          <a href="#" className="hover:text-gold transition-colors">SINCRONIZACIÓN</a>
          <a href="#" className="hover:text-gold transition-colors">VENTAJA</a>
          <a href="#" className="hover:text-gold transition-colors">OPERADORES</a>
        </div>

        <a href="portal.html" className="bg-gold text-black px-7 py-3 text-[0.72rem] font-bold tracking-[0.18em] rounded-sm hover:bg-gold-light hover:shadow-[0_0_20px_rgba(212,175,55,0.4)] transition-all uppercase">
          AUTORIZAR ACCESO
        </a>
      </nav>

      {/* --- HERO SECTION DE ALTO IMPACTO --- */}
      <main className="relative z-10 flex flex-col items-center justify-center pt-36 px-4 text-center pb-24">
        
        {/* Badge NASA (Pequeño y nítido) */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 border border-gold/15 bg-gold/5 px-6 py-2.5 rounded-full mb-12 shadow-[0_0_15px_rgba(212,175,55,0.05)]"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-[#00ff88] animate-pulse"></div>
          <span className="text-gold text-[0.68rem] tracking-[0.28em] font-terminal uppercase">NASA JPL DE441 // SINCRONIZACIÓN ACTIVA</span>
        </motion.div>

        {/* TÍTULO MASIVO (La clave del impacto) */}
        <motion.h1 
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1, duration: 0.7 }}
          className="flex flex-col items-center"
        >
          {/* Aquí forzamos el degradado metálico */}
          <span className="text-gradient-gold text-6xl md:text-8xl font-black tracking-tighter leading-[0.92] uppercase">
            NO PREDIGA EL MERCADO
          </span>
          {/* Aquí forzamos el color blanco sólido */}
          <span className="text-white text-6xl md:text-8xl font-black italic tracking-tighter leading-[1.0] uppercase mt-2">
            SINCRONÍCELO
          </span>
        </motion.h1>

        {/* Subtítulo (Más delgado y elegante) */}
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-12 text-gray-400 max-w-2xl text-lg md:text-xl font-light leading-relaxed px-6"
        >
          Los líderes corporativos no dependen de la intuición.<br/>
          <strong className="text-white font-normal">Vault Logic</strong> convierte matemática orbital en decisiones ejecutivas de alta precisión.
        </motion.p>
      </main>
    </div>
  );
}
