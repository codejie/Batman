<script setup lang="ts">
import { KLineChart4 } from '@/components/KLine'
import { HistoryDataModel } from '@/api/data/wrap';
import { onMounted, PropType, ref, watch } from 'vue';
import { TradeRecord } from './TradeTraceForm.vue';
import { KLineChartData, makeKLineChartData, YData } from '@/utils/kline';

const props = defineProps({
  history: {
    type: Object as PropType<HistoryDataModel[]>,
    required: true
  },
  records: {
    type: Object as PropType<TradeRecord[]>,
    required: true
  }
})

const chart = ref<typeof KLineChart4>()

function initChart() {
  chart.value?.addGrid(0, '4%', '4%', '4%', '40%')
  chart.value?.addGrid(1, '4%', '70%', '4%', '6%')
}

function setKLineData(kline: KLineChartData) {
  chart.value?.addAxis(0, kline.xData, true)
  chart.value?.addAxis(1, kline.xData, false)
  chart.value?.addAxisPointer([0, 1])

  chart.value?.addKLine(0, 'KLine', kline.klineData.data, true, false)
}

function setActionData(buy: YData, sell: YData) {
  chart.value?.addLine(0, '买入', buy, false)
  chart.value?.addLine(0, '卖出', sell, false)
}

function setQuantityData(buy: YData, sell: YData, total: YData) {
  chart.value?.addBar(1, '买入', buy, false)
  chart.value?.addBar(1, '卖出', sell, false)
  chart.value?.addStepLine(1, '数量', total, false)
}

onMounted(() => {
  initChart()  
})

function tradeData(data: TradeRecord[]) {
  const buy = {}
  const sell = {}
  const total = []
  let sum: number = 0
  for (let i = data.length - 1; i >=0; -- i) {
    const item = data[i]
  // data.forEach(item => {
    if (item.action == '买入') {
      buy[item.created] = {
        quantity: (buy[item.created] ? buy[item.created].quantity + item.quantity : item.quantity),
        expense: (buy[item.created] ? buy[item.created].expense + item.expense : item.expense)
      }
      sum += item.quantity
      // total[item.created] = total[item.created] ? total[item.created] + item.quantity : item.quantity
    } else {
      sell[item.created] = {
        quantity: (sell[item.created] ? sell[item.created].quantity + item.quantity : item.quantity),
        expense: (sell[item.created] ? sell[item.created].expense + item.expense : item.expense)
      }
      sum -= item.quantity
      // total[item.created] = total[item.created] ? total[item.created] - item.quantity : -item.quantity
    }
    total[item.created] = sum
  }

  const buyLine: YData = []
  const sellLine: YData = []
  const buyQuantity: YData = []
  const sellQuantity: YData = []
  const totalQuantity: YData = []
  for (const k in buy) {
    buyLine.push([k, (buy[k].expense / buy[k].quantity).toFixed(2)])
    buyQuantity.push([k, buy[k].quantity, 1])
  }
  for (const k in sell) {
    sellLine.push([k, (sell[k].expense / sell[k].quantity).toFixed(2)])
    sellQuantity.push([k, -sell[k].quantity, -1])
  }
  for (const k in total) {
    totalQuantity.push([k, total[k]])
  }
  return {
    buyLine,
    sellLine,
    buyQuantity,
    sellQuantity,
    totalQuantity
  }
}

watch(
  () => [props.history, props.records],
  () => {
    const klineData = makeKLineChartData(props.history)
    setKLineData(klineData)

    const { buyLine, sellLine, buyQuantity, sellQuantity, totalQuantity} = tradeData(props.records)
    setActionData(buyLine, sellLine)
    setQuantityData(buyQuantity, sellQuantity, totalQuantity)   
  }
)

</script>
<template>
  <KLineChart4 ref="chart" style="height: 300px;"/>
</template>