<template>
  <div style="padding:30px;">
    <div>{{ stockSymbol }}</div>
    <div>
      <label>
        stock symbol:
        <input v-model="symbol" type="string" placeholder="002236"/>
      </label>
      <el-button style="margin-left: 8px;" type="primary" @click="onStockSymbol()">OK</el-button>
    </div>
    <stock-detail ref="refDetail" :stockSymbol="childSymbol"/>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from 'vue-property-decorator'
import StockDetail from './components/stockdetail.vue'

@Component({
  name: 'DataStock',
  components: {
    StockDetail
  }
})
export default class extends Vue {
  @Prop({required: false})
  private stockSymbol?: string // = this.$route.params.stockSymbol

  private symbol: string = '000001'
  private childSymbol: string = this.symbol

  @Watch('stockSymbol')
  onStockSymbolChanged() {
    this.symbol = this.stockSymbol || '000001'
    this.childSymbol = this.stockSymbol || this.symbol
  }

  created() {
    this.symbol = this.stockSymbol || '000001'
    this.childSymbol = this.stockSymbol || this.symbol
  }

  private async onStockSymbol() {
    this.childSymbol = this.symbol
  }
}
</script>

