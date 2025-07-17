<script setup lang="ts">
import { PropType, ref, watch } from 'vue'
import { ElDialog, ElButton, ElLink } from 'element-plus'
import { ReqParam, KLinePanel2 } from '..';
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data/types';

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
    default: '60%'
  }
})

const showDialog = ref<boolean>(props.visible && props.reqParam != undefined)

watch(
  () =>props.visible,
  (value: boolean) => {
    showDialog.value = value
  }
)

const emit = defineEmits(['update:onClose'])

function onClose() {
  emit('update:onClose')
}

function getMarketCode(type: number, code: string): string {
  let marketCode = code;
  if (type === TYPE_STOCK) {
      if (code.startsWith('6')) {
          marketCode = `SH${code}`;
      } else if (code.startsWith('0') || code.startsWith('3')) {
          marketCode = `SZ${code}`;
      } else if (code.startsWith('8') || code.startsWith('4')) {
          marketCode = `BJ${code}`;
      }
  } else if (type === TYPE_INDEX) {
      if (!code.startsWith('sh') && !code.startsWith('sz')) {
          if (code.startsWith('000') || code.startsWith('999')) {
              marketCode = `SH${code}`;
          } else if (code.startsWith('399')) {
              marketCode = `SZ${code}`;
          }
      }
  }
  return marketCode.toUpperCase();
}

function onTitleClick() {
  if (!props.reqParam) return;
  const { code, type } = props.reqParam;
  const marketCode = getMarketCode(type, code);
  const url = `https://xueqiu.com/S/${marketCode}`;
  window.open(url, '_blank');
}

</script>
<template>
  <ElDialog v-model="showDialog" :width="width" :destroy-on-close="true" @closed="onClose">
    <template #header>
      <ElLink @click="onTitleClick" :underline="false">
        <span style="font-size: 18px; color: #303133; font-weight: bold;">
          {{ title || `${reqParam.name} (${reqParam.code})` }}
        </span>
      </ElLink>
    </template>
    <KLinePanel2 :req-param="reqParam!" />
    <template #footer>
      <ElButton type="primary" @click="onClose">关闭</ElButton>
    </template>    
  </ElDialog>    
</template>