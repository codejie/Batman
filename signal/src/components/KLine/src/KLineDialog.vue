<script setup lang="ts">
import { PropType, ref, watch } from 'vue'
import { ElDialog, ElButton } from 'element-plus'
import { ReqParam, KLinePanel2 } from '..';

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

</script>
<template>
    <ElDialog v-model="showDialog" :title="title || `${reqParam.name} (${reqParam.code})`" :width="width" :destroy-on-close="true" @closed="onClose">
    <KLinePanel2 :req-param="reqParam!" />
    <template #footer>
      <ElButton type="primary" @click="onClose">关闭</ElButton>
    </template>    
  </ElDialog>    
</template>