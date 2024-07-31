import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'
import { Layout, getParentLayout } from '@/utils/routerHelper'
import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Root',
    meta: {
      hidden: true
    }
  },
  {
    path: '/redirect',
    component: Layout,
    name: 'Redirect',
    children: [
      {
        path: '/redirect/:path(.*)',
        name: 'Redirect',
        component: () => import('@/views/Redirect/Redirect.vue'),
        meta: {}
      }
    ],
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/login',
    component: () => import('@/views/Login/Login.vue'),
    name: 'Login',
    meta: {
      hidden: true,
      title: t('router.login'),
      noTagsView: true
    }
  },
  {
    path: '/404',
    component: () => import('@/views/Error/404.vue'),
    name: 'NoFind',
    meta: {
      hidden: true,
      title: '404',
      noTagsView: true
    }
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Layout,
    meta: {
      title: t('router.dashboard'),
      icon: 'carbon:dashboard'
    }
  },
  {
    path: '/customized',
    component: Layout,
    name: 'customized',
    meta:{},
    children: [
      {
        path: 'index',
        component: () => import('@/views/Customized/index.vue'),
        name: 'Customized',
        meta: {
          title: '自选',
          icon: 'carbon:chart-custom'
        }
      },
      {
        path: 'summary',
        name: 'Summary',
        component: () => import('@/views/Customized/Summary.vue'),
        props: route => ({ code: route.query.code }),
        meta: {
          title: 'Summary',
          noTagsView: true,
          noCache: true,
          hidden: true,
          // showMainRoute: true,
          activeMenu: '/customized/index'
        }
      }        
    ]
  },
  {
    name: 'data',
    path: '/data',
    component: Layout,
    meta: {
      title: '数据',
      icon: 'carbon:table-alias'      
    },
    children: [
      {
        path: 'third',
        name: 'third',
        component: getParentLayout(),
        meta: {
          title: '技术数据'
        },
        children: [
          {
            path: 'new-high',
            name: 'new-high',
            component: () => import('@/views/Third/Stock/NewHigh.vue'),
            meta: {
              title: '创新高'
            }
          }
        ]
      }
    ]
  },
  {
    path: '/strategy',
    component: Layout,
    name: 'Strategy',
    meta: {
      title: t('router.strategy.main'),
      icon: 'carbon:network-4-reference'
    },
    children: [
      {
        path: 'filter',
        name: 'Filter',
        component: () => import('@/views/Strategy/Filter/index.vue'),
        meta: {
          title: t('router.strategy.filter'),
          icon: 'carbon:chart-logistic-regression'
        },
        children: [
          {
            path: 'create',
            name: 'Create',
            component: () => import('@/views/Strategy/Filter/Create.vue'),
            meta: {
              title: t('router.strategy.filter_create'),
              noTagsView: true,
              noCache: true,
              hidden: true,
              showMainRoute: true,
              activeMenu: '/strategy/filter'
            }
          }
        ]
      },
      {
        path: 'trader',
        name: '',
        component: () => '/strategy/trader',
        meta: {
          title: t('router.strategy.trader'),
          icon: 'carbon:pricing-traditional'
        }
      }
    ]
  },
  {
    path: '/test',
    component: Layout,
    name: 'Test',
    meta:{},
    children: [
      {
        path: 'index',
        component: () => import('@/views/Test/Test.vue'),
        name: 'TestDemo',
        meta: {
          title: 'Test',
          icon: 'carbon:test-tool'
        }        
      }
    ]
  },
  {
    path: '/level',
    component: Layout,
    redirect: '/level/menu1/menu1-1/menu1-1-1',
    name: 'Level',
    meta: {
      title: t('router.level'),
      icon: 'carbon:skill-level-advanced'
    },
    children: [
      {
        path: 'menu1',
        name: 'Menu1',
        component: getParentLayout(),
        redirect: '/level/menu1/menu1-1/menu1-1-1',
        meta: {
          title: t('router.menu1')
        },
        children: [
          {
            path: 'menu1-1',
            name: 'Menu11',
            component: getParentLayout(),
            redirect: '/level/menu1/menu1-1/menu1-1-1',
            meta: {
              title: t('router.menu11'),
              alwaysShow: true
            },
            children: [
              {
                path: 'menu1-1-1',
                name: 'Menu111',
                component: () => import('@/views/Level/Menu111.vue'),
                meta: {
                  title: t('router.menu111')
                }
              }
            ]
          },
          {
            path: 'menu1-2',
            name: 'Menu12',
            component: () => import('@/views/Level/Menu12.vue'),
            meta: {
              title: t('router.menu12')
            }
          }
        ]
      },
      {
        path: 'menu2',
        name: 'Menu2',
        component: () => import('@/views/Level/Menu2.vue'),
        meta: {
          title: t('router.menu2')
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const resetRouter = (): void => {
  const resetWhiteNameList = ['Redirect', 'Login', 'NoFind', 'Root']
  router.getRoutes().forEach((route) => {
    const { name } = route
    if (name && !resetWhiteNameList.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
