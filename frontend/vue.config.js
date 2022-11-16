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
      "/auth": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/pylsp": {
        target: "ws://localhost:30000",
        ws: true,
        changeOrigin: true,
        pathRewrite: function (path, req) { return path.replace('/pylsp', '') }
      }
    },
  },
});
