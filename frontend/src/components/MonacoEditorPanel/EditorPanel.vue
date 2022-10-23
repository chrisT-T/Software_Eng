<template>
  <div>
    <!-- <div style="margin-bottom: 20px">
      <el-button size="small" @click="addTab(editableTabsValue)">
        add tab
      </el-button>
    </div> -->
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
        <MonacoEditor :editor-option="options"></MonacoEditor>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import MonacoEditor from "@/components/MonacoEditorPanel/MonacoEditor.vue";
import * as monaco from "monaco-editor";
import { ref } from "vue";

const options = {
  theme: "vs",
  glyphMargin: true,
  language: "python",
  automaticLayout: true,
  bracketPairColorization: true,
  model: monaco.editor.createModel("import os", "python"),
} as monaco.editor.IStandaloneEditorConstructionOptions;

let tabIndex = 1;
const editableTabsValue = ref("1");
const editableTabs = ref([
  {
    title: "Get Started",
    name: "1",
    content: "Tab 1 content",
  },
]);

const addTab = (targetName: string) => {
  const newTabName = `${++tabIndex}`;
  editableTabs.value.push({
    title: "New Tab",
    name: newTabName,
    content: "New Tab content",
  });
  editableTabsValue.value = newTabName;
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
        }
      }
    });
  }

  editableTabsValue.value = activeName;
  editableTabs.value = tabs.filter((tab) => tab.name !== targetName);
};
</script>
<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
