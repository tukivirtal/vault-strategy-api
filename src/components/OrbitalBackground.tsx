import { motion } from "motion/react";

export const OrbitalBackground = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[1000px]">
        {/* Concentric Orbits */}
        {[1, 2, 3, 4, 5].map((i) => (
          <motion.div
            key={i}
            initial={{ rotate: 0 }}
            animate={{ rotate: 360 }}
            transition={{
              duration: 20 + i * 10,
              repeat: Infinity,
              ease: "linear",
            }}
            className="absolute inset-0 border border-gold/10 rounded-full"
            style={{
              width: `${i * 20}%`,
              height: `${i * 20}%`,
              top: `${50 - i * 10}%`,
              left: `${50 - i * 10}%`,
            }}
          >
            {/* Planet/Point */}
            <div
              className="absolute w-1 h-1 bg-gold rounded-full"
              style={{
                top: "0",
                left: "50%",
                transform: "translateX(-50%)",
                boxShadow: "0 0 10px #D4AF37",
              }}
            />
          </motion.div>
        ))}
      </div>
      
      {/* Radial Gradient Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gold/5 blur-[120px] rounded-full" />
    </div>
  );
};
