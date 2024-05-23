<template>
    <el-dialog :visible="visibled" width="40%">
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
              <el-form-item label="时间" style="margin-top: 10px;">
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
import { IITriggerInfo, IInstanceInfo } from '@/api/def/finder_strategy'
import { reschedule } from '@/api/strategy/finder'
import { Component, Prop, Vue, Watch} from 'vue-property-decorator'

@Component({
    name: 'TriggerEditForm'
})
export default class extends Vue {
  @Prop({ required: true })
  private visibled: boolean = false
  @Prop({ required: true })
  private instance?: IInstanceInfo

  private mode: string = 'daily'
  private time: Date = new Date()
  
  @Watch('instance')
  onInstanceChanged(newVal: IInstanceInfo, oldVal: IInstanceInfo) {
    this.mode = newVal.trigger.mode
    this.time = new Date()
    this.time.setHours(newVal.trigger.hour!, newVal.trigger.minute!)
  }

  // private onopen() {
  //   console.log('===onopen')
  // }
  // private onOpened() {
  //   console.log(this.instance)
  //   this.mode = this.instance!.trigger.mode
  //   this.time = new Date()
  //   this.time!.setHours(this.instance!.trigger.hour, this.instance!.trigger.minute)
  //   console.log(this.time)
  // }

  // private updateMode() {
  //   return this.instance!.trigger.mode
  // }

  // private updateTime() {
  //   const time = new Date()
  //   time.setHours(this.instance!.trigger.hour, this.instance!.trigger.minute)
  //   return time
  // }

  private async onOKClick() {
    const { data } = await reschedule({
      id: this.instance!.id,
      trigger: {
        mode: this.mode,
        hour: this.time?.getHours(),
        minute: this.time?.getMinutes()
      }
    })

    this.$emit('closed', { code: 0})
  }

  private onCancelClick() {
    this.$emit('closed', { code: -1})
  }
}
</script>

<style lang="scss">
</style>