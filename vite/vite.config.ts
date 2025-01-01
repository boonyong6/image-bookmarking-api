import { globSync } from "glob";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

// https://rollupjs.org/configuration-options/#input
const rollupInput = Object.fromEntries(
  globSync("src/**/*.ts", { ignore: "src/**/*.d.ts" }).map((file) => [
    path.relative(
      "src",
      file.slice(0, file.length - path.extname(file).length)
    ),
    fileURLToPath(new URL(file, import.meta.url)),
  ])
);
// console.info("Rollup input:", rollupInput);

export default defineConfig({
  build: {
    rollupOptions: {
      input: rollupInput,
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
