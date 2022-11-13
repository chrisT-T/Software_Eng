<template>
  <div class="custom-tree-container">
    <div class="tree-main">
      <span class="spanStyle" style="margin-left: 10px">PROJECT NAME</span>
      <a-button-group type="text">
        <a-button @click="(dialogNewFVisible = true), addNew2Proj()">
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
                  @click="(dialogNewFVisible = true), append(data)"
                  :disabled="data.type === 'file'"
                  >Append</el-dropdown-item
                >
                <el-dropdown-item
                  :icon="DeleteFilled"
                  @click="remove(node, data)"
                  >Delete</el-dropdown-item
                >
                <el-dropdown-item :icon="EditPen">Change name</el-dropdown-item>
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
        <el-button type="primary" @click="submitForm(NewFRef)">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue";
import type Node from "element-plus/es/components/tree/src/model/node";
import {
  Plus,
  DeleteFilled,
  EditPen,
  CaretRight,
  Download,
} from "@element-plus/icons-vue";
import { IconFolderAdd, IconPlus } from "@arco-design/web-vue/es/icon";
import type { FormInstance } from "element-plus";

const NewFRef = ref<FormInstance>();
let dialogNewFVisible = ref(false);

const NewFform = reactive({
  name: "",
  type: "",
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

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log("submit!");
      dialogNewFVisible = ref(false);
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
  console.log(data);
};

interface Tree {
  id: number;
  label: string;
  path: string;
  type: string;
  children?: Tree[];
}
let id = 1000;

const append = (data: Tree) => {
  const name = "test";
  const child_path = data.path + "/" + name;
  const newChild = {
    id: id++,
    label: name,
    path: child_path,
    type: "file",
    children: [],
  };
  if (!data.children) {
    data.children = [];
  }
  data.children.push(newChild);
  dataSource.value = [...dataSource.value];
};

const addNew2Proj = () => {
  const name = "test";
  const child_path = name;
  const newChild = {
    id: id++,
    label: name,
    path: child_path,
    type: "folder",
    children: [],
  };
  dataSource.value.push(newChild);
};

const remove = (node: Node, data: Tree) => {
  const parent = node.parent;
  const children: Tree[] = parent.data.children || parent.data;
  const index = children.findIndex((d) => d.id === data.id);
  children.splice(index, 1);
  dataSource.value = [...dataSource.value];
};

const dataSource = ref<Tree[]>([
  {
    id: 1,
    label: "task_1",
    path: "task_1",
    type: "folder",
    children: [
      {
        id: 2,
        label: "task_2",
        path: "task_1/task_2",
        type: "folder",
        children: [
          {
            id: 3,
            label: "task_3",
            path: "task_1/task_2/tasl_3",
            type: "file",
          },
          {
            id: 4,
            label: "task_4",
            path: "task_1/task_2/tasl_4",
            type: "file",
          },
        ],
      },
    ],
  },
]);
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
