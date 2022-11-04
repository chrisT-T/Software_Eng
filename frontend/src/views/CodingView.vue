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
        <a-resize-box
          :directions="['bottom']"
          style="
            width: 100%;
            text-align: center;
            max-height: 90%;
            min-height: 0;
          "
        >
          <el-button size="small" @click="openFile"> open file </el-button>
          <el-button size="small" @click="changeTheme">change theme </el-button>
          <el-button size="small" @click="changeName">change name </el-button>
          <el-button size="small" @click="deleteFile"> delete file </el-button>
          <el-button size="small" @click="getBreakpoints">
            getBreakpoints
          </el-button>
          <EditorPanel
            ref="editorPanel"
            :theme="editorTheme"
            @save-file="saveFile"
            @start-debug="(path) => runDebugger(name + '/' + path)"
          >
          </EditorPanel>
        </a-resize-box>
      </el-container>
    </el-container>
  </div>
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
import { ref } from "vue";
import FileTreeBox from "@/components/FileTreeBox.vue";
import EditorPanel from "@/components/MonacoEditorPanel/EditorPanel.vue";
import router from "@/router";
import { useRouter } from "vue-router";
const name = useRouter().currentRoute.value.params.username;

const editorTheme = ref("vs");
const editorPanel = ref<InstanceType<typeof EditorPanel> | null>(null);

const backmain = () => {
  console.log(name);
  router.replace({ name: "main", params: { username: name } });
};

function openFile(path: string) {
  console.log("open File");
  editorPanel.value?.addFile("adfa/df.py", "alkdsfjlasdjflad");
}

function changeTheme() {
  editorTheme.value = "vs-dark";
}

function changeName() {
  editorPanel.value?.renameFile("adfa/df.py", "asfs/adf.cpp");
}

function deleteFile() {
  editorPanel.value?.deleteFile("adfa/df.py");
}

function getBreakpoints() {
  console.log(editorPanel.value?.getBreakpoints());
}
function saveFile(path: string, value: string) {
  console.log(path, value);
  return;
}

function runDebugger(filePath: string) {
  return;
}
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
