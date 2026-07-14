<script setup lang="ts">
import {
  ElDescriptions,
  ElDescriptionsItem,
  ElDialog,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem
} from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { useDesign } from '@/hooks/web/useDesign'
import LockDialog from './components/LockDialog.vue'
import { ref, computed } from 'vue'
import LockPage from './components/LockPage.vue'
import { useLockStore } from '@/store/modules/lock'
import { useUserStore } from '@/store/modules/user'
import { useRouter } from 'vue-router'
import { systemInfo } from '@/constants/systemInfo'

const { push } = useRouter()

const userStore = useUserStore()

const lockStore = useLockStore()

const getIsLock = computed(() => lockStore.getLockInfo?.isLock ?? false)

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('user-info')

const { t } = useI18n()

const loginOut = () => {
  userStore.logoutConfirm()
}

const dialogVisible = ref<boolean>(false)
const systemInfoVisible = ref<boolean>(false)

// 锁定屏幕
const lockScreen = () => {
  dialogVisible.value = true
}

const showSystemInfo = () => {
  systemInfoVisible.value = true
}

const toDocument = () => {
  window.open('https://element-plus-admin-doc.cn/')
}

const toPage = (path: string) => {
  push(path)
}
</script>

<template>
  <ElDropdown
    class="custom-hover"
    :class="prefixCls"
    trigger="click"
    popper-class="user-info-dropdown"
  >
    <div class="flex items-center">
      <img
        src="@/assets/imgs/avatar.png"
        alt=""
        class="w-[calc(var(--logo-height)-25px)] rounded-[50%]"
      />
      <span class="<lg:hidden text-14px pl-[5px] text-[var(--top-header-text-color)]">{{
        userStore.getUserInfo?.username
      }}</span>
    </div>
    <template #dropdown>
      <ElDropdownMenu>
        <!-- <ElDropdownItem>
          <div @click="toPage('/personal/personal-center')">
            {{ t('router.personalCenter') }}
          </div>
        </ElDropdownItem> -->
        <!-- <ElDropdownItem>
          <div @click="toDocument">{{ t('common.document') }}</div>
        </ElDropdownItem> -->
        <ElDropdownItem class="user-info-dropdown-item" @click="showSystemInfo">
          <div class="user-info-dropdown-action">
            <Icon class="user-info-dropdown-icon" icon="vi-bi:info-circle-fill" :size="15" />
            <span>系统信息</span>
          </div>
        </ElDropdownItem>
        <ElDropdownItem class="user-info-dropdown-item" @click="lockScreen">
          <div class="user-info-dropdown-action">
            <Icon class="user-info-dropdown-icon" icon="vi-ep:lock" :size="15" />
            <span>{{ t('lock.lockScreen') }}</span>
          </div>
        </ElDropdownItem>
        <ElDropdownItem class="user-info-dropdown-item" @click="loginOut">
          <div class="user-info-dropdown-action">
            <Icon class="user-info-dropdown-icon" icon="vi-ant-design:logout-outlined" :size="15" />
            <span>{{ t('common.loginOut') }}</span>
          </div>
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>

  <LockDialog v-if="dialogVisible" v-model="dialogVisible" />
  <ElDialog v-model="systemInfoVisible" title="系统信息" width="430px" class="system-info-dialog">
    <ElDescriptions :column="1" border>
      <ElDescriptionsItem label="系统名称">
        <span class="system-info-value">{{ systemInfo.name }}</span>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="系统版本">
        <span class="system-info-value">{{ systemInfo.version }}</span>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="Git 提交">
        <span class="system-info-value system-info-code">{{ systemInfo.gitCommit }}</span>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="编译时间">
        <span class="system-info-value">{{ systemInfo.buildTime }}</span>
      </ElDescriptionsItem>
    </ElDescriptions>
  </ElDialog>
  <teleport to="body">
    <transition name="fade-bottom" mode="out-in">
      <LockPage v-if="getIsLock" />
    </transition>
  </teleport>
</template>

<style scoped lang="less">
.fade-bottom-enter-active,
.fade-bottom-leave-active {
  transition:
    opacity 0.25s,
    transform 0.3s;
}

.fade-bottom-enter-from {
  opacity: 0;
  transform: translateY(-10%);
}

.fade-bottom-leave-to {
  opacity: 0;
  transform: translateY(10%);
}

:deep(.system-info-dialog) {
  max-width: calc(100vw - 32px);
}

:deep(.system-info-dialog .el-descriptions__label) {
  width: 96px;
  white-space: nowrap;
}

.system-info-value {
  word-break: break-all;
}

.system-info-code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
}

:global(.user-info-dropdown) {
  min-width: 138px;
}

:global(.user-info-dropdown .el-dropdown-menu) {
  padding: 6px;
}

:global(.user-info-dropdown .el-dropdown-menu__item) {
  border-radius: 4px;
  color: var(--el-text-color-regular);
  line-height: 1;
  padding: 0;
}

:global(.user-info-dropdown .el-dropdown-menu__item:not(.is-disabled):focus) {
  background-color: var(--el-fill-color-light);
  color: var(--el-color-primary);
}

:global(.user-info-dropdown .el-dropdown-menu__item:not(.is-disabled):hover) {
  background-color: var(--el-fill-color-light);
  color: var(--el-color-primary);
}

:global(
  .user-info-dropdown .el-dropdown-menu__item:not(.is-disabled):hover .user-info-dropdown-icon
),
:global(
  .user-info-dropdown .el-dropdown-menu__item:not(.is-disabled):focus .user-info-dropdown-icon
) {
  color: var(--el-color-primary);
}

.user-info-dropdown-action {
  display: flex;
  align-items: center;
  width: 100%;
  min-width: 126px;
  height: 34px;
  gap: 8px;
  padding: 0 10px;
  box-sizing: border-box;
  white-space: nowrap;
}

.user-info-dropdown-icon {
  color: var(--el-text-color-secondary);
  transition: color var(--el-transition-duration);
}
</style>
