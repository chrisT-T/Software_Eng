<template>
  <div class="card">
    <a-card title="项目列表" class="list-card">
      <template #extra>
        <a-space>
          <a-button type="outline" shape="round" size="small">导入</a-button>
          <a-button type="primary" shape="round" size="small">新建</a-button>
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
          <a-table-column title="可编辑成员">
            <template #cell="{ record }">
              <a-avatar-group :size="24" :max-count="3">
                <a-avatar v-for="site in record.permissionGp" :key="site">
                  {{ site }}
                </a-avatar>
              </a-avatar-group>
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
                    <!-- <a-dsubmenu value="share-gp">
                      <template #default>分享项目</template>
                    </a-dsubmenu> -->
                    <a-doption>删除项目</a-doption>
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
</template>

<script lang="ts" setup>
import { reactive, getCurrentInstance } from "vue";
import { PaginationProps } from "@arco-design/web-vue/es/pagination";
import { IconDownload, IconEdit } from "@arco-design/web-vue/es/icon";
import router from "@/router";
import { useRouter } from "vue-router";

const name = useRouter().currentRoute.value.params.username;

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
  permissionGp?: string[];
  lastUpdateTime: string;
}

const data: ProjectData[] = [
  {
    projectID: "A123",
    projectName: "Project1",
    language: "C",
    creater: "sam",
    permissionGp: ["A", "B", "C", "D"],
    lastUpdateTime: "2022/10/01 12:33",
  },
  {
    projectID: "A1U83",
    projectName: "Project2",
    language: "Cpp",
    creater: "sam2",
    permissionGp: ["D", "B", "C", "Arco", "some"],
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
    permissionGp: ["C"],
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
