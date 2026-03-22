import { motion } from "framer-motion";

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-gold/30 relative overflow-hidden">
      
      {/* Capa de Ruido/Textura de fondo */}
      <div className="absolute inset-0 z-0 opacity-20 pointer-events-none" 
           style={{ backgroundImage: 'radial-gradient(circle at 50% 0%, #1a1a1a 0%, transparent 70%)' }}>
      </div>

      {/* Navegación Superior */}
      <nav className="relative z-50 flex justify-between items-center px-8 py-6 border-b border-white/5 bg-black/40 backdrop-blur-md">
        <div className="flex flex-col">
          <span className="font-bold tracking-[0.2em] text-sm text-white">VAULT LOGIC</span>
          <span className="text-[0.45rem] text-gray-500 tracking-[0.3em] font-terminal mt-1">NASA JPL SYNC: ACTIVE</span>
        </div>
        
        {/* Menú Central */}
        <div className="hidden md:flex gap-12 text-[0.65rem] tracking-[0.2em] text-gray-400 font-bold">
          <a href="#" className="hover:text-gold transition-colors">SINCRONIZACIÓN</a>
          <a href="#" className="hover:text-gold transition-colors">VENTAJA</a>
          <a href="#" className="hover:text-gold transition-colors">OPERADORES</a>
        </div>

        {/* Botón Acción */}
        <a href="portal.html" className="bg-gold text-black px-6 py-2.5 text-[0.7rem] font-bold tracking-[0.15em] rounded-sm hover:bg-gold-light hover:shadow-[0_0_20px_rgba(212,175,55,0.4)] transition-all">
          AUTORIZAR ACCESO
        </a>
      </nav>

      {/* Contenido Principal (Hero) */}
      <main className="relative z-10 flex flex-col items-center justify-center pt-32 px-4 text-center">
        
        {/* Badge NASA */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 border border-gold/20 bg-gold/5 px-5 py-2 rounded-full mb-10"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-[#00ff88] animate-pulse"></div>
          <span className="text-gold text-[0.65rem] tracking-[0.25em] font-terminal">NASA JPL DE441 // SINCRONIZACIÓN ACTIVA</span>
        </motion.div>

        {/* Título Masivo */}
        <motion.h1 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="flex flex-col items-center"
        >
          <span className="text-gradient-gold text-6xl md:text-8xl font-black tracking-tighter leading-[0.9] uppercase">
            NO PREDIGA EL MERCADO
          </span>
          <span className="text-white text-6xl md:text-8xl font-black italic tracking-tighter leading-[1.1] uppercase mt-2">
            SINCRONÍCELO
          </span>
        </motion.h1>

        {/* Subtítulo */}
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-10 text-gray-400 max-w-2xl text-lg font-light leading-relaxed"
        >
          Los líderes corporativos no dependen de la intuición.<br/>
          <strong className="text-white font-normal">Vault Logic</strong> convierte matemática orbital en decisiones ejecutivas de alta precisión.
        </motion.p>

      </main>
    </div>
  );
}
