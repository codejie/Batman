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
  height?: number
  props: ILineChartDataProp[]
}

export interface ILineChartDataProp {
  name: string
  type?: string
  label?: string
  color?: string
  yAxisIndex?: number
  lineType?: string
}

@Component({
  name: 'LineChart'
})
export default class extends mixins(ResizeMixin) {
  @Prop({ required: true }) private chartData!: Object
  @Prop({ required: true }) private chartProp!: ILineChartProp | ILineChartProp[]
  @Prop({ default: 'chart' }) private className!: string
  @Prop({ default: '100%' }) private width!: string
  @Prop({ default: '350px' }) private height!: string

  @Watch('chartData', { deep: true })
  private onChartDataChange(value: any) {
    // this.setOptions(value)
    this.initChart(value)
  }

  mounted() {
    // this.$nextTick(() => {
    //   this.initChart()
    // })
  }

  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  }

  private initChart(chartData: any) {
    this.chart = echarts.init(this.$el as HTMLDivElement, 'macarons')
    this.setOptions(chartData)
  }

  
  private setOptions(chartData: any) {
    // let chartProp = (this.chartProp  instanceof Array) ? this.chartProp[0] : this.chartProp
    // let chartProp = this.chartProp.length?this.chartProp[0]:this.chartProp
    const gridGap = 25, legendGap = 30, legendTop = 0, zoomHeight = 65
    if (this.chart) {
      let chartPropArray : ILineChartProp[] = (this.chartProp instanceof Array)?this.chartProp:[this.chartProp]
      // let chartProp = chartPropArray[0]
      
      let grid : Object[] = [], xAxis : Object[] = [], xAxisIndex : Number[] = [], yAxis : Object[] = []
      let series : Object[] = [] , legend : Object[] = []
      let totalYAxisIndex = 0;

      // let chartHeight = 100 / chartPropArray.length - 10
      let propHeight = 0, propHeightCount = 0
      chartPropArray.forEach((chartProp : ILineChartProp, idx)=>{
        if(chartProp.height){
          propHeight = propHeight + chartProp.height;
          propHeightCount++;
        }
      })
      
      let chartHeight = 0
      if(chartPropArray.length>propHeightCount){
        let totalChartHeight = (parseInt)(this.height.replaceAll('px', ''))
        totalChartHeight = totalChartHeight - legendTop - legendGap * (chartPropArray.length - 1) 
            - gridGap * chartPropArray.length - zoomHeight
        chartHeight = Math.floor((totalChartHeight - propHeight) / (chartPropArray.length - propHeightCount))
      }
      
      let curTop = 0
      chartPropArray.forEach((chartProp : ILineChartProp, idx)=>{
        let legendData : String[] = []
        let curLegendTop = curTop==0?legendTop:(curTop + legendGap)
        let curChartHeight = chartProp.height?chartProp.height:chartHeight
        grid.push({
          // top: (idx * chartHeight + 5) + '%', 
          top: curLegendTop + gridGap,
          height: curChartHeight
        })
        xAxis.push({
          gridIndex: idx,
          data: chartData[chartProp.keyProp],
          boundaryGap: false,
          axisTick: {
            show: false
          }
        })
        xAxisIndex.push(idx)
        //计算y坐标轴
        let yAxisMap = new Map([
          ["0", 0]
        ]); 

        let yAxisIndex = 0
        chartProp.props.forEach((prop: ILineChartDataProp)=>{
          let yIndex = (prop.yAxisIndex?prop.yAxisIndex:0) + ''
          if(yAxisMap.get(yIndex)==null){
            console.log('create')
            yAxisMap.set(yIndex, ++yAxisIndex)
          }
        })

        let preYAxisCount = yAxis.length
        for(var index=0; index<=yAxisIndex; index++){
          if(index==0){
            yAxis.push({ gridIndex: idx })
          } else if(index==1){
            yAxis.push({ gridIndex: idx, position : 'right' })
          } else {
            yAxis.push({ gridIndex: idx, position : 'right', offset : (index-1) * 40 })
          }
        }

        chartProp.props.forEach((prop: ILineChartDataProp, index)=>{
          let label = prop.label?prop.label:prop.name
          // legend.push(label)
          legendData.push(label)

          let yAxisIndex = (prop.yAxisIndex?prop.yAxisIndex:0) + ''
          series.push({
            name: label,
            xAxisIndex: idx,
            yAxisIndex: preYAxisCount + yAxisMap.get(yAxisIndex)!,
            symbolSize: chartProp.lineWidth?chartProp.lineWidth*1.4:null,
            color: prop.color,
            itemStyle: {
              // color: '#FF005A',
              normal: {
                lineStyle: {
                  type: prop.lineType,
                  // color: prop.color,
                  width: chartProp.lineWidth
                }
              }
            },
            smooth: false,
            type: prop.type?prop.type:'line',
            data: chartData[prop.name],
            animationDuration: 2800,
            animationEasing: 'cubicInOut'
          })
        })
        legend.push({
          "top": curLegendTop,
          "data": legendData
        })
        curTop = curLegendTop + gridGap + curChartHeight
      })

      let chartOption = {
        // xAxis: {
        //   // data: [chartData.data[0]['month'], 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        //   data: chartData[chartProp.keyProp],
        //   boundaryGap: false,
        //   axisTick: {
        //     show: false
        //   }
        // },
        xAxis: xAxis,
        // legend: {
        //   data: legend,
        // },
        legend: legend,
        // grid: [{
        //   left: 10,
        //   // right: (yAxisIndex-1) * 40,
        //   bottom: 20,
        //   top: 30,
        //   containLabel: true
        // }],
        grid: grid,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: 8
        },
        // yAxis: [{
        //   axisTick: {
        //     show: false
        //   }
        // }],
        yAxis: yAxis,
        dataZoom: [{
          show: true,
          xAxisIndex: xAxisIndex,
          // bottom: 30,
          bottom: 10,
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
          xAxisIndex: xAxisIndex,   //表示在所有区域中滚动鼠标都可以实现放大/缩小效果
          start: 1,
          end: 35
        }],
        series: series
      }
      console.log(chartOption)
      this.chart.setOption(chartOption)
      
    }
  }
}
</script>
