<script setup lang="ts">
import { ref } from 'vue'
// 1. 导入所有图表组件
import { FlexChart, FlexChartDialog, SplitChart, SplitChartDialog, TripleChart, TripleChartDialog, type SeriesDataItem } from '@/components/Chart'

// --- FlexChart & FlexChartDialog Demo Data ---
const chartTitle = ref('FlexChart 综合示例')
const isLegendVisible = ref(true)
const isDialogVisible = ref(false)
const categories = ref(['2024-01', '2024-02', '2024-03', '2024-04'])
const mixedSeries = ref<SeriesDataItem[]>([
  { name: '蒸发量', type: 'bar', data: [2.0, 4.9, 7.0, 23.2] },
  { name: '平均温度', type: 'line', data: [2.0, 2.2, 3.3, 4.5] },
  { name: '指数K线', type: 'candlestick', data: [[20, 34, 10, 38], [40, 35, 30, 50], [31, 38, 33, 44], [38, 15, 5, 42]] }
])

// --- SplitChart & SplitChartDialog Demo Data ---
const isSplitDialogVisible = ref(false)
const gridRatio = ref(2) // 新增：为grid-ratio提供响应式数据
const splitChartCategories = ref(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
const topChartData = ref<SeriesDataItem[]>([
    { name: '日K', type: 'candlestick', data: [[20, 30, 18, 33], [30, 38, 28, 40], [38, 32, 30, 39], [32, 35, 31, 38], [35, 45, 33, 48], [45, 42, 40, 49], [42, 55, 41, 58]] },
    { name: 'MA5', type: 'line', data: [25, 33, 35, 36, 41, 45, 48] }
])
const bottomChartData = ref<SeriesDataItem[]>([
    { name: '成交量', type: 'bar', data: [100, 230, 180, 280, 200, 350, 480] }
])

// --- TripleChart & TripleChartDialog Demo Data ---
const isTripleDialogVisible = ref(false)
const tripleChartCategories = ref(['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06'])
const topKLineData = ref<SeriesDataItem[]>([
    { name: 'K线', type: 'candlestick', data: [[100, 120, 95, 122], [120, 130, 118, 135], [130, 125, 122, 138], [125, 140, 123, 142], [140, 142, 138, 145], [142, 135, 133, 148]] }
])
const middleVolumeData = ref<SeriesDataItem[]>([
    { name: '成交量', type: 'bar', data: [500, 600, 750, 800, 700, 900] }
])
const bottomBarData = ref<SeriesDataItem[]>([
    { name: 'MACD', type: 'bar', data: [20, -10, 30, 15, 40, -5] }
])

</script>

<template>
  <div style="padding: 20px; background-color: #fff;">
    <h1>FlexChart 组件演示页面</h1>
    <p>这是一个在同一个坐标系中混合显示柱状图、折线图和K线图的示例。</p>
    
    <div style="margin-bottom: 20px;">
      <button @click="isLegendVisible = !isLegendVisible" style="padding: 5px 10px; margin-right: 10px;">
        切换页内图例 (当前: {{ isLegendVisible ? '显示' : '隐藏' }})
      </button>
      <button @click="isDialogVisible = true" style="padding: 5px 10px;">
        打开图表对话框
      </button>
    </div>

    <FlexChart
      :title="chartTitle"
      height="600px"
      :x-axis-data="categories"
      :series-data="mixedSeries"
      x-axis-name="月份"
      y-axis-name="数值 / 指数"
      :show-legend="isLegendVisible"
    />

    <FlexChartDialog
      v-model="isDialogVisible"
      title="对话框中的图表"
      :x-axis-data="categories"
      :series-data="mixedSeries"
      x-axis-name="月份"
      y-axis-name="数值 / 指数"
    />

    <hr style="margin: 40px 0;">

    <h2>SplitChart 组件演示</h2>
    <p>这是一个包含上下两个图表区域，并共享X轴的示例。</p>
    <div style="margin-bottom: 20px; display: flex; align-items: center; gap: 20px;">
        <button @click="isSplitDialogVisible = true" style="padding: 5px 10px;">
            在对话框中显示
        </button>
        <div style="display: flex; align-items: center; gap: 10px;">
            <label for="ratio-slider">调整上下占比 ({{ gridRatio.toFixed(1) }}:1):</label>
            <input id="ratio-slider" type="range" v-model.number="gridRatio" min="0.5" max="5" step="0.1" style="width: 200px;" />
        </div>
    </div>
    <SplitChart
        title="K线与成交量"
        height="600px"
        :x-axis-data="splitChartCategories"
        :top-series-data="topChartData"
        :bottom-series-data="bottomChartData"
        x-axis-name="日期"
        top-y-axis-name="价格"
        bottom-y-axis-name="成交量"
        :grid-ratio="gridRatio"
    />

    <SplitChartDialog
        v-model="isSplitDialogVisible"
        title="对话框中的分屏图表"
        :x-axis-data="splitChartCategories"
        :top-series-data="topChartData"
        :bottom-series-data="bottomChartData"
        x-axis-name="日期"
        top-y-axis-name="价格"
        bottom-y-axis-name="成交量"
    />

    <hr style="margin: 40px 0;">

    <h2>TripleChart 组件演示</h2>
    <p>这是一个包含上、中、下三个图表区域，并共享X轴的示例。</p>
    <div style="margin-bottom: 20px;">
        <button @click="isTripleDialogVisible = true" style="padding: 5px 10px;">
            打开三层图表对话框
        </button>
    </div>

    <TripleChartDialog
        v-model="isTripleDialogVisible"
        title="K线、成交量与MACD指标"
        :x-axis-data="tripleChartCategories"
        :top-series-data="topKLineData"
        :middle-series-data="middleVolumeData"
        :bottom-series-data="bottomBarData"
        x-axis-name="月份"
        top-y-axis-name="价格"
        middle-y-axis-name="成交量"
        bottom-y-axis-name="MACD"
    />
  </div>
</template>
