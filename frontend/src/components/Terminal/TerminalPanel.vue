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
      <SimpleTerminal :containerId="item.container" />
    </el-tab-pane>
  </el-tabs>
</template>
<script lang="ts" setup>
import { ref, defineProps } from "vue";
import SimpleTerminal from "@/components/Terminal/SimpleTerminal.vue";

const containerId = "";

const props = defineProps<{
  containerId: string;
}>();

let tabIndex = 2;
const editableTabsValue = ref("2");
const editableTabs = ref([
  {
    title: "Terminal 1",
    name: "1",
    container: props.containerId,
  },
]);

const handleTabsEdit = (targetName: string, action: "remove" | "add") => {
  if (action === "add") {
    const newTabName = `${++tabIndex}`;
    editableTabs.value.push({
      title: `Terminal ${tabIndex}`,
      name: newTabName,
      container: props.containerId,
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
<style></style>
