<template>
  <div class="monaco-editor-container" ref="monacoEditorContainer"></div>
</template>

<script lang="ts" setup>
import {
  onMounted,
  ref,
  shallowRef,
  defineProps,
  onUnmounted,
  defineEmits,
  defineExpose,
} from "vue";
import * as monaco from "monaco-editor";
import {
  MonacoLanguageClient,
  MonacoServices,
  CloseAction,
  ErrorAction,
  MessageTransports,
} from "monaco-languageclient";

import {
  toSocket,
  WebSocketMessageReader,
  WebSocketMessageWriter,
} from "vscode-ws-jsonrpc";
import * as common from "./common";

const props = defineProps<{
  editorOption: monaco.editor.IStandaloneEditorConstructionOptions;
}>();

const emit = defineEmits<{
  (e: "saveFile"): void;
  (e: "modified"): void;
  (e: "debug"): void;
}>();

defineExpose({
  locateLine,
});

const editor = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null);
const monacoEditorContainer = ref<HTMLElement | null>(null);

function getAllDecorationByClass(className: string) {
  return editor.value
    ?.getModel()
    ?.getAllDecorations()
    .filter(
      (decoration) => decoration.options.glyphMarginClassName === className
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

function locateLine(lineNumber: number) {
  const lineCount = editor.value?.getModel()?.getLineCount() as number;
  if (lineCount < 1 || lineNumber > lineCount) {
    console.error("line number is not valid");
  }
  editor.value?.revealLineInCenter(lineNumber);
  editor.value?.setPosition({ lineNumber, column: 1 });
}

function createPythonLanguageClient(
  transports: MessageTransports
): MonacoLanguageClient {
  return new MonacoLanguageClient({
    name: "Python Language Client",
    clientOptions: {
      documentSelector: ["python"],
      errorHandler: {
        error: () => ({ action: ErrorAction.Continue }),
        closed: () => ({ action: CloseAction.DoNotRestart }),
      },
    },
    connectionProvider: {
      get: () => {
        return Promise.resolve(transports);
      },
    },
  });
}

onMounted(() => {
  console.log("Monaco Editor Mounted");
  if (monacoEditorContainer.value !== null && props.editorOption !== null) {
    editor.value = monaco.editor.create(
      monacoEditorContainer.value,
      props.editorOption
    );
  } else {
    console.error("monacEeditorContainner is null or editorOption is null");
  }

  editor.value?.onDidChangeModelContent(() => {
    emit("modified");
  });

  editor.value?.addAction({
    id: "save-current-file",
    label: "save",
    keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS],
    precondition: undefined,
    keybindingContext: undefined,
    contextMenuGroupId: undefined,
    contextMenuOrder: 1.5,
    run: function () {
      emit("saveFile");
    },
  });

  editor.value?.addAction({
    id: "debug-current-file",
    label: "debug",
    keybindings: [monaco.KeyCode.F5],
    precondition: undefined,
    keybindingContext: undefined,
    contextMenuGroupId: undefined,
    contextMenuOrder: 1.5,
    run: function () {
      emit("debug");
    },
  });

  editor.value?.onMouseMove((e) => {
    const { target } = e;
    if (
      target.type === monaco.editor.MouseTargetType.GUTTER_GLYPH_MARGIN ||
      target.type === monaco.editor.MouseTargetType.GUTTER_LINE_DECORATIONS
    ) {
      if (
        !existDecoration(common.breakPointClassName, target.position.lineNumber)
      ) {
        clearAllDecorationByClass(common.shadowBreakpointClassName);
        addDecoration(
          common.shadowBreakpointClassName,
          target.position.lineNumber,
          ""
        );
      }
    } else {
      clearAllDecorationByClass(common.shadowBreakpointClassName);
    }
  });

  editor.value?.onMouseLeave(() => {
    clearAllDecorationByClass(common.shadowBreakpointClassName);
  });

  editor.value?.onMouseDown((e) => {
    const { target } = e;
    if (
      target.type === monaco.editor.MouseTargetType.GUTTER_GLYPH_MARGIN ||
      target.type === monaco.editor.MouseTargetType.GUTTER_LINE_DECORATIONS
    ) {
      clearAllDecorationByClass(common.shadowBreakpointClassName);
      if (
        !existDecoration(common.breakPointClassName, target.position.lineNumber)
      ) {
        addDecoration(
          common.breakPointClassName,
          target.position.lineNumber,
          ""
        );
      } else {
        removeDecoration(
          common.shadowBreakpointClassName,
          target.range.startLineNumber
        );
        removeDecoration(
          common.breakPointClassName,
          target.position.lineNumber
        );
      }
    }
  });

  // initialize language server

  // MonacoServices.install();

  let lspUrl = "/lsp";
  // python language server
  if (props.editorOption.language === "python") {
    lspUrl = "ws://" + location.host + "/pylsp";
  }

  // create websocket
  const webSocket = new WebSocket(lspUrl);
  webSocket.onopen = () => {
    const socket = toSocket(webSocket);
    const reader = new WebSocketMessageReader(socket);
    const writer = new WebSocketMessageWriter(socket);
    const languageClient = createPythonLanguageClient({ reader, writer });
    languageClient.start();
    reader.onClose(() => languageClient.stop());
  };
});

onUnmounted(() => {
  console.log("Monaco Editor Destroyed");
  editor.value?.dispose();
});
</script>

<style>
.monaco-editor-container {
  height: 100%;
  width: 100%;
  min-height: 100px;
  text-align: left;
}

.monaco-editor-breakpoint {
  margin-left: 10%;
  border-radius: 100%;
  background: radial-gradient(
    circle at center,
    #ff0000 0%,
    #ff0000 30%,
    transparent 31%,
    transparent 100%
  );
}

.monaco-editor-breakpoint-shadow {
  margin-left: 10%;
  border-radius: 100%;
  background: radial-gradient(
    circle at center,
    rgba(255, 0, 0, 0.5) 0%,
    rgba(255, 0, 0, 0.5) 30%,
    transparent 31%,
    transparent 100%
  );
}

.monaco-editor-focus-line {
  background: rgba(255, 0, 0, 0.3);
}
</style>
