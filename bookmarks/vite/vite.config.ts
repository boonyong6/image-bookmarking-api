import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      input: ["src/bookmarklet.ts"],
      output: {
        dir: "../dist/js",
        entryFileNames: "[name].js",
      },
    },
    sourcemap: true,
  },
});
