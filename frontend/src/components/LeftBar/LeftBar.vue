<template>
  <div class="left-bar">
    <el-tabs :tab-position="tabPosition" class="left-bar-tabs">
      <el-tab-pane label="File">
        <fileTree @open-file="openFile" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps } from "vue";
import fileTree from "@/components/fileTree.vue";
import DebugLeftBar from "./DebugLeftBar.vue";
const tabPosition = ref("left");

const props = defineProps<{
  language: string;
}>();

const emit = defineEmits<{
  (e: "openFile", path: string): void;
}>();

function openFile(path: string) {
  emit("openFile", path);
}
</script>

<style scoped>
.left-bar {
  height: 100%;
}
.left-bar-tabs {
  height: 100%;
  width: 100%;
}

:deep(.left-bar-tabs > .el-tabs__header) {
  margin: 0px;
}

:deep(.left-bar-tabs > .el-tabs__content) {
  height: 100%;
}

:deep(.left-bar-tabs > .el-tabs__content > .el-tab-pane) {
  height: 100%;
  width: 100%;
}
</style>
