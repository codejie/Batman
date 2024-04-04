<template>
  <div class="dashboard-editor-container">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" :chart-prop="chartProp" :height="'250px'" />
    </el-row>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData2" :chart-prop="chartProp2" :width="'80%'" />
    </el-row>
  </div>
</template>

<script lang="ts">
import 'echarts/theme/macarons.js' // Theme used in BarChart, LineChart, PieChart and RadarChart
import { Component, Vue } from 'vue-property-decorator'
import LineChart, { ILineChartProp } from './components/LineChart.vue'

@Component({
  name: 'LineChartDemo',
  components: {
    LineChart
  }
})

export default class extends Vue {
  private lineChartData: Object[] = [
    {
      month: '2021-01',
      dose: 183,
      hLine: 209,
      mLine: 355,
      lLine: 272
    },
    {
      month: '2021-02',
      dose: 205,
      hLine: 211,
      mLine: 336,
      lLine: 290
    },
    {
      month: '2021-03',
      dose: 205,
      hLine: 211,
      mLine: 336,
      lLine: 290
    },
    {
      month: '2021-04',
      dose: 205,
      hLine: 211,
      mLine: 336,
      lLine: 290
    },
    {
      month: '2021-05',
      dose: 205,
      hLine: 211,
      mLine: 336,
      lLine: 290
    },
    {
      month: '2021-06',
      dose: 205,
      hLine: 211,
      mLine: 336,
      lLine: 290
    }
  ]

  private chartProp: ILineChartProp = {
    keyProp: 'month',
    lineWidth: 0.3,
    props: [
        {
            name: 'dose',
            label: 'dose'
        },
        {
            name: 'hLine',
            label: 'H_line'
        },
        {
            name: 'mLine',
            label: 'M_line'
        },
        {
            name: 'lLine',
            label: 'L_line'
        }
    ],
  }

  private lineChartData2: Object[] = [
    {
      week: '周一',
      maxTemperature: 25,
      minTemperature: 13,
      avgTemperature: 21
    },
    {
      week: '周二',
      maxTemperature: 26,
      minTemperature: 12,
      avgTemperature: 21
    },
    {
      week: '周三',
      maxTemperature: 27,
      minTemperature: 15,
      avgTemperature: 21
    },
    {
      week: '周四',
      maxTemperature: 22,
      minTemperature: 10,
      avgTemperature: 21
    },
    {
      week: '周五',
      maxTemperature: 20,
      minTemperature: 11,
      avgTemperature: 21
    },
    {
      week: '周六',
      maxTemperature: 28,
      minTemperature: 16,
      avgTemperature: 21
    },
    {
      week: '周日',
      maxTemperature: 27,
      minTemperature: 12,
      avgTemperature: 21
    }
  ]

  private chartProp2: ILineChartProp = {
    keyProp: 'week',
    lineWidth: 2,
    props: [
        {
            name: 'maxTemperature',
            label: '最高温度',
            lineColor: '#FF0000',
            lineType: 'dashed'
        },
        {
            name: 'minTemperature',
            label: '最低温度',
            lineColor: '#00FF00',
            lineType: 'dotted'
        },
        {
            name: 'avgTemperature',
            label: '平均温度',
            lineColor: '#0000FF',
            lineType: 'solid'
        }
    ],
    // color: [
        
    // ]
  }

  // private handleSetLineChartData(type: string) {
  //   this.lineChartData = {
  //     expectedData: [450, 120, 161, 134, 105, 160, 165],
  //     actualData: [120, 82, 91, 154, 162, 140, 145]
  //   }
  // }
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
