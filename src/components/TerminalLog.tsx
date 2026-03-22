import { motion } from "motion/react";

interface TerminalLogProps {
  operator: string;
  status: string;
  message: string;
  delay?: number;
}

export const TerminalLog = ({ operator, status, message, delay = 0 }: TerminalLogProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      className="font-mono text-sm md:text-base border-l-2 border-gold/30 pl-6 py-4 mb-8 group hover:border-gold transition-colors"
    >
      <div className="flex flex-wrap gap-4 mb-3 opacity-60 group-hover:opacity-100 transition-opacity">
        <span className="text-gold font-bold uppercase tracking-widest">
          {">"} OPERADOR: {operator}
        </span>
        <span className="text-white/40 uppercase tracking-widest">
          {">"} ESTADO: {status}
        </span>
      </div>
      <p className="text-white/80 italic leading-relaxed max-w-2xl group-hover:text-white transition-colors">
        "{message}"
      </p>
    </motion.div>
  );
};
