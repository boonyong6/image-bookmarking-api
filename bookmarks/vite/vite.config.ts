import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      input: ["src/bookmarklet.ts", "src/image-detail.ts"],
      output: {
        dir: "../dist/js",
        entryFileNames: "[name].js",
        manualChunks: {
          vendor: ["js-cookie"],
        },
      },
    },
    sourcemap: true,
  },
});
