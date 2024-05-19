<template>
  <el-row>
    <el-col :span="5">
      <el-table :data="strategyInfos" @row-click="onStrategyClick" :border="true" :stripe="true" style="width: 100%; height: 100;">
        <el-table-column label="名称" prop="name"/>
        <el-table-column label="算法" prop="algorithm.name"/>
      </el-table>
      <!-- <el-card class="box-card">{{curStrategy.description}}</el-card> -->
    </el-col>
    <el-col :span="40" style="padding: 10px;">
      <el-card class="box-card">{{ currentStrategy ? currentStrategy.name + ': ' + currentStrategy.desc : ''}}</el-card>
      <el-button size="mini" style="padding-top: 10px; padding-bottom: 10px;" @click="createFormVisabled=true">创建</el-button>
      <el-table :border="true" :stripe="true" align="center"
        :data="instanceList" @row-click="onInstanceClick"
        style="width: 100%; margin-top: 15px;"
      >
        <el-table-column label="实例名称" prop="title" width="120"/>
        <!-- <el-table-column label="策略" prop="strategy" min-width="80" /> -->
        <el-table-column label="执行时间" align="center" prop="lastUpdated" width="170"/>
        <el-table-column label="次数" align="center" prop="runTimes" width="60"/>
        <el-table-column label="计划时间" prop="scheduleTime" width="115">
          <template slot-scope="{row}">
            <el-button v-if="row.trigger" size="mini" type="text" icon="el-icon-edit" @click="onEditTrigger(row)">
              {{row.trigger.mode}}{{row.trigger.hour}}:{{row.trigger.minute}}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="180">
          <template slot-scope="{row}">
            <el-button type="text" size="mini" icon="el-icon-tickets" @click="onShowResult(row)">查看</el-button>
            <el-button type="text" size="mini" icon="el-icon-delete" @click="deleteInstance(row)">删除</el-button>
            <!-- {{ row.id }}查看 -->
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="text-align:center"
        layout="prev, pager, next, sizes, jumper"
        :page-size="pager.pageSize"
        :current-page="pager.currentPage"
        :total="pager.total" />
    </el-col>
    <strategy-create-form ref="StrategyCreateForm" :visibled="createFormVisabled" :strategy="currentStrategy || null" @closed="onCreateFormClosed"/>
    <trigger-edit-form ref="TriggerEditForm" :visibled="triggerFormVisabled" :instance="currentInstance" @closed="onTriggerFormClosed"/>
    <strategy-result-form :visibled="resultFormVisibled" :instance="currentInstance" :strategy="currentStrategy" @closed="onResultFormClosed"/>
    <!-- <trigger-form ref="refTriggerForm" :strategy="curStrategy" :reload-parent="loadInstanceList"/>
    <strategy-result ref="refResult" :strategy="curStrategy" :instance="curInstance"/> -->
  </el-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Pager } from '@/api/pager'
// import { IStrategyData, IStrategyInstanceData } from '@/api/def/strategy'
import { IArgumentInfo, IAlgorithmInfo, IStrategyInfo, IInstanceInfo } from '@/api/def/finder_strategy'
// import StrategyForm from './form.vue'
// import TriggerForm from './triggerform.vue'
// import StrategyResult from './resultindex.vue'
import { getInfos, getInstanceByStategy } from '@/api/strategy/finder'
import StrategyCreateForm from './create_form.vue'
import TriggerEditForm from './trigger_form.vue'
import StrategyResultForm from './result_form.vue'
// import { getInstanceByDom } from 'echarts'

@Component({
  name: 'StrategyFilter',
  components: {
    StrategyCreateForm,
    TriggerEditForm,
    StrategyResultForm
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
export default class IndexVue extends Vue {
  private pager: Pager = {
    total: 0,
    pageSize: 20,
    currentPage: 1
  }
  private strategyInfos: IStrategyInfo[] = []
  private currentStrategy?: IStrategyInfo
  private currentInstance?: IInstanceInfo;
  private instanceList: IInstanceInfo[] = []

  // private modeMap = { daily:'每天' }

  private createFormVisabled: boolean = false
  private triggerFormVisabled: boolean = false
  private resultFormVisibled: boolean = false

  created() { 
    this.loadStrategyInfos()
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
    console.log('=============== loadStrategyInstances' + this.currentStrategy!.name)
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
    this.currentInstance = row
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

  private onShowResult(row: any) {
    this.currentInstance = row
    this.resultFormVisibled = true
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


