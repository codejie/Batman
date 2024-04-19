<template>
  <div
    :class="className"
    :style="{height: height, width: width}"
  />
</template>

<script lang="ts">
import * as echarts from 'echarts'
import { Component, Prop, Watch } from 'vue-property-decorator'
import { mixins } from 'vue-class-component'
import ResizeMixin from '@/components/Charts/mixins/resize'

// export interface ILineChartData {
//   expectedData: number[]
//   actualData: number[]
//   data: Object[]
// }

export interface ILineChartProp {
  keyProp: string
  lineWidth: number
  props: ILineChartDataProp[]
}

export interface ILineChartDataProp {
  name: string
  label: string
  lineColor?: string
  lineType?: string
}

@Component({
  name: 'LineChart'
})
export default class extends mixins(ResizeMixin) {
  @Prop({ required: true }) private chartData!: Object[]
  @Prop({ required: true }) private chartProp!: ILineChartProp
  @Prop({ default: 'chart' }) private className!: string
  @Prop({ default: '100%' }) private width!: string
  @Prop({ default: '350px' }) private height!: string

  @Watch('chartData', { deep: true })
  private onChartDataChange(value: Object[]) {
    this.setOptions(value)
  }

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

  private initChart() {
    this.chart = echarts.init(this.$el as HTMLDivElement, 'macarons')
    this.setOptions(this.chartData)
  }

  private setOptions(chartData: Object[]) {
    console.log('==============================')
    let chartProp = this.chartProp
    if (this.chart) {
      var xAxis : String[] = [], series : Object[], seriesData: Number[][] = []
      chartProp.props.forEach((prop: ILineChartDataProp)=>{
        console.log(prop)
        var data : Number[] = []
        seriesData.push(data)
      })
      chartData.forEach((data : any) =>{
        console.log(data)
        xAxis.push(data[chartProp.keyProp])
        
        chartProp.props.forEach((prop  ,index )=>{
          seriesData[index].push(data[prop.name])
        })
      })

      var series : Object[] = []
      chartProp.props.forEach((prop: ILineChartDataProp, index)=>{
        series.push({
          name: prop.label,
          itemStyle: {
            // color: '#FF005A',
            normal: {
              lineStyle: {
                type: prop.lineType,
                color: prop.lineColor,
                width: chartProp.lineWidth
              }
            }
          },
          smooth: false,
          type: 'line',
          data: seriesData[index],
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        })
      })
      
      this.chart.setOption({
        xAxis: {
          // data: [chartData.data[0]['month'], 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          data: xAxis,
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: 8
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          data: ['expected', 'actual']
        },
        series: series
      })
      
    }
  }
}
</script>
