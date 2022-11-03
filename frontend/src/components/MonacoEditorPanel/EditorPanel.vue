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
        ></MonacoEditor>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import MonacoEditor from "@/components/MonacoEditorPanel/MonacoEditor.vue";
import { ta } from "element-plus/es/locale";
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
  let fileIndex = fileInfos.findIndex(
    (fileInfo) => fileInfo.index.toString() === targetName
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
    addTab(fileName, fileInfos[fileIndex].index.toString());
  } else {
    editableTabsValue.value = fileInfos[fileIndex].index.toString();
  }
}

function setTheme(theme: string) {
  fileInfos.forEach((item) => {
    item.options.theme = theme;
    let curEditor = getEditorByIndex(
      item.index.toString()
    ) as monaco.editor.IStandaloneCodeEditor;
    curEditor.updateOptions(item.options);
  });
}

function setLanguage(language: string, index: string) {
  let fileIndex = fileInfos.findIndex(
    (item) => item.index.toString() === index
  );
  fileInfos[fileIndex].options.language = language;
  let model = fileInfos[fileIndex].options.model as monaco.editor.ITextModel;
  monaco.editor.setModelLanguage(model, language);

  let curEditor = getEditorByIndex(
    index
  ) as monaco.editor.IStandaloneCodeEditor;

  curEditor.updateLanguage(fileInfos[fileIndex].options.language);
}

function renameFile(oldPath: string, newPath: string) {
  let newTitle = newPath.split("/").pop() as string;
  let fileIndex = fileInfos.findIndex((item) => item.path === oldPath);
  if (fileIndex === -1) {
    return;
  }

  fileInfos[fileIndex].path = newPath;
  let newLanguage = getLanguageByFileName(newTitle);
  if (fileInfos[fileIndex].options.language !== newLanguage) {
    setLanguage(newLanguage, fileInfos[fileIndex].index.toString());
  }

  let tabIndex = editableTabs.value.findIndex(
    (item) => item.title === oldPath.split("/").pop()
  );
  editableTabs.value[tabIndex].title = newTitle;
}

function deleteFile(path: string) {
  let fileIndex = fileInfos.findIndex((item) => item.path === path);
  if (fileIndex === -1) {
    return;
  }
  removeTab(fileInfos[fileIndex].index.toString());
  fileInfos.splice(fileIndex, 1);
}

function moveFile(oldPath: string, newPath: string) {
  let fileIndex = fileInfos.findIndex((item) => item.path === oldPath);
  if (fileIndex === -1) {
    return;
  }
  fileInfos[fileIndex].path = newPath;
}

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
