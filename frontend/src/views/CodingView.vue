<template>
  <div class="coding">
    <el-container>
      <el-header>
        <div class="header">
          <a-button @click="backmain">
            <template #icon
              ><icon-home
                :style="{ fontSize: '20px', margin: '3px' }"
                :stroke-width="3"
                @click="backmain"
            /></template>
          </a-button>

          <icon-save
            :style="{ fontSize: '20px', margin: '3px' }"
            :stroke-width="3"
          />
          <span class="header-span">TO-CODE</span>
          <a-avatar :size="20">Arco</a-avatar>
        </div>
        <div class="user-part">
          <a-button-group type="primary" size="small">
            <a-button>
              <template #icon><icon-play-arrow-fill /></template>
            </a-button>
            <a-button>
              <template #icon><icon-bug /></template>
            </a-button>
            <a-button>
              <template #icon><icon-pause /></template>
            </a-button>
          </a-button-group>
          <a-divider direction="vertical" />
          <icon-user-add
            :style="{ fontSize: '20px', margin: '0 5px' }"
            :stroke-width="3"
            @click="dialogTableVisible = true"
          />
        </div>
      </el-header>
      <el-container class="el2">
        <a-resize-box
          :directions="['right']"
          style="
            width: 200px;
            min-width: 100px;
            max-width: 50%;
            text-align: center;
          "
          ><FileTreeBox />
        </a-resize-box>
        <el-container direction="vertical">
          <a-resize-box
            :directions="['bottom']"
            style="
              width: 100%;
              text-align: center;
              max-height: 90%;
              min-height: 0;
            "
          >
            <EditorPanel> </EditorPanel>
          </a-resize-box>
          <TerminalPanel />
        </el-container>
      </el-container>
    </el-container>
  </div>
  <el-dialog v-model="dialogTableVisible" title="权限组" width="600px">
    <el-table :data="changepr" style="width: 100%" max-height="250">
      <el-table-column prop="user" label="用户名" />
      <el-table-column label="权限">
        <template #default="scope">
          <span v-if="scope.row.permission === 'administrator'">
            项目管理员
          </span>
          <span v-if="scope.row.permission === 'readonly'"> 只可读 </span>
          <span v-if="scope.row.permission === 'edit'"> 可编辑 </span>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="180">
        <template #default>
          <el-button link type="primary" size="small"> 移除成员 </el-button>
          <el-button link type="primary" size="small"> 修改权限 </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-button
      class="mt-4"
      style="width: 100%"
      @click="dialogShareVisible = true"
      >新增权限组</el-button
    >
  </el-dialog>
  <el-dialog
    v-model="dialogShareVisible"
    title="共享项目"
    class="share-dialog"
    align-center
  >
    <el-form :model="form" ref="addForm">
      <el-form-item label="用户ID" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="共享权限" :label-width="formLabelWidth">
        <el-select v-model="form.region" placeholder="选择用户权限">
          <el-option label="只可读" value="readonly" />
          <el-option label="可编辑" value="edit" />
          <el-option label="项目管理员" value="administrator" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogShareVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogShareVisible = false">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, getCurrentInstance, ref, onMounted } from "vue";
import {
  IconHome,
  IconUserAdd,
  IconSave,
  IconPlayArrowFill,
  IconBug,
  IconPause,
} from "@arco-design/web-vue/es/icon";
import FileTreeBox from "@/components/FileTreeBox.vue";
import EditorPanel from "@/components/MonacoEditorPanel/EditorPanel.vue";
import router from "@/router";
import { useRouter } from "vue-router";
import SimpleTerminal from "@/components/Terminal/SimpleTerminal.vue";
import TerminalPanel from "@/components/Terminal/TerminalPanel.vue";
import { Component } from "vue-property-decorator";

onMounted(() => {
  setInterval(() => {
    const time = new Date().getTime();
    sessionStorage.setItem("active_time", time);
  }, 5 * 60 * 1000);
});
const name = useRouter().currentRoute.value.params.username;

const dialogTableVisible = ref(false);
const dialogShareVisible = ref(false);

const formLabelWidth = "140px";
const form = reactive({
  name: "",
  region: "",
  date1: "",
  date2: "",
  delivery: false,
  type: [],
  resource: "",
  desc: "",
});

interface PermissionTest {
  user: string;
  permission: "administrator" | "readonly" | "edit";
}

const changepr: PermissionTest[] = [
  {
    user: "A",
    permission: "readonly",
  },
  {
    user: "B",
    permission: "readonly",
  },
  {
    user: "C",
    permission: "edit",
  },
  {
    user: "D",
    permission: "administrator",
  },
];

const backmain = () => {
  console.log(name);
  router.replace({ name: "main", params: { username: name } });
};
</script>

<style scoped>
.coding {
  height: 100%;
  background-color: var(--color-neutral-2);
}
.header-span {
  margin: 0 10px;
}
.el-header {
  height: 40px;
  background-color: #fff;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  border-bottom-style: solid;
  border-bottom-width: 1.5px;
  border-bottom-color: var(--color-neutral-3);
}
.header {
  display: flex;
  justify-content: center;
  align-items: center;
}
.el-container {
  height: 100%;
  width: 100%;
}
.a-resize-box {
  height: 100%;
}
.el2 {
  flex-grow: 1;
}
</style>
