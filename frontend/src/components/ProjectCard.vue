<template>
  <div class="card">
    <a-card title="项目列表" class="list-card">
      <template #extra>
        <a-space>
          <a-button
            type="outline"
            shape="round"
            size="small"
            @click="dialogUploadVisible = true"
            >导入</a-button
          >
          <a-button
            type="primary"
            shape="round"
            size="small"
            @click="dialogFormVisible = true"
          >
            新建
          </a-button>
        </a-space>
      </template>
      <a-table :pagination="basePagination" :data="data" ellipsis="true">
        <template #columns>
          <a-table-column title="项目名称">
            <template #cell="{ record }">
              <router-link
                replace
                :to="{
                  name: 'coding',
                  params: { username: name, projectid: record.projectID },
                }"
              >
                <div class="type-box">
                  <img
                    v-if="record.language === 'Python'"
                    alt="avater"
                    src="https://api.iconify.design/logos:python.svg"
                  />
                  <img
                    v-if="record.language === 'Java'"
                    alt="avater"
                    src="https://api.iconify.design/logos:java.svg"
                  />
                  <img
                    v-if="record.language === 'C'"
                    alt="avater"
                    src="https://api.iconify.design/logos:c.svg"
                  />
                  <img
                    v-if="record.language === 'Cpp'"
                    alt="avater"
                    src="https://api.iconify.design/logos:c-plusplus.svg"
                  />
                  <!-- <span>{{ record.projectName }}</span> -->

                  <span :style="{ margin: '10px' }">
                    {{ record.projectName }}
                  </span>
                </div>
              </router-link>
            </template>
          </a-table-column>
          <a-table-column title="创建人">
            <template #cell="{ record }">
              <div class="creater-box">
                {{ record.creater }}
              </div>
            </template>
          </a-table-column>
          <a-table-column title="权限组">
            <template #cell="{ record }">
              <a-dropdown position="bl">
                <div class="pr-gp">
                  <a-avatar-group :size="24" :max-count="3">
                    <a-avatar v-for="site in record.permissionGp" :key="site">
                      {{ site.user }}
                    </a-avatar>
                  </a-avatar-group>
                </div>
                <template #content>
                  <a-doption>修改权限组</a-doption>
                </template>
              </a-dropdown>
            </template>
          </a-table-column>

          <a-table-column
            title="最后更新时间"
            data-index="lastUpdateTime"
            :width="150"
            :sortable="{
              sortDirections: ['ascend', 'descend'],
            }"
          ></a-table-column>
          <a-table-column :width="100">
            <template #cell>
              <div class="btn-gp">
                <a-dropdown position="bottom">
                  <a-button type="text" shape="circle"><icon-edit /></a-button>
                  <template #content>
                    <a-doption>修改名称</a-doption>
                    <a-doption>删除项目</a-doption>
                    <a-doption>修改权限组</a-doption>
                  </template>
                </a-dropdown>
                <a-button type="text" shape="circle"
                  ><icon-download
                /></a-button>
              </div>
            </template>
          </a-table-column>
        </template>
      </a-table>
    </a-card>
  </div>

  <el-dialog v-model="dialogFormVisible" title="新建项目">
    <el-form :model="form" red="addForm">
      <el-form-item label="项目名称" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="项目模板" :label-width="formLabelWidth">
        <el-select v-model="form.region" placeholder="选择项目语言">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
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
  <el-dialog v-model="dialogUploadVisible" title="上传项目">
    <el-upload
      class="upload-demo"
      drag
      action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
      multiple
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
      <!-- <template #tip>
        <div class="el-upload__tip">上传新项目</div>
      </template> -->
    </el-upload>
  </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, getCurrentInstance, ref } from "vue";
import { PaginationProps } from "@arco-design/web-vue/es/pagination";
import { IconDownload, IconEdit } from "@arco-design/web-vue/es/icon";
import { UploadFilled } from "@element-plus/icons-vue";
import router from "@/router";
import { useRouter } from "vue-router";
import { ElMessageBox } from "element-plus";

const name = useRouter().currentRoute.value.params.username;

const dialogFormVisible = ref(false);
const dialogUploadVisible = ref(false);

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

const handleClose = (done: () => void) => {
  ElMessageBox.confirm("确定关闭新建项目表单")
    .then(() => {
      done();
    })
    .catch(() => {
      // catch error
    });
};

const basePagination: PaginationProps = {
  current: 1,
  pageSize: 10,
  hideOnSinglePage: true,
};

interface ProjectData {
  projectID: string;
  projectName: string;
  language: "C" | "Python" | "Java" | "Cpp";
  creater: string;
  permissionGp?: PermissionTest[];
  lastUpdateTime: string;
}

interface PermissionTest {
  user: string;
  permission: "readonly" | "edit";
}

const data: ProjectData[] = [
  {
    projectID: "A123",
    projectName: "Project1",
    language: "C",
    creater: "sam",
    permissionGp: [
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
    ],
    lastUpdateTime: "2022/10/01 12:33",
  },
  {
    projectID: "A1U83",
    projectName: "Project2",
    language: "Cpp",
    creater: "sam2",
    permissionGp: [
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
    ],
    lastUpdateTime: "2022/03/01 15:47",
  },
  {
    projectID: "A1po23",
    projectName: "Project3",
    language: "Python",
    creater: "sam",
    lastUpdateTime: "2021/11/08 02:53",
  },
  {
    projectID: "KJ1d3",
    projectName: "Project4",
    language: "Java",
    creater: "sam",
    permissionGp: [
      {
        user: "A",
        permission: "readonly",
      },
      {
        user: "Arco",
        permission: "edit",
      },
      {
        user: "C",
        permission: "edit",
      },
    ],
    lastUpdateTime: "2022/02/01 05:13",
  },
  {
    projectID: "AJKpo0",
    projectName: "Project5",
    language: "Python",
    creater: "sam2",
    lastUpdateTime: "2020/10/01 21:00",
  },
];
</script>

<style scoped>
.card {
  padding: 10px;
  flex-grow: 1;
}
.list-card {
  height: 100%;
  margin-top: 10px;
}
.creater-box {
  min-width: 100px;
}
.type-box {
  display: flex;
}
.type-box span {
  margin: 0 10px;
  white-space: nowrap;
}
.router-link-active {
  text-decoration: none;
  color: black;
}
a {
  text-decoration: none;
  color: black;
}
</style>

<style>
.card .list-card .arco-card-header-title {
  display: flex;
  padding-left: 20px;
}
</style>
