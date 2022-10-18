<template>
  <div class="main">
    <el-header>
      <div class="header">TO-CODE</div>
      <div class="user-part">
        <a-avatar :size="34">Arco</a-avatar>
      </div>
    </el-header>
    <el-container>
      <MenuBox></MenuBox>
      <ProjectCard></ProjectCard>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import MenuBox from "@/components/MenuBox.vue";
import ProjectCard from "@/components/ProjectCard.vue";
</script>

<style scoped>
.main {
  height: 100%;
  width: 100%;
  background-color: var(--color-neutral-1);
}
.el-header {
  height: 50px;
  background-color: #fff;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-container {
  height: 90%;
}
</style>
