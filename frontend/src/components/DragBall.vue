<template>
  <div
    class="drag-ball"
    draggable="true"
    @dragstart="dragstart($event)"
    @dragend="dragend($event)"
    :style="`right:${elRight}px;bottom:${elBottom}px;`"
    v-if="chatboxVisible === true"
  >
    <span>ChatBox</span>
    <el-button
      :icon="ArrowDownBold"
      circle
      @click="chatboxVisible = false"
      type="text"
    />
    <div>
      <ul class="infinite-list" style="overflow: auto">
        <li v-for="i in msgList" :key="i" class="infinite-list-item">
          <el-avatar> {{ i.sender }} </el-avatar>
          <div class="msgbox">{{ i.msg }}</div>
          <span class="msgtime">{{ i.time }}</span>
        </li>
      </ul>
      <div style="width: 100%">
        <el-input
          v-model="input"
          placeholder="Please input"
          clearable
          @keyup.enter="chatNewMsg"
        />
      </div>
    </div>
  </div>
  <div
    class="drag-ball_collapse"
    draggable="true"
    @dragstart="dragstart($event)"
    @dragend="dragend($event)"
    :style="`right:${elRight}px;bottom:${elBottom}px;`"
    v-if="chatboxVisible === false"
  >
    <el-badge is-dot class="item" :hidden="newMsg">ChatBox</el-badge>
    <el-button
      :icon="ArrowUpBold"
      circle
      @click="(chatboxVisible = true), (newMsg = true)"
      type="text"
    />
  </div>
</template>
<script lang="ts" setup>
import { ref } from "vue";
import { ArrowUpBold, ArrowDownBold } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";
import { Search } from "@element-plus/icons-vue";
import ReconnectingWebSocket from "reconnecting-websocket";

const name = useRouter().currentRoute.value.params.username;
const projectID = useRouter().currentRoute.value.params.projectid;

const newMsg = ref(true);

const input = ref("");

const chatboxVisible = ref(false);

const ws = new ReconnectingWebSocket(
  `ws://${location.host}/communication/websocket/${projectID}/${name}`
);

ws.onopen = function () {
  console.log("open");
};

ws.onmessage = function (e) {
  console.log(e.data);
  let r = JSON.parse(e.data);
  console.log(r, typeof r);
  msgList.value.push(r);
  newMsg.value = false;
};

ws.onclose = function () {
  console.log("close");
};

ws.onerror = function () {
  console.log("error");
};

const chatNewMsg = () => {
  console.log(input);
  ws.send(input.value);
  input.value = "";
  // 可以提交当前用户，发送的消息input，以及发送时间
};

const startclientX = ref(0); //记录开始的横坐标位置
const startclientY = ref(0); //记录开始的纵坐标位置
const elRight = ref(50); //定位-初始位置
const elBottom = ref(70); //定位-初始位置

// 拖拽开始事件
const dragstart = (e: any) => {
  // 记录拖拽元素初始位置
  startclientX.value = e.clientX;
  startclientY.value = e.clientY;
};
// 拖拽完成事件
const dragend = (e: any) => {
  console.log("eeeeee", e);
  let x = startclientX.value - e.clientX; // 计算偏移量
  let y = startclientY.value - e.clientY;
  elRight.value += x; // 实现拖拽元素随偏移量移动
  elBottom.value += y;
};

interface codingChat {
  sender: string;
  msg: string;
  time: string;
}

const msgList = ref([]);
</script>
<style scoped>
.msgbox {
  border: solid;
  border-radius: 5px;
  border-width: 1px;
  border-color: #fff;
  width: 80%;
  margin-left: 10px;
  display: flex;
  padding-left: 5px;
  padding-right: 5px;
}
.msgtime {
  color: darkgray;
  font-size: 10px;
  line-height: 10px;
}
.drag-ball {
  width: 400px;
  cursor: pointer;
  position: absolute;
  background: #242b3a;
  box-shadow: 0px 6px 16px -8px rgb(0 0 0 / 8%),
    0px 9px 28px 0px rgb(0 0 0 / 5%), 0px 12px 48px 16px rgb(0 0 0 / 3%);
  border-radius: 23px;
  text-align: center;
  color: #fff;
  z-index: 999;
  line-height: 30px;
  overflow: hidden;
}
.drag-ball_collapse {
  height: 30px;
  width: 100px;
  cursor: pointer;
  position: absolute;
  background: #242b3a;
  box-shadow: 0px 6px 16px -8px rgb(0 0 0 / 8%),
    0px 9px 28px 0px rgb(0 0 0 / 5%), 0px 12px 48px 16px rgb(0 0 0 / 3%);
  border-radius: 23px;
  text-align: center;
  color: #fff;
  z-index: 999;
  line-height: 30px;
  overflow: hidden;
}
.infinite-list {
  height: 400px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.infinite-list .infinite-list-item {
  display: flex;
  align-items: center;
  height: 40px;
  margin: 5px;
  border-radius: 5px;
}
.infinite-list .infinite-list-item + .list-item {
  margin-top: 5px;
}
</style>
