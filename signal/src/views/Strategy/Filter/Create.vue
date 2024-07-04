<script setup lang="ts">
import { computed, ref, unref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import CreateForm from '@/views/Strategy/Filter/components/CreateForm.vue'
import { CreateInstanceRequest, TriggerModel } from '@/api/strategy/types'
import { apiCreate } from '@/api/strategy'
import { ElMessage } from 'element-plus'
// import { useEmitt } from '@/hooks/event/useEmitt'

const { t } = useI18n()
const { push, go } = useRouter()
// const { emitter } = useEmitt()

const form = ref<any>(null)
const submitEnabled = computed(() => {
  return unref(form)?.form.name && unref(form)?.form.strategy
})

function makeTrigger(): TriggerModel {
  const trigger = unref(form).trigger.data
  return {
    mode: trigger.mode,
    days: trigger.days,
    hour: trigger.hour,
    minute: trigger.minute,
    seconds: trigger.seconds,
    period: trigger.peroid
  }
}

function makeArgValues(): any {
  const data = unref(form).argument.data
  const ret = {}
  for (const item of data) {
    ret[item.arg.name] = item.value
  }
  return ret
}

function makeAlgoValues(): any {
  const algos = unref(form).algorithms
  const ret = {}
  for (const algo of algos) {
    ret[algo.name] = {}
    for (const item of algo.data) {
      ret[algo.name][item.arg.name] = item.value
    }
  }
  return ret
}

const loading = ref<boolean>(false)
const onBtnSubmit = async () => {
  loading.value = true
  const req: CreateInstanceRequest = {
    name: unref(form).form.name,
    strategy: unref(form).form.strategy.id,
    trigger: makeTrigger(),
    arg_values: makeArgValues(),
    algo_values: makeAlgoValues()
  }
  const ret = await apiCreate(req)
  loading.value = false
  if (ret.code == 0) {
    ElMessage({
      message: `Strategy create successfully - ${ret.result}.`,
      type: 'success'
    })
  }
  push('/strategy/filter')
}
</script>
<template>
  <ContentDetailWrap :title="t('common.create')">
    <template #header>
      <BaseButton @click="go(-1)">{{ t('common.back') }}</BaseButton>
      <BaseButton type="primary" :disabled="!submitEnabled" :loading="loading" @click="onBtnSubmit">
        {{ t('common.submit') }}
      </BaseButton>
    </template>
    <CreateForm ref="form" />
  </ContentDetailWrap>
  <div>
    {{ form }}
    {{ submitEnabled }}
  </div>
</template>
