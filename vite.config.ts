import { defineConfig } from "vitest/config";

// base: GitHub Pages serve una project page sotto https://<user>.github.io/gym-timer/,
// quindi gli asset vanno richiesti con il prefisso del repository. Se in futuro l'app
// passa a un dominio dedicato o a Cloudflare Pages, basta cambiare questa stringa in "/".
export default defineConfig({
  base: "/gym-timer/",
  build: {
    target: "es2020",
    outDir: "dist",
    assetsDir: "assets",
  },
  test: {
    include: ["src/**/*.test.ts"],
    environment: "node",
  },
});
