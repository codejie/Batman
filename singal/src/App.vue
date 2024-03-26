<template>
  <div id="app">
    <router-view />
    <service-worker-update-popup />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ServiceWorkerUpdatePopup from '@/pwa/components/ServiceWorkerUpdatePopup.vue'

@Component({
  name: 'App',
  components: {
    ServiceWorkerUpdatePopup
  }
  // computed: {
  //   console: () => console
  // }
})
export default class extends Vue {}
</script>

<style lang="scss">
.el-table th{
  padding: 2px;
}

.el-table td{
  padding: 2px;
}

.el-form-item {
  margin: 2px;

}
</style>
