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
          :editor-option="getOption(item.name)"
          @modified="fileModified"
          @saveFile="saveFile"
        ></MonacoEditor>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import MonacoEditor from "@/components/MonacoEditorPanel/MonacoEditor.vue";
import * as monaco from "monaco-editor";
import { ref, defineEmits, defineExpose } from "vue";

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

const emit = defineEmits<{
  (e: "saveFile", path: string, value: string): void;
  (e: "startDebug", path: string): void;
}>();

defineExpose({
  addFile,
  getBreakpoints,
  focusLine,
  clearFocusLine,
});

const fileInfos = ref<Array<FileInfo>>(new Array<FileInfo>());

let tabIndex = 0;
const editableTabsValue = ref("0");
const editableTabs = ref<Array<TabInfo>>(new Array<TabInfo>());

const getOption = (index: string) => {
  let fileIndex = fileInfos.value.findIndex(
    (fileInfo) => fileInfo.index.toString() === index
  );
  return fileInfos.value[fileIndex].options;
};

const addTab = (title: string, name: string) => {
  editableTabs.value.push({
    title: title,
    name: name,
  });
  editableTabsValue.value = name;
};

const removeTab = (targetName: string) => {
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
  let fileIndex = fileInfos.value.findIndex(
    (fileInfo) => fileInfo.index.toString() === targetName
  );
  fileInfos.value[fileIndex].show = false;
};

function addFile(path: string, value: string) {
  console.log("addFile", path);
  let fileName = path.split("/").pop() as string;
  let fileIndex = fileInfos.value.findIndex(
    (fileInfo) => fileInfo.path === path
  );
  if (fileIndex === -1) {
    fileInfos.value.push({
      path: path,
      modified: false,
      index: ++tabIndex,
      show: true,
      options: {
        theme: "vs",
        glyphMargin: true,
        language: "python",
        automaticLayout: true,
        bracketPairColorization: true,
        model: monaco.editor.createModel(
          value,
          undefined,
          monaco.Uri.file(path)
        ),
      },
    });
    addTab(fileName, tabIndex.toString());
  } else if (fileInfos.value[fileIndex].show === false) {
    fileInfos.value[fileIndex].show = true;
    addTab(fileName, fileInfos.value[fileIndex].index.toString());
  } else {
    editableTabsValue.value = fileInfos.value[fileIndex].index.toString();
  }
}

function getBreakpoints() {
  return;
}

function focusLine() {
  return;
}

function clearFocusLine() {
  return;
}

function fileModified() {
  return;
}

function saveFile() {
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
