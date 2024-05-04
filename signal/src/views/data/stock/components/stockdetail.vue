<template>
  <div style="padding:30px;">
    <el-select size="mini" style="width: 80px" v-model="showYear" @change="yearChange">
      <el-option v-for="year in years" :value="year" :key="year"/>
    </el-select>
    <div class="chart-container">
      <k-line-chart width="100%" :height="'550px'"
          :chartData="chartData" :showStart="showStart" :selectStart="selectStart" :selectEnd="selectEnd"/>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import KLineChart from '@/components/ChartsCustomize/KLineChart.vue'

import { getStockHistory } from '@/api/data/stock'

@Component({
  name: 'StockDetail',
  components: {
    KLineChart
  }
})

export default class extends Vue {
  // @Prop({ default: '000001' }) private stockSymbol!: string

  private stockSymbol: string = '000001'
  private showYear: number = (new Date()).getFullYear()
  private years: number[] = []
  private showStart?:string
  private selectStart?:string
  private selectEnd?:string
  
  private chartData = {}

  created() {
    for(var i=2004; i<=(new Date()).getFullYear(); i++){
      this.years.push(i)
    }
    // console.log(this.stockSymbol)
    // if(this.stockSymbol){
    this.loadStock(this.stockSymbol)
    // }
  }

  private async loadStock(symbol: string) {
    this.stockSymbol = symbol
    const { data } = await getStockHistory({
        "symbol": this.stockSymbol,
        "start": (this.showYear - 1) + "-11-01",
        "end": this.showYear + "-12-31",
        "period": "daily",
        'adjust': 'qfq'
    })
    let categoryData = data.result['日期'];
    if(!categoryData || categoryData.length==0){
      alert('该年度无数据')
      return
    }
    this.showStart = this.showYear + "-01-01"
    this.selectStart = categoryData[categoryData.length>60?(categoryData.length-20):0]
    this.selectEnd = categoryData[categoryData.length - 1]

    this.chartData = data.result
  }

  private yearChange(index: number){
    this.loadStock(this.stockSymbol)
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
