<script lang="ts">
type LinkInfo = {
  title: string,
  url: string,
  tooltip?: string,
}
</script>
<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap';
import { ref } from 'vue';
import { ElButton, ElInput, ElLink, ElRow, ElCol, ElIcon, ElMenu, ElMenuItem, ElMenuItemGroup, ElAutoResizer } from 'element-plus';
import { Document, Menu as IconMenu, Location, Setting, Search } from '@element-plus/icons-vue'
import { TYPE_STOCK } from '@/api/data';

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
const url = ref<string>()

const linkInfos: LinkInfo[] = [
  {
    title: '东方财富',
    url: 'https://quote.eastmoney.com/center/gridlist.html#hs_a_board',
    tooltip: '东方财富'
  },
  {
    title: '新浪财经',
    url: 'https://finance.sina.com.cn/realstock/company/sh600000/nc.shtml',
    tooltip: '新浪财经'
  },
  {
    title: '同花顺',
    url: 'https://stock.10jqka.com.cn/market/',
    tooltip: '同花顺'
  }
]

</script>
<template>
  <ContentWrap>
    <ElRow :gutter="24">
      <ElCol :span="3">
        <ElInput :placeholder="'请输入股票代码'" v-model="props.code" />
      </ElCol>
      <ElCol :span="1">
        <ElButton>查询</ElButton>
      </ElCol>
      <ElCol :span="20"></ElCol>
    </ElRow>
    <ElRow :gutter="24" class="tac" style="margin-top: 10px;">
      <ElCol :span="collapse ? 2 : 4">
        <ElButton type="primary" @click="collapse = !collapse">Collape</ElButton>
        <ElMenu class="el-menu-vertical-demo" :collapse="collapse">
          <ElMenuItem v-for="(info, index) in linkInfos" :key="info.title" :index="index.toString()">
            <ElIcon><Setting /></ElIcon>
            <template #title>
              {{ info.title }}
              <ElButton @click="(index) => url = info.url"> {{ info.title }}</ElButton>
            </template>
          </ElMenuItem>
        </ElMenu>
      </ElCol>
      <ElCol :span="collapse ? 22 : 20">
        <iframe :src="url" width="100%" height="800px" frameborder="0"></iframe>
        <!-- <ElAutoResizer v-if="url">
          <template #default="{ height, width }">
            <iframe :src="url" :width="width" :height="height" frameborder="0"></iframe>
          </template>
        </ElAutoResizer> -->
      </ElCol>
    </ElRow>
    <!-- <ElButton @click="onClick">Test</ElButton>
    <iframe
        :src="url"
        width="100%"
        height="500px"
        frameborder="0"
    ></iframe> -->
  </ContentWrap>
</template>