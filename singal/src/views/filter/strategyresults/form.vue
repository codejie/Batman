<template>
  <el-dialog :visible.sync="dialogVisible" width="55%">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="策略名称">{{strategy.name}}</el-form-item>
      <el-form-item label="策略说明">{{strategy.description}}</el-form-item>
      <el-form-item label="实例名称">
        <el-input v-model="form.title" style="width:100%"/>
      </el-form-item>
      <el-table :border="1"
          :data="form.arguments"
          style="width: 100%;margin-top: 15px;">
          <el-table-column label="参数名" prop="name" width="120"/>
          <el-table-column label="单位" prop="unit" width="80"/>
          <el-table-column label="值" width="120">
            <template slot-scope="{row}">
              <el-input v-model="row.value" style="width:100%"/>
            </template>
          </el-table-column>
          <el-table-column label="说明" prop="notes"/>
      </el-table>
      <div style="text-align:right; margin-top:10px;">
        <el-button type="primary" @click="saveStrategy">确认</el-button>
        <el-button @click="dialogVisible=false">取消</el-button>
      </div>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { IStrategyData, IStrategyInstanceData, IStrategyArgumentData } from '@/api/def/strategy'

@Component({
  name: 'StrategyInstanceForm'
})

export default class extends Vue {
  @Prop({ required: true }) private strategy!: IStrategyData
  @Prop({ required: false }) private reloadParent!: Function 

  private dialogVisible: boolean = false
  private form: IStrategyInstanceData = { title: '', arguments: [] }

  created() {
  }

  private init(id: number) {
    let args: IStrategyArgumentData[] = []

    if(this.strategy && this.strategy.arguments){
      this.strategy.arguments.forEach(argument=>{
        args.push({
          name: argument.name, 
          unit: argument.unit, 
          notes: argument.notes
        })
      })
    }
    this.form = { 
      id: id, 
      strategyId: this.strategy.id,
      title: '', 
      arguments: args 
    }
    this.dialogVisible = true
  }

  private saveStrategy(){
    let form = this.form
    if(form.id){
      alert('修改实例')
      console.log('修改实例')
      console.log(form)
    } else {
      alert('新增实例')
      console.log('新增实例')
      console.log(form)
    }
    this.dialogVisible = false
    if(this.reloadParent){
      this.reloadParent()
    }
  }

}
</script>
