<script setup lang="ts">
import { PropType, ref, watch } from 'vue'
import { ElDialog, ElButton, ElLink } from 'element-plus'
import { ReqParam, KLinePanelPro } from '..'
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data/types'

const props = defineProps({
  reqParam: {
    type: Object as PropType<ReqParam>,
    required: true
  },
  visible: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: false,
    default: null
  },
  width: {
    type: String,
    required: false,
    default: '60%' // Match KLineDialog
  },
  height: {
    type: String,
    required: false,
    default: '650px'
  }
})

const showDialog = ref<boolean>(props.visible && props.reqParam != undefined)

watch(
  () => props.visible,
  (value: boolean) => {
    showDialog.value = value
  }
)

const emit = defineEmits(['update:onClose'])

function onClose() {
  emit('update:onClose')
}

function getMarketCode(type: number, code: string): string {
  let marketCode = code
  if (type === TYPE_STOCK) {
    if (code.startsWith('6')) {
      marketCode = `SH${code}`
    } else if (code.startsWith('0') || code.startsWith('3')) {
      marketCode = `SZ${code}`
    } else if (code.startsWith('8') || code.startsWith('4')) {
      marketCode = `BJ${code}`
    }
  } else if (type === TYPE_INDEX) {
    if (!code.startsWith('sh') && !code.startsWith('sz')) {
      if (code.startsWith('000') || code.startsWith('999')) {
        marketCode = `SH${code}`
      } else if (code.startsWith('399')) {
        marketCode = `SZ${code}`
      }
    }
  }
  return marketCode.toUpperCase()
}

function onTitleClick() {
  if (!props.reqParam) return
  const { code, type } = props.reqParam
  const marketCode = getMarketCode(type, code)
  const url = `https://xueqiu.com/S/${marketCode}`
  window.open(url, '_blank')
}
</script>

<template>
  <ElDialog
    v-model="showDialog"
    :width="width"
    :destroy-on-close="true"
    append-to-body
    @closed="onClose"
  >
    <template #header>
      <ElLink @click="onTitleClick" :underline="false">
        <span class="dialog-title-text">
          {{ title || `${reqParam.name} (${reqParam.code})` }}
        </span>
        <span class="dialog-title-tag">Minute Analysis</span>
      </ElLink>
    </template>
    
    <div class="dialog-body-container">
      <KLinePanelPro :req-param="reqParam!" />
    </div>

    <template #footer>
      <div class="dialog-footer">
        <ElButton type="primary" @click="onClose">关闭</ElButton>
      </div>
    </template>
  </ElDialog>
</template>

<style scoped>
.dialog-title-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-right: 12px;
}

.dialog-title-tag {
  font-size: 0.75rem;
  padding: 2px 8px;
  background-color: #f0f7ff;
  color: #0066ff;
  border-radius: 4px;
  vertical-align: middle;
}

.dialog-body-container {
  min-height: 400px;
}

.dialog-footer {
  padding: 10px 0 0;
  text-align: right;
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-dialog__body) {
  padding: 16px 24px;
}

:deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>
