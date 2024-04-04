import { RouteConfig } from "vue-router"
import Layout from '@/layout/index.vue'

/**
 * Signal Router
 */

const signalRouters: RouteConfig[] = [
    {
      path: '/data',
      component: Layout,
      redirect: '/data',
    //   name: 'Data',
      meta: {
        title: 'Data',
        icon: 'component',
        roles: ['admin', 'signal'],
        alwaysShow: true
      },
      children: [
        {
            path: '/stock',
            component: () => import(/* webpackChunkName: "DataStock" */ '@/views/data/stock/index.vue'),
            name: 'DataStock',
            meta: {
                title: 'DataStock',
                roles: ['admin', 'signal'],
                // affix: true
            }
        },
        {
            path: '/index',
            component: () => import(/* webpackChunkName: "DataIndex" */ '@/views/data/index/index.vue'),
            name: 'DataSIndex',
            meta: {
                title: 'DataIndex',
                roles: ['admin', 'signal']
            }
        },
        {
          path: '/stocklinechart',
          component: () => import(/* webpackChunkName: "DataStock" */ '@/views/data/stock/stocklinechart.vue'),
          name: 'DataStockLineChart',
          meta: {
              title: 'DataStockLineChart',
              roles: ['admin', 'signal'],
              // affix: true
          }
        },
        {
          path: '/multistocklinechart',
          component: () => import(/* webpackChunkName: "DataStock" */ '@/views/data/stock/multistocklinechart.vue'),
          name: 'MultiStockLineChart',
          meta: {
              title: 'MultiStockLineChart',
              roles: ['admin', 'signal'],
              // affix: true
          }
        },
      ]
    },
    {
      path: '/filter',
      component: Layout,
      redirect: '/filter',
      meta: {
        title: 'Filtering',
        icon: 'tree',
        roles: ['admin', 'signal'],
        alwaysShow: true
      },
      children: [
        {
          path: '/search',
          component: () => import(/* webpackChunkName: "FilterSearch" */ '@/views/filter/search/index.vue'),
          name: 'FilterSearch',
          meta: {
              title: 'FilterSearch',
              roles: ['admin', 'signal'],
              // affix: true
          }
        },
        {
            path: '/results',
            component: () => import(/* webpackChunkName: "FilterResults" */ '@/views/filter/results/index.vue'),
            name: 'FilterResults',
            meta: {
                title: 'FilterResults',
                roles: ['admin', 'signal']
            }
        },
        {
            path: '/strategyresults',
            component: () => import(/* webpackChunkName: "FilterResults" */ '@/views/filter/strategyresults/index.vue'),
            name: 'StrategyResults',
            meta: {
                title: 'StrategyResults',
                roles: ['admin', 'signal']
            }
        }        
      ]
    },
    {
      path: '/strategy',
      component: Layout,
      redirect: '/strategy',
      meta: {
        title: 'Strategy',
        icon: 'skill',
        roles: ['admin', 'signal'],
        alwaysShow: true
      },
      children: [
        {
          path: '/design',
          component: () => import(/* webpackChunkName: "StrategyDesign" */ '@/views/strategy/design/index.vue'),
          name: 'StrategyDesign',
          meta: {
              title: 'StrategyDesign',
              roles: ['admin', 'signal'],
          }
        },
        {
            path: '/collection',
            component: () => import(/* webpackChunkName: "StrategyCollection" */ '@/views/strategy/collection/index.vue'),
            name: 'StrategyCollection',
            meta: {
                title: 'StrategyCollection',
                roles: ['admin', 'signal']
            }
        }        
      ]
    },
    {
      path: 'Watching',
      component: Layout,
      redirect: '/watching',
      meta: {
        title: 'Watching',
        icon: 'example',
        roles: ['admin', 'signal'],
        alwaysShow: true
      }
    },
    {
      path: 'Holdings',
      component: Layout,
      redirect: '/holdings',
      meta: {
        title: 'Holdings',
        icon: 'star',
        roles: ['admin', 'signal'],
        alwaysShow: true
      }
    },
    {
      path: '/demo',
      component: Layout,
      redirect: '/demo',
      meta: {
        title: 'Demo',
        icon: 'skill',
        roles: ['admin', 'signal'],
        alwaysShow: true
      },
      children: [
        {
          path: '/linechart',
          component: () => import(/* webpackChunkName: "StrategyDesign" */ '@/views/demo/linechart/index.vue'),
          name: 'LineChartDemo',
          meta: {
              title: 'LineChartDemo',
              roles: ['admin', 'signal'],
          }
        },
        {
          path: '/klinechart',
          component: () => import(/* webpackChunkName: "StrategyDesign" */ '@/views/demo/klinechart/index.vue'),
          name: 'KLineChartDemo',
          meta: {
              title: 'KLineChartDemo',
              roles: ['admin', 'signal'],
          }
        }       
      ]
    }
  ]

  export default signalRouters