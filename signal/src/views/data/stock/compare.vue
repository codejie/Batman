<template>
  <div style="padding:30px;">
    <div>
      <label>
        stock symbol:
        <input v-model="stockSymbol" type="string" name="stockSymbol" placeholder="002236"/>
      </label>
      <el-button style="margin-left: 8px;" type="primary" @click="onStockSymbol()">OK</el-button>
    </div>
    <stock-detail ref="refDetail" :stockSymbol="stockSymbol"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import StockDetail from './components/stockdetail.vue'

@Component({
  name: 'DataStock',
  components: {
    StockDetail
  }
})

export default class extends Vue {
  private stockSymbol: string = '002236'

  created() {
  }

  private async onStockSymbol() {
    if(!this.stockSymbol){
      alert('编号不能为空')
      return
    }

    let ref:any =this.$refs.refDetail
    ref.loadStock()
  }
}
</script>

