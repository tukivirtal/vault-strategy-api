import { motion, AnimatePresence } from "motion/react";
import { X, Shield, Cpu, CheckCircle2, AlertCircle } from "lucide-react";
import { useState, useEffect } from "react";

interface AccessModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AccessModal = ({ isOpen, onClose }: AccessModalProps) => {
  const [step, setStep] = useState(0);
  const [logs, setLogs] = useState<string[]>([]);

  const steps = [
    "Iniciando protocolo de enlace seguro...",
    "Sincronizando con NASA JPL DE441...",
    "Verificando integridad de terminal...",
    "Calculando vectores de mercado orbital...",
    "Acceso autorizado. Bienvenido, Operador."
  ];

  useEffect(() => {
    if (isOpen) {
      setStep(0);
      setLogs([]);
      let currentStep = 0;
      const interval = setInterval(() => {
        if (currentStep < steps.length) {
          setLogs(prev => [...prev, steps[currentStep]]);
          setStep(currentStep + 1);
          currentStep++;
        } else {
          clearInterval(interval);
        }
      }, 800);
      return () => clearInterval(interval);
    }
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-8">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/90 backdrop-blur-md"
          />
          
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="relative w-full max-w-2xl glass-gold rounded-3xl overflow-hidden border border-gold/30 shadow-2xl"
          >
            <div className="p-8 md:p-12">
              <button 
                onClick={onClose}
                className="absolute top-6 right-6 p-2 text-white/40 hover:text-gold transition-colors"
              >
                <X className="w-6 h-6" />
              </button>

              <div className="flex items-center gap-4 mb-12">
                <div className="w-12 h-12 bg-gold/10 rounded-xl flex items-center justify-center border border-gold/20">
                  <Shield className="w-6 h-6 text-gold" />
                </div>
                <div>
                  <h3 className="text-2xl font-mono font-bold text-white uppercase tracking-tighter">
                    Protocolo de Autorización
                  </h3>
                  <p className="text-xs font-mono text-white/40 uppercase tracking-widest">
                    Nivel de Seguridad: ALPHA-9
                  </p>
                </div>
              </div>

              <div className="space-y-4 mb-12 font-mono text-sm">
                {logs.map((log, i) => (
                  <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={i}
                    className="flex items-center gap-3"
                  >
                    {i === logs.length - 1 && i < steps.length - 1 ? (
                      <div className="w-1.5 h-1.5 bg-gold rounded-full animate-pulse" />
                    ) : (
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    )}
                    <span className={i === logs.length - 1 ? "text-white" : "text-white/40"}>
                      {log}
                    </span>
                  </motion.div>
                ))}
                
                {step === steps.length && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-8 p-4 bg-gold/5 border border-gold/20 rounded-lg flex gap-3"
                  >
                    <AlertCircle className="w-5 h-5 text-gold shrink-0" />
                    <p className="text-[10px] text-white/60 leading-relaxed uppercase tracking-wider">
                      <span className="text-gold font-bold">Aviso de Cumplimiento:</span> Al autorizar el acceso, usted reconoce que los datos orbitales son para fines informativos y no constituyen asesoría financiera directa.
                    </p>
                  </motion.div>
                )}
              </div>

              {step === steps.length ? (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-8"
                >
                  <div className="p-6 bg-emerald-500/5 border border-emerald-500/20 rounded-xl">
                    <p className="text-emerald-500 font-mono text-sm leading-relaxed">
                      Su terminal ha sido vinculada con éxito. Para completar el acceso a la red privada de Vault Logic, un oficial de enlace se pondrá en contacto con usted en las próximas 24 horas.
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <span className="block text-[10px] text-white/40 uppercase mb-1">ID de Sesión</span>
                      <span className="font-mono text-xs text-white">VL-9928-XJ-2026</span>
                    </div>
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <span className="block text-[10px] text-white/40 uppercase mb-1">Encriptación</span>
                      <span className="font-mono text-xs text-white">Quantum AES-512</span>
                    </div>
                  </div>

                  <button
                    onClick={() => {
                      onClose();
                      // Si quieres que tras el modal vaya a tu portal real, descomenta la siguiente línea:
                      // window.location.href = "portal.html";
                    }}
                    className="w-full py-4 bg-gold text-black font-mono font-bold uppercase tracking-widest rounded-xl hover:glow-gold transition-all"
                  >
                    Cerrar Terminal
                  </button>
                </motion.div>
              ) : (
                <div className="flex flex-col items-center justify-center py-12 gap-6">
                  <div className="relative">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                      className="w-24 h-24 border-2 border-gold/20 border-t-gold rounded-full"
                    />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Cpu className="w-8 h-8 text-gold animate-pulse" />
                    </div>
                  </div>
                  <span className="font-mono text-xs text-gold animate-pulse uppercase tracking-[0.3em]">
                    Procesando...
                  </span>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
