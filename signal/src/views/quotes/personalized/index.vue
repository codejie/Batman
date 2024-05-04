<template>
    <div style="padding:30px;">
      <h1>Personalized Portfolio</h1>
      <div>日期:{{today}}</div>
      <ve-table
        :fixed-header="true"
        :columns="columns"
        :table-data="tableData"
        :border-x="true"
        :border-y="true"
        :rowStyleOption="rowStyleOption"
      />
    </div>
  </template>
  
  <script lang="ts">
  import { Component, Vue } from 'vue-property-decorator'
  import { getPersonalized } from '@/api/quotes'
  
  @Component({
    name: 'Personsalized'
  })
  export default class extends Vue {
      private rowStyleOption = {
                hoverHighlight: true,
              }
      private columns = [
          { field: 'code', key: 'a', title: '代码', align: 'center', fixed: "left", renderBodyCell: ({ row, column, rowIndex }, h) => {
            return h(
              'span', [h('span', {
                domProps: {
                  innerHTML: this.tableData[rowIndex].code
                },
                style: {
                  color: 'blue',
                  marginRight: '4px',
                  cursor: 'pointer'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'DataStock', params: {stockSymbol: this.tableData[rowIndex].code}})
                  }
                }
              })]
            )
          }},
          { field: 'name', key: 'b', title: '名称', align: 'center', fixed: "left"},
          { field: 'price', key: 'c', title: '现价', align: 'center'},
          { field: 'percentage', key: 'd', title: '涨跌幅%', align: 'center'},
          { field: 'amount', key: 'e', title: '涨跌额', align: 'center'},
          { field: 'volatility', key: 'm', title: '振幅%', align: 'center'},          
          { field: 'open', key: 'f', title: '今开', align: 'center'},
          { field: 'close', key: 'g', title: '昨收', align: 'center'},
          { field: 'high', key: 'h', title: '最高', align: 'center'},
          { field: 'low', key: 'i', title: '最低', align: 'center'},
          { field: 'volume', key: 'j', title: '成交量', align: 'center'},
          { field: 'turnover', key: 'k', title: '成交额', align: 'center'},
          { field: 'rate', key: 'l', title: '换手率%', align: 'center'}
        ]
      private tableData: any = []
      private today: string | null = null
      created() {
        this.today = '2024-04-30' //(new Date()).toISOString().slice(0, 10)
        this.loadPersonalized()
      }

      private async loadPersonalized() {
        const { data } = await getPersonalized({
          date: this.today //'2024-04-30'
        })
        for (const item of data.result) {
          this.tableData.push({
            code: item.code, //'<a>item.code</a>',
            name: item.name,
            price: item.quote.price,
            percentage: item.quote.percentage + '%',
            amount: item.quote.amount,
            volatility: item.quote.volatility + '%',
            open: item.quote.open,
            close: item.quote.close,
            high: item.quote.high,
            low: item.quote.low,
            volume: item.quote.volume,
            turnover: item.quote.turnover,
            rate: item.quote.rate + '%'
          })
        }
      }
          
  }
  </script>
  