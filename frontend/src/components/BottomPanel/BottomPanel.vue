<template>
  <div class="bottom-panel">
    <el-tabs :tab-position="tabPosition" class="bottom-panel-tabs">
      <el-tab-pane label="Terminal">
        <TerminalPanel :containerId="containerId" :key="containerId" />
      </el-tab-pane>
      <el-tab-pane label="Debug">
        <DebugTerminal
          :containerId="$props.containerId"
          :container-subdomain="$props.containerSubdomain"
          :key="containerId"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted } from "vue";
import TerminalPanel from "../Terminal/TerminalPanel.vue";
import DebugTerminal from "../Terminal/DebugTerminal.vue";
const tabPosition = ref("left");

const props = defineProps<{
  containerId: string;
  containerSubdomain: string;
}>();

onMounted(() => {
  console.log(props);
});
</script>

<style scoped>
.botton-panel {
  height: 100%;
}
.bottom-panel-tabs {
  height: 100%;
  width: 100%;
}

::v-deep .bottom-panel-tabs > .el-tabs__header {
  margin: 0px;
}

::v-deep .bottom-panel-tabs > .el-tabs__content {
  height: 100%;
}

::v-deep .bottom-panel-tabs > .el-tabs__content > .el-tab-pane {
  height: 100%;
  width: 100%;
}
</style>
