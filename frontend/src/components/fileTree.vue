<template>
  <div class="custom-tree-container">
    <div class="tree-main">
      <span class="spanStyle" style="margin-left: 10px">{{ projectName }}</span>
      <a-button-group type="text">
        <a-button @click="(dialogNewFVisible = true), (NewFform.path = '')">
          <template #icon><icon-plus /></template>
        </a-button>
      </a-button-group>
    </div>
    <el-tree
      :data="dataSource"
      node-key="id"
      default-expand-all
      :expand-on-click-node="false"
      @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <span class="custom-tree-node">
          <el-dropdown
            v-if="!data.showInput"
            trigger="contextmenu"
            size="small"
          >
            <span class="el-dropdown-link spanStyle">
              {{ node.label }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item
                  :icon="Plus"
                  @click="
                    (dialogNewFNodeVisible = true),
                      (nodeappend = data),
                      (NewFform.path = data.path)
                  "
                  :disabled="data.type === 'file'"
                  >Append</el-dropdown-item
                >
                <el-dropdown-item
                  :icon="DeleteFilled"
                  @click="remove(node, data)"
                  >Delete</el-dropdown-item
                >
                <el-dropdown-item
                  :icon="EditPen"
                  @click="
                    (dialogChangeNameVisible = true),
                      (ChgNform.path = data.path)
                  "
                  >Change name</el-dropdown-item
                >
                <el-dropdown-item :icon="CaretRight">Debug</el-dropdown-item>
                <el-dropdown-item :icon="Download">Download</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </span>
      </template>
    </el-tree>
  </div>
  <el-dialog
    v-model="dialogNewFVisible"
    title="新增"
    class="new-dialog"
    align-center
    width="350px"
  >
    <el-form
      ref="NewFRef"
      :model="NewFform"
      label-position="top"
      :rules="NewFrules"
      status-icon
    >
      <el-form-item label="Name" prop="name">
        <el-input v-model="NewFform.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Type" prop="type">
        <el-radio-group v-model="NewFform.type">
          <el-radio label="folder" />
          <el-radio label="file" />
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="resetForm(NewFRef), (dialogNewFVisible = false)"
          >Cancel</el-button
        >
        <el-button
          type="primary"
          @click="submitForm(NewFRef), (dialogNewFVisible = false)"
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog
    v-model="dialogNewFNodeVisible"
    title="新增"
    class="new-dialog"
    align-center
    width="350px"
  >
    <el-form
      ref="NewFRef"
      :model="NewFform"
      label-position="top"
      :rules="NewFrules"
      status-icon
    >
      <el-form-item label="Name" prop="name">
        <el-input v-model="NewFform.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Type" prop="type">
        <el-radio-group v-model="NewFform.type">
          <el-radio label="folder" />
          <el-radio label="file" />
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="resetForm(NewFRef), (dialogNewFNodeVisible = false)"
          >Cancel</el-button
        >
        <el-button
          type="primary"
          @click="submitNodeForm(NewFRef), (dialogNewFNodeVisible = false)"
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog
    v-model="dialogChangeNameVisible"
    title="修改文件名"
    class="new-dialog"
    align-center
    width="350px"
  >
    <el-form ref="ChgNRef" :model="ChgNform" label-position="top" status-icon>
      <el-form-item label="Name" prop="name">
        <el-input v-model="ChgNform.newName" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button
          @click="resetForm(ChgNRef), (dialogChangeNameVisible = false)"
          >Cancel</el-button
        >
        <el-button
          type="primary"
          @click="
            changeName(ChgNRef),
              resetForm(ChgNRef),
              (dialogChangeNameVisible = false)
          "
        >
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from "vue";
import type Node from "element-plus/es/components/tree/src/model/node";
import {
  Plus,
  DeleteFilled,
  EditPen,
  CaretRight,
  Download,
  defineEmits,
} from "@element-plus/icons-vue";
import { IconFolderAdd, IconPlus } from "@arco-design/web-vue/es/icon";
import { useRouter } from "vue-router";
import type { FormInstance } from "element-plus";
import axios from "axios";

const NewFRef = ref<FormInstance>();
const ChgNRef = ref<FormInstance>(); // Change file Name
let dialogNewFVisible = ref(false);
let dialogNewFNodeVisible = ref(false);
let dialogChangeNameVisible = ref(false);
const nodeappend = ref<Tree>();
const projectName = ref("");
const dataSource = ref<Tree[]>([]);
const projectID = useRouter().currentRoute.value.params.projectid;
const NewFform = reactive({
  name: "",
  type: "",
  path: "",
});
const ChgNform = reactive({
  newName: "",
  path: "",
});

const NewFrules = reactive({
  name: [{ required: true, message: "Please input name", trigger: "blur" }],
  type: [
    {
      required: true,
      message: "Please select type",
      trigger: "change",
    },
  ],
});

const emit = defineEmits<{
  (e: "openFile", path: string): void;
}>();

const getFileList = () => {
  axios.get(`/api/project/${projectID}/tree/`).then((response) => {
    console.log(response.data);
    dataSource.value = response.data.children;
  });
};

const submitNodeForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      axios
        .post(`/api/file/${projectID}/${NewFform.path}/${NewFform.name}`, {
          type: NewFform.type,
        })
        .catch((err) => {
          console.log(err);
        });
      console.log(NewFform);
      append();
      formEl.resetFields();
    } else {
      console.log("error submit!");
      return false;
    }
  });
};
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      axios
        .post(`/api/file/${projectID}/${NewFform.name}`, {
          type: NewFform.type,
        })
        .catch((err) => {
          console.log(err);
        });
      console.log(NewFform);
      addNew2Proj();
      formEl.resetFields();
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

const handleNodeClick = (data: Tree) => {
  if (data.type == "file") {
    emit("openFile", data.path);
  }
  console.log(data);
};

interface Tree {
  label: string;
  path: string;
  type: string;
  children?: Tree[];
}
let id = 5;

const append = () => {
  const data = nodeappend.value;
  if (!data) {
    console.log("error append");
  } else {
    const name = NewFform.name;
    const child_path = data.path + "/" + name;
    const newChild = {
      label: name,
      path: child_path,
      type: NewFform.type,
      children: [],
    };
    if (!data.children) {
      data.children = [];
    }
    data.children.push(newChild);
    dataSource.value = [...dataSource.value];
  }
};

const addNew2Proj = () => {
  const name = NewFform.name;
  const child_path = name;
  const newChild = {
    id: id++,
    label: name,
    path: child_path,
    type: NewFform.type,
    children: [],
  };
  dataSource.value.push(newChild);
};

const remove = (node: Node, data: Tree) => {
  console.log(node);
  console.log(data);
  const parent = node.parent;
  const children: Tree[] = parent.data.children || parent.data;
  const index = children.findIndex((d) => d.id === data.id);
  children.splice(index, 1);
  dataSource.value = [...dataSource.value];

  axios.delete(`/api/file/${projectID}${data.path}`).catch((err) => {
    console.log(err);
  });
};

const changeName = () => {
  axios
    .post(`/api/file/${projectID}/rename/${ChgNform.path}`, {
      new_name: ChgNform.newName,
    })
    .catch((err) => {
      console.log(err);
    });
  getFileList();
};

onMounted(() => {
  getFileList();

  axios.get(`api/project/${projectID}/`).then((resp) => {
    console.log(resp);
    projectName.value = resp.data["project_name"];
  });
});
</script>

<style>
.custom-tree-container {
  width: 100%;
  height: 100%;
  background-color: white;
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  width: 100%;
}
.tree-main {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.spanStyle {
  white-space: nowrap; /*强制span不换行*/
  display: inline-block; /*将span当做块级元素对待*/
  overflow: hidden; /*超出宽度部分隐藏*/
  text-overflow: ellipsis; /*超出部分以点号代替*/
  line-height: 0.9; /*数字与之前的文字对齐*/
}
</style>
