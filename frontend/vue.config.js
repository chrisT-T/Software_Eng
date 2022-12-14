const { defineConfig } = require("@vue/cli-service");
const MonacoWebpackPlugin = require("monaco-editor-webpack-plugin");
module.exports = defineConfig({
  transpileDependencies: true,
  css: {
    extract: false,
  },
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
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/terminal": {
        target: "ws://localhost:5005",
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          "^/terminal": "/",
        },
      },
      "/yjs": {
        target: "ws://localhost:1234",
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          "^/yjs": "/",
        },
      },
      "/communication": {
        target: "ws://localhost:6006",
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          "^/communication": "/",
        },
      },
      "/lsp": {
        target: "ws://localhost:8088",
        changeOrigin: true,
        ws: true,
      },
    },
  },
});
