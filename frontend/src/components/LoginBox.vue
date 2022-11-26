<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div class="login_">
    <el-form
      ref="ruleFormRef"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="120px"
      class="demo-ruleForm"
      label-position="top"
    >
      <el-form-item label="Username" prop="username">
        <el-input v-model.number="ruleForm.username" />
      </el-form-item>
      <el-form-item label="Password" prop="password">
        <el-input
          v-model="ruleForm.password"
          type="password"
          autocomplete="off"
          show-password
        />
      </el-form-item>
      <el-form-item>
        <div class="button_gp">
          <el-button type="primary" @click="submitForm(ruleFormRef)"
            >Sign In</el-button
          >
          <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import router from "@/router";
import { reactive, ref } from "vue";
import type { FormInstance } from "element-plus";
import { ElMessage } from "element-plus";
import axios from "axios";
import qs from "qs";

const ruleFormRef = ref<FormInstance>();

const checkUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("Please input the username"));
  } else {
    callback();
  }
};

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("Please input the password"));
  } else {
    callback();
  }
};

const ruleForm = reactive({
  password: "",
  username: "",
});

const rules = reactive({
  password: [{ validator: validatePass, trigger: "blur" }],
  username: [{ validator: checkUsername, trigger: "blur" }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      axios
        .post("/api/login", qs.stringify(ruleForm))
        .then(function (response) {
          const code = response.status;
          console.log(code);
          if (code === 204) {
            sessionStorage.setItem("username", ruleForm.username);
            router.replace({
              name: "main",
              params: { username: ruleForm.username },
            });
          } else {
            ElMessage("Invalid Username or Password");
          }
        });
    } else {
      ElMessage("Error Submit!");
      return false;
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};
</script>

<style scoped>
.login_ {
  padding-top: 30px;
}
.button_gp {
  display: flex;
  justify-content: center;
  flex-grow: 1;
  margin-top: 10px;
}
</style>
