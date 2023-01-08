<template>
  <div class="bottom-panel">
    <el-tabs
      v-model="editableTabsValue"
      :tab-position="tabPosition"
      class="bottom-panel-tabs"
    >
      <el-tab-pane label="Terminal" name="Terminal">
        <TerminalPanel :containerId="containerId" :key="containerId" />
      </el-tab-pane>
      <el-tab-pane label="Output" name="Output">
        <OutputTerminal
          ref="outputTerm"
          :containerId="containerId"
          :key="containerId"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted, defineExpose } from "vue";
import TerminalPanel from "../Terminal/TerminalPanel.vue";
import DebugTerminal from "../Terminal/DebugTerminal.vue";
import OutputTerminal from "../Terminal/OutputTerminal.vue";
defineExpose({
  outputRunCommand,
});

const tabPosition = ref("left");
const editableTabsValue = ref("Terminal");

const props = defineProps<{
  containerId: string;
  containerSubdomain: string;
}>();

const outputTerm = ref<InstanceType<typeof OutputTerminal> | null>(null);

function outputRunCommand(cmd: string) {
  console.log(cmd);
  editableTabsValue.value = "Output";
  outputTerm.value?.runCommandInTerminal(cmd);
}

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

:deep(.bottom-panel-tabs > .el-tabs__header) {
  margin: 0px;
}

:deep(.bottom-panel-tabs > .el-tabs__content) {
  height: 100%;
}

:deep(.bottom-panel-tabs > .el-tabs__content > .el-tab-pane) {
  height: 100%;
  width: 100%;
}
</style>
