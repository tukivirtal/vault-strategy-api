import { useEffect } from "react";
import { motion } from "motion/react";
import { 
  Shield, 
  Zap, 
  FileText, 
  ArrowRight, 
  Globe, 
  CheckCircle2,
  XCircle,
  AlertCircle
} from "lucide-react";

import { Navbar } from "./components/Navbar";
import { OrbitalBackground } from "./components/OrbitalBackground";
import { FeatureCard } from "./components/FeatureCard";
import { TerminalLog } from "./components/TerminalLog";

export default function App() {
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
      document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="relative min-h-screen bg-black overflow-x-hidden">
      <div className="noise-overlay" />
      
      <Navbar />

      <main className="relative pt-24">
        {/* Hero Section */}
        <section className="relative min-h-[90vh] flex flex-col items-center justify-center px-8 md:px-16 py-24">
          <OrbitalBackground />
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="relative z-10 text-center max-w-6xl"
          >
            <div className="flex items-center justify-center gap-3 mb-8">
              <div className="px-4 py-1.5 rounded-full border border-gold/20 bg-gold/5 flex items-center gap-2">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                <span className="text-[10px] md:text-xs font-mono uppercase tracking-[0.2em] text-gold font-bold">
                  🛰 NASA JPL DE441 // SINCRONIZACIÓN ACTIVA
                </span>
              </div>
            </div>

       {/* TÍTULO CORREGIDO: Forzamos el espaciado natural anulando el "tighter" global */}
            <h1 className="text-6xl md:text-8xl lg:text-[8.5rem] font-sans font-black tracking-normal leading-[0.95] mb-12 flex flex-col items-center text-center">
              <motion.span
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                className="text-gradient-gold pb-2"
              >
                NO PREDIGA EL MERCADO
              </motion.span>
              <motion.span
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8, duration: 1 }}
                className="text-white italic mt-2 md:mt-4 tracking-wide"
              >
                SINCRONÍCELO
              </motion.span>
            </h1>

            <p className="text-xl md:text-3xl text-white/60 font-light leading-relaxed max-w-4xl mx-auto mb-16 px-4">
              Los líderes corporativos no dependen de la intuición.<br />
              <span className="text-white font-medium">Vault Logic</span> convierte matemática orbital en decisiones ejecutivas de alta precisión.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-8">
              {/* Botón convertido en enlace directo */}
              <motion.a
                href="portal.html"
                whileHover={{ scale: 1.05, x: 5 }}
                whileTap={{ scale: 0.95 }}
                className="group px-12 py-6 bg-gold text-black font-sans font-black text-xl uppercase tracking-widest rounded-xl flex items-center gap-4 hover:glow-gold-strong transition-all inline-flex"
              >
                Autorizar Acceso
                <ArrowRight className="w-6 h-6 group-hover:translate-x-2 transition-transform" />
              </motion.a>
              
              <div className="flex flex-col items-start gap-1">
                <span className="text-2xl font-mono font-bold text-white">+847</span>
                <span className="text-xs font-mono uppercase tracking-widest text-white/40">
                  Terminales activas en 23 países
                </span>
              </div>
            </div>
          </motion.div>
        </section>

        {/* Features Section */}
        <section id="features" className="relative py-32 px-8 md:px-16 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={Shield}
              title="Protección de Capital"
              description="Algoritmos de sincronización diseñados para preservar la liquidez en ventanas de alta volatilidad orbital."
              delay={0.1}
            />
            <FeatureCard
              icon={Zap}
              title="Ejecución Instantánea"
              description="Conexión directa con los efemérides de la NASA para una precisión de milisegundos en la toma de decisiones."
              delay={0.2}
            />
            <FeatureCard
              icon={FileText}
              title="Reportes Ejecutivos"
              description="Documentación técnica detallada de cada movimiento, alineada con los estándares de cumplimiento global."
              delay={0.3}
            />
          </div>
        </section>

        {/* Advantage Section */}
        <section id="advantage" className="relative py-32 px-8 md:px-16 bg-white/5 border-y border-white/5">
          <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-24 items-center">
            <div>
              <h2 className="text-5xl md:text-7xl font-sans font-black mb-12 leading-tight tracking-tighter">
                LA VENTAJA <span className="text-gold">ASIMÉTRICA</span>
              </h2>
              <div className="space-y-12">
                <div className="flex gap-8">
                  <div className="text-6xl font-sans font-black text-gold/20">10</div>
                  <div>
                    <h4 className="text-2xl font-sans font-bold mb-2 tracking-tight">AÑOS DE PROYECCIÓN</h4>
                    <p className="text-white/60 text-lg">Historial calibrado por perfil ejecutivo individual, garantizando una alineación total con su estrategia.</p>
                  </div>
                </div>
                <div className="flex gap-8">
                  <div className="text-6xl font-sans font-black text-gold/20">01</div>
                  <div>
                    <h4 className="text-2xl font-sans font-bold mb-2 tracking-tight">DIRECTIVA OPERATIVA</h4>
                    <p className="text-white/60 text-lg">No entregamos datos crudos. Entregamos directivas claras y accionables para su mesa de operaciones.</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="glass-gold rounded-3xl p-12 overflow-hidden relative">
              <div className="absolute top-0 right-0 p-8 opacity-10">
                <Globe className="w-64 h-64 text-gold" />
              </div>
              
              <h3 className="text-2xl font-sans font-bold mb-8 uppercase tracking-widest text-gold">Comparativa de Sistema</h3>
              <div className="space-y-6">
                <div className="grid grid-cols-2 pb-4 border-b border-white/10 font-mono text-xs uppercase tracking-widest text-white/40">
                  <span>Métrica</span>
                  <div className="flex justify-between">
                    <span>Vault Logic</span>
                    <span>Tradicional</span>
                  </div>
                </div>
                
                {[
                  { label: "Output", vault: "Directiva", trad: "Datos" },
                  { label: "Interpretación", vault: "Automática", trad: "Manual" },
                  { label: "Perfil Natal", vault: "Calibrado", trad: "Genérico" },
                  { label: "Base de Datos", vault: "NASA JPL", trad: "Feeds" },
                ].map((item, i) => (
                  <div key={i} className="grid grid-cols-2 py-4 items-center group">
                    <span className="font-mono text-lg group-hover:text-gold transition-colors">{item.label}</span>
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-2 text-gold">
                        <CheckCircle2 className="w-5 h-5" />
                        <span className="font-bold">{item.vault}</span>
                      </div>
                      <div className="flex items-center gap-2 text-white/20">
                        <XCircle className="w-5 h-5" />
                        <span>{item.trad}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section id="testimonials" className="relative py-32 px-8 md:px-16 max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-6xl font-sans font-black mb-24 text-center tracking-tighter">
            LOGS DE <span className="text-gold">OPERADORES</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <TerminalLog
              operator="C.M. — Director Comercial, México"
              status="GENESIS ACTIVO // 14 MESES"
              message="Cerré la negociación más grande de mi carrera en una ventana de 3 días que el sistema marcó como óptima. Coincidencia o no, fue real."
              delay={0.1}
            />
            <TerminalLog
              operator="R.V. — Private Equity, Madrid"
              status="SINCRONIZACIÓN NIVEL 4"
              message="La precisión en los puntos de inflexión del mercado es aterradora. Vault Logic se ha convertido en mi brújula operativa diaria."
              delay={0.2}
            />
            <TerminalLog
              operator="A.L. — Hedge Fund Manager, NY"
              status="TERMINAL ACTIVA"
              message="Finalmente un sistema que entiende que el tiempo no es lineal, sino cíclico y orbital. Una ventaja injusta en el mercado actual."
              delay={0.3}
            />
            <TerminalLog
              operator="S.T. — CEO Tech, Silicon Valley"
              status="CALIBRACIÓN COMPLETA"
              message="La integración de mi perfil natal con los movimientos de mercado ha cambiado mi forma de entender el riesgo corporativo."
              delay={0.4}
            />
          </div>
        </section>

      {/* CTA Section */}
        <section className="relative py-48 px-8 md:px-16 text-center">
          <div className="absolute inset-0 bg-gold/5 blur-[150px] rounded-full scale-50" />
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative z-10"
          >
            {/* ARREGLADO: Cambiamos a tracking-wide para separar las letras */}
            <h2 className="text-6xl md:text-9xl font-sans font-black mb-12 tracking-wide">
              ¿ESTÁ <span className="text-gold">LISTO?</span>
            </h2>
            <p className="text-2xl md:text-4xl text-white/40 font-light mb-16 max-w-4xl mx-auto">
              El mercado no espera. La sincronización orbital es ahora.
            </p>
            <motion.a
              href="portal.html"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="inline-block px-16 py-8 bg-white text-black font-sans font-black text-2xl uppercase tracking-[0.2em] rounded-2xl hover:bg-gold hover:text-black hover:glow-gold-strong transition-all"
            >
              Autorizar Acceso
            </motion.a>
          </motion.div>
        </section>
      </main>

    {/* Footer Ampliado y Mejorado */}
 {/* Footer Ampliado: Contacto y Enlaces Legales */}
      <footer className="relative py-32 px-8 md:px-16 border-t border-white/5 bg-black">
        <div className="max-w-7xl mx-auto">
          {/* Cambiamos la cuadrícula a 5 columnas para hacer espacio a "Contacto" */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-12 md:gap-16 mb-24">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center gap-4 mb-10">
                <Shield className="w-12 h-12 text-gold" />
                <span className="font-sans font-black text-4xl tracking-tighter">VAULT LOGIC</span>
              </div>
              <p className="text-white/40 text-xl md:text-2xl max-w-xl leading-relaxed font-light">
                Transformando matemática orbital en directivas operativas de alta precisión para el liderazgo global.
              </p>
            </div>
            
            {/* Columna Legal conectada a tus futuros archivos HTML */}
            <div>
              <h5 className="font-sans font-bold text-base uppercase tracking-widest text-gold mb-8">Legal</h5>
              <ul className="space-y-6 text-white/50 font-mono text-sm">
                <li><a href="privacidad.html" className="hover:text-white transition-colors">Privacidad</a></li>
                <li><a href="terminos.html" className="hover:text-white transition-colors">Términos</a></li>
                <li><a href="garantia.html" className="hover:text-white transition-colors">Garantía</a></li>
              </ul>
            </div>

            {/* NUEVA COLUMNA DE CONTACTO */}
            <div>
              <h5 className="font-sans font-bold text-base uppercase tracking-widest text-gold mb-8">Contacto</h5>
              <ul className="space-y-6 text-white/50 font-mono text-sm">
                <li>
                  <span className="block text-[10px] text-white/30 uppercase mb-2">Soporte Ejecutivo</span>
                  <a href="mailto:contact@emotionalvaults.com" className="hover:text-gold transition-colors break-words">
                    contact@emotionalvaults.com
                  </a>
                </li>
              </ul>
            </div>
            
            <div>
              <h5 className="font-sans font-bold text-base uppercase tracking-widest text-gold mb-8">Sistema</h5>
              <ul className="space-y-6 text-white/50 font-mono text-sm">
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                  NASA JPL DE441: ONLINE
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                  LATENCIA: 12ms
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                  ENCRIPTACIÓN: AES-256
                </li>
              </ul>
            </div>
          </div>
          
          <div className="flex flex-col md:flex-row justify-between items-center gap-8 pt-16 border-t border-white/5 font-mono text-xs uppercase tracking-widest">
            <div className="flex flex-col gap-6">
              <div className="flex items-center gap-4 p-6 bg-gold/5 border border-gold/20 rounded-xl max-w-3xl">
                <AlertCircle className="w-6 h-6 text-gold shrink-0" />
                <p className="text-[10px] md:text-xs text-white/60 normal-case leading-relaxed">
                  <span className="text-gold font-bold uppercase tracking-widest mr-2">Advertencia de Riesgo:</span>
                  La sincronización orbital y el uso de efemérides de la NASA JPL DE441 son herramientas de análisis técnico avanzado. El trading implica un riesgo sustancial de pérdida.
                </p>
              </div>
              <div className="flex items-center gap-4 text-white/40">
                <span>© 2026 VAULT LOGIC — TODOS LOS DERECHOS RESERVADOS</span>
                <span className="hidden md:inline">|</span>
                <span className="text-gold font-bold">SISTEMA: OPERATIVO</span>
              </div>
            </div>
            <div className="flex gap-10 text-white/40">
              <span className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                NASA SYNC: ACTIVO
              </span>
              <span>LATENCIA: 12ms</span>
            </div>
          </div>
        </div>
      </footer>

      {/* Custom Cursor Glow (Subtle) */}
      <div className="fixed inset-0 pointer-events-none z-[9999] mix-blend-screen opacity-50">
        <div className="absolute w-64 h-64 bg-gold/10 blur-[100px] rounded-full -translate-x-1/2 -translate-y-1/2" style={{ left: 'var(--mouse-x, 50%)', top: 'var(--mouse-y, 50%)' }} />
      </div>
    </div>
  );
}
