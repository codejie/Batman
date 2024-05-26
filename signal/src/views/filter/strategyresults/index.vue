<template>
  <el-row>
    <el-col :span="5">
      <el-table :data="strategyInfos" @row-click="onStrategyClick" :border="true" :stripe="true" style="width: 100%; height: 100;">
        <el-table-column label="名称" prop="name"/>
        <el-table-column label="算法" prop="algorithm.name"/>
      </el-table>
      <!-- <el-card class="box-card">{{curStrategy.description}}</el-card> -->
    </el-col>
    <el-col :span="50" style="padding: 10px;">
      <!-- <el-card class="box-card">{{ currentStrategy ? currentStrategy.name + ': ' + currentStrategy.desc : ''}}</el-card> -->
      <el-card class="box-card"> {{  strategyTitle() }}</el-card>
      <el-button size="mini" style="padding-top: 10px; padding-bottom: 10px;" @click="createFormVisabled=true">创建</el-button>
      <el-table :border="true" :stripe="true" align="center"
        :data="instanceList" @row-click="onInstanceClick"
        style="width: 100%; margin-top: 15px;"
      >
        <el-table-column label="实例名称" prop="title" width="160">
          <template slot-scope="{row}">
            <el-button type="text" size="mini" @click="onShowResult(row)">{{row.title}}</el-button>
          </template>
        </el-table-column>
        <el-table-column label="命中" width="60">
          <template slot-scope="{row}">
            {{  row.result ? row.result.items.length : 0 }}
          </template>
        </el-table-column>
        <el-table-column label="更新时间" align="center" prop="lastUpdated" width="170"/>
        <el-table-column label="次数" align="center" prop="runTimes" width="60"/>
        <el-table-column label="计划时间" prop="scheduleTime" width="115">
          <template slot-scope="{row}">
            <el-button v-if="row.trigger" size="mini" type="text" @click="onEditTrigger(row)">
              {{row.trigger.mode}} - {{row.trigger.hour}}:{{row.trigger.minute}}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="180">
          <template slot-scope="{row}">
            <el-button type="text" size="mini" icon="el-icon-tickets" style="margin-right: 15px;" @click="onRunInstance(row)">RUN</el-button>
            <el-button type="text" size="mini" icon="el-icon-delete" @click="onDeleteInstance(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="text-align:center"
        layout="prev, pager, next, sizes, jumper"
        :page-size="pager.pageSize"
        :current-page="pager.currentPage"
        :total="pager.total" />
    </el-col>
    <strategy-create-form ref="StrategyCreateForm" :visibled="createFormVisabled" :strategy="getCurrentStrategy()" @closed="onCreateFormClosed"/>
    <trigger-edit-form ref="TriggerEditForm" :visibled="triggerFormVisabled" :instance="getCurrentInstance()" @closed="onTriggerFormClosed"/>
    <strategy-result-form :visibled="resultFormVisibled" :instance="getCurrentInstance()" :strategy="getCurrentStrategy()" @closed="onResultFormClosed" @selected="onResultFormSelected"/>
  </el-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Pager } from '@/api/pager'
import { IStrategyInfo, IInstanceInfo } from '@/api/def/finder_strategy'
import { getInfos, getInstanceByStategy } from '@/api/strategy/finder'
import StrategyCreateForm from './create_form.vue'
import TriggerEditForm from './trigger_form.vue'
import StrategyResultForm from './result_form.vue'
import { removeInstance, runInstance } from '@/api/strategy/finder'

@Component({
  name: 'StrategyFilter',
  components: {
    StrategyCreateForm,
    TriggerEditForm,
    StrategyResultForm
  }
})
export default class IndexVue extends Vue {
  private pager: Pager = {
    total: 0,
    pageSize: 20,
    currentPage: 1
  }
  private strategyInfos: IStrategyInfo[] = []
  private currentStrategy: IStrategyInfo | undefined = undefined
  private currentInstance?: IInstanceInfo
  private instanceList: IInstanceInfo[] = []

  private createFormVisabled: boolean = false
  private triggerFormVisabled: boolean = false
  private resultFormVisibled: boolean = false

  private strategyTitle(): string  {
    return this.currentStrategy ? `${this.currentStrategy.name}: ${this.currentStrategy.desc}` : ''
  }

  created() { 
    this.loadStrategyInfos()
  }

  private getCurrentStrategy(): IStrategyInfo | undefined {
    return this.currentStrategy
  }

  private getCurrentInstance(): IInstanceInfo | undefined {
    return this.currentInstance
  }

  private async loadStrategyInfos() {
    const { data } = await getInfos({})
    for (const info of data.result) {
      const item: IStrategyInfo = {
        name: info.name,
        desc: info.desc,
        algorithm: info.algorithm
      }

      this.strategyInfos.push(item)
    }

    this.currentStrategy = this.strategyInfos[0]
    this.loadStrategyInstances()
  }

  async loadStrategyInstances() {
    const { data } = await getInstanceByStategy({
      strategy: this.currentStrategy!.name
    })

    this.instanceList = data.result
  }

  private onStrategyClick(row: IStrategyInfo) {
    this.currentStrategy = row
    this.loadStrategyInstances()
  }

  private onInstanceClick(row: IInstanceInfo) {
    // this.currentInstance = row
    // this.resultFormVisibled = true
  }

  private onCreateFormClosed(args: any) {
    if (args.code == 0)
      this.loadStrategyInstances()

    this.createFormVisabled = false;
  }

  private onEditTrigger(row: any) {
    this.currentInstance = row
    this.triggerFormVisabled = true;
  }

  private onTriggerFormClosed(args: any) {
    if (args.code == 0)
      this.loadStrategyInstances()

    this.triggerFormVisabled = false;
  }

  private onResultFormClosed(args: any) {
    this.resultFormVisibled = false;   
  }

  private onResultFormSelected(args: any) {
    this.resultFormVisibled = false;
    if (args.symbol)
      this.$router.push({name: 'DataStock', params: {stockSymbol: args.symbol}})     
  }

  private onShowResult(row: any) {
    this.currentInstance = row
    this.resultFormVisibled = true
  }

  private async onDeleteInstance(row: any) {
    try {
      const ret = await this.$confirm(
        `Delete strategy instance '${row.title}' ?`,
        'Warning',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
      
      const { data } = await removeInstance({
        id: row.id
      })

      this.loadStrategyInstances()
    } catch (e) {

    } 
  }

  private async onRunInstance(row: any) {
    try {
      const ret = await this.$confirm(
        `Start to execute strategy instance '${row.title}' ?`,
        'Information',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'info',          
        })
      const { data } = await runInstance({
        id: row.id
      })

      this.loadStrategyInstances()
    } catch (e) {

    }
  }
}
</script>

<style lang="scss">
.header-center {
  text-align: center;
}

.box-card {
  margin-top: 10px;
  margin-bottom: 10px;
}

</style>


