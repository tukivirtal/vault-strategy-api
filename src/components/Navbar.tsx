import { motion } from "motion/react";
import { Shield, Activity } from "lucide-react";

interface NavbarProps {
  onOpenModal: () => void;
}

export const Navbar = ({ onOpenModal }: NavbarProps) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-[100] h-24 flex items-center justify-between px-8 md:px-16 glass backdrop-blur-xl border-b border-white/5">
      <div className="flex items-center gap-4 group cursor-pointer">
        <div className="w-12 h-12 bg-gold/10 rounded-lg flex items-center justify-center border border-gold/20 group-hover:bg-gold/20 transition-all group-hover:glow-gold">
          <Shield className="w-6 h-6 text-gold" />
        </div>
        <div className="flex flex-col">
          <span className="font-mono font-bold text-xl tracking-tighter text-white group-hover:text-gold transition-colors">
            VAULT LOGIC
          </span>
          <div className="flex items-center gap-2 opacity-40 group-hover:opacity-100 transition-opacity">
            <Activity className="w-3 h-3 text-emerald-500 animate-pulse" />
            <span className="text-[10px] uppercase tracking-widest font-mono">
              NASA JPL SYNC: ACTIVE
            </span>
          </div>
        </div>
      </div>
      
      <div className="hidden md:flex items-center gap-12 text-sm font-mono uppercase tracking-widest text-white/60">
        <a href="#features" className="hover:text-gold transition-colors">Sincronización</a>
        <a href="#advantage" className="hover:text-gold transition-colors">Ventaja</a>
        <a href="#testimonials" className="hover:text-gold transition-colors">Operadores</a>
      </div>
      
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onOpenModal}
        className="px-8 py-3 bg-gold text-black font-mono font-bold text-sm uppercase tracking-widest rounded-lg hover:glow-gold transition-all"
      >
        Autorizar Acceso
      </motion.button>
    </nav>
  );
};
