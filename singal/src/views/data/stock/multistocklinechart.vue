<template>
  <div style="padding:30px;">
    <h1>Multi Data Stock Line Chart</h1>
    <div>
      <label>
        stock symbol:
        <input v-model="stockSymbol" type="string" name="stockSymbol" placeholder="002236"/>
      </label>
      <el-button style="margin-left: 8px;" type="primary" @click="onStockSymbol()">OK</el-button>
    </div>
    <!-- <div class="chart-container">
      <mixed-chart height="80%" width="100%" :chartData="chartData">
      </mixed-chart>
    </div> -->
    <div class="chart-container">
      <!-- <line-chart :chart-data="lineChartData" :chart-prop="chartProp2" :height="'150px'"/> -->
      <line-chart :chart-data="lineChartData" :chart-prop="chartProp" :height="'650px'"/>
      <!-- <line-chart :chart-data="lineChartData" :chart-prop="chartProp3" :height="'150px'"/> -->
    </div>
    <div><br/><br/><br/><br/><br/><br/><br/><br/><br/></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { ChartData, default as MixedChart } from '@/components/Charts/MixedChart.vue'
import LineChart, { ILineChartProp } from '@/components/ChartsCustomize/LineChart.vue'
import { getStockHistory } from '@/api/data/stock'

@Component({
  name: 'DataStock',
  components: {
    LineChart
  }
})

export default class extends Vue {
  private stockSymbol: string = '002236'
  private lineChartData: Map<string, number[]> = new Map()
  private chartProp: ILineChartProp[] = [{
      keyProp: '日期',
      lineWidth: 0.5,
      height: 100,
      props: [
          {
              name: '振幅'
          },
          {
              name: '涨跌幅'
          },
          {
              name: '涨跌额',
              yAxisIndex: 1
          },
          {
              name: '换手率'
          }
      ],
    },{
      keyProp: '日期',
      lineWidth: 0.5,
      props: [
          {
              name: '开盘',
              color: '#000000'
          },
          {
              name: '收盘',
              color: '#ff0000'
          },
          {
              name: '最高',
              color: '#00ff00'
          },
          {
              name: '最低',
              color: '#0000ff'
          }
      ],
    },
    {
      keyProp: '日期',
      lineWidth: 0.5,
      height: 150,
      props: [
          {
              name: '成交额'
          },
          {
              name: '成交量',
              yAxisIndex: 1
          }
      ],
  }]

  created() {
  }

  private async onStockSymbol() {

    const { data } = await getStockHistory(
      {
        "symbol": this.stockSymbol,
        "start": "2023-01-01",
        "end": "2024-01-01",
        "period": "daily",
        'adjust': 'qfq'
      })

    this.lineChartData =  data.result
  }
}
</script>

<style lang="scss" scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
</style>
