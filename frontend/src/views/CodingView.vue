<template>
  <div class="coding">
    <DragBall />
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
          <a-avatar-group>
            <a-avatar
              v-for="item in Editing"
              :key="item.username"
              :style="{ backgroundColor: item.color }"
            >
              {{ item.username }}
            </a-avatar>
          </a-avatar-group>
        </div>
        <div class="user-part">
          <a-button-group type="primary" size="small">
            <a-button @click="runCurrentCode()">
              <template #icon><icon-play-arrow-fill /></template>
            </a-button>
          </a-button-group>
          <a-divider direction="vertical" />
        </div>
      </el-header>
      <el-container class="el2">
        <splitpanes class="default-theme">
          <pane size="30">
            <LeftBar @open-file="openFile" :language="projectLanguage" />
          </pane>
          <pane>
            <splitpanes horizontal>
              <pane>
                <EditorPanel
                  ref="editorPanel"
                  :theme="editorTheme"
                  :container-subdomain="projectSubdomain"
                  :username="name"
                  :projectid="projectID"
                  @save-file="saveFile"
                  @start-debug="(path) => runDebugger(name + '/' + path)"
                >
                </EditorPanel>
              </pane>
              <pane>
                <BottomPanel
                  ref="bottomPanel"
                  :container-id="containerId"
                  :container-subdomain="projectSubdomain"
                  :key="containerId"
                ></BottomPanel>
              </pane>
            </splitpanes>
            <!-- <el-button size="small" @click="changeTheme"
                >change theme
              </el-button>
              <el-button size="small" @click="changeName">change name </el-button>
              <el-button size="small" @click="deleteFile">
                delete file
              </el-button>
              <el-button size="small" @click="getBreakpoints">
                getBreakpoints
              </el-button>
              <el-button size="small" @click="getcolorMap">
                getcolorMap
              </el-button>
              <el-button size="small" @click="focusLine"> focusLine </el-button>
              <el-button size="small" @click="clearFocusLine">
                clearFocusLine
              </el-button> -->
          </pane>
        </splitpanes>
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
import {
  reactive,
  getCurrentInstance,
  ref,
  onMounted,
  onUnmounted,
  watch,
} from "vue";
import {
  IconHome,
  IconUserAdd,
  IconSave,
  IconPlayArrowFill,
  IconBug,
  IconPause,
  IconDoubleRight,
} from "@arco-design/web-vue/es/icon";
import LeftBar from "@/components/LeftBar/LeftBar.vue";
import EditorPanel from "@/components/MonacoEditorPanel/EditorPanel.vue";
import router from "@/router";
import { useRouter } from "vue-router";
import BottomPanel from "@/components/BottomPanel/BottomPanel.vue";
import DragBall from "@/components/DragBall.vue";
import axios from "axios";
import { ElNotification } from "element-plus";
import { Splitpanes, Pane } from "splitpanes";

onMounted(() => {
  axios.get(`/api/project/${projectID}/`).then((response) => {
    containerId.value = response.data["docker_id"];
    projectSubdomain.value = response.data["hash_id"];
    projectLanguage.value = response.data["project_language"];
    projectName = response.data["project_name"];
    console.log(response.data);
  });

  setInterval(() => {
    const time = new Date().getTime();
    localStorage.setItem("active_time", time);
  }, 5 * 60 * 1000);
});
const name = useRouter().currentRoute.value.params.username;
const projectID = useRouter().currentRoute.value.params.projectid;

const Editing = ref([]);
const editorTheme = ref("vs");
const editorPanel = ref<InstanceType<typeof EditorPanel> | null>(null);
const bottomPanel = ref<InstanceType<typeof BottomPanel> | null>(null);
const dialogTableVisible = ref(false);
const dialogShareVisible = ref(false);

const containerId = ref("");
const projectSubdomain = ref("");
const projectLanguage = ref("");
let projectName = "";

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
  console.log("dispose panel");
  editorPanel.value?.disposePanel();
  console.log(name);
  console.log(typeof name);
  router.replace({ name: "main", params: { username: name } });
};

function openFile(path: string) {
  axios
    .get(`/api/file/${projectID}/${path}`)
    .then((response) => {
      let file = response.data;
      editorPanel.value?.addFile(path, file);
    })
    .catch();
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

watch(
  () => editorPanel.value?.userColor,
  (val) => {
    console.log("watch updated");
    Editing.value = val;
  },
  { deep: true }
);
function getcolorMap() {
  console.log(editorPanel.value?.userColor[0]);
  console.log(Editing.value);
}

// run current code in terminal
function runCurrentCode() {
  console.log("run code");

  let path = "";
  path = editorPanel.value?.getFilePath();
  if (path === "") {
    ElNotification({
      title: "Warning",
      message: "No opening file to run",
      type: "warning",
    });
  } else {
    if (path[0] == "/") {
      path = path.substring(1, path.length);
    }
    path = `/${projectName}/${path}`;
    console.log(path);
    if (projectLanguage.value.includes("python")) {
      bottomPanel.value?.outputRunCommand(`python ${path}`);
    } else {
      ElNotification({
        title: "Warning",
        message: "Running current language is not supported",
        type: "warning",
      });
    }
  }
}

function saveFile(path: string, value: string) {
  const param = new FormData();
  const export_blob = new Blob([value]);
  param.append("file", export_blob);
  axios
    .put(`/api/file/${projectID}/${path}`, param)
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      if (err.response.status === 404) {
        ElNotification({
          title: "Warning",
          message: "Permission denied",
          type: "warning",
        });
      }
    });

  return;
}

function runDebugger(filePath: string) {
  console.log(filePath);
  return;
}

function focusLine() {
  editorPanel.value?.focusLine("adfa/df.py", 35);
  return;
}

function clearFocusLine() {
  editorPanel.value?.clearFocusLine();
  return;
}
</script>

<style scoped>
@import "splitpanes/dist/splitpanes.css";
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
.splitpanes {
  display: flex;
  width: 100%;
  height: 100%;
}
.splitpanes--horizontal {
  flex-direction: column;
}
.splitpanes--vertical {
  flex-direction: row;
}
</style>
