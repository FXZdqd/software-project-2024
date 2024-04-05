import vue from '@vitejs/plugin-vue'
import { UserConfig, ConfigEnv, loadEnv, defineConfig } from "vite";

import path from "path";
const pathSrc = path.resolve(__dirname, "src");

// https://vitejs.dev/config/
export default defineConfig(({ mode }: ConfigEnv): UserConfig => {
  const env = loadEnv(mode, process.cwd());
  const { VITE_APP_BASE_API, VITE_APP_DEV_URL } = env;
  return {
    resolve: {
      alias: {
        "@": pathSrc,
      },
    },
    plugins: [
      vue()
    ],
    css: {
      // CSS 预处理器
      preprocessorOptions: {
        //define global scss variable
        scss: {
          javascriptEnabled: true,//开启sass
          additionalData: '@import "@/styles/variables.scss";'
        }
      }
    },
    server: {
      cors: true,
      open: true,
      proxy: {
        '/api': {
          target: 'http://39.109.126.173:39000',   //代理接口
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: false,
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true,
        },
      },
    },
  }
})
