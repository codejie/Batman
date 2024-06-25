<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import CreateForm from './components/CreateForm.vue'

const { t } = useI18n()
const { push, go } = useRouter()

const loading = ref<boolean>(false)
const onBtnSubmit = async () => {}
</script>
<template>
  <ContentDetailWrap :title="t('common.create')" @back="push('/strategy/filter')">
    <template #header>
      <BaseButton @click="go(-1)">{{ t('common.back') }}</BaseButton>
      <BaseButton type="primary" :loading="loading" @click="onBtnSubmit">
        {{ t('common.submit') }}
      </BaseButton>
    </template>
    <CreateForm />
  </ContentDetailWrap>
</template>
