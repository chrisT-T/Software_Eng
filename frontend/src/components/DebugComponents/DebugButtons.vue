<template>
  <div class="icon-bar">
    <icon-play-arrow
      @click="sendCommand('cont')"
      title="Continue"
      :size="buttonSize"
    />
    <icon-arrow-right
      @click="sendCommand('next')"
      title="Next Line"
      :size="buttonSize"
    />
    <icon-double-down
      @click="sendCommand('stepInto')"
      title="Step Into"
      :size="buttonSize"
    />
    <icon-double-up
      @click="sendCommand('stepOut')"
      title="Step Out"
      :size="buttonSize"
    />
    <icon-record-stop
      @click="sendCommand('stop')"
      title="Stop"
      :size="buttonSize"
    />
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import { defineProps, defineEmits } from "vue";
let mPort = 0;
const buttonSize = 30 as number;

const props = defineProps<{
  language: string;
}>();

const commandDict = {
  Python: {
    cont: "c",
    next: "n",
    stepInto: "s",
    stepOut: "u",
    stop: "q",
  },
};

function sendCommand(commandType: string) {
  console.log(props.language);
  console.log(commandDict[props.language][commandType]);
}
</script>

<style scoped>
.icon-bar > .el-icon {
  cursor: pointer;
}
.icon-bar {
  display: flex;
  width: 100%;
  height: auto;
  justify-content: space-between;
  z-index: 999;
}
</style>
