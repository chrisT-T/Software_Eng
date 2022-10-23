<template>
  <div>
    <div class="monaco-editor-container" ref="monacoEditorContainer"></div>
  </div>
</template>

<script lang="ts" setup>
import {
  onMounted,
  ref,
  shallowRef,
  defineProps,
  onUnmounted,
  watch,
} from "vue";
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
const monacoEditorContainer = ref<HTMLElement | null>(null);

const breakPointClassName = "monaco-editor-breakpoint";
const shadowBreakpointClassName = "monaco-editor-breakpoint-shadow";
const focusLineClassName = "monaco-editor-focus-line";

watch(
  () => props.editorOption,
  (val: monaco.editor.IStandaloneEditorConstructionOptions) => {
    console.log(val);
    editor.value?.updateOptions(val);
  },
  { deep: true }
);

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

onMounted(() => {
  console.log("Monaco Editor Mounted");
  if (monacoEditorContainer.value !== null && props.editorOption !== null) {
    editor.value = monaco.editor.create(
      monacoEditorContainer.value,
      props.editorOption
    );
  } else {
    console.log("monacEeditorContainner is null or editorOption is null");
  }

  editor.value?.onMouseMove((e) => {
    const { target } = e;
    if (
      target.type === monaco.editor.MouseTargetType.GUTTER_GLYPH_MARGIN ||
      target.type === monaco.editor.MouseTargetType.GUTTER_LINE_DECORATIONS
    ) {
      if (!existDecoration(breakPointClassName, target.position.lineNumber)) {
        clearAllDecorationByClass(shadowBreakpointClassName);
        addDecoration(
          shadowBreakpointClassName,
          target.position.lineNumber,
          ""
        );
      }
    } else {
      clearAllDecorationByClass(shadowBreakpointClassName);
    }
  });

  editor.value?.onMouseLeave(() => {
    clearAllDecorationByClass(shadowBreakpointClassName);
  });

  editor.value?.onMouseDown((e) => {
    const { target } = e;
    console.log(target.type);
    if (
      target.type === monaco.editor.MouseTargetType.GUTTER_GLYPH_MARGIN ||
      target.type === monaco.editor.MouseTargetType.GUTTER_LINE_DECORATIONS
    ) {
      clearAllDecorationByClass(shadowBreakpointClassName);
      if (!existDecoration(breakPointClassName, target.position.lineNumber)) {
        addDecoration(breakPointClassName, target.position.lineNumber, "");
      } else {
        removeDecoration(
          shadowBreakpointClassName,
          target.range.startLineNumber
        );
        removeDecoration(breakPointClassName, target.position.lineNumber);
      }
    }
  });
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
  min-height: 800px;
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
</style>
