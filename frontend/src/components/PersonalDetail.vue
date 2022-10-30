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
    <a-descriptions style="margin-top: 50px" :data="data" :column="1" />
    <el-button-group class="ml-4" style="margin-top: 20px">
      <el-button :icon="Edit">修改用户名</el-button>
      <el-button :icon="Cpu">修改密码</el-button>
      <el-button :icon="Message">修改邮箱</el-button>
    </el-button-group>
  </div>
</template>

<script lang="ts" setup>
import { IconEdit } from "@arco-design/web-vue/es/icon";
import { Cpu, Edit, Message } from "@element-plus/icons-vue";
import { ref } from "vue";

const data = [
  {
    label: "用户名",
    value: "Socrates",
  },
  {
    label: "用户ID",
    value: "12HSD2334",
  },
  {
    label: "用户密码",
    value: "uyh*****iug",
  },
  {
    label: "用户邮箱",
    value: "abc@email.com",
  },
];
</script>
