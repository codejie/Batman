<script setup lang="ts">
import { ElTable, ElTableColumn, ElButton } from 'element-plus'

function onCreateClick() {
  
}
</script>
<template>
  <ContentWrap title="Customized">
    <div>
      <ElButton class="btn" type="primary" @click="onCreateClick">Create</ElButton>
    </div>
    <ElTable :data="tableData" :stripe="true" :border="true" style="width: 100%;" @selection-change="onSelectionChange">
      <!-- <ElTableColumn type="selection" fixed width="50" /> -->
      <ElTableColumn prop="code" label="代码" width="80">
        <template #default="{row}">
          <el-button type="text" @click="onCodeClick(row.code)">
          {{ row.code }}
          </el-button>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="name" label="名称" width="90"/>
      <ElTableColumn prop="price" label="现价" width="80"/>
      <ElTableColumn prop="percentage" label="涨跌幅%" width="90"/>
      <ElTableColumn prop="amount" label="涨跌额" width="80"/>
      <ElTableColumn prop="volatility" label="振幅%" width="80"/>          
      <ElTableColumn prop="open" label="今开" width="80"/>
      <ElTableColumn prop="close" label="昨收" width="80"/>
      <ElTableColumn prop="high" label="最高" width="80"/>
      <ElTableColumn prop="low" label="最低" width="80"/>
      <ElTableColumn prop="volume" label="成交量" width="120"/>
      <ElTableColumn prop="turnover" label="成交额" width="140"/>
      <ElTableColumn prop="rate" label="换手率%" width="90"/>
      <ElTableColumn prop="date" label="行情日期" width="120"/>
      <ElTableColumn prop="updated" label="添加日期" width="120"/>
	</ElTable>
  </ContentWrap>
</template>
<style lang="css">
.btn {
  margin: 12px;
}
</style>
