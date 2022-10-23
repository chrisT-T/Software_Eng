<template>
  <div>
    <div class="monaco-editor" ref="monacoEditor"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, shallowRef, defineProps } from "vue";
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

const props = defineProps<{
  editorOption: monaco.editor.IStandaloneEditorConstructionOptions;
}>();

const editor = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null);
const monacoEditor = ref<HTMLElement | null>(null);

function setModel(model: monaco.editor.ITextModel) {
  editor.value?.setModel(model);
}

function getAllDecorationByClass(className: string) {
  return editor.value
    ?.getModel()
    ?.getAllDecorations()
    .filter(
      (decoration) => decoration.options.glyphMarginClassName == className
    );
}

function clearAllDecorationByClass(className: string) {
  const decorationsId = getAllDecorationByClass(className)?.map(
    (decoration) => decoration.id
  );
  if (decorationsId) {
    editor.value?.getModel()?.deltaDecorations(decorationsId, []);
  }
}

function existDecoration(className: string, lineNumber: number) {
  return getAllDecorationByClass(className)?.some(
    (decoration) => decoration.range.startLineNumber === lineNumber
  );
}

function addDecoration(
  className: string,
  lineNumber: number,
  hoverMessage: string
) {
  const old = getAllDecorationByClass(
    className
  ) as monaco.editor.IModelDecoration[];
  const oldId = old.map((decoration) => decoration.id);
  const index = old.findIndex(
    (decoration) => decoration.range.startLineNumber === lineNumber
  );

  if (index === -1) {
    old.push({
      id: "",
      ownerId: 0,
      range: new monaco.Range(lineNumber, 1, lineNumber, 1),
      options: {
        isWholeLine: true,
        glyphMarginClassName: className,
        stickiness:
          monaco.editor.TrackedRangeStickiness.NeverGrowsWhenTypingAtEdges,
        glyphMarginHoverMessage: {
          value: hoverMessage,
        },
      },
    });
    editor.value?.getModel()?.deltaDecorations(oldId, old);
  }
}

function removeDecoration(className: string, lineNumber: number) {
  const old = getAllDecorationByClass(
    className
  ) as monaco.editor.IModelDecoration[];
  const oldId = old.map((decoration) => decoration.id);
  const index = old.findIndex(
    (decoration) => decoration.range.startLineNumber === lineNumber
  );

  if (index !== -1) {
    old.splice(index, 1);
    editor.value?.getModel()?.deltaDecorations(oldId, old);
  }
}

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
