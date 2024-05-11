<template>
  <el-dialog :visible.sync="true" width="55%">
    <el-form ref="form" label-width="80px">
      <el-form-item label="策略名称">strategy.name</el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({
  name: 'StrategyCreateForm'
})

export default class extends Vue {
  private dlgVisable: boolean = false
  @Prop({ required: true}) private visable: boolean = true
}

</script>

<style lang="scss">
</style>