<template>
  <el-dialog :visible.sync="visable" width="55%">
    <el-form ref="form" label-position="right" label-width="80px">
      <el-form-item label="策略名称">
        {{ strategy.name }}({{ strategy.algorithm.name }}) {{ strategy }}
      </el-form-item>      
      <el-form-item label="实例名称">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="参数">
        <div v-for="item in strategy.algorithm.args" :key="item">
          <el-form-item label="item" :key="item"></el-form-item>
        </div>
      </el-form-item>
      <el-form-item label="定时器">
        <el-form ref="form.trigger" label-position="right">
          <el-form-item label="类型">
            <el-checkbox-group v-model="form.trigger.mode">
              <el-checkbox-button label="每日" name="daily" checked="true"/>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="时间">
            <el-time-picker placeholder="select time" format="HH:mm" v-model="form.trigger.time" />
          </el-form-item>
        </el-form>
      </el-form-item>
    </el-form>
    <el-form ref="form" label-width="80px">
      <el-form-item label="策略名称">strategy.name</el-form-item>
    </el-form>
    <div style="text-align:right; margin-top:10px;">
        <el-button type="primary" @click="onOKClick">确认</el-button>
        <el-button @click="onCancelClick">取消</el-button>
      </div>
  </el-dialog>
</template>

<script lang="ts">
import { IStrategyInfo } from '@/api/def/finder_strategy'
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({
  name: 'StrategyCreateForm'
})

export default class StrategyCreateForm extends Vue {
  visable: boolean = false
  strategy?: IStrategyInfo
  
  private form: {
    name: string,
    args: {
      [key in string]: any
    },
    trigger: {
      mode: string,
      time: string
    }
  } = {
    name: '',
    args: {
    },
    trigger: {
      mode: 'daily',
      time: ''
    }
  }

  created() {

  }

  private onOKClick() {
    this.visable = false
  }

  private onCancelClick() {
    this.visable = false
  }
}

</script>

<style lang="scss">
</style>