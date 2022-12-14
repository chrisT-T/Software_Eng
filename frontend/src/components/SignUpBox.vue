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
    <el-form-item label="Password" prop="password">
      <el-input
        v-model="ruleForm.password"
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
    <el-form-item label="Email" prop="email">
      <el-input v-model="ruleForm.email" autocomplete="off" />
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
import router from "@/router";
import type { FormInstance } from "element-plus";
import { ElMessage } from "element-plus";
import axios from "axios";
import qs from "qs";

const ruleFormRef = ref<FormInstance>();

const checkUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("Please input the username"));
  }
  setTimeout(() => {
    var uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
    if (!uPattern.test(value)) {
      callback(new Error("用户名规则, 4到16位 (字母，数字，下划线，减号)"));
    } else {
      axios
        .get("/api/user?username=" + ruleForm.username)
        .then(function (response) {
          callback(new Error("用户名重复或无效"));
        })
        .catch(function (error) {
          const code = error.response.status;
          if (code !== 404) {
            callback(new Error("服务器错误"));
          } else {
            callback();
          }
        });
    }
  }, 1000);
};

const checkEmail = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("Please input the email"));
  }
  setTimeout(() => {
    var uPattern = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if (!uPattern.test(value)) {
      callback(new Error("请输入合法邮箱域名"));
    } else {
      callback();
    }
  }, 500);
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
  } else if (value !== ruleForm.password) {
    callback(new Error("Two inputs don't match!"));
  } else {
    callback();
  }
};

const ruleForm = reactive({
  password: "",
  checkPass: "",
  username: "",
  email: "",
});

const rules = reactive({
  password: [{ validator: validatePass, trigger: "blur" }],
  checkPass: [{ validator: validatePass2, trigger: "blur" }],
  username: [{ validator: checkUsername, trigger: "blur" }],
  email: [{ validator: checkEmail, trigger: "blur" }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      axios.post("/api/user", qs.stringify(ruleForm)).then(function (response) {
        const code = response.status;
        if (code === 201) {
          axios
            .post("/api/login", qs.stringify(ruleForm))
            .then(function (response) {
              const code = response.status;
              if (code === 204) {
                const timestamp = new Date().getTime();
                localStorage.setItem("username", ruleForm.username);
                localStorage.setItem("active_time", timestamp);
                router.replace({
                  name: "main",
                  params: { username: ruleForm.username },
                });
              }
            });
        } else {
          ElMessage("Register Failed");
        }
      });
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
.signup_ {
  padding-top: 5px;
}
.button_gp {
  display: flex;
  justify-content: center;
  flex-grow: 1;
  margin-top: 10px;
}
</style>
