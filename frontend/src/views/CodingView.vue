<template>
  <div class="coding">
    <el-container>
      <el-header>
        <div class="header">
          <icon-home :style="{ fontSize: '18px' }" :stroke-width="3" />
          <icon-save :style="{ fontSize: '18px' }" :stroke-width="3" />
          <span class="header-span">TO-CODE</span>
          <a-avatar :size="20">Arco</a-avatar>
        </div>
        <div class="user-part">
          <a-button-group type="primary" size="mini">
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
          <icon-user-add :stroke-width="3" />
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
  height: 30px;
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
