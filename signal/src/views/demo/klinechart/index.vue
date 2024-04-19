<template>
  <div class="dashboard-editor-container">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="kLineChartData" :selectStart="selectStart" :selectEnd="selectEnd" :height="'550px'" />
    </el-row>
  </div>
</template>

<script lang="ts">
import 'echarts/theme/macarons.js' // Theme used in BarChart, LineChart, PieChart and RadarChart
import { Component, Vue } from 'vue-property-decorator'
import LineChart from './components/KLineChart.vue'
import { kData } from './components/KData'

@Component({
  name: 'LineChartDemo',
  components: {
    LineChart
  }
})

export default class extends Vue {
  private kLineChartData: (string|number)[][] = []
  private selectStart?:string
  private selectEnd?:string

  created() {
    this.loadData()
  }

  private loadData() {
    // this.kLineChartData = kData
    let kLineChartData: (string|number)[][] = []
    kData.forEach(data=>{
      let day = data[0].toString()
      if(day.substring(0,4)=='2004'){
        kLineChartData.push(data)
      }
    })
    this.selectStart = '2004-11-10'
    this.selectEnd = '2004-12-03'
    this.kLineChartData = kLineChartData
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
