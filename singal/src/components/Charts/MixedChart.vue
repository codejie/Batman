<template>
  <div
    :id="id"
    :class="className"
    :style="{height: height, width: width}"
  />
</template>

<script lang="ts">
import * as echarts from 'echarts'
import { Component, Prop, Watch } from 'vue-property-decorator'
import { mixins } from 'vue-class-component'
import ResizeMixin from './mixins/resize'


export interface ChartData {
  xData: string[],
  priceData: number[],
  volumeData: number[]
}

@Component({
  name: 'MixedChart'
})

export default class extends mixins(ResizeMixin) {
  @Prop({ default: 'chart' }) private className!: string
  @Prop({ default: 'chart' }) private id!: string
  @Prop({ default: '200px' }) private width!: string
  @Prop({ default: '200px' }) private height!: string
  @Prop({ default: () => { return {xData: [], priceData: [], volumeData: []} } }) private chartData!: ChartData 

  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  }

  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  }

  @Watch('chartData')
  private onMyDataChange(value: ChartData) {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
    this.initChart()
  }

  private initChart() {
    this.chart = echarts.init(document.getElementById(this.id) as HTMLDivElement)
    this.chart.setOption({
      backgroundColor: '#344b58',
      title: {
        text: '历史数据',
        top: '20',
        textStyle: {
          color: '#fff',
          fontSize: 22
        },
        subtextStyle: {
          color: '#90979c',
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis'
      },
      grid: {
        left: '5%',
        right: '5%',
        borderWidth: 0,
        top: 150,
        bottom: 95,
        textStyle: {
          color: '#fff'
        }
      },
      legend: {
        x: '5%',
        top: '10%',
        textStyle: {
          color: '#90979c'
        },
        data: ['Price', 'Volume']
      },
      xAxis: [{
        type: 'category',
        axisLine: {
          lineStyle: {
            color: '#90979c'
          }
        },
        splitLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        splitArea: {
          show: false
        },
        axisLabel: {
          interval: 0

        },
        data: this.chartData.xData
      }],
      yAxis: [{
        type: 'value',
        splitLine: {
          show: false
        },
        axisLine: {
          lineStyle: {
            color: '#90979c'
          }
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          interval: 0
        },
        splitArea: {
          show: false
        }
      }],
      dataZoom: [{
        show: true,
        xAxisIndex: [
          0
        ],
        bottom: 30,
        start: 10,
        end: 80,
        handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
        handleSize: '110%',
        handleStyle: {
          color: '#d3dee5'

        },
        textStyle: {
          color: '#fff'
        },
        borderColor: '#90979c'
      }, {
        type: 'inside',
        show: true,
        start: 1,
        end: 35
      }],
      series: [{
        name: 'Volume',
        type: 'bar',
        stack: 'total',
        barMaxWidth: 35,
        barGap: '10%',
        itemStyle: {
          color: 'rgba(255,144,128,1)',
          label: {
            show: true,
            textStyle: {
              color: '#fff'
            },
            position: 'insideTop',
            formatter(p: any) {
              return p.value > 0 ? p.value : ''
            }
          }
        },
        data: this.chartData.volumeData
      },
      {
        name: 'Price',
        type: 'line',
        stack: 'total',
        symbolSize: 10,
        symbol: 'circle',
        itemStyle: {
          color: 'rgba(252,230,48,1)',
          barBorderRadius: 0,
          label: {
            show: true,
            position: 'top',
            formatter(p: any) {
              return p.value > 0 ? p.value : ''
            }
          }
        },
        data: this.chartData.priceData 
      }
      ]
    })
  }
}
</script>
