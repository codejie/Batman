<script setup lang="tsx">
import { reactive, ref, watch, onMounted, unref } from 'vue'
import { Form, FormSchema } from '@/components/Form'
import { useI18n } from '@/hooks/web/useI18n'
import { ElCheckbox } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
// import { loginApi, getTestRoleApi, getAdminRoleApi } from '@/api/login'
import { LoginRequest } from '@/api/account/types'
import { apiLogin } from '@/api/account'
import { useAppStore } from '@/store/modules/app'
import { usePermissionStore } from '@/store/modules/permission'
import { useRouter } from 'vue-router'
import type { RouteLocationNormalizedLoaded } from 'vue-router'
import { useValidator } from '@/hooks/web/useValidator'
import { useUserStore } from '@/store/modules/user'
import { BaseButton } from '@/components/Button'

const { required } = useValidator()

const appStore = useAppStore()

const userStore = useUserStore()

const permissionStore = usePermissionStore()

const { currentRoute, push } = useRouter()

const { t } = useI18n()

const rules = {
  username: [required()],
  password: [required()]
}

const schema = reactive<FormSchema[]>([
  {
    field: 'title',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return <h2 class="text-2xl font-bold text-center w-[100%]">{t('login.login')}</h2>
        }
      }
    }
  },
  {
    field: 'account',
    label: t('login.username'),
    // value: 'admin',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      placeholder: 'admin or test'
    }
  },
  {
    field: 'passwd',
    label: t('login.password'),
    // value: 'admin',
    component: 'InputPassword',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: 'admin or test'
    }
  },
  {
    field: 'tool',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="flex justify-between items-center w-[100%]">
                <ElCheckbox v-model={remember.value} label={t('login.remember')} size="small" />
              </div>
            </>
          )
        }
      }
    }
  },
  {
    field: 'login',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="w-[100%]">
                <BaseButton
                  loading={loading.value}
                  type="primary"
                  class="w-[100%]"
                  onClick={signIn}
                >
                  {t('login.login')}
                </BaseButton>
              </div>
            </>
          )
        }
      }
    }
  }
])
const remember = ref(userStore.getRememberMe)

const initLoginInfo = () => {
  const loginInfo = userStore.getLoginInfo
  if (loginInfo) {
    const { account, passwd } = loginInfo
    setValues({ account, passwd })
  }
}
onMounted(() => {
  initLoginInfo()
})

const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose, setValues } = formMethods

const loading = ref(false)

const redirect = ref<string>('')

watch(
  () => currentRoute.value,
  (route: RouteLocationNormalizedLoaded) => {
    redirect.value = route?.query?.redirect as string
  },
  {
    immediate: true
  }
)

// 登录
const signIn = async () => {
  const formRef = await getElFormExpose()
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const formData = await getFormData<LoginRequest>()

      try {
        // const res = await loginApi(formData)
        const res = await apiLogin(formData)
        if (res) {
          // 是否记住我
          if (unref(remember)) {
            userStore.setLoginInfo({
              account: formData.account,
              passwd: formData.passwd
            })
          } else {
            userStore.setLoginInfo(undefined)
          }
          userStore.setRememberMe(unref(remember))
          userStore.setUserInfo({
            // account: formData.account,
            // passwd: formData.account,
            accessToken: res.result.accessToken,
            refreshToken: res.result.refreshToken,
            expired: res.result.expired,
            // uid: res.result.uid,
            avatar: res.result.avatar
          })
          userStore.setToken(res.result.accessToken)
          // 是否使用动态路由
          if (appStore.getDynamicRouter) {
            getRole()
          } else {
            await permissionStore.generateRoutes('static').catch(() => {})
            // permissionStore.getAddRouters.forEach((route) => {
            //   addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
            // })
            // permissionStore.setIsAddRouters(true)
            console.log(redirect.value)
            console.log(permissionStore.addRouters[0].path)
            push({ path: redirect.value || permissionStore.addRouters[0].path })
          }
        }
      } finally {
        loading.value = false
      }
    }
  })
}

// 获取角色信息
const getRole = async () => {
  // const formData = await getFormData<UserInfo>()
  // console.log('===============')
  // console.log(formData)
  // const params = {
  //   roleName: formData.account
  // }
  // const res =
  //   appStore.getDynamicRouter && appStore.getServerDynamicRouter
  //     ? await getAdminRoleApi(params)
  //     : await getTestRoleApi(params)
  // if (res) {
  //   const routers = res.data || []
  //   userStore.setRoleRouters(routers)
  //   appStore.getDynamicRouter && appStore.getServerDynamicRouter
  //     ? await permissionStore.generateRoutes('server', routers).catch(() => {})
  //     : await permissionStore.generateRoutes('frontEnd', routers).catch(() => {})
  //   permissionStore.getAddRouters.forEach((route) => {
  //     addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
  //   })
  //   permissionStore.setIsAddRouters(true)
  //   push({ path: redirect.value || permissionStore.addRouters[0].path })
  // }
}
</script>
<template>
  <Form
    :schema="schema"
    :rules="rules"
    label-position="top"
    hide-required-asterisk
    size="large"
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
    @register="formRegister"
  />
</template>
