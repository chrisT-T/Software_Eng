<template>
  <div class="main">
    <el-header>
      <div class="header">TO-CODE</div>
      <div class="user-part">
        <!-- <a-dropdown trigger="hover">
          <a-avatar :size="36">{{ name }}</a-avatar>
          <template #content>
            <a-doption>Option 1</a-doption>
            <a-doption>Option 2</a-doption>
          </template>
        </a-dropdown> -->
        <a-dropdown position="br" trigger="hover">
          <a-avatar
            :trigger-icon-style="{ color: '#3491FA' }"
            :auto-fix-font-size="false"
            :style="{ backgroundColor: '#168CFF' }"
            :size="34"
          >
            {{ name }}
          </a-avatar>
          <template #content>
            <a-doption>个人详情</a-doption>
            <a-doption @click="logout">
              <template #icon>
                <icon-export />
              </template>
              <template #default>登出</template>
            </a-doption>
          </template>
        </a-dropdown>
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
import router from "@/router";
import { useRouter } from "vue-router";
import { IconExport } from "@arco-design/web-vue/es/icon";

const name = useRouter().currentRoute.value.params.username;

const logout = () => {
  console.log("logout");
  sessionStorage.removeItem("username");
  router.replace("/login");
};
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
