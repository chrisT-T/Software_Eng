<template>
  <div class="tree">
    <a-tree
      :default-selected-keys="['0-0-1']"
      :data="treeData"
      show-line
      size="mini"
      :animation="false"
    >
      <template #extra="nodeData">
        <IconPlus
          style="
            position: absolute;
            right: 8px;
            font-size: 12px;
            top: 10px;
            color: #3370ff;
          "
          @click="() => onIconClick(nodeData)"
        />
        <IconMinus
          style="
            position: absolute;
            right: 8px;
            font-size: 12px;
            top: 10px;
            color: #3370ff;
          "
          @click="() => onIconClick(nodeData)"
        />
      </template>
    </a-tree>
  </div>
</template>

<script lang="ts" setup>
import { reactive, getCurrentInstance, ref } from "vue";
import { IconPlus, IconMinus } from "@arco-design/web-vue/es/icon";
import { TreeNodeData } from "@arco-design/web-vue/es/tree";

const treeData = ref([
  {
    title: "Trunk 1",
    key: "0-0",
    children: [
      {
        title: "Trunk 1-0",
        key: "0-0-0",
        children: [
          { title: "leaf", key: "0-0-0-0" },
          {
            title: "leaf",
            key: "0-0-0-1",
            children: [{ title: "leaf", key: "0-0-0-1-0" }],
          },
          { title: "leaf", key: "0-0-0-2" },
        ],
      },
      {
        title: "Trunk 1-1",
        key: "0-0-1",
      },
      {
        title: "Trunk 1-2",
        key: "0-0-2",
        children: [
          { title: "leaf", key: "0-0-2-0" },
          {
            title: "leaf",
            key: "0-0-2-1",
          },
        ],
      },
    ],
  },
  {
    title: "Trunk 2",
    key: "0-1",
  },
  {
    title: "Trunk 3",
    key: "0-2",
    children: [
      {
        title: "Trunk 3-0",
        key: "0-2-0",
        children: [
          { title: "leaf", key: "0-2-0-0" },
          { title: "leaf", key: "0-2-0-1" },
        ],
      },
    ],
  },
]);

const onIconClick = (nodeData: TreeNodeData) => {
  const children = nodeData.children;
  children?.push({
    title: "new tree node",
    key: nodeData.key + "-" + (children.length + 1),
  });
  nodeData.children = children;

  treeData.value = [...treeData.value];
};
</script>

<style scoped>
.tree {
  background-color: #fff;
  height: 100%;
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
}
</style>
