<template>
  <div class="login">
    <el-container>
      <el-header> <div class="header">TO-CODE</div> </el-header>
      <el-main>
        <div class="rollbox">
          <div class="block text-center">
            <el-carousel height="400px" interval="7000">
              <el-carousel-item v-for="item in 3" :key="item">
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <div class="loginbox">
          <el-tabs
            v-model="activeName"
            class="demo-tabs"
            @tab-click="handleClick"
          >
            <el-tab-pane label="Sign in" name="first"
              ><LoginBox></LoginBox
            ></el-tab-pane>
            <el-tab-pane label="Sign up" name="second"
              ><SigninBox></SigninBox
            ></el-tab-pane>
          </el-tabs>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import LoginBox from "@/components/LoginBox.vue";
import SigninBox from "@/components/SignUpBox.vue";
import { ref } from "vue";
import type { TabsPaneContext } from "element-plus";

const activeName = ref("first");

const handleClick = (tab: TabsPaneContext, event: Event) => {
  // console.log(tab, event);
};
</script>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item:nth-child(3n) {
  background-color: #99a9bf;
  background-size: 600px 400px;
  background-image: url(../assets/RollingImg/cm2.png);
}

.el-carousel__item:nth-child(3n + 1) {
  background-color: #d3dce6;
  background-size: 600px 400px;
  background-image: url(../assets/RollingImg/terminal.png);
}
.el-carousel__item:nth-child(3n + 2) {
  background-color: #d3dce6;
  background-size: 600px 400px;
  background-image: url(../assets/RollingImg/communication.png);
}
.login {
  height: 100%;
  width: 100%;
  background-image: linear-gradient(170deg, rgb(var(--arcoblue-2)), #fff 33%);
}

.el-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.el-header {
  height: 50px;
  background-color: #fff;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-main {
  display: flex;
  height: 100%;
  width: 100%;
  align-items: center;
  justify-content: space-around;
}

.rollbox {
  height: 400px;
  width: 600px;
  /*background-color: var(--el-color-warning-light-5);*/
}

.loginbox {
  height: 430px;
  width: 300px;
  background-color: var(--el-color-primary-light-9);
  box-shadow: 3px 4px 5px 0px rgb(8 89 170 / 24%);
  border-radius: 10px;
  padding: 15px;
  overflow: hidden;
}

.head2 {
  height: 30px;
}
</style>
