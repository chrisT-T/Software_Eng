<template>
  <div class="main">
    <el-header>
      <div class="header">TO-CODE</div>
      <div class="mt-4">
        <el-input
          v-model="input3"
          placeholder="Please input"
          class="input-with-select"
          style="width: 500px"
        >
          <template #prepend>
            <el-select
              v-model="select"
              placeholder="Select"
              style="width: 100px"
            >
              <el-option label="创建人" value="1" />
              <el-option label="项目名称" value="2" />
              <el-option label="个人权限" value="3" />
            </el-select>
          </template>
          <template #append>
            <el-button :icon="Search" />
          </template>
        </el-input>
      </div>
      <div class="user-part">
        <el-popover placement="bottom" :width="500" trigger="hover">
          <template #reference>
            <el-button style="margin-right: 16px">Alert</el-button>
          </template>
          <ul class="infinite-list" style="overflow: auto">
            <li v-for="i in resMsg" :key="i" class="infinite-list-item">
              <span>
                {{ i.srcUser }} invite you to join {{ i.srcProject }}
              </span>
              <el-button-group v-if="!i.handled">
                <el-button type="success" text :icon="Check"></el-button>
                <el-button type="danger" text :icon="Close"></el-button>
              </el-button-group>
            </li>
          </ul>
        </el-popover>
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
            <a-doption @click="dialogPDVisible = true">个人详情</a-doption>
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
      <ProjectCard></ProjectCard>
    </el-container>
  </div>
  <el-dialog v-model="dialogPDVisible" width="405px">
    <PersonalDetail></PersonalDetail>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import ProjectCard from "@/components/ProjectCard.vue";
import PersonalDetail from "@/components/PersonalDetail.vue";
import router from "@/router";
import { useRouter } from "vue-router";
import { IconExport } from "@arco-design/web-vue/es/icon";
import axios from "axios";
import { Search, Check, Close } from "@element-plus/icons-vue";
import { tr } from "element-plus/es/locale";

const count = ref(6);

interface resMsgStr {
  srcUser: string;
  srcProject: string;
  time: string;
  handled: boolean;
}

const resMsg: resMsgStr[] = [
  {
    srcUser: "Dave",
    srcProject: "test",
    time: "123",
    handled: true,
  },
  {
    srcUser: "aas",
    srcProject: "tsFDst",
    time: "1S3",
    handled: false,
  },
];

onMounted(() => {
  setInterval(() => {
    const time = new Date().getTime();
    localStorage.setItem("active_time", time);
  }, 5 * 60 * 1000);
});

const name = useRouter().currentRoute.value.params.username;

const dialogPDVisible = ref(false);

const input3 = ref("");
const select = ref("");

const logout = () => {
  console.log("logout");
  localStorage.removeItem("username");
  localStorage.removeItem("login_time");
  axios.get("/api/logout");
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

.infinite-list {
  height: 300px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.infinite-list .infinite-list-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  margin: 5px;
  border-radius: 5px;
}
.infinite-list .infinite-list-item:hover {
  background-color: #f4f4f5;
}
.infinite-list .infinite-list-item + .list-item {
  margin-top: 5px;
}
</style>

<style>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
</style>
