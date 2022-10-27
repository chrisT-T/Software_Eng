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
const terminalWs = new WebSocket("ws://localhost:5005");
const attachAddon = new AttachAddon(terminalWs);

onMounted(() => {
  term.open(termDiv?.value as HTMLElement);
  term.loadAddon(fitAddon);
  // term.loadAddon(attachAddon);

  term.writeln("welcome to use docker web terminal!");
});
</script>

<style scoped>
.terminal {
  text-align: left;
}
@import "xterm/css/xterm.css";
</style>
