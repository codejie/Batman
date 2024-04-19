<template>
  <el-dialog :visible.sync="dialogVisible" width="35%">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="策略名称">{{strategy.name}}</el-form-item>
      <el-form-item label="策略说明">{{strategy.description}}</el-form-item>
      <el-form-item label="执行时间">
        <el-time-select
          v-model="form.triggerTime"
          :picker-options="{
            start: '00:00',
            step: '00:15',
            end: '23:45'
          }"
          placeholder="选择时间">
        </el-time-select>
      </el-form-item>
      <div style="text-align:right; margin-top:10px;">
        <el-button type="primary" @click="saveStrategy">确认</el-button>
        <el-button @click="dialogVisible=false">取消</el-button>
      </div>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { IStrategyData } from '@/api/def/strategy'

@Component({
  name: 'StrategyInstanceForm'
})

export default class extends Vue {
  @Prop({ required: true }) private strategy!: IStrategyData
  @Prop({ required: false }) private reloadParent!: Function 

  private dialogVisible: boolean = false
  private id?:number
  private form: any = { triggerTime: '' }

  created() {
  }

  private init(id: number, trigger: any) {
    this.form.id = id
    if(trigger){
      this.form.triggerTime = trigger.hour + ':' + trigger.minute
    } else {
      this.form.triggerTime = ''
    }
    
    this.dialogVisible = true
  }

  private saveStrategy(){
    alert('保存时间');
    console.log({
      id: this.form.id,
      hour: this.form.triggerTime.split(':')[0],
      minute: this.form.triggerTime.split(':')[1]
    })
    if(this.reloadParent){
      this.reloadParent()
    }
    this.dialogVisible = false

  }

}
</script>
