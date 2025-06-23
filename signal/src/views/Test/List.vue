<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap';
import { ref } from 'vue';
import { ElButton } from 'element-plus';

const url = ref<string>('https://example.com');

function onClick() {
  url.value = 'https://quote.eastmoney.com/center/gridlist.html#hs_a_board';
}

</script>
<template>
  <ContentWrap>
    <ElButton @click="onClick">Test</ElButton>
    <iframe
        :src="url"
        width="100%"
        height="500px"
        frameborder="0"
    ></iframe>
  <router-view />
  </ContentWrap>
</template>