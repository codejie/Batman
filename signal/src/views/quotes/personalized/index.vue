<template>
    <div style="padding:30px;">
      <h1>Personalized Portfolio</h1>
      <el-button size="mini" @click="createPersonalized">创建</el-button>
      <!-- <el-table :data="tableData" border style="width: 100%; height: 100%;" @row-click="onRowClick"> -->
      <el-table :data="tableData" border style="width: 100%; height: 100%;">
        <el-table-column prop="code" label="代码"  width="80%" fixed>
          <template slot-scope="{row}">
              <el-button type="text" @click="onCodeClick(row.code)">
                {{ row.code }}
              </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" width="90%"/>
        <el-table-column prop="price" label="现价" width="80%"/>
        <el-table-column prop="percentage" label="涨跌幅%" width="100%"/>
        <el-table-column prop="amount" label="涨跌额" width="90%"/>
        <el-table-column prop="volatility" label="振幅%" width="100%"/>          
        <el-table-column prop="open" label="今开" width="80%"/>
        <el-table-column prop="close" label="昨收" width="80%"/>
        <el-table-column prop="high" label="最高" width="80%"/>
        <el-table-column prop="low" label="最低" width="80%"/>
        <el-table-column prop="volume" label="成交量" width="130%"/>
        <el-table-column prop="turnover" label="成交额" width="150%"/>
        <el-table-column prop="rate" label="换手率%" width="100%"/>
        <el-table-column prop="date" label="日期" width="120%"/>  
      </el-table>
      <personalized-create-form ref="PersonalizedCreateForm" />
    </div>
  </template>
  
  <script lang="ts">
  import { Component, Vue } from 'vue-property-decorator'
  import { getPersonalized } from '@/api/quotes'
  import PersonalizedCreateForm from './create_form.vue'
  
  @Component({
    name: 'Personsalized',
    components: {
      PersonalizedCreateForm
    }
  })
  export default class extends Vue {
      private tableData: any = []
      // private today: string | null = null
      created() {
        // this.today = '2024-04-30' //(new Date()).toISOString().slice(0, 10)
        this.loadPersonalized()
      }

      public async loadPersonalized() {
        const { data } = await getPersonalized({
          // date: this.today //'2024-04-30'
        })
        this.tableData = []
        for (const item of data.result) {
          this.tableData.push({
            code: item.code, //'<a>item.code</a>',
            name: item.name,
            price: item.quote ? item.quote.price : '-',
            percentage: item.quote ? item.quote.percentage + '%' : '-',
            amount: item.quote ? item.quote.amount : '-',
            volatility: item.quote ? item.quote.volatility + '%' : '-',
            open: item.quote ? item.quote.open : '-',
            close: item.quote ? item.quote.close : '-',
            high: item.quote ? item.quote.high : '-',
            low: item.quote ? item.quote.low : '-',
            volume: item.quote ? item.quote.volume : '-',
            turnover: item.quote ? item.quote.turnover : '-',
            rate: item.quote ? item.quote.rate + '%' : '-',
            date: item.quote ? item.quote.date : '-'
          })
        }
      }

      private onRowClick(row: any, column: any, event: Event) {
        this.$router.push({name: 'DataStock', params: {stockSymbol: row.code}})
        // console.log(row)
        // console.log(column)
      }

      private onCodeClick(code: string) {
        this.$router.push({name: 'DataStock', params: {stockSymbol: code}})
      }
      
      private async createPersonalized() {
        const ref: any = this.$refs.PersonalizedCreateForm
        ref.init()
      }

          
  }
  </script>
  