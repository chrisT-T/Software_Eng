<template>
  <div>
    <div class="monaco-editor" ref="monacoEditor"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, shallowRef } from "vue";
import * as monaco from "monaco-editor";
import {
  MonacoLanguageClient,
  MonacoServices,
  MessageTransports,
} from "monaco-languageclient";

import {
  toSocket,
  WebSocketMessageReader,
  WebSocketMessageWriter,
} from "vscode-ws-jsonrpc";

const editor = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null);
const monacoEditor = ref<HTMLElement | null>(null);

const options = {
  theme: "vs-dark",
  glyphMargin: true,
  language: "python",
  automaticLayout: true,
  bracketPairColorization: true,
  model: monaco.editor.createModel("import os", "python"),
};

function createLanguageClient(
  transports: MessageTransports
): MonacoLanguageClient {
  return new MonacoLanguageClient({
    name: "Python Language Client",
    clientOptions: {
      documentSelector: ["python"],
    },
    connectionProvider: {
      get: () => {
        return Promise.resolve(transports);
      },
    },
  });
}

onMounted(() => {
  editor.value = monaco.editor.create(monacoEditor.value, options);

  MonacoServices.install();

  const webSocket = new WebSocket("ws://localhost:30000");
  // define the connection(websocket) to the language server
  webSocket.onopen = () => {
    const socket = toSocket(webSocket);
    const reader = new WebSocketMessageReader(socket);
    const writer = new WebSocketMessageWriter(socket);
    const languageClient = createLanguageClient({ reader, writer });
    languageClient.start();
    reader.onClose(() => languageClient.stop());
    console.log("websocket on open");
  };
});
</script>

<style>
.monaco-editor {
  height: 100%;
  width: 100%;
  min-height: 800px;
  text-align: left;
}
</style>
