<template>
  <div class="personal-detail">
    <a-avatar trigger-type="mask" :size="110">
      <img
        alt="avatar"
        src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
      />
      <template #trigger-icon>
        <icon-edit :size="30" />
      </template>
    </a-avatar>
    <el-descriptions
      class="margin-top"
      title="Personal Information"
      :column="1"
    >
      <el-descriptions-item label="Username">
        <el-input
          v-model="UserData.username"
          style="width: 120px"
          v-if="ChangeName === true"
          size="small"
          autofocus
        />
        <span v-else>{{ UserData.username }}</span>
      </el-descriptions-item>
      <el-descriptions-item label="User ID">
        {{ UserData.userID }}
      </el-descriptions-item>
      <el-descriptions-item label="Email">
        <el-input
          v-model="UserData.email"
          style="width: 120px"
          v-if="ChangeEmail === true"
          size="small"
          autofocus
        />
        <span v-else>{{ UserData.email }}</span>
      </el-descriptions-item>
    </el-descriptions>
    <el-button-group class="ml-4" style="margin-top: 20px">
      <el-button
        :icon="Edit"
        @click="ChangeName = true"
        v-if="ChangeName != true"
      >
        <span>修改用户名</span>
      </el-button>
      <el-button
        :icon="Edit"
        @click="ChangeName = false"
        v-if="ChangeName === true"
      >
        <span>确认用户名</span>
      </el-button>
      <el-button
        :icon="Message"
        @click="ChangeEmail = true"
        v-if="ChangeEmail != true"
      >
        <span>修改邮箱</span>
      </el-button>
      <el-button
        :icon="Message"
        @click="ChangeEmail = false"
        v-if="ChangeEmail === true"
      >
        <span>确认邮箱</span>
      </el-button>
    </el-button-group>
  </div>
</template>

<script lang="ts" setup>
import { IconEdit } from "@arco-design/web-vue/es/icon";
import { Cpu, Edit, Message } from "@element-plus/icons-vue";
import { computed, reactive, ref } from "vue";

const ChangeName = ref(false);
const ChangeEmail = ref(false);

const UserData = reactive({
  username: "THU",
  email: "acb@cdf.com",
  userID: "12564309",
});
</script>

<style scoped>
.personal-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
</style>
