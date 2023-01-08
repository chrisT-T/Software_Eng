<template>
  <div class="terminal">
    <div ref="termDiv"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineProps } from "vue";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { AttachAddon } from "xterm-addon-attach";

const props = defineProps<{
  containerId: string;
}>();

const termDiv = ref<HTMLDivElement>();
const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
});
const fitAddon = new FitAddon();
const terminalWs = new WebSocket(
  `ws://${location.host}/terminal/websocket/${props.containerId}`
);
const attachAddon = new AttachAddon(terminalWs);

onMounted(() => {
  console.log(`ws://${location.host}/terminal/websocket/${props.containerId}`);
  term.open(termDiv?.value as HTMLElement);
  term.loadAddon(fitAddon);
  term.loadAddon(attachAddon);

  window.addEventListener("resize", resizeScreen);
  function resizeScreen() {
    try {
      // 窗口大小改变时，触发xterm的resize方法使自适应
      fitAddon.fit();
    } catch (e) {
      console.log("e", e.message);
    }
  }
  setTimeout(() => {
    fitAddon.fit();
  }, 6);
});
</script>

<style scoped>
.terminal {
  text-align: left;
}
@import "xterm/css/xterm.css";
</style>
