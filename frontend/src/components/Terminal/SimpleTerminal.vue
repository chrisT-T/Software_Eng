<template>
  <div class="terminal">
    <h1>Terminal</h1>
    <div ref="termDiv"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { AttachAddon } from "xterm-addon-attach";

const termDiv = ref<HTMLDivElement>();
const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
});
const fitAddon = new FitAddon();
const terminalWs = new WebSocket(
  "ws://localhost:5005/websocket/ee44d43ade04376eb44e9db9c028ed8e857474d4a4c59a55e5661ee9062d82a3"
);
const attachAddon = new AttachAddon(terminalWs);

onMounted(() => {
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
