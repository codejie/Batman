import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'
import { Layout, getParentLayout } from '@/utils/routerHelper'
import { useI18n } from '@/hooks/web/useI18n'
import { NO_RESET_WHITE_LIST } from '@/constants'

const { t } = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/holding/list',
    name: 'Root',
    meta: {
      hidden: true
    }
  },
  // {
  //   path: '/redirect',
  //   component: Layout,
  //   name: 'RedirectWrap',
  //   children: [
  //     {
  //       path: '/redirect/:path(.*)',
  //       name: 'Redirect',
  //       component: () => import('@/views/Redirect/Redirect.vue'),
  //       meta: {}
  //     }
  //   ],
  //   meta: {
  //     hidden: true,
  //     noTagsView: true
  //   }
  // },
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
    path: '/personal',
    component: Layout,
    redirect: '/personal/personal-center',
    name: 'Personal',
    meta: {
      title: t('router.personal'),
      hidden: true,
      canTo: true
    },
    children: [
      {
        path: 'personal-center',
        component: () => import('@/views/Personal/PersonalCenter/PersonalCenter.vue'),
        name: 'PersonalCenter',
        meta: {
          title: t('router.personalCenter'),
          hidden: true,
          canTo: true
        }
      }
    ]
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
  // {
  //   name: 'Home',
  //   path: '/',
  //   component: Layout,
  //   redirect: '/home',
  //   meta: {
  //     hidden: true
  //   },
  //   children: [
  //     {
  //       name: 'Home-Index',
  //       path: '/home',
  //       component: () => import('@/views/Home/Home.vue'),
  //       meta: {
  //         title: t('router.home'),
  //         noCache: true,
  //         affix: true
  //       }
  //     }
  //   ]
  // },
  {
    name: 'Customized',
    path: '/customized',
    component: Layout,
    meta: {},
    children: [
      {
        name: 'CustomizedList',
        path: 'list',
        component: () => import('@/views/Customized/List.vue'),
        meta: {
          title: t('router.customized_list'),
          icon: 'vi-carbon:chart-custom'
          // noCache: true,
          // affix: false
        }
      }
    ]
  },
  {
    name: 'Holding',
    path: '/holding',
    component: Layout,
    redirect: '/holding/list',
    meta: {
      // title: t('router.holding'),
      // icon: 'carbon:currency-yen',
      // alwaysShow: true,
      // canTo: true
    },
    children: [
      {
        name: 'List',
        path: 'list',
        component: () => import('@/views/Holding/List.vue'),
        meta: {
          title: t('router.holding_list'),
          icon: 'vi-carbon:currency-yen',
          noCache: true,
          affix: true
        }
      },
      {
        name: 'Detail',
        path: 'detail',
        component: () => import('@/views/Holding/Detail.vue'),
        props: (router) => ({ id: router.query.id, ids: router.query.ids }),
        meta: {
          title: t('router.holding_detail'),
          // noCache: true,
          // affix: false,
          // hidden: true,
          // canTo: true
          noTagsView: true,
          noCache: true,
          hidden: true,
          canTo: true,
          activeMenu: '/holding/list'          
        }
      }
    ]
  },
  {
    name: 'analysis',
    path: '/analysis',
    component: Layout,
    meta: {
      title: '数据分析',
      icon: 'vi-carbon:chart-multitype',
      alwaysShow: true
    },
    children: [
      // {
      //   name: 'page',
      //   path: 'page',
      //   component: () => import('@/views/Analysis/Analysis.vue'),
      //   meta: {
      //     title: '分析测试'
      //   }
      // },
      {
        name: 'Trend',
        path: 'trend',
        component: () => import('@/views/Analysis/Trend.vue'),
        meta: {
          title: '趋势计算'
        }
      },
      {
        name: 'TrendArgument',
        path: 'trend-argument',
        component: () => import('@/views/Analysis/TrendArgument.vue'),
        meta: {
          title: '计算参数设置',
          noTagsView: true,
          noCache: true,
          hidden: true,
          canTo: true,
          activeMenu: '/trend/trend'
        }
      },
      {
        name: 'TrendReportChart',
        path: 'trend-report-chart/:id',
        component: () => import('@/views/Analysis/TrendReportChart.vue'),
        meta: {
          title: '聚合图表',
          noCache: true,
          hidden: true,
          canTo: true
        }
      }
    ]
  },
  {
    name: 'data',
    path: '/data',
    component: Layout,
    meta: {
      title: '三方数据',
      icon: 'vi-carbon:table-alias'
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
          },
          {
            path: 'uptrend',
            name: 'uptrend',
            component: () => import('@/views/Third/Stock/Uptrend.vue'),
            meta: {
              title: '连续上涨'
            }
          },
          {
            path: 'high_volume',
            name: 'high_volume',
            component: () => import('@/views/Third/Stock/HighVolume.vue'),
            meta: {
              title: '持续放量'
            }
          },
          {
            path: 'rise_volume_price',
            name: 'rise_volume_price',
            component: () => import('@/views/Third/Stock/RiseVolumePrice.vue'),
            meta: {
              title: '量价齐升'
            }
          },
          {
            path: 'limit_up_pool',
            name: 'limit_up_pool',
            component: () => import('@/views/Third/Stock/LimitUpPool.vue'),
            meta: {
              title: '涨停股池'
            }
          }
        ]
      },
      {
        path: 'links',
        name: 'links',
        component: () => import('@/views/Third/Info/Links.vue'),
        meta: {
          title: '资讯链接'
        }
      },
      {
        path: 'market-cloud',
        name: 'market-cloud',
        component: () => import('@/views/Third/MarketCloud/index.vue'),
        meta: {
          title: '大盘云图'
        }
      }
    ]
  },
  {
    name: 'System',
    path: '/sytem',
    component: Layout,
    meta: {},
    children: [
      {
        name: 'Configuration',
        path: 'configuration',
        component: () => import('@/views/System/Configuration.vue'),
        meta: {
          title: t('router.system_configuration'),
          icon: 'vi-carbon:settings'
          // noCache: true,
          // affix: false
        }
      }
    ]
  }
  /*
  {
    name: 'Test',
    path: '/test',
    component: Layout,
    meta: {},
    children: [
      {
        name: 'TestList',
        path: 'list',
        component: () => import('@/views/Test/List.vue'),
        meta: {
          title: t('router.test_list'),
          icon: 'vi-carbon:chart-custom',
          // noCache: true,
          // affix: false
        }
      }
    ]
  }
  */
  // {
  //   path: '/dashboard',
  //   component: Layout,
  //   redirect: '/dashboard/analysis',
  //   name: 'Dashboard',
  //   meta: {
  //     title: t('router.dashboard'),
  //     icon: 'vi-ant-design:dashboard-filled',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: 'analysis',
  //       component: () => import('@/views/Dashboard/Analysis.vue'),
  //       name: 'Analysis',
  //       meta: {
  //         title: t('router.analysis'),
  //         noCache: true,
  //         affix: true
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/external-link',
  //   component: Layout,
  //   meta: {},
  //   name: 'ExternalLink',
  //   children: [
  //     {
  //       path: 'https://element-plus-admin-doc.cn/',
  //       name: 'DocumentLink',
  //       meta: {
  //         title: t('router.document'),
  //         icon: 'vi-clarity:document-solid'
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/guide',
  //   component: Layout,
  //   name: 'Guide',
  //   meta: {},
  //   children: [
  //     {
  //       path: 'index',
  //       component: () => import('@/views/Guide/Guide.vue'),
  //       name: 'GuideDemo',
  //       meta: {
  //         title: t('router.guide'),
  //         icon: 'vi-cib:telegram-plane'
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/components',
  //   component: Layout,
  //   name: 'ComponentsDemo',
  //   meta: {
  //     title: t('router.component'),
  //     icon: 'vi-bx:bxs-component',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: 'form',
  //       component: getParentLayout(),
  //       redirect: '/components/form/default-form',
  //       name: 'Form',
  //       meta: {
  //         title: t('router.form'),
  //         alwaysShow: true
  //       },
  //       children: [
  //         {
  //           path: 'default-form',
  //           component: () => import('@/views/Components/Form/DefaultForm.vue'),
  //           name: 'DefaultForm',
  //           meta: {
  //             title: t('router.defaultForm')
  //           }
  //         },
  //         {
  //           path: 'use-form',
  //           component: () => import('@/views/Components/Form/UseFormDemo.vue'),
  //           name: 'UseForm',
  //           meta: {
  //             title: 'UseForm'
  //           }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'table',
  //       component: getParentLayout(),
  //       redirect: '/components/table/default-table',
  //       name: 'TableDemo',
  //       meta: {
  //         title: t('router.table'),
  //         alwaysShow: true
  //       },
  //       children: [
  //         {
  //           path: 'default-table',
  //           component: () => import('@/views/Components/Table/DefaultTable.vue'),
  //           name: 'DefaultTable',
  //           meta: {
  //             title: t('router.defaultTable')
  //           }
  //         },
  //         {
  //           path: 'use-table',
  //           component: () => import('@/views/Components/Table/UseTableDemo.vue'),
  //           name: 'UseTable',
  //           meta: {
  //             title: 'UseTable'
  //           }
  //         },
  //         {
  //           path: 'tree-table',
  //           component: () => import('@/views/Components/Table/TreeTable.vue'),
  //           name: 'TreeTable',
  //           meta: {
  //             title: t('router.treeTable')
  //           }
  //         },
  //         {
  //           path: 'table-image-preview',
  //           component: () => import('@/views/Components/Table/TableImagePreview.vue'),
  //           name: 'TableImagePreview',
  //           meta: {
  //             title: t('router.PicturePreview')
  //           }
  //         },
  //         {
  //           path: 'table-video-preview',
  //           component: () => import('@/views/Components/Table/TableVideoPreview.vue'),
  //           name: 'TableVideoPreview',
  //           meta: {
  //             title: t('router.tableVideoPreview')
  //           }
  //         },
  //         {
  //           path: 'card-table',
  //           component: () => import('@/views/Components/Table/CardTable.vue'),
  //           name: 'CardTable',
  //           meta: {
  //             title: t('router.cardTable')
  //           }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'editor-demo',
  //       component: getParentLayout(),
  //       redirect: '/components/editor-demo/editor',
  //       name: 'EditorDemo',
  //       meta: {
  //         title: t('router.editor'),
  //         alwaysShow: true
  //       },
  //       children: [
  //         {
  //           path: 'editor',
  //           component: () => import('@/views/Components/Editor/Editor.vue'),
  //           name: 'Editor',
  //           meta: {
  //             title: t('router.richText')
  //           }
  //         },
  //         {
  //           path: 'json-editor',
  //           component: () => import('@/views/Components/Editor/JsonEditor.vue'),
  //           name: 'JsonEditor',
  //           meta: {
  //             title: t('router.jsonEditor')
  //           }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'search',
  //       component: () => import('@/views/Components/Search.vue'),
  //       name: 'Search',
  //       meta: {
  //         title: t('router.search')
  //       }
  //     },
  //     {
  //       path: 'descriptions',
  //       component: () => import('@/views/Components/Descriptions.vue'),
  //       name: 'Descriptions',
  //       meta: {
  //         title: t('router.descriptions')
  //       }
  //     },
  //     {
  //       path: 'image-viewer',
  //       component: () => import('@/views/Components/ImageViewer.vue'),
  //       name: 'ImageViewer',
  //       meta: {
  //         title: t('router.imageViewer')
  //       }
  //     },
  //     {
  //       path: 'dialog',
  //       component: () => import('@/views/Components/Dialog.vue'),
  //       name: 'Dialog',
  //       meta: {
  //         title: t('router.dialog')
  //       }
  //     },
  //     {
  //       path: 'icon',
  //       component: () => import('@/views/Components/Icon.vue'),
  //       name: 'Icon',
  //       meta: {
  //         title: t('router.icon')
  //       }
  //     },
  //     {
  //       path: 'icon-picker',
  //       component: () => import('@/views/Components/IconPicker.vue'),
  //       name: 'IconPicker',
  //       meta: {
  //         title: t('router.iconPicker')
  //       }
  //     },
  //     {
  //       path: 'echart',
  //       component: () => import('@/views/Components/Echart.vue'),
  //       name: 'Echart',
  //       meta: {
  //         title: t('router.echart')
  //       }
  //     },
  //     {
  //       path: 'count-to',
  //       component: () => import('@/views/Components/CountTo.vue'),
  //       name: 'CountTo',
  //       meta: {
  //         title: t('router.countTo')
  //       }
  //     },
  //     {
  //       path: 'qrcode',
  //       component: () => import('@/views/Components/Qrcode.vue'),
  //       name: 'Qrcode',
  //       meta: {
  //         title: t('router.qrcode')
  //       }
  //     },
  //     {
  //       path: 'highlight',
  //       component: () => import('@/views/Components/Highlight.vue'),
  //       name: 'Highlight',
  //       meta: {
  //         title: t('router.highlight')
  //       }
  //     },
  //     {
  //       path: 'infotip',
  //       component: () => import('@/views/Components/Infotip.vue'),
  //       name: 'Infotip',
  //       meta: {
  //         title: t('router.infotip')
  //       }
  //     },
  //     {
  //       path: 'input-password',
  //       component: () => import('@/views/Components/InputPassword.vue'),
  //       name: 'InputPassword',
  //       meta: {
  //         title: t('router.inputPassword')
  //       }
  //     },
  //     {
  //       path: 'waterfall',
  //       component: () => import('@/views/Components/Waterfall.vue'),
  //       name: 'waterfall',
  //       meta: {
  //         title: t('router.waterfall')
  //       }
  //     },
  //     {
  //       path: 'image-cropping',
  //       component: () => import('@/views/Components/ImageCropping.vue'),
  //       name: 'ImageCropping',
  //       meta: {
  //         title: t('router.imageCropping')
  //       }
  //     },
  //     {
  //       path: 'video-player',
  //       component: () => import('@/views/Components/VideoPlayer.vue'),
  //       name: 'VideoPlayer',
  //       meta: {
  //         title: t('router.videoPlayer')
  //       }
  //     },
  //     {
  //       path: 'avatars',
  //       component: () => import('@/views/Components/Avatars.vue'),
  //       name: 'Avatars',
  //       meta: {
  //         title: t('router.avatars')
  //       }
  //     },
  //     {
  //       path: 'i-agree',
  //       component: () => import('@/views/Components/IAgree.vue'),
  //       name: 'IAgree',
  //       meta: {
  //         title: t('router.iAgree')
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/function',
  //   component: Layout,
  //   redirect: '/function/multipleTabs',
  //   name: 'Function',
  //   meta: {
  //     title: t('router.function'),
  //     icon: 'vi-ri:function-fill',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: 'multiple-tabs',
  //       component: () => import('@/views/Function/MultipleTabs.vue'),
  //       name: 'MultipleTabs',
  //       meta: {
  //         title: t('router.multipleTabs')
  //       }
  //     },
  //     {
  //       path: 'multiple-tabs-demo/:id',
  //       component: () => import('@/views/Function/MultipleTabsDemo.vue'),
  //       name: 'MultipleTabsDemo',
  //       meta: {
  //         hidden: true,
  //         title: t('router.details'),
  //         canTo: true,
  //         activeMenu: '/function/multiple-tabs'
  //       }
  //     },
  //     {
  //       path: 'request',
  //       component: () => import('@/views/Function/Request.vue'),
  //       name: 'Request',
  //       meta: {
  //         title: t('router.request')
  //       }
  //     },
  //     {
  //       path: 'test',
  //       component: () => import('@/views/Function/Test.vue'),
  //       name: 'Test',
  //       meta: {
  //         title: t('router.permission'),
  //         permission: ['add', 'edit', 'delete']
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/hooks',
  //   component: Layout,
  //   redirect: '/hooks/useWatermark',
  //   name: 'Hooks',
  //   meta: {
  //     title: 'hooks',
  //     icon: 'vi-ic:outline-webhook',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: 'useWatermark',
  //       component: () => import('@/views/hooks/useWatermark.vue'),
  //       name: 'UseWatermark',
  //       meta: {
  //         title: 'useWatermark'
  //       }
  //     },
  //     {
  //       path: 'useTagsView',
  //       component: () => import('@/views/hooks/useTagsView.vue'),
  //       name: 'UseTagsView',
  //       meta: {
  //         title: 'useTagsView'
  //       }
  //     },
  //     {
  //       path: 'useValidator',
  //       component: () => import('@/views/hooks/useValidator.vue'),
  //       name: 'UseValidator',
  //       meta: {
  //         title: 'useValidator'
  //       }
  //     },
  //     {
  //       path: 'useCrudSchemas',
  //       component: () => import('@/views/hooks/useCrudSchemas.vue'),
  //       name: 'UseCrudSchemas',
  //       meta: {
  //         title: 'useCrudSchemas'
  //       }
  //     },
  //     {
  //       path: 'useClipboard',
  //       component: () => import('@/views/hooks/useClipboard.vue'),
  //       name: 'UseClipboard',
  //       meta: {
  //         title: 'useClipboard'
  //       }
  //     },
  //     {
  //       path: 'useNetwork',
  //       component: () => import('@/views/hooks/useNetwork.vue'),
  //       name: 'UseNetwork',
  //       meta: {
  //         title: 'useNetwork'
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/level',
  //   component: Layout,
  //   redirect: '/level/menu1/menu1-1/menu1-1-1',
  //   name: 'Level',
  //   meta: {
  //     title: t('router.level'),
  //     icon: 'vi-carbon:skill-level-advanced'
  //   },
  //   children: [
  //     {
  //       path: 'menu1',
  //       name: 'Menu1',
  //       component: getParentLayout(),
  //       redirect: '/level/menu1/menu1-1/menu1-1-1',
  //       meta: {
  //         title: t('router.menu1')
  //       },
  //       children: [
  //         {
  //           path: 'menu1-1',
  //           name: 'Menu11',
  //           component: getParentLayout(),
  //           redirect: '/level/menu1/menu1-1/menu1-1-1',
  //           meta: {
  //             title: t('router.menu11'),
  //             alwaysShow: true
  //           },
  //           children: [
  //             {
  //               path: 'menu1-1-1',
  //               name: 'Menu111',
  //               component: () => import('@/views/Level/Menu111.vue'),
  //               meta: {
  //                 title: t('router.menu111')
  //               }
  //             }
  //           ]
  //         },
  //         {
  //           path: 'menu1-2',
  //           name: 'Menu12',
  //           component: () => import('@/views/Level/Menu12.vue'),
  //           meta: {
  //             title: t('router.menu12')
  //           }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'menu2',
  //       name: 'Menu2',
  //       component: () => import('@/views/Level/Menu2.vue'),
  //       meta: {
  //         title: t('router.menu2')
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/example-dialog',
  //   name: 'Example',
  //   meta: {
  //     title: t('router.example'),
  //     icon: 'vi-ep:management',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: 'example-dialog',
  //       component: () => import('@/views/Example/Dialog/ExampleDialog.vue'),
  //       name: 'ExampleDialog',
  //       meta: {
  //         title: t('router.exampleDialog')
  //       }
  //     },
  //     {
  //       path: 'example-page',
  //       component: () => import('@/views/Example/Page/ExamplePage.vue'),
  //       name: 'ExamplePage',
  //       meta: {
  //         title: t('router.examplePage')
  //       }
  //     },
  //     {
  //       path: 'example-add',
  //       component: () => import('@/views/Example/Page/ExampleAdd.vue'),
  //       name: 'ExampleAdd',
  //       meta: {
  //         title: t('router.exampleAdd'),
  //         noTagsView: true,
  //         noCache: true,
  //         hidden: true,
  //         canTo: true,
  //         activeMenu: '/example/example-page'
  //       }
  //     },
  //     {
  //       path: 'example-edit',
  //       component: () => import('@/views/Example/Page/ExampleEdit.vue'),
  //       name: 'ExampleEdit',
  //       meta: {
  //         title: t('router.exampleEdit'),
  //         noTagsView: true,
  //         noCache: true,
  //         hidden: true,
  //         canTo: true,
  //         activeMenu: '/example/example-page'
  //       }
  //     },
  //     {
  //       path: 'example-detail',
  //       component: () => import('@/views/Example/Page/ExampleDetail.vue'),
  //       name: 'ExampleDetail',
  //       meta: {
  //         title: t('router.exampleDetail'),
  //         noTagsView: true,
  //         noCache: true,
  //         hidden: true,
  //         canTo: true,
  //         activeMenu: '/example/example-page'
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/error',
  //   component: Layout,
  //   redirect: '/error/404',
  //   name: 'Error',
  //   meta: {
  //     title: t('router.errorPage'),
  //     icon: 'vi-ci:error',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: '404-demo',
  //       component: () => import('@/views/Error/404.vue'),
  //       name: '404Demo',
  //       meta: {
  //         title: '404'
  //       }
  //     },
  //     {
  //       path: '403-demo',
  //       component: () => import('@/views/Error/403.vue'),
  //       name: '403Demo',
  //       meta: {
  //         title: '403'
  //       }
  //     },
  //     {
  //       path: '500-demo',
  //       component: () => import('@/views/Error/500.vue'),
  //       name: '500Demo',
  //       meta: {
  //         title: '500'
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/authorization',
  //   component: Layout,
  //   redirect: '/authorization/user',
  //   name: 'Authorization',
  //   meta: {
  //     title: t('router.authorization'),
  //     icon: 'vi-eos-icons:role-binding',
  //     alwaysShow: true
  //   },
  //   children: [
  //     {
  //       path: 'department',
  //       component: () => import('@/views/Authorization/Department/Department.vue'),
  //       name: 'Department',
  //       meta: {
  //         title: t('router.department')
  //       }
  //     },
  //     {
  //       path: 'user',
  //       component: () => import('@/views/Authorization/User/User.vue'),
  //       name: 'User',
  //       meta: {
  //         title: t('router.user')
  //       }
  //     },
  //     {
  //       path: 'menu',
  //       component: () => import('@/views/Authorization/Menu/Menu.vue'),
  //       name: 'Menu',
  //       meta: {
  //         title: t('router.menuManagement')
  //       }
  //     },
  //     {
  //       path: 'role',
  //       component: () => import('@/views/Authorization/Role/Role.vue'),
  //       name: 'Role',
  //       meta: {
  //         title: t('router.role')
  //       }
  //     }
  //   ]
  // }
]

const router = createRouter({
  history: createWebHashHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const resetRouter = (): void => {
  router.getRoutes().forEach((route) => {
    const { name } = route
    if (name && !NO_RESET_WHITE_LIST.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
