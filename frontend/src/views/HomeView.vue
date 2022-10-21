<template>
  <!-- <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div> -->
  <tab-editor></tab-editor>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import TabEditor from "@/components/MonacoEditorPanel/TabEditor.vue";

export default defineComponent({
  name: "HomeView",
  components: {
    TabEditor,
  },
});
</script>
