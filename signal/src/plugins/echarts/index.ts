import * as echarts from 'echarts/core'

import {
  BarChart,
  LineChart,
  PieChart,
  MapChart,
  PictorialBarChart,
  RadarChart,
  CandlestickChart
} from 'echarts/charts'

import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  AriaComponent,
  ParallelComponent,
  LegendComponent,
  VisualMapComponent
} from 'echarts/components'

import { CanvasRenderer } from 'echarts/renderers'
import {
  DataZoomComponent,
  MarkPointComponent,
  VisualMapComponent
} from 'echarts/components'

echarts.use([
  LegendComponent,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  AriaComponent,
  ParallelComponent,
  BarChart,
  LineChart,
  PieChart,
  MapChart,
  CanvasRenderer,
  PictorialBarChart,
  RadarChart,
  CandlestickChart,
  VisualMapComponent,
  DataZoomComponent,
  MarkPointComponent
])

export default echarts
