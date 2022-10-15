<template>
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
    <el-form-item label="Confirm Password" prop="checkPass">
      <el-input
        v-model="ruleForm.checkPass"
        type="password"
        autocomplete="off"
        show-password
      />
    </el-form-item>
    <el-form-item>
      <div class="button_gp">
        <el-button type="primary" @click="submitForm(ruleFormRef)"
          >Sign Up</el-button
        >
        <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
      </div>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import type { FormInstance } from "element-plus";

const ruleFormRef = ref<FormInstance>();

const checkUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("Please input the username"));
  }
  setTimeout(() => {
    var uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
    if (!uPattern.test(value)) {
      callback(new Error("用户名正则, 4到16位 (字母，数字，下划线，减号)"));
    } else {
      callback();
    }
  }, 1000);
};

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("Please input the password"));
  } else {
    var pPattern =
      /^.*(?=.{6,20})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/;
    if (!pPattern.test(value)) {
      callback(
        new Error(
          "6-20位, 包括至少1个大写字母, 1个小写字母, 1个数字, 1个特殊字符!@#$%^&*?"
        )
      );
    } else {
      callback();
    }
    callback();
  }
};
const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("Please input the password again"));
  } else if (value !== ruleForm.pass) {
    callback(new Error("Two inputs don't match!"));
  } else {
    callback();
  }
};

const ruleForm = reactive({
  pass: "",
  checkPass: "",
  username: "",
});

const rules = reactive({
  pass: [{ validator: validatePass, trigger: "blur" }],
  checkPass: [{ validator: validatePass2, trigger: "blur" }],
  username: [{ validator: checkUsername, trigger: "blur" }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
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
.button_gp {
  display: flex;
  justify-content: center;
  flex-grow: 1;
}
</style>
