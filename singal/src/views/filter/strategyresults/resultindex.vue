<template>
  <el-dialog :visible.sync="dialogVisible" width="55%">
    <el-form ref="form" label-width="80px">
      <el-form-item label="策略名称">{{strategy.name}}</el-form-item>
      <el-form-item label="策略说明">{{strategy.description}}</el-form-item>
      <el-row v-if="instance!=null">
        <el-col :span="6" v-for="argument in instance.arguments">
          <el-form-item :label="argument.name">{{argument.value}}{{argument.unit}}</el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table :border="true" :stripe="true"
      :data="resultList"
      style="width: 100%;margin-top: 15px;">
      <el-table-column label="编码" prop="code" min-width="150"/>
      <el-table-column label="名称" prop="name" min-width="150"/>
      <el-table-column label="block" prop="block" min-width="150"/>
      <el-table-column label="block rate" prop="blockRate" min-width="150"/>
    </el-table>
    <el-pagination style="text-align:center"
      layout="prev, pager, next, sizes, jumper"
      :page-size="pager.pageSize"
      :current-page="pager.currentPage"
      :total="pager.total"
      @size-change="sizeChange"
      @current-change="currentChange">
    </el-pagination>
  </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Pager } from '@/api/pager'
import { IStrategyData, IStrategyInstanceData } from '@/api/def/strategy'

@Component({
  name: 'StrategyResult'
})
export default class extends Vue {
  @Prop({ required: true }) private strategy!: IStrategyData
  @Prop({ required: true }) private instance!: IStrategyInstanceData
  private pager: Pager = {
    total: 0,
    pageSize: 20,
    currentPage: 1
  }
  private dialogVisible: boolean = false
  private resultList: Object[] = [] 

  created() {
  }

  private init() {
    this.pager.currentPage = 1
    this.dialogVisible = true
    this.loadResultList()
  }

  private loadResultList(){
    console.log('===========加载结果列表==========')
    console.log(this.pager)
    var resultList = []
    for(var i=1; i<=2; i++){
      resultList.push({
        code: '00000' + i,
        name: '财富密码' + i,
        block: 5300,
        blockRate: '1' + i + '%'
      })
    }
    this.resultList = resultList
    this.pager.total = 50
  }

  private currentChange(currentPage: number) {
    this.pager.currentPage = currentPage
    this.loadResultList()
  }

  private sizeChange(pageSize: number) {
    this.pager.pageSize = pageSize
    this.loadResultList()
  }
  
}
</script>
