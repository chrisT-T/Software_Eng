<template>
  <div class="terminal">
    <div ref="termDiv"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineProps, defineExpose } from "vue";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { AttachAddon } from "xterm-addon-attach";
import ReconnectingWebSocket from "reconnecting-websocket";

defineExpose({
  runCommandInTerminal,
});

const props = defineProps<{
  containerId: string;
}>();

const termDiv = ref<HTMLDivElement>();
const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
});
const fitAddon = new FitAddon();
const terminalWs = new ReconnectingWebSocket(
  `ws://${location.host}/terminal/websocket/${props.containerId}`
);
const attachAddon = new AttachAddon(terminalWs);

function runCommandInTerminal(cmd: string) {
  console.log(cmd);
  terminalWs.send("clear\n");
  terminalWs.send(`${cmd}\n`);
}

onMounted(() => {
  console.log(`ws://${location.host}/terminal/websocket/${props.containerId}`);
  term.open(termDiv?.value as HTMLElement);
  term.loadAddon(fitAddon);
  term.loadAddon(attachAddon);

  term.writeln("welcome to use docker web terminal!");

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
