<script setup lang="ts">
import { ref } from 'vue'
import { ElSelect, ElOption, ElButton, ElDivider } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import TrendArgumentTable from './components/TrendArgumentTable.vue'

const selectedValue = ref('')
const options = ref([
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  { value: 'option3', label: 'Option 3' }
])

const showArgumentTable = ref(false)

const toggleTable = () => {
  showArgumentTable.value = !showArgumentTable.value
}
</script>

<template>
  <ContentWrap>
    <div class="section-title">计算参数</div>
    <div class="action-container">
      <el-select v-model="selectedValue" placeholder="Select" class="select-width">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-button type="primary" style="margin-left: 10px;">提交</el-button>
      <el-button  @click="toggleTable">{{ showArgumentTable ? '收起参数列表' : '查看参数列表' }}</el-button>
    </div>
    <TrendArgumentTable v-if="showArgumentTable" />

    <el-divider />

    <div class="section-title">计算结果</div>
    <!-- Content for calculation results goes here -->
  </ContentWrap>
</template>

<style scoped>
.section-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 10px;
}
.action-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.select-width {
  width: 33.33%;
}
</style>
