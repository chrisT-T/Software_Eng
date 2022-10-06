<template>
  <div>
    <MonacoEditor
      theme="vs"
      language="python"
      :width="800"
      :height="800"
      :diffEditor="false"
      v-model:value="value"
    ></MonacoEditor>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "@vue/reactivity";
import MonacoEditor from "monaco-editor-vue3";

const value = ref<string>("# plz code here");
</script>
