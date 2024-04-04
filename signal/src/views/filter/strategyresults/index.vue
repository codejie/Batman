<template>
  <el-row>
    <el-col :span="4">
      <el-menu default-active="0" style="height: 400px;">
        <el-menu-item v-for="(strategy,index) in strategyList" :index="index.toString()" @click="selectStrategy(strategy)">
          <i class="el-icon-data-analysis"></i>
          <span slot="title">{{strategy.name}}</span>
        </el-menu-item>
      </el-menu>
      <el-card class="box-card">{{curStrategy.description}}</el-card>
    </el-col>
    <el-col :span="20" style="padding: 10px">
      <el-button size="mini" @click="createStrategy">创建</el-button>
      <el-table :border="true" :stripe="true" align="center"
        :data="instanceList"
        style="width: 100%;margin-top: 15px;"
      >
        <el-table-column label="标题" prop="title" min-width="150"/>
        <el-table-column label="策略" min-width="150">
          <template>
            {{ curStrategy.name }}
          </template>
        </el-table-column>
        <el-table-column label="最后执行时间" align="center" prop="lastRunTime" width="165"/>
        <el-table-column label="执行次数" align="center" prop="runTimes" width="60"/>
        <el-table-column label="计划时间" prop="scheduleTime" width="115">
          <template slot-scope="{row}">
            <el-button v-if="row.trigger" size="mini" type="text" icon="el-icon-edit" @click="editTrigger(row)">
              {{modeMap[row.trigger.mode]}}{{row.trigger.hour}}:{{row.trigger.minute}}
            </el-button>
            <el-button v-else type="text" size="mini" icon="el-icon-edit" @click="editTrigger(row)">
              编辑
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="60">
          <template slot-scope="{row}">
            <el-button type="text" size="mini" icon="el-icon-tickets" @click="showResults(row)">查看</el-button>
            <!-- {{ row.id }}查看 -->
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="text-align:center"
        layout="prev, pager, next, sizes, jumper"
        :page-size="pager.pageSize"
        :current-page="pager.currentPage"
        :total="pager.total"
        @size-change="sizeChange"
        @current-change="currentChange">
      </el-pagination>
    </el-col>
    <strategy-form ref="refForm" :strategy="curStrategy" :reload-parent="loadInstanceList"/>
    <trigger-form ref="refTriggerForm" :strategy="curStrategy" :reload-parent="loadInstanceList"/>
    <strategy-result ref="refResult" :strategy="curStrategy" :instance="curInstance"/>
  </el-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Pager } from '@/api/pager'
import { IStrategyData, IStrategyInstanceData } from '@/api/def/strategy'
import StrategyForm from './form.vue'
import TriggerForm from './triggerform.vue'
import StrategyResult from './resultindex.vue'
import { getInfo, getInstanceByStategy } from '@/api/strategy/finder'
import { getInstanceByDom } from 'echarts'

@Component({
  name: 'StrategyFilter',
  components: {
    StrategyForm, TriggerForm, StrategyResult
  },
  filters: {
    transactionStatusFilter: (status: string) => {
      const statusMap: { [key: string]: string } = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    },
    orderNoFilter: (str: string) => str.substring(0, 30),
    // Input 10000 => Output "10,000"
    toThousandFilter: (num: number) => {
      return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
    }
  }
})
export default class extends Vue {
  private pager: Pager = {
    total: 0,
    pageSize: 20,
    currentPage: 1
  }
  private strategyList: IStrategyData[] = []
  private curStrategyId: String = '1'
  private curStrategy: IStrategyData = {
    id: 0,
    name: '',
    description: ''
  }
  private instanceList: IStrategyInstanceData[] = [] 
  private modeMap = { daily:'每天' }
 
  private curInstance?: IStrategyInstanceData

  created() { 
    this.loadStrategyList()
  }

  private async loadStrategyList(){
    // var strategyList = []
    const { data } = await getInfo({})
    console.log(data)
    for (const info of data.result) {
      console.log(info)
      const item: IStrategyData = {
        id: 0,
        name: info.name,
        description: info.desc,
        arguments: []        
      }
      for (const arg of info.strategy.args) {
        (<any[]>item.arguments).push({
          name: arg.name,
          unit: arg.unit,
          value: arg.default,
          notes: arg.desc
        })
      }

      this.strategyList.push(item)
    }

    this.curStrategy = this.strategyList[0]
    this.loadInstanceList()
  }

  private async loadInstanceList(){
    console.log('===========加载实例列表==========')

    const { data } = await getInstanceByStategy({
      strategy: this.curStrategy.name
    })

    console.log(data)
    console.log(data.result)
    let instanceList: IStrategyInstanceData[] = []
    
    for (const inst of data.result) {
      instanceList.push({
        id: 0,
        strategyId: (<any>inst).id,
        title: (<any>inst).title,
        trigger: (<any>inst).trigger,
        arguments: (<any>inst).args,
        lastRunTime: (<any>inst).response ? (<any>inst).response.updated : '<>',
        runTimes: (<any>inst).response ? (<any>inst).response.runTimes : '<>'
      })
    }


    // console.log(this.pager)
    // var instanceList = []
    // let now = new Date()
    // let nowStr = now.getFullYear() + '-' + (now.getMonth()+1) + '-' + now.getDate()
    //     + ' ' + now.getHours() + '-' + now.getMinutes() + '-' + now.getSeconds() 
    // for(var i=1; i<=2; i++){
    //   instanceList.push({
    //     id: i,
    //     strategyId: this.curStrategy.id,
    //     title: this.curStrategy.name + ' instance' + i,
    //     lastRunTime: nowStr,
    //     runTimes: 27,
    //     scheduleTime: 'Every Trade Day 20:30',
    //     trigger: {
    //       mode: 'daily',
    //       hour: 23,
    //       minute: 30
    //     },
    //     arguments: [
    //       { name: '上涨天数', unit: '天', value: 123, notes: '最近交易日前的连续上涨天数' },
    //       { name: '上涨幅度', unit: '%', value: 66, notes: '最近交易日前的每天上涨幅度' },
    //       { name: '下跌天数', unit: '天', value: 456, notes: '最近交易日前的连续下跌天数' },
    //       { name: '下跌幅度', unit: '%', value: 88, notes: '最近交易日前的每天下跌幅度' }
    //     ]
    //   })
    // }

    this.instanceList = instanceList
    this.pager.total = this.instanceList.length
  }

  private selectStrategy(strategy: IStrategyData) {
    this.curStrategy = strategy
    this.pager.currentPage = 1
    this.loadInstanceList()
  }

  private createStrategy() {
    let ref:any =this.$refs.refForm
    ref.init()
  }

  private editTrigger(row: any) {
    let ref:any =this.$refs.refTriggerForm
    ref.init(row.id, row.trigger)
  }

  private showResults(instance: IStrategyInstanceData){
    this.curInstance = instance
    let ref:any =this.$refs.refResult
    ref.init()
  }

  private currentChange(currentPage: number) {
    this.pager.currentPage = currentPage
    this.loadInstanceList()
  }

  private sizeChange(pageSize: number) {
    this.pager.pageSize = pageSize
    this.loadInstanceList()
  }
  
}
</script>

<style lang="scss">
.header-center {
  text-align: center;
}

</style>


