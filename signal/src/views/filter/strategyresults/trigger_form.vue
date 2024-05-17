<template>
    <el-dialog :visible.sync="visibled" width="40%" @opened="onOpened">
      <el-form ref="form" label-position="right" label-width="80px">
        <el-form-item label="定时器" style="margin-top: 15px;">
          <div>
            <el-form label-position="right">
              <el-form-item label="类型">
                <el-radio-group v-model="mode">
                  <el-radio-button label="daily" value="daily"/>
                  <el-radio-button label="interval" value="interval" disabled/>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="时间">
                <el-time-picker placeholder="select time" format="HH:mm" v-model="time" />
              </el-form-item>
            </el-form>
          </div>
        </el-form-item>        
      </el-form>
      <div style="text-align:right; margin-top:15px;">
          <el-button type="primary" @click="onOKClick">确认</el-button>
          <el-button @click="onCancelClick">取消</el-button>
      </div>
    </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue} from 'vue-property-decorator'

@Component({
    name: 'TriggerEditForm'
})
export default class extends Vue {
  @Prop({ required: true })
  private visibled: boolean = true

  private mode: string = 'daily'
  private time?: Date
  
  private onOpened() {

  }

  private onOKClick() {
    this.$emit('closed', { code: 0})
  }

  private onCancelClick() {
    this.$emit('closed', { code: -1})
  }
}
</script>

<style lang="scss">
</style>