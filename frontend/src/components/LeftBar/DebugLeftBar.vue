<template>
  <div class="debug-left-bar">
    <h2>Debugger Sidebar</h2>
    <splitpanes horizontal>
      <pane min-size="20">
        <debug-buttons :language="props.language" :key="props.language" />
        <h4>Variables</h4>
      </pane>
      <pane min-size="20">
        <h4>Watching</h4>
      </pane>
      <pane min-size="20">
        <h4>Call Stack</h4>
      </pane>
    </splitpanes>
  </div>
</template>

<script setup lang="ts">
import { Splitpanes, Pane } from "splitpanes";
import DebugButtons from "../DebugComponents/DebugButtons.vue";
import { defineProps } from "vue";

const props = defineProps<{
  language: string;
}>();
</script>

<style scoped>
@import "splitpanes/dist/splitpanes.css";
:deep(.splitpanes__splitter) {
  height: 5px;
  background-color: var(--el-border-color-light);
}
.debug-left-bar {
  height: 100%;
}
</style>
