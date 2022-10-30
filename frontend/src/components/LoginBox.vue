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
      <el-form-item label="Password" prop="pass">
        <el-input
          v-model="ruleForm.pass"
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
  pass: "",
  username: "",
});

const rules = reactive({
  pass: [{ validator: validatePass, trigger: "blur" }],
  username: [{ validator: checkUsername, trigger: "blur" }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      router.replace({ name: "main", params: { username: ruleForm.username } });
    } else {
      console.log("error submit!");
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
