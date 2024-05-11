<template>
  <el-row>
    <el-col :span="4">
      <!-- <el-menu default-active="0" style="height: 400px;">
        <el-menu-item v-for="(strategy,index) in strategyList" :index="index.toString()" @click="selectStrategy(strategy)">
          <i class="el-icon-data-analysis"></i>
          <span slot="title">{{strategy.name}}</span>
        </el-menu-item>
      </el-menu> -->
      <el-table :data="strategyInfos" @row-click="handleRowClick" :border="true" :stripe="true" style="width: 100%; height: 100;">
        <el-table-column label="名称" prop="name"/>
        <el-table-column label="算法" prop="algorithm.name"/>
      </el-table>
      <!-- <el-card class="box-card">{{curStrategy.description}}</el-card> -->
    </el-col>
    <el-col :span="20" style="padding: 10px">
      <el-card class="box-card">{{ currentStrategy ? currentStrategy.name + ': ' + currentStrategy.desc : ''}}</el-card>
      <el-button size="mini" style="padding-top: 10px; padding-bottom: 10px;" @click="createStrategy">创建</el-button>
      <el-table :border="true" :stripe="true" align="center"
        :data="instanceList"
        style="width: 100%;margin-top: 15px;"
      >
        <el-table-column label="标题" prop="title" min-width="150"/>
        <el-table-column label="策略" prop="strategy" min-width="150" />
        <el-table-column label="最后执行时间" align="center" prop="lastUpdated" width="165"/>
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
    <strategy-create-form ref="StrategyCreateForm" :visable="createFrameVisable"/>
    <!-- <trigger-form ref="refTriggerForm" :strategy="curStrategy" :reload-parent="loadInstanceList"/>
    <strategy-result ref="refResult" :strategy="curStrategy" :instance="curInstance"/> -->
  </el-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Pager } from '@/api/pager'
// import { IStrategyData, IStrategyInstanceData } from '@/api/def/strategy'
import { IArgumentInfo, IAlgorithmInfo, IStrategyInfo, InstanceInfo } from '@/api/def/finder_strategy'
// import StrategyForm from './form.vue'
// import TriggerForm from './triggerform.vue'
// import StrategyResult from './resultindex.vue'
import { getInfos, getInstanceByStategy } from '@/api/strategy/finder'
import StrategyCreateForm from './create_form.vue'
// import { getInstanceByDom } from 'echarts'

@Component({
  name: 'StrategyFilter',
  components: {
    StrategyCreateForm
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
  private strategyInfos: IStrategyInfo[] = []
  private currentStrategy?: IStrategyInfo
  private instanceList: InstanceInfo[] = []

  private createFrameVisable: boolean = true

  private modeMap = { daily:'每天' }
 
  created() { 
    // this.loadStrategyList()
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

  private async loadStrategyInstances() {
    const { data } = await getInstanceByStategy({
      strategy: this.currentStrategy!.name
    })

    this.instanceList = data.result
    // console.log(this.instanceList)
  }

  private handleRowClick(row: IStrategyInfo) {
    this.currentStrategy = row
    this.loadStrategyInstances()
  }

  private createStrategy() {

    this.createFrameVisable = true

    console.log('==========' + this.createFrameVisable)
    // let ref:any =this.$refs.refForm
    // ref.init()
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


