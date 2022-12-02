<template>
  <div class="left-bar">
    <el-tabs :tab-position="tabPosition" class="left-bar-tabs">
      <el-tab-pane label="File">
        <fileTree @open-file="openFile" />
      </el-tab-pane>
      <el-tab-pane label="Debug">
        <DebugLeftBar></DebugLeftBar>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";
import fileTree from "@/components/fileTree.vue";
import DebugLeftBar from "./DebugLeftBar.vue";
const tabPosition = ref("left");

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

::v-deep .left-bar-tabs > .el-tabs__header {
  margin: 0px;
}

::v-deep .left-bar-tabs > .el-tabs__content {
  height: 100%;
}

::v-deep .left-bar-tabs > .el-tabs__content > .el-tab-pane {
  height: 100%;
  width: 100%;
}
</style>
