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
        :key="item.name"
        :label="item.title"
        :name="item.name"
      >
        <MonacoEditor
          ref="monacoEditors"
          :name="item.name"
          :editor-option="getOption(item.name)"
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

export interface FileInfo {
  path: string;
  modified: boolean;
  index: number;
  show: boolean;
  options: monaco.editor.IStandaloneEditorConstructionOptions;
}

export interface TabInfo {
  title: string;
  name: string;
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

const addTab = (title: string, name: string) => {
  editableTabs.value.push({
    title: title,
    name: name,
  });
  editableTabsValue.value = name;
};

const justRemoveTab = (targetName: string) => {
  const tabs = editableTabs.value;
  let activeName = editableTabsValue.value;
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1];
        if (nextTab) {
          activeName = nextTab.name;
        } else {
          activeName = "0";
        }
      }
    });
  }

  editableTabsValue.value = activeName;
  editableTabs.value = tabs.filter((tab) => tab.name !== targetName);

  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === targetName
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
    addTab(fileName, tabIndex.toString());
  } else if (fileInfos[fileIndex].show === false) {
    fileInfos[fileIndex].show = true;
    let model = fileInfos[fileIndex].options.model;
    let decorations = model?.getAllDecorations();
    model?.setValue(value);
    if (decorations) {
      model?.deltaDecorations([], decorations);
    }
    addTab(fileName, fileInfos[fileIndex].index.toString());
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

function removeTab(targetName: string) {
  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === targetName
  );
  if (fileInfos[fileIndex].modified === false) {
    justRemoveTab(targetName);
    return;
  }

  ElMessageBox.confirm("该文件未保存，是否继续？", "Warning", {
    confirmButtonText: "OK",
    cancelButtonText: "Cancel",
    type: "warning",
  })
    .then(() => {
      justRemoveTab(targetName);
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
  let value = fileInfos[fileIndex].options.model?.getValue() as string;
  if (fileInfos[fileIndex].modified === true) {
    let fileName = path.split("/").pop() as string;
    let tabIndex = editableTabs.value.findIndex(
      (item) => item.title === "* " + fileName
    );
    editableTabs.value[tabIndex].title = fileName;
    fileInfos[fileIndex].modified = false;
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
    let fileName = fileInfos[fileIndex].path.split("/").pop();
    let tabIndex = editableTabs.value.findIndex(
      (item) => item.title === fileName
    );
    editableTabs.value[tabIndex].title = "* " + fileName;
    fileInfos[fileIndex].modified = true;
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

function focusToFileByIndex() {
  return;
}
function focusLine() {
  return;
}

function clearFocusLine() {
  return;
}
</script>

<style>
.editor-panel-container {
  height: 100%;
  width: 100%;
}

.demo-tabs {
  height: 100%;
  width: 100%;
}

.demo-tabs > .el-tabs__header {
  margin: 0px;
}

.demo-tabs > .el-tabs__content {
  padding: 0px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
  height: calc(100% - 41px);
  width: 100%;
}

.demo-tabs > .el-tabs__content > .el-tab-pane {
  height: 100%;
  width: 100%;
}
</style>
