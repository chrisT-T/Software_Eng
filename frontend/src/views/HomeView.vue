<template>
  <!-- <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div> -->
  <simple-editor></simple-editor>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SimpleEditor from "@/components/MonacoEditorPanel/SimpleEditor.vue";

export default defineComponent({
  name: "HomeView",
  components: {
    SimpleEditor,
  },
});
</script>
