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
        relos: ['admin', 'signal'],
        alwaysShow: true
      },
      children: [
        {
            path: 'stock',
            component: () => import(/* webpackChunkName: "DataStock" */ '@/views/data/stock/index.vue'),
            name: 'DataStock',
            meta: {
                title: 'DataStock',
                roles: ['admin', 'signal'],
                affix: true
            }
        },
        {
            path: 'index',
            component: () => import(/* webpackChunkName: "DataIndex" */ '@/views/data/index/index.vue'),
            name: 'DataSIndex',
            meta: {
                title: 'DataIndex',
                roles: ['admin', 'signal']
            }
        }
      ]
    }
  ]

  export default signalRouters