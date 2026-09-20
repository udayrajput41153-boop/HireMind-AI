import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    allowedHosts: [".e2b.app", "5173-iv4zu3q62ulck48pajb31.e2b.app"],
    proxy: { "/api": "http://localhost:8000" },
  },
  build: {
    outDir: "../backend/static",
    emptyOutDir: true,
  },
});
