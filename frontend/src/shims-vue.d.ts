/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
  import Vue from 'vue'
  export default Vue
}

declare module "vue-session"