<template>
  <el-tabs
    v-model="editableTabsValue"
    type="card"
    editable
    class="demo-tabs"
    @edit="handleTabsEdit"
  >
    <el-tab-pane
      v-for="item in editableTabs"
      :key="item.name"
      :label="item.title"
      :name="item.name"
    >
      <simple-editor></simple-editor>
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import SimpleEditor from "@/components/MonacoEditorPanel/SimpleEditor.vue";
import { ref } from "vue";

let tabIndex = 1;
const editableTabsValue = ref("1");
const editableTabs = ref([
  {
    title: "Tab 1",
    name: "1",
    content: "Tab 1 content",
  },
]);

const handleTabsEdit = (targetName: string, action: "remove" | "add") => {
  if (action === "add") {
    const newTabName = `${++tabIndex}`;
    editableTabs.value.push({
      title: "New Tab",
      name: newTabName,
      content: "New Tab content",
    });
    editableTabsValue.value = newTabName;
  } else if (action === "remove") {
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
  }
};
</script>
<style>
.demo-tabs > .el-tabs__content {
  margin: 0px;
  background-color: #000000;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs__header {
  padding: 0;
  position: relative;
  margin: 0 0 0px;
}
</style>
