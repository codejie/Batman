<template>
  <el-dialog :visible.sync="visabled" width="55%" @opened="onOpened">
    <el-form ref="form" label-position="right" label-width="80px">
      <el-form-item label="策略名称">
        {{ strategy.name }}({{ strategy.algorithm.name }})
      </el-form-item>      
      <el-form-item label="实例名称">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="参数" style="margin-top: 15px;">
        <el-table :border="true" :data="form.args">
          <el-table-column label="名称" prop="info.name" width="120" />
          <el-table-column label="描述" prop="info.desc" width="200" />          
          <el-table-column label="单位" prop="info.unit" width="60" />
          <el-table-column label="数值" width="100">
            <template slot-scope="{row}">
              <el-input v-model="row.value" size="mini" />
            </template>
          </el-table-column>
        </el-table>
      </el-form-item>
      <el-form-item label="定时器" style="margin-top: 15px;">
        <div>
          <el-form ref="form.trigger" label-position="right">
            <el-form-item label="类型">
              <el-radio-group v-model="form.trigger.mode">
                <el-radio-button label="daily" value="daily"/>
                <el-radio-button label="interval" value="interval" disabled/>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="时间">
              <el-time-picker placeholder="select time" format="HH:mm" v-model="form.trigger.time" />
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
import { IStrategyInfo, IArgumentInfo } from '@/api/def/finder_strategy'
import { Component, Prop, Vue} from 'vue-property-decorator'
import { schedule } from '@/api/strategy/finder'

@Component({
  name: 'StrategyCreateForm'
})
export default class StrategyCreateForm extends Vue {
  @Prop()
  private visabled: boolean = false
  @Prop()
  private strategy?: IStrategyInfo
  
  private form: {
    name: string,
    args: {
      info: IArgumentInfo,
      value: any
    }[],
    trigger: {
      mode: string,
      time?: Date
    }
  } = {
    name: '',
    args: [],
    trigger: {
      mode: 'daily',
      time: undefined
    }
  }

  private onOpened() {
    this.resetForm()

    if (this.strategy && this.strategy.algorithm.args) {
      this.strategy.algorithm.args.forEach(arg => {
        this.form.args.push({
          info: arg,
          value: ''
        })
      })
    }    
  }

  private resetForm() {
   this.form = {
      name: '',
      args: [],
      trigger: {
        mode: 'daily',
        time: undefined
      }
    } 
  }

  private async onOKClick() {
    console.log(JSON.stringify(this.form))

    const args: {
      [key in string]: any
    } = {}
    this.form.args.forEach(arg => {
      args[arg.info.name] = arg.value
    })

    const trigger = {
      mode: this.form.trigger.mode,
      hour: this.form.trigger.time ? this.form.trigger.time.getHours() : 0,
      minute: this.form.trigger.time ? this.form.trigger.time?.getMinutes() : 0
    }


    const { data } = await schedule({
      title: this.form.name,
      strategy: this.strategy?.name,
      args: args,
      trigger: trigger
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