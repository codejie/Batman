<script setup lang="ts">
import { ref, unref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import CreateForm from '@/views/Strategy/filter/components/CreateForm.vue'
import { CreateInstanceRequest } from '@/api/strategy/types'

const { t } = useI18n()
const { push, go } = useRouter()

const form = ref<any>(null)

const loading = ref<boolean>(false)
const onBtnSubmit = async () => {
  const req: CreateInstanceRequest = {
    name: '',
    trigger: {
      mode: '',
      days: undefined,
      hour: undefined,
      minute: undefined,
      seconds: undefined,
      period: false
    },
    arg_values: undefined,
    algo_values: undefined
  }
}
</script>
<template>
  <ContentDetailWrap :title="t('common.create')" @back="push('/strategy/filter')">
    <template #header>
      <BaseButton @click="go(-1)">{{ t('common.back') }}</BaseButton>
      <BaseButton type="primary" :loading="loading" @click="onBtnSubmit">
        {{ t('common.submit') }}
      </BaseButton>
    </template>
    <CreateForm ref="form" />
  </ContentDetailWrap>
  <div>
    {{ form }}
  </div>
</template>
