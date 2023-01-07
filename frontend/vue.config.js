const { defineConfig } = require("@vue/cli-service");
const MonacoWebpackPlugin = require("monaco-editor-webpack-plugin");
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
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/pylsp": {
        target: "ws://localhost:30000",
        ws: true,
        changeOrigin: true,
        pathRewrite: function (path, req) {
          return path.replace("/pylsp", "");
        },
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
    },
  },
});
