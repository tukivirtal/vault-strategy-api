import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion";
import { Shield, X, Terminal, Activity, Lock, CheckCircle2, Menu, Globe, Cpu, Zap, ChevronRight } from "lucide-react";

// --- COMPONENTE: FONDO ORBITAL ---
const OrbitalBackground = () => (
  <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
    {[1, 2, 3].map((i) => (
      <motion.div
        key={i}
        animate={{ rotate: 360 }}
        transition={{ duration: 20 + i * 10, repeat: Infinity, ease: "linear" }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border border-[#C9A84C]/20 rounded-full"
        style={{ width: `${i * 30}%`, aspectRatio: "1/1" }}
      />
    ))}
  </div>
);

// --- COMPONENTE: MODAL DE ACCESO ---
const AccessModal = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
  const [step, setStep] = useState(0);
  const logs = ["INICIALIZANDO PROTOCOLO...", "CONECTANDO NASA JPL DE441...", "VERIFICANDO VECTORES...", "ACCESO AUTORIZADO."];
  useEffect(() => {
    if (isOpen) {
      const interval = setInterval(() => setStep(s => (s < logs.length - 1 ? s + 1 : s)), 800);
      return () => clearInterval(interval);
    } else setStep(0);
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} className="absolute inset-0 bg-black/90 backdrop-blur-xl" />
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="relative w-full max-w-md bg-black border border-[#C9A84C]/30 rounded-2xl p-8 font-mono">
            <div className="flex items-center gap-3 mb-6 text-[#C9A84C]"><Shield className="w-5 h-5" /><span className="text-xs font-bold tracking-widest uppercase">Seguridad Vault</span></div>
            {logs.slice(0, step + 1).map((log, i) => (
              <div key={i} className="flex items-center gap-3 text-sm mb-2">
                <span className="text-[#C9A84C] opacity-50">{">"}</span>
                <span className={i === step ? "text-white" : "text-white/40"}>{log}</span>
              </div>
            ))}
            {step === logs.length - 1 && (
              <motion.button initial={{ opacity: 0 }} animate={{ opacity: 1 }} onClick={onClose} className="w-full mt-6 py-3 bg-[#C9A84C] text-black font-bold rounded-lg uppercase text-xs tracking-widest">Entrar al Sistema</motion.button>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

// --- APP PRINCIPAL ---
export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="relative min-h-screen bg-black text-white selection:bg-[#C9A84C]/30 selection:text-[#C9A84C]">
      <div className="fixed inset-0 z-50 pointer-events-none opacity-[0.03] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
      <OrbitalBackground />
      
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-[100] border-b border-white/5 bg-black/50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-[#C9A84C] rounded-lg flex items-center justify-center shadow-lg shadow-[#C9A84C]/20"><Shield className="text-black w-6 h-6" /></div>
            <span className="font-mono font-bold tracking-[0.3em] text-sm">VAULT STRATEGY</span>
          </div>
          <button onClick={() => setIsModalOpen(true)} className="px-6 py-2 border border-[#C9A84C]/30 text-[#C9A84C] text-[10px] font-bold tracking-[0.2em] rounded-full hover:bg-[#C9A84C] hover:text-black transition-all">AUTORIZAR ACCESO</button>
        </div>
      </nav>

      {/* Hero */}
      <main className="relative pt-40 pb-20 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#C9A84C]/20 bg-[#C9A84C]/5 mb-8">
            <Activity className="w-3 h-3 text-[#C9A84C]" /><span className="text-[10px] font-mono text-[#C9A84C] tracking-widest uppercase">NASA JPL DE441 SYNC ACTIVE</span>
          </motion.div>
          <h1 className="text-6xl md:text-8xl font-mono font-bold tracking-tighter mb-8 leading-[0.9]">NO PREDIGA EL MERCADO. <span className="text-transparent bg-clip-text bg-gradient-to-b from-[#C9A84C] to-[#C9A84C]/50 italic">SINCRONÍCELO.</span></h1>
          <p className="text-white/40 max-w-2xl mx-auto text-lg mb-12 font-light leading-relaxed">Estrategias de alta frecuencia basadas en matemática orbital. Precisión absoluta donde otros ven caos.</p>
          <button onClick={() => setIsModalOpen(true)} className="group relative px-12 py-5 bg-[#C9A84C] text-black font-bold rounded-full overflow-hidden transition-transform active:scale-95">
            <span className="relative z-10 flex items-center gap-3 text-xs tracking-[0.2em]">INICIAR PROTOCOLO <ChevronRight className="w-4 h-4" /></span>
          </button>
        </div>
      </main>

      <AccessModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
