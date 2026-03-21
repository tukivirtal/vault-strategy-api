import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion";
import { Shield, X, Activity, ChevronRight, Lock, User, AlertCircle, Loader2 } from "lucide-react";

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

// --- COMPONENTE: MODAL DE ACCESO (CONECTADO A FASTAPI) ---
const AccessModal = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setMessage("Iniciando protocolo de verificación...");

    try {
      const response = await fetch("/api/consultar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          login_only: true // Modo VIP activado
        }),
      });

      const data = await response.json();

      if (data.status === "success") {
        setStatus("success");
        setMessage(`Acceso concedido. Bienvenido, ${data.nombre}.`);
        // Aquí podrías redirigir al usuario o guardar su sesión
        setTimeout(() => onClose(), 2000);
      } else {
        setStatus("error");
        setMessage(data.analisis_ejecutivo || "Error de credenciales.");
      }
    } catch (error) {
      setStatus("error");
      setMessage("Fallo en la conexión con el núcleo.");
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} className="absolute inset-0 bg-black/90 backdrop-blur-xl" />
          
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="relative w-full max-w-md bg-black border border-[#C9A84C]/30 rounded-2xl p-8 font-mono shadow-2xl shadow-[#C9A84C]/10">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-3 text-[#C9A84C]">
                <Shield className="w-5 h-5" />
                <span className="text-xs font-bold tracking-widest uppercase text-gold">Autorización Requerida</span>
              </div>
              <button onClick={onClose} className="text-white/40 hover:text-white"><X className="w-5 h-5" /></button>
            </div>

            <form onSubmit={handleLogin} className="space-y-6">
              <div className="space-y-4">
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#C9A84C]/50" />
                  <input 
                    type="email" required placeholder="EMAIL DE OPERADOR"
                    value={email} onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-lg py-3 pl-10 pr-4 text-sm focus:border-[#C9A84C]/50 outline-none transition-all"
                  />
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#C9A84C]/50" />
                  <input 
                    type="password" required placeholder="CONTRASEÑA ESTRATÉGICA"
                    value={password} onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-lg py-3 pl-10 pr-4 text-sm focus:border-[#C9A84C]/50 outline-none transition-all"
                  />
                </div>
              </div>

              <button 
                type="submit" disabled={status === "loading"}
                className="w-full py-4 bg-[#C9A84C] text-black font-bold rounded-lg uppercase text-[10px] tracking-[0.2em] hover:bg-[#C9A84C]/80 transition-all flex items-center justify-center gap-2"
              >
                {status === "loading" ? <Loader2 className="w-4 h-4 animate-spin" /> : "EJECUTAR ACCESO"}
              </button>

              {message && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  className={`flex items-center gap-3 p-4 rounded-lg text-[10px] border ${
                    status === "error" ? "bg-red-500/10 border-red-500/20 text-red-400" : "bg-green-500/10 border-green-500/20 text-green-400"
                  }`}
                >
                  {status === "error" ? <AlertCircle className="w-4 h-4" /> : <Activity className="w-4 h-4" />}
                  <span className="uppercase tracking-widest">{message}</span>
                </motion.div>
              )}
            </form>
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
      {/* Efecto de Grano */}
      <div className="fixed inset-0 z-50 pointer-events-none opacity-[0.03] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
      
      <OrbitalBackground />
      
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-[100] border-b border-white/5 bg-black/50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-[#C9A84C] rounded-lg flex items-center justify-center shadow-lg shadow-[#C9A84C]/20">
              <Shield className="text-black w-6 h-6" />
            </div>
            <span className="font-mono font-bold tracking-[0.3em] text-sm">VAULT STRATEGY</span>
          </div>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="px-6 py-2 border border-[#C9A84C]/30 text-[#C9A84C] text-[10px] font-bold tracking-[0.2em] rounded-full hover:bg-[#C9A84C] hover:text-black transition-all"
          >
            AUTORIZAR ACCESO
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative pt-40 pb-20 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#C9A84C]/20 bg-[#C9A84C]/5 mb-8"
          >
            <Activity className="w-3 h-3 text-[#C9A84C]" />
            <span className="text-[10px] font-mono text-[#C9A84C] tracking-widest uppercase">NASA JPL DE441 SYNC ACTIVE</span>
          </motion.div>

          <h1 className="text-6xl md:text-8xl font-mono font-bold tracking-tighter mb-8 leading-[0.9]">
            NO PREDIGA EL MERCADO. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-b from-[#C9A84C] to-[#C9A84C]/50 italic">
              SINCRONÍCELO.
            </span>
          </h1>

          <p className="text-white/40 max-w-2xl mx-auto text-lg mb-12 font-light leading-relaxed">
            Estrategias de alta frecuencia basadas en matemática orbital. 
            Precisión absoluta donde otros ven caos.
          </p>

          <div className="flex flex-col md:flex-row items-center justify-center gap-6">
            <button 
              onClick={() => setIsModalOpen(true)}
              className="group relative px-12 py-5 bg-[#C9A84C] text-black font-bold rounded-full overflow-hidden transition-transform active:scale-95"
            >
              <span className="relative z-10 flex items-center gap-3 text-xs tracking-[0.2em]">
                INICIAR PROTOCOLO <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </span>
            </button>
          </div>
        </div>
      </main>

      <AccessModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
