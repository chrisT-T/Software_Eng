<template>
  <div class="terminal">
    <h2>{{ stage.message }}</h2>
    <h2>{{ props.containerSubdomain }}</h2>
    <div ref="termDiv"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineProps, reactive } from "vue";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { AttachAddon } from "xterm-addon-attach";
import axios from "axios";
import { io } from "socket.io-client";

const props = defineProps<{
  containerId: string;
  containerSubdomain: string;
}>();

// terminal connection test
const termDiv = ref<HTMLDivElement>();
const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
});
const fitAddon = new FitAddon();
const terminalWs = new WebSocket(
  `ws://localhost:5005/websocket/${props.containerId}`
);
const attachAddon = new AttachAddon(terminalWs);
const stage = reactive({
  flag: false,
  message: "Debug service is not running",
});
// debugger functions
let debugServiceURL = "";

function getDebugStage() {
  if (props.containerSubdomain == "") {
    return;
  }
  // axios
  //   .get(`http://${debugServiceURL}/pdb/test`)
  //   .then(() => {
  //     stage.flag = true;
  //     stage.message = "Debug service is running";
  //   })
  //   .catch(() => {
  //     stage.flag = false;
  //     stage.message = "Debug service is not running";
  //   });
}

onMounted(() => {
  console.log(`ws://localhost:5005/websocket/${props.containerId}`);
  term.open(termDiv?.value as HTMLElement);
  term.loadAddon(fitAddon);
  term.loadAddon(attachAddon);

  term.writeln("welcome to use debug Termainal");

  setTimeout(() => {
    fitAddon.fit();
  }, 6);

  debugServiceURL = `${props.containerSubdomain}.debug.localhost:8088`;

  if (props.containerSubdomain != "") {
    console.log(debugServiceURL);
    // socket = io(`ws://${debugServiceURL}`);

    // socket.on("connect", () => {
    //   stage.flag = true;
    //   stage.message = "test";
    // });
  }

  setTimeout(() => {
    getDebugStage();
    console.log(debugServiceURL);
  }, 5000);
});
</script>

<style scoped>
.terminal {
  text-align: left;
}
@import "xterm/css/xterm.css";
</style>
