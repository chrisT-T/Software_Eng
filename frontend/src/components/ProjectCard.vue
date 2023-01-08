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
      <a-table
        class="table"
        :data="data"
        ellipsis="true"
        noDataElement="创建你的新项目"
        hoverable
      >
        <template #columns>
          <a-table-column
            title="项目名称"
            :filterable="{
              filters: [
                {
                  text: 'Python',
                  value: 'python',
                },
                {
                  text: 'Cpp',
                  value: 'Cpp',
                },
                {
                  text: 'C',
                  value: 'C',
                },
                {
                  text: 'Java',
                  value: 'Java',
                },
              ],
              filter: (value, row) => row.language.includes(value),
            }"
          >
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
                    v-if="
                      record.language.includes('python') ||
                      record.language.includes('Python')
                    "
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
                  <span :style="{ margin: '10px' }">
                    {{ record.projectName }}
                  </span>
                </div>
              </router-link>
            </template>
          </a-table-column>
          <a-table-column
            title="创建人"
            data-index="creator"
            :sortable="{
              sortDirections: ['ascend', 'descend'],
            }"
          ></a-table-column>
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
                  <a-doption
                    @click="
                      printtable(record.permissionGp),
                        (dialogTableVisible = true),
                        (Userform.project_id = record.projectID),
                        (PermissionChangeform.project_id = record.projectID)
                    "
                    >查看权限组</a-doption
                  >
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
          <a-table-column
            title="创建时间"
            data-index="createTime"
            :width="150"
            :sortable="{
              sortDirections: ['ascend', 'descend'],
            }"
          ></a-table-column>
          <a-table-column :width="100">
            <template #cell="{ record }">
              <div class="btn-gp">
                <a-dropdown position="bottom">
                  <a-button type="text" shape="circle"><icon-edit /></a-button>
                  <template #content>
                    <a-doption
                      @click="
                        (NameEditform.originalName = record.projectName),
                          (NameEditform.projectId = record.projectID),
                          (dialogEditNameVisible = true)
                      "
                    >
                      修改名称
                    </a-doption>
                    <a-doption
                      @click="
                        (Deleteform.name = record.projectName),
                          (Deleteform.projectId = record.projectID),
                          (dialogDeleteVisible = true)
                      "
                    >
                      删除项目
                    </a-doption>
                    <a-doption
                      @click="
                        printtable(record.permissionGp),
                          (dialogTableVisible = true),
                          (Userform.project_id = record.projectID),
                          (PermissionChangeform.project_id = record.projectID)
                      "
                      >查看权限组</a-doption
                    >
                  </template>
                </a-dropdown>
                <a-button
                  type="text"
                  shape="circle"
                  @click="DownloadProject(record.projectID)"
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
    <el-form :model="NewProjform" ref="addProjectForm">
      <el-form-item label="项目名称" :label-width="formLabelWidth">
        <el-input v-model="NewProjform.project_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="项目模板" :label-width="formLabelWidth">
        <el-select v-model="NewProjform.language" placeholder="选择项目语言">
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
        <el-button
          type="primary"
          @click="addNewProject(), (dialogFormVisible = false)"
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog v-model="dialogUploadVisible" title="上传项目">
    <el-upload
      class="upload-demo"
      drag
      :action="getUploadPath()"
      multiple
      :beforeUpload="beforeProjectUpload"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
    </el-upload>
    <el-input
      label="项目名称"
      v-model="NewProjform.project_name"
      autocomplete="off"
    />
    <el-select
      label="项目名称"
      v-model="NewProjform.language"
      :label-width="formLabelWidth"
      placeholder="选择项目语言"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </el-dialog>

  <el-dialog v-model="dialogTableVisible" title="权限组" width="600px">
    <el-button @click="clearFilter">reset all filters</el-button>
    <el-table
      :data="changepr"
      style="width: 100%"
      max-height="250"
      ref="permissionGpRef"
    >
      <el-table-column prop="user" label="用户名" />
      <el-table-column
        label="权限"
        prop="permission"
        :filters="[
          { text: '只可读', value: 'read' },
          { text: '可编辑', value: 'edit' },
          { text: '管理员', value: 'admin' },
          { text: '邀请待接受', value: 'pending' },
        ]"
        filter-placement="bottom-end"
        :filter-method="filterTag"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.permission === 'admin' ? 'warning' : 'info'"
            disable-transitions
            effect="plain"
          >
            <span v-if="scope.row.permission === 'admin'"> 管理员 </span>
            <span v-if="scope.row.permission === 'read'"> 只可读 </span>
            <span v-if="scope.row.permission === 'edit'"> 可编辑 </span>
            <span v-if="scope.row.permission === 'pending'"> 邀请待接受 </span>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column>
        <template #default="scope">
          <span
            v-if="scope.row.state === 'pending'"
            :style="{ color: 'rgb(var(--red-5))' }"
          >
            pending
          </span>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="180">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click="
              removeCurrentPermission(scope.row.user, scope.row.permission)
            "
          >
            移除成员
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click="
              OpenChangePermission(scope.row.user, scope.row.permission),
                (dialogPermissionChangeVisible = true)
            "
          >
            修改权限
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogShareVisible = true" style="width: 100%"
          >新增权限组</el-button
        >
      </span>
    </template>
  </el-dialog>

  <el-dialog
    v-model="dialogShareVisible"
    title="邀请新成员"
    class="share-dialog"
    width="350px"
    align-center
  >
    <el-form :model="Userform" ref="addForm">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="Userform.username" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogShareVisible = false">Cancel</el-button>
        <el-button
          type="primary"
          @click="(dialogShareVisible = false), addNewUserPermission()"
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog
    v-model="dialogEditNameVisible"
    title="修改项目名称"
    class="share-dialog"
    align-center
    width="350px"
  >
    <el-form
      ref="NameEditRef"
      :model="NameEditform"
      label-position="top"
      :rules="NameEditrules"
      status-icon
    >
      <el-form-item label="新名称" prop="new_name">
        <el-input v-model="NameEditform.new_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="NameEditform.password"
          autocomplete="off"
          type="password"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button
          @click="resetForm(NameEditRef), (dialogEditNameVisible = false)"
          >Cancel</el-button
        >
        <el-button
          type="primary"
          @click="
            changeProjectName(NameEditRef), (dialogEditNameVisible = false)
          "
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog
    v-model="dialogDeleteVisible"
    title="删除项目"
    align-center
    width="350px"
  >
    <el-form
      :model="Deleteform"
      ref="ProjDeleteRef"
      label-position="top"
      status-icon
      :rules="Deleterules"
    >
      <el-form-item label="项目名称" prop="confirmname">
        <el-input v-model="Deleteform.confirmname" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="Deleteform.password"
          autocomplete="off"
          type="password"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button
          @click="resetForm(ProjDeleteRef), (dialogDeleteVisible = false)"
          >Cancel</el-button
        >
        <el-button
          type="primary"
          @click="removeProject(ProjDeleteRef), (dialogDeleteVisible = false)"
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog
    v-model="dialogPermissionChangeVisible"
    title="修改用户权限"
    class="share-dialog"
    align-center
    width="350px"
    draggable
  >
    <el-form
      ref="PermissionChangeRef"
      :model="PermissionChangeform"
      label-position="top"
      status-icon
    >
      <el-form-item label="共享权限" prop="new_permission">
        <el-select
          v-model="PermissionChangeform.new_permission"
          placeholder="选择新用户权限"
        >
          <el-option label="只可读" value="read" />
          <el-option label="可编辑" value="edit" />
          <el-option label="项目管理员" value="admin" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button
          type="primary"
          @click="
            changeCurrentPermission(), (dialogPermissionChangeVisible = false)
          "
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted, vue } from "vue";
import { PaginationProps } from "@arco-design/web-vue/es/pagination";
import { IconDownload, IconEdit } from "@arco-design/web-vue/es/icon";
import { UploadFilled } from "@element-plus/icons-vue";
import router from "@/router";
import { useRouter } from "vue-router";
import type { FormInstance } from "element-plus";
import { ElTable, ElMessage } from "element-plus";
import axios from "axios";
import qs from "qs";

const permissionGpRef = ref<InstanceType<typeof ElTable>>();
const NameEditRef = ref<FormInstance>();
const ProjDeleteRef = ref<FormInstance>();
const PermissionChangeRef = ref<FormInstance>();
const data = ref<ProjectData[]>([]);

const name = useRouter().currentRoute.value.params.username;

onMounted(() => {
  GetProjectList();
});

// 下载当前项目文件
const DownloadProject = (proj_id: number) => {
  window.open(`/api/project/${proj_id}/download/`);
};
// 添加新权限组
const addNewUserPermission = () => {
  if (Userform.username === "") {
    console.log("error!");
  } else {
    axios
      .post(
        `/api/project/${Userform.project_id}/invite/`,
        qs.stringify(Userform)
      )
      .then(function (response) {
        const code = response.status;
        if (code === 204) {
          GetProjectList();
        }
      })
      .catch(function (error) {
        ElMessage({
          message: "Add new user permission failed",
          type: "warning",
        });
        console.log(error);
      });
  }
  Userform.username = "";
};

// 移除用户
const removeCurrentPermission = (user: string, permission: string) => {
  console.log(user); // 删除的用户名
  PermissionChangeform.original_permission = permission;
  PermissionChangeform.new_permission = "remove";
  PermissionChangeform.username = user;
  changeCurrentPermission();
};

// 拉取项目列表
const GetProjectList = () => {
  axios.get(`/api/user/${name}/projects/`).then(function (response) {
    data.value = response.data;
  });
};

const PermissionChangeform = reactive({
  username: "",
  original_permission: "",
  new_permission: "",
  project_id: "",
});

const OpenChangePermission = (user: string, permission: string) => {
  PermissionChangeform.username = user;
  PermissionChangeform.original_permission = permission;
};

// 修改权限
const changeCurrentPermission = () => {
  console.log(PermissionChangeform); // 修改权限细节(包括修改权限的用户名，原来的权限和新权限)
  axios
    .post(
      `/api/project/${PermissionChangeform.project_id}/perm/`,
      qs.stringify(PermissionChangeform)
    )
    .then(function (response) {
      const code = response.status;
      console.log(response.data);
      GetProjectList();
    })
    .catch(function (error) {
      ElMessage({
        message: "Change permission failed",
        type: "warning",
      });
      console.log(error);
    });
  PermissionChangeform.username = "";
  PermissionChangeform.original_permission = "";
  PermissionChangeform.new_permission = "";
};

const clearFilter = () => {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  permissionGpRef.value!.clearFilter();
};

const addNewProject = () => {
  if (NewProjform.language === "" || NewProjform.project_name === "") {
    console.log("New Proj Error");
  } else {
    console.log(NewProjform);
    // 新增项目
    axios
      .post("/api/project/", qs.stringify(NewProjform))
      .then(function (response) {
        const code = response.status;
        console.log(response.data);
        GetProjectList();
      })
      .catch(function (error) {
        ElMessage({
          message: "Create project failed",
          type: "warning",
        });
      });
  }
  NewProjform.language = "";
  NewProjform.name = "";
};

const removeProject = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      axios
        .delete(`/api/project/${Deleteform.projectId}/`, {
          data: Deleteform,
        })
        .then(function (response) {
          const code = response.status;
          console.log(response.data);
          GetProjectList();
        })
        .catch(function (error) {
          ElMessage({
            message: "Delete project failed",
            type: "warning",
          });
        });
      formEl.resetFields();
    } else {
      ElMessage({
        message: "Error Message",
        type: "warning",
      });
      formEl.resetFields();
      return false;
    }
  });
};

const changeProjectName = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      console.log(NameEditform);
      axios
        .put(
          `/api/project/${NameEditform.projectId}/`,
          qs.stringify(NameEditform)
        )
        .then(function (response) {
          const code = response.status;
          console.log(response.data);
          GetProjectList();
        })
        .catch(function (error) {
          ElMessage({
            message: "Change project name failed",
            type: "warning",
          });
        });
      formEl.resetFields();
    } else {
      console.log("error submit!");
      formEl.resetFields();
      return false;
    }
  });
};

const dialogFormVisible = ref(false);
const dialogUploadVisible = ref(false);
const dialogTableVisible = ref(false);
const dialogShareVisible = ref(false);
const dialogEditNameVisible = ref(false);
const dialogDeleteVisible = ref(false);
const dialogPermissionChangeVisible = ref(false);

const formLabelWidth = "140px";
const NewProjform = reactive({
  project_name: "",
  language: "",
  creator_name: name,
});

const Userform = reactive({
  username: "",
  project_id: "",
});

const NameEditform = reactive({
  originalName: "",
  new_name: "",
  projectId: "",
  password: "",
});

const Deleteform = reactive({
  name: "",
  projectId: "",
  confirmname: "",
  password: "",
});

const validateNewName = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入项目新名称"));
  } else if (value === NameEditform.originalName) {
    callback(new Error("新名称不应该与原名称相同"));
  } else {
    callback();
  }
};

const validatepass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入密码"));
  } else {
    callback();
  }
};

const validateconfirmName = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入需要删除的项目名称"));
  } else if (value !== Deleteform.name) {
    callback(new Error("新名称应该与原名称相同"));
  } else {
    callback();
  }
};

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

const NameEditrules = reactive({
  new_name: [{ validator: validateNewName, trigger: "blur" }],
  password: [{ validator: validatepass, trigger: "blur" }],
});

const Deleterules = reactive({
  confirmname: [{ validator: validateconfirmName, trigger: "blur" }],
  password: [{ validator: validatepass, trigger: "blur" }],
});

interface lang_opt {
  value:
    | "python3.8"
    | "python3.9"
    | "python3.10"
    | "python3.10-datasci"
    | "python3.10-ml"
    | "C"
    | "Java"
    | "Cpp";
  label: string;
}

const options: lang_opt[] = [
  {
    value: "python3.8",
    label: "Python3.8",
  },
  {
    value: "python3.9",
    label: "Python3.9",
  },
  {
    value: "python3.10",
    label: "Python3.10",
  },
  {
    value: "python3.10-datasci",
    label: "Python3.10-DataSci",
  },
  {
    value: "python3.10-ml",
    label: "Python3.10-ML",
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

const basePagination: PaginationProps = {
  current: 1,
  pageSize: 10,
  hideOnSinglePage: true,
};

interface ProjectData {
  projectID: string;
  projectName: string;
  language: string;
  creator: string;
  permissionGp?: PermissionTest[];
  lastUpdateTime: string;
  createTime: string;
  dockerId: string;
}

interface PermissionTest {
  user: string;
  permission: string;
  state: string;
}

const changepr = ref<PermissionTest[]>();

const printtable = (data: PermissionTest[] | undefined) => {
  if (!data) {
    data = [];
  }
  changepr.value = [...data];
  console.log(changepr);
};

const filterTag = (value: string, row: PermissionTest) => {
  return row.permission === value;
};

function beforeProjectUpload(file) {
  let extension = file.name.replace(/.+\./, "");
  if (extension !== "zip") {
    ElMessage({
      message: "上传文件必须为 zip 格式",
      type: "warning",
    });
    return false;
  }

  if (NewProjform.project_name === "") {
    ElMessage({
      message: "请填写项目名称",
      type: "warning",
    });
    return false;
  }
  if (NewProjform.language === "") {
    ElMessage({
      message: "请填写项目名称",
      type: "warning",
    });
    return false;
  }
  return true;
}

function getUploadPath() {
  let url = `/api/project/upload/${NewProjform.creator_name}/${NewProjform.project_name}/${NewProjform.language}`;
  console.log(NewProjform);
  return url;
}
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
.card .list-card .arco-card-header-title {
  display: flex;
  padding-left: 20px;
}
</style>
