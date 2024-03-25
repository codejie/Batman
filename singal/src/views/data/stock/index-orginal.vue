<template>
  <div style="padding:30px;">
    <h1>Data Stock</h1>
    <div>
      <label>
        stock symbol:
        <input v-model="stockSymbol" type="string" name="stockSymbol" placeholder="002236"/>
      </label>
      <el-button style="margin-left: 8px;" type="primary" @click="onStockSymbol()">OK</el-button>
    </div>
    <div class="chart-container">
      <mixed-chart height="80%" width="100%" :chartData="chartData">
      </mixed-chart>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { ChartData, default as MixedChart } from '@/components/Charts/MixedChart.vue'

import { getStockHistory } from '@/api/data/stock'

@Component({
  name: 'DataStock',
  components: {
    MixedChart
  }
})

export default class extends Vue {
  private stockSymbol: string = '002236'
  private chartData: ChartData = {
    xData: [],
    priceData: [],
    volumeData: []
  }

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

    console.log('==============click')
    console.log(data.result)
    const cdata: ChartData = { xData: data.result['日期'], priceData: data.result['收盘'], volumeData: data.result['成交量'] }
    console.debug(cdata)
    this.chartData = cdata
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
