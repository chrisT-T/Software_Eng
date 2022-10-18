<template>
  <div class="menu-demo">
    <a-menu mode="pop" showCollapseButton>
      <a-menu-item key="1">
        <template #icon><icon-apps></icon-apps></template>
        项目管理
      </a-menu-item>
    </a-menu>
  </div>
</template>

<script lang="ts">
import { IconApps, IconFire, IconHome } from "@arco-design/web-vue/es/icon";

export default {
  components: {
    IconApps,
  },
};
</script>
<style scoped>
.menu-demo {
  padding: 10px;
  margin-right: 15px;
  height: 100%;
}
.menu-demo .arco-menu {
  width: 200px;
  height: 100%;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.3);
  padding-top: 12px;
}

.menu-demo .arco-menu :deep(.arco-menu-collapse-button) {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.menu-demo
  .arco-menu:not(.arco-menu-collapsed)
  :deep(.arco-menu-collapse-button) {
  right: 0;
  bottom: 8px;
  transform: translateX(50%);
}

.menu-demo .arco-menu:not(.arco-menu-collapsed)::before {
  content: "";
  position: absolute;
  right: 0;
  bottom: 0;
  width: 48px;
  height: 48px;
  background-color: inherit;
  border-radius: 50%;
  box-shadow: -4px 0 2px var(--color-bg-2), 0 0 1px rgba(0, 0, 0, 0.3);
  transform: translateX(50%);
}

.menu-demo .arco-menu.arco-menu-collapsed {
  width: 48px;
  height: 100%;
  padding-top: 12px;
  padding-bottom: 138px;
  border-radius: 22px;
}

.menu-demo .arco-menu.arco-menu-collapsed :deep(.arco-menu-collapse-button) {
  right: 8px;
  bottom: 8px;
}
</style>
