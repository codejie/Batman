/*
* only one grid
*/
export const Layout_0 = {
  grid: [
    { left: '0%', top: '0%', width: '98%', height: '98%' }
    ],
    xAxis: [
      {
        type: 'category',
        gridIndex: 0,
        data: []
      }      
    ],
    yAxis: [{
      type: 'value',
      gridIndex: 0,
      show: true,
      position: 'left',
      nameGap: 30,
      scale: true,
      splitArea: {
        show: true
      }
    }],
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