<template>
  <div class="editor-panel-container">
    <el-tabs
      v-model="editableTabsValue"
      type="card"
      class="demo-tabs"
      closable
      @tab-remove="removeTab"
    >
      <el-tab-pane
        v-for="item in editableTabs"
        :key="item.index"
        :label="item.title"
        :name="item.index"
      >
        <MonacoEditor
          ref="monacoEditors"
          :name="item.index"
          :editor-option="getOption(item.index)"
          :container-subdomain="`testid`"
          @modified="fileModified"
          @saveFile="saveFile"
          @debug="startDebug"
        ></MonacoEditor>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import MonacoEditor from "@/components/MonacoEditorPanel/MonacoEditor.vue";
import { ta } from "element-plus/es/locale";
import { ElMessage, ElMessageBox } from "element-plus";
import * as Y from "yjs";
import { MonacoBinding } from "y-monaco";
import { WebsocketProvider } from "y-websocket";
import * as monaco from "monaco-editor";
import {
  ref,
  defineEmits,
  defineExpose,
  defineProps,
  shallowRef,
  watch,
} from "vue";
import * as common from "./common";
import { NullLogger } from "vscode-jsonrpc";

export interface FileInfo {
  path: string;
  modified: boolean;
  index: number;
  show: boolean;
  options: monaco.editor.IStandaloneEditorConstructionOptions;
}

export interface TabInfo {
  title: string;
  fileName: string;
  parentPath: string;
  dup: boolean;
  modified: boolean;
  index: string;
}

const props = defineProps<{
  theme: string;
}>();

const emit = defineEmits<{
  (e: "saveFile", path: string, value: string): void;
  (e: "startDebug", path: string): void;
}>();

defineExpose({
  addFile,
  renameFile,
  deleteFile,
  getBreakpoints,
  focusLine,
  clearFocusLine,
  disposePanel,
});

watch(
  () => props.theme,
  (val: string) => {
    setTheme(val);
  }
);

const fileInfos = new Array<FileInfo>();

let tabIndex = 0;
const editableTabsValue = ref("0");
const editableTabs = ref<Array<TabInfo>>(new Array<TabInfo>());
const monacoEditors = shallowRef([]);

const getOption = (index: string) => {
  let fileIndex = fileInfos.findIndex(
    (fileInfo) => fileInfo.index.toString() === index
  );
  return fileInfos[fileIndex].options;
};

function getEditorByIndex(index: string) {
  let editorIndex = monacoEditors.value.findIndex(
    (item) => item.$attrs["name"] === index
  );
  return monacoEditors.value[editorIndex];
}

function isDup(fileName: string): boolean {
  let flag = false;
  editableTabs.value.forEach((tab, index) => {
    if (tab.fileName === fileName) {
      flag = true;
    }
  });
  return flag;
}

function updateTitle(curTab: TabInfo) {
  if (curTab.dup) {
    curTab.title = curTab.fileName + " " + curTab.parentPath;
  } else {
    curTab.title = curTab.fileName;
  }
  if (curTab.modified) {
    curTab.title = "* " + curTab.title;
  }
  return;
}

function updateOtherTitle(fileName: string) {
  let count = 0;
  editableTabs.value.forEach((item, index) => {
    if (item.fileName === fileName) {
      count++;
    }
  });

  editableTabs.value.forEach((item, index) => {
    if (item.fileName === fileName) {
      if (count > 1) {
        item.dup = true;
        updateTitle(item);
      } else {
        item.dup = false;
        updateTitle(item);
      }
    }
  });
}

const addTab = (fileName: string, parentPath: string, index: string) => {
  let dup = isDup(fileName);
  let newTab = {
    title: "",
    fileName: fileName,
    parentPath: parentPath,
    dup: dup,
    modified: false,
    index: index,
  };
  updateTitle(newTab);
  editableTabs.value.push(newTab);
  if (dup) {
    updateOtherTitle(fileName);
  }
  editableTabsValue.value = index;
};

const justRemoveTab = (targetIndex: string) => {
  const tabs = editableTabs.value;
  let activeIndex = editableTabsValue.value;
  let tabIndex = tabs.findIndex((item) => item.index === targetIndex);
  if (activeIndex === targetIndex) {
    const nextTab = tabs[tabIndex + 1] || tabs[tabIndex - 1];
    if (nextTab) {
      activeIndex = nextTab.index;
    } else {
      activeIndex = "0";
    }
  }

  editableTabsValue.value = activeIndex;
  let dup = tabs[tabIndex].dup;
  let fileName = tabs[tabIndex].fileName;
  editableTabs.value.splice(tabIndex, 1);
  if (dup) {
    updateOtherTitle(fileName);
  }

  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === targetIndex
  );
  fileInfos[fileIndex].show = false;
};

function getLanguageByFileName(fileName: string) {
  let fileSplit = fileName.split(".");
  let fileSuffix = fileSplit[fileSplit.length - 1] as string;
  let language = "plaintext";
  if (fileSplit.length === 1) {
    if (common.nameTypeDict.has(fileSplit[0])) {
      language = common.nameTypeDict.get(fileSplit[0]) as string;
    }
  } else {
    if (common.suffixTypeDict.has(fileSuffix)) {
      language = common.suffixTypeDict.get(fileSuffix) as string;
    }
  }
  return language;
}

function addFile(path: string, value: string) {
  console.log("addFile", path);
  let fileName = path.split("/").pop() as string;
  let language = getLanguageByFileName(fileName);
  let parentPath = path.substring(0, path.length - fileName.length) as string;
  console.log(parentPath);
  let fileIndex = fileInfos.findIndex((fileInfo) => fileInfo.path === path);

  if (fileIndex === -1) {
    fileInfos.push({
      path: path,
      modified: false,
      index: ++tabIndex,
      show: true,
      options: {
        theme: props.theme, // 'vs', 'vs-dark', 'hc-black', 'hc-light'
        glyphMargin: true,
        language: language,
        automaticLayout: true,
        bracketPairColorization: {
          enabled: true,
          independentColorPoolPerBracketType: true,
        },
        model: monaco.editor.createModel(
          value,
          language,
          monaco.Uri.file(path)
        ),
      },
    });
    addTab(fileName, parentPath, tabIndex.toString());
    // setTimeout(() => {
    //   const ydoc = new Y.Doc();
    //   const provider = new WebsocketProvider(
    //     "ws://localhost:1234",
    //     "test",
    //     ydoc
    //   );
    //   const awareness = provider.awareness;
    //   // awareness.setLocalStateField("user", {
    //   // name:
    //   // })
    //   const type = ydoc.getText("monaco");
    //   let editor = getEditorByIndex(tabIndex.toString()).getEditor();
    //   const monacoBinding = new MonacoBinding(
    //     type,
    //     editor.getModel(),
    //     new Set([editor]),
    //     provider.awareness
    //   );
    // }, 5);
  } else if (fileInfos[fileIndex].show === false) {
    fileInfos[fileIndex].show = true;
    let model = fileInfos[fileIndex].options.model;
    let decorations = model?.getAllDecorations();
    model?.setValue(value);
    if (decorations) {
      model?.deltaDecorations([], decorations);
    }
    addTab(fileName, parentPath, fileInfos[fileIndex].index.toString());
  } else {
    editableTabsValue.value = fileInfos[fileIndex].index.toString();
  }
}

function setTheme(theme: string) {
  fileInfos.forEach((item) => {
    item.options.theme = theme;
  });
  monaco.editor.setTheme(theme);
}

function renameFile(oldPath: string, newPath: string) {
  let fileIndex = fileInfos.findIndex((item) => item.path === oldPath);
  if (fileIndex === -1) {
    return;
  }
  let value = fileInfos[fileIndex].options.model?.getValue() as string;

  deleteFile(fileInfos[fileIndex].path);
  addFile(newPath, value);
}

function deleteFile(path: string) {
  let fileIndex = fileInfos.findIndex((item) => item.path === path);
  if (fileIndex === -1) {
    return;
  }
  fileInfos[fileIndex].options.model?.dispose();
  justRemoveTab(fileInfos[fileIndex].index.toString());
  fileInfos.splice(fileIndex, 1);
}

function removeTab(targetIndex: string) {
  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === targetIndex
  );
  if (fileInfos[fileIndex].modified === false) {
    justRemoveTab(targetIndex);
    return;
  }

  ElMessageBox.confirm("该文件未保存，是否继续？", "Warning", {
    confirmButtonText: "OK",
    cancelButtonText: "Cancel",
    type: "warning",
  })
    .then(() => {
      justRemoveTab(targetIndex);
      ElMessage({
        type: "success",
        message: "completed",
      });
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "canceled",
      });
    });
}

// function moveFile(oldPath: string, newPath: string) {
//   let fileIndex = fileInfos.findIndex((item) => item.path === oldPath);
//   if (fileIndex === -1) {
//     return;
//   }
//   fileInfos[fileIndex].path = newPath;
// }

function getBreakpoints() {
  const breakpoints = new Map<string, Array<number>>();
  fileInfos.forEach((fileInfo) => {
    const model = fileInfo.options["model"] as monaco.editor.ITextModel;
    const lines = model
      .getAllDecorations()
      .filter(
        (item) =>
          item.options.glyphMarginClassName === common.breakPointClassName
      )
      .map((item) => item.range.startLineNumber);
    breakpoints.set(fileInfo.path, lines);
  });
  return breakpoints;
}

function saveFile() {
  if (editableTabsValue.value === "0") {
    console.log("no focus editor now");
    return;
  }

  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === editableTabsValue.value
  );
  let path = fileInfos[fileIndex].path as string;
  let index = fileInfos[fileIndex].index;
  let value = fileInfos[fileIndex].options.model?.getValue() as string;
  if (fileInfos[fileIndex].modified === true) {
    let tabIndex = editableTabs.value.findIndex(
      (item) => item.index === index.toString()
    );
    fileInfos[fileIndex].modified = false;
    let curTab = editableTabs.value[tabIndex];
    curTab.modified = false;
    updateTitle(curTab);
  }

  emit("saveFile", path, value);
  return;
}

function fileModified() {
  if (editableTabsValue.value === "0") {
    console.log("no focus editor now");
    return;
  }

  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === editableTabsValue.value
  );
  if (fileInfos[fileIndex].modified === false) {
    let index = fileInfos[fileIndex].index;
    let tabIndex = editableTabs.value.findIndex(
      (item) => item.index === index.toString()
    );
    fileInfos[fileIndex].modified = true;
    let curTab = editableTabs.value[tabIndex];
    curTab.modified = true;
    updateTitle(curTab);
  }
  return;
}

function startDebug() {
  if (editableTabsValue.value === "0") {
    console.log("no focus editor now");
    return;
  }

  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === editableTabsValue.value
  );
  let path = fileInfos[fileIndex].path as string;
  emit("startDebug", path);
}

function focusToFileByPath(path: string, value: string) {
  let fileIndex = fileInfos.findIndex((item) => item.path === path);
  if (fileIndex === -1) {
    addFile(path, value);
    return;
  }
  editableTabsValue.value = fileInfos[fileIndex].index.toString();
  return;
}

function focusLine(path: string, line: number) {
  focusToFileByPath(path, ""); // there need to modify in the future
  let fileIndex = fileInfos.findIndex((item) => item.path === path);

  let model = fileInfos[fileIndex].options.model as monaco.editor.ITextModel;
  let lineCount = model.getLineCount();
  if (line < 1 || line > lineCount) {
    console.error("line out of range");
    return;
  }

  const decoration = {
    range: new monaco.Range(line, 1, line, 1),
    options: {
      isWholeLine: true,
      className: common.focusLineClassName,
      stickiness:
        monaco.editor.TrackedRangeStickiness.NeverGrowsWhenTypingAtEdges,
    },
  };
  model.deltaDecorations([], [decoration]);

  let curEditor = getEditorByIndex(fileInfos[fileIndex].index.toString());

  setTimeout(() => {
    curEditor.locateLine(line);
  }, 5);
  return;
}

function clearFocusLine() {
  fileInfos.forEach((item) => {
    let model = item.options.model as monaco.editor.ITextModel;
    let decorations = model
      .getAllDecorations()
      .filter((item) => item.options.className === common.focusLineClassName);
    model.deltaDecorations(
      decorations.map((item) => item.id),
      []
    );
  });
  return;
}

function disposePanel() {
  fileInfos.forEach((item) => {
    let model = item.options.model as monaco.editor.ITextModel;
    model.dispose();
  });
  fileInfos.splice(0);
  editableTabs.value.splice(0);
}
</script>

<style scoped>
.editor-panel-container {
  height: 100%;
  width: 100%;
}

.demo-tabs {
  height: 100%;
  width: 100%;
}

::v-deep .demo-tabs > .el-tabs__header {
  margin: 0px;
}

::v-deep .demo-tabs > .el-tabs__content {
  padding: 0px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
  height: calc(100% - 41px);
  width: 100%;
}

::v-deep .demo-tabs > .el-tabs__content > .el-tab-pane {
  height: 100%;
  width: 100%;
}
</style>
