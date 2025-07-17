<script lang="ts">
export const options = reactive({
  type: undefined as number | undefined,
  code: undefined as string | undefined,
  name: undefined as string | undefined,
  collapse: false as boolean,
  target: undefined as string | undefined
})
// type LinkInfo = {
//   title: string,
//   url: string,
//   tooltip?: string,
// }
</script>
<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap';
import { reactive, ref, watch } from 'vue';
import { ElButton, ElInput, ElRow, ElCol } from 'element-plus';
import { DArrowLeft, DArrowRight } from '@element-plus/icons-vue'
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data';
import Navigator from './components/Navigator.vue';

const props = defineProps({
  type: {
    type: Number,
    required: false,
    default: TYPE_STOCK
  },
  code : {
    type: String,
    required: false
  },
  name: {
    type: String,
    required: false,
    default: undefined
  }
})

const collapse = ref<boolean>(false)
const url = ref<string | undefined>()

watch(
  () => collapse.value,
  (newVal) => {
    options.collapse = newVal
  },
  { immediate: true }
)

watch(
  () => options.target,
  (newVal) => {
    url.value = newVal
  },
  { immediate: true }
)

watch(
  () => props.code,
  (newVal) => {
    options.code = newVal
  },
  { immediate: true }
)

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

function onSearch() {
  const marketCode = getMarketCode(props.type, options.code!);
  const url = `https://xueqiu.com/S/${marketCode}`;
  window.open(url, '_blank');
}

</script>
<template>
  <ContentWrap>
    <ElRow :gutter="24">
      <ElCol :span="3">
        <ElInput :placeholder="'请输入股票代码'" v-model="options.code" />
      </ElCol>
      <ElCol :span="1">
        <ElButton :disabled="!options.code"  @click="onSearch">雪球个股</ElButton>
      </ElCol>
      <ElCol :span="20"></ElCol>
    </ElRow>
    <ElRow :gutter="24" class="tac" style="margin-top: 10px;">
      <ElCol :span="collapse ? 1 : 3">
        <ElButton type="info" :icon="collapse ? DArrowRight : DArrowLeft" @click="collapse = !collapse" />
        <Navigator />
      </ElCol>
      <ElCol :span="collapse ? 23 : 21">
        <iframe :src="url" width="100%" height="800px" frameborder="0"></iframe>
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>
