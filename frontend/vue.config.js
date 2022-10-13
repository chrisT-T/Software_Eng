const { defineConfig } = require("@vue/cli-service");
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        components: "@/components",
      },
      fallback: {
        path: false,
      },
    },
    plugins: [
      new MonacoWebpackPlugin({
        languages: ["python"],
      }),
    ],
  },
});
