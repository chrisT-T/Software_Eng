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
  CloseAction,
  ErrorAction,
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
  inDiffEditor: true,
};

onMounted(() => {
  editor.value = monaco.editor.create(monacoEditor.value, options);

  MonacoServices.install();

  const webSocket = new WebSocket("ws://localhost:30005");
  // define the connection(websocket) to the language server
  webSocket.onopen = () => {
    const socket = toSocket(webSocket);
    const reader = WebSocketMessageReader(socket);
    const writer = WebSocketMessageWriter(socket);
    const languageClient = new MonacoLanguageClient({
      clientOptions: {
        documentSelector: ["python"],
        errorHandler: {
          error: () => ({ action: ErrorAction.Continue }),
          closed: () => ({ action: CloseAction.DoNotRestart }),
        },
      },
      connectionProvider: {
        get: () => {
          return Promise.resolve(MessageTransports({ reader, writer }));
        },
      },
    });
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
