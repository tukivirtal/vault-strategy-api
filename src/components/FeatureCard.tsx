import { motion } from "motion/react";
import { LucideIcon } from "lucide-react";

interface FeatureCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  delay?: number;
}

export const FeatureCard = ({ title, description, icon: Icon, delay = 0 }: FeatureCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -5, scale: 1.02 }}
      className="glass-gold p-8 rounded-2xl group cursor-default transition-all duration-300 hover:glow-gold"
    >
      <div className="w-14 h-14 rounded-xl bg-gold/10 flex items-center justify-center mb-6 border border-gold/20 group-hover:bg-gold/20 transition-colors">
        <Icon className="w-7 h-7 text-gold" />
      </div>
      <h3 className="text-2xl font-mono font-bold mb-4 text-white group-hover:text-gold transition-colors">
        {title}
      </h3>
      <p className="text-white/60 leading-relaxed text-lg">
        {description}
      </p>
    </motion.div>
  );
};
