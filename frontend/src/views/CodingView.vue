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
        <div>
          <span>{{ project_name }}</span>
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
            @click="dialogFormVisible = true"
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
        <div style="width: 100%">
          <a-resize-box
            :directions="['bottom']"
            style="
              width: 100%;
              text-align: center;
              max-height: 90%;
              min-height: 0;
            "
          >
          </a-resize-box>
        </div>
      </el-container>
    </el-container>
  </div>
  <el-dialog v-model="dialogFormVisible" title="共享项目">
    <el-form :model="form" red="addForm">
      <el-form-item label="用户ID" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="共享权限" :label-width="formLabelWidth">
        <el-select v-model="form.region" placeholder="选择项目语言">
          <el-option label="只可读" value="readonly" />
          <el-option label="可编辑" value="edit" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import {
  IconHome,
  IconUserAdd,
  IconSave,
  IconPlayArrowFill,
  IconBug,
  IconPause,
} from "@arco-design/web-vue/es/icon";
import FileTreeBox from "@/components/FileTreeBox.vue";
import router from "@/router";
import { useRouter } from "vue-router";
import { reactive, getCurrentInstance, ref } from "vue";

const name = useRouter().currentRoute.value.params.username;
const project_name = "Project Name";

const dialogFormVisible = ref(false);

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

interface lang_opt {
  value: "C" | "Python" | "Java" | "Cpp";
  label: string;
}

const options: lang_opt[] = [
  {
    value: "Python",
    label: "python",
    // 根据拓展语言添加
  },
  {
    value: "C",
    label: "C",
  },
  {
    value: "Cpp",
    label: "C++",
  },
  {
    value: "Java",
    label: "Java",
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
