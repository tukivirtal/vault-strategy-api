import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';
import { fileURLToPath } from 'url';

// 1. Solución para __dirname en entornos modernos (ESM)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig(({ mode }) => {
  // Carga variables de entorno de forma segura
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
    // 2. Base corregida para despliegue en raíz
    base: '/',
    plugins: [
      react(),
      tailwindcss(), // Plugin para Tailwind v4
    ],
    define: {
      // Inyecta la API Key solo si existe en el entorno
      'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY || ''),
    },
    resolve: {
      alias: {
        // 3. Alias configurado correctamente sin errores de ruta
        '@': path.resolve(__dirname, './src'),
      },
    },
    build: {
      outDir: 'dist',
      emptyOutDir: true,
    },
    server: {
      hmr: true,
    },
  };
});
