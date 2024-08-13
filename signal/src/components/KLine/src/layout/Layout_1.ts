/*
* two grid, top for kline, bottom for others
*/
export const Layout_1 = {
  grid: [
      { left: '0%', top: '0%', width: '98%', height: '60%' },
      { left: '0%', buttom: '0%', width: '98%', height: '40%' }
    ],
    xAxis: [
      {
        type: 'category',
        gridIndex: 0,
        data: []
      },
      {
        type: 'category',
        gridIndex: 1,
        data: []
      }      
    ],
    yAxis: [
      {
        type: 'value',
        gridIndex: 0,
        show: true,
        position: 'left',
        nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        }
      },
      {
        type: 'value',
        // name: 'Volume',
        nameLocation : 'middle',
        show: true,
        gridIndex: 1,
        position: 'left',
        nameGap: 30,
        // inverse: true
        scale: true,
        splitArea: {
          show: true
        },
        splitNumber: 8,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }        
      }
    ],
    axisPointer: {
      label: {
        backgroundColor: '#777'
      }
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
      }
    },      
    series: []
}

// visualMap:
// function makeVisualMap() {
//   return  {
//     show: false,
//     seriesIndex: 1,
//     dimension: 2,
//     pieces: [
//       {
//         value: 1,
//         color: downColor
//       },
//       {
//         value: -1,
//         color: upColor
//       }
//     ]
//   }
// }