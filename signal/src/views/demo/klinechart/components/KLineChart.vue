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

@Component({
  name: 'LineChart'
})

export default class extends mixins(ResizeMixin) {
  @Prop({ required: true }) private chartData!: (string|number)[][]
  @Prop({ default: '#00da3c' }) private upColor!: string
  @Prop({ default: '#ec0000' }) private downColor!: string
  @Prop({ default: 60 }) private showDays!: number
  @Prop({  }) private selectStart!: string
  @Prop({  }) private selectEnd!: string
  @Prop({ default: 'chart' }) private className!: string
  @Prop({ default: '100%' }) private width!: string
  @Prop({ default: '350px' }) private height!: string

  @Watch('chartData', { deep: true })
  private onChartDataChange(value: (string|number)[][]) {
    this.setOptions(value)
  }

  // private upColor = '#00da3c';  //绿色部分
  // private downColor = '#ec0000';  //红色部分
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

  private setOptions(chartData: (string|number)[][]) {
    if (this.chart) {
      var data = this.splitData(chartData);
      let zoomStart = 0
      //默认显示60天数据
      if(data.categoryData.length>this.showDays){
        zoomStart = Math.round((data.categoryData.length - this.showDays) * 100/data.categoryData.length)
      }
      let chartOption: any = {
        animationDuration: 2800,
        animationEasing: 'cubicInOut',
        legend: {
          bottom: 10,
          left: 'center',
          data: ['Dow-Jones index', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          borderWidth: 1,
          borderColor: '#ccc',
          padding: 10,
          textStyle: {
            color: '#000'
          },
          position: function (pos: number[], params?:Object|Object[], el?: any, elRect?: Object, size?: any) {
            const obj: any = {
              top: 10
            };
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            // console.log(obj)
            return obj;
          }
          // extraCssText: 'width: 170px'
        },
        axisPointer: {
          link: [
            {
              xAxisIndex: 'all'
            }
          ],
          label: {
            backgroundColor: '#777'
          }
        },
        toolbox: {
          feature: {
            //工具栏-缩放及还原
            dataZoom: {
              yAxisIndex: false
            },
            //工具栏-选择及清除
            brush: {
              type: ['lineX', 'clear']
            }
          }
        },
        brush: {
          xAxisIndex: 'all',
          brushLink: 'all',
          outOfBrush: {
            colorAlpha: 0.1
          }
        },
        //主要是为了在volume的条目中根据是上涨还是下跌显示不同颜色而定义的
        visualMap: {
          show: false,
          seriesIndex: 5,
          dimension: 2,
          pieces: [
            {
              value: 1,
              color: this.downColor
            },
            {
              value: -1,
              color: this.upColor
            }
          ]
        },
        grid: [
          {
            left: '10%',
            right: '8%',
            height: '50%'
          },
          {
            left: '10%',
            right: '8%',
            top: '63%',
            height: '16%'
          }
        ],
        xAxis: [
          {
            type: 'category',
            data: data.categoryData,
            boundaryGap: false,
            axisLine: { onZero: false },
            splitLine: { show: false },
            min: 'dataMin',
            max: 'dataMax',
            axisPointer: {
              z: 100
            }
          },
          {
            type: 'category',
            gridIndex: 1,
            data: data.categoryData,
            boundaryGap: false,
            axisLine: { onZero: false },
            axisTick: { show: false },
            splitLine: { show: false },
            axisLabel: { show: false },
            min: 'dataMin',
            max: 'dataMax'
          }
        ],
        yAxis: [
          {
            scale: true,
            splitArea: {
              show: true
            }
          },
          {
            scale: true,
            gridIndex: 1,
            splitNumber: 2,
            axisLabel: { show: false },
            axisLine: { show: false },
            axisTick: { show: false },
            splitLine: { show: false }
          }
        ],
        dataZoom: [
          {
            type: 'inside',
            xAxisIndex: [0, 1],
            start: zoomStart,
            end: 100
          },
          {
            show: true,
            xAxisIndex: [0, 1],
            type: 'slider',
            top: '85%',
            start: zoomStart,
            end: 100
          }
        ],
        series: [
          {
            name: 'Dow-Jones index',
            type: 'candlestick',
            data: data.values,
            itemStyle: {
              color: this.upColor,
              color0: this.downColor,
              borderColor: undefined,
              borderColor0: undefined
            }
          },
          {
            name: 'MA5',
            type: 'line',
            data: this.calculateMA(5, data),
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: this.calculateMA(10, data),
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'MA20',
            type: 'line',
            data: this.calculateMA(20, data),
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'MA30',
            type: 'line',
            data: this.calculateMA(30, data),
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'Volume',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: data.volumes
          }
        ]
      }
      // console.log(chartOption)
      this.chart.setOption(chartOption);
      //设置默认选中
      if(this.selectStart && this.selectEnd){
        this.chart.dispatchAction({
          type: 'brush',
          areas: [
            {
              brushType: 'lineX',
              coordRange: [this.selectStart, this.selectEnd],
              xAxisIndex: 0
            }
          ]
        });
      }
    }
  }

  private splitData(rawData: (string|number)[][]) {
    let categoryData = [];
    let values = [];
    let volumes = [];
    for (let i = 0; i < rawData.length; i++) {
      // categoryData.push(rawData[i].splice(0, 1)[0]);
      // values.push(rawData[i]);
      // volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1]); //索引、总成交额？涨跌
      //不改变原始数据
      categoryData.push(rawData[i][0]);
      let dataValue : (string|number)[] = this.getDataValue(rawData[i]);
      values.push(dataValue);
      volumes.push([i, dataValue[4], dataValue[0] > dataValue[1] ? 1 : -1]); //索引、总成交额？涨跌
    }

    let result = {
      categoryData: categoryData,
      values: values,
      volumes: volumes
    }
    // console.log(result)
    return result;
  }

  private getDataValue(data : (string|number)[]){
    let returnData: (string|number)[] = []
    for (let i = 1; i < data.length; i++) {
      returnData.push(data[i])
    }
    return returnData
  }

  private calculateMA(dayCount : number, data : any) {
    var result = [];
    for (var i = 0, len = data.values.length; i < len; i++) {
      if (i < dayCount) {
        result.push('-');
        continue;
      }
      var sum = 0;
      for (var j = 0; j < dayCount; j++) {
        // console.log(data.values[i - j])
        // console.log(data.values[i - j][1])
        sum += data.values[i - j][1];
      }
      result.push(+(sum / dayCount).toFixed(3));
    }
    return result;
  }
}
</script>
