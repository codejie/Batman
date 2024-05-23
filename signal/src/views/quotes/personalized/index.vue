<template>
<div style="padding:30px;">
	<!-- <h1>Personalized Portfolio</h1> -->
	<div style="margin-top: 10px; margin-bottom: 10px;" >
	<el-button type="primary" @click="createFormVisibled=true">创建</el-button>
	<el-button :disabled="!itemSelected" @click="onItemDeleteClick">删除</el-button>
	</div>
	<el-table :data="tableData" :stripe="true" :border="true" style="width: 100%;" @selection-change="onSelectionChange">
	<el-table-column type="selection" fixed width="50" />
	<el-table-column prop="code" label="代码" width="80">
		<template slot-scope="{row}">
			<el-button type="text" @click="onCodeClick(row.code)">
			{{ row.code }}
			</el-button>
		</template>
	</el-table-column>
	<el-table-column prop="name" label="名称" width="90"/>
	<el-table-column prop="price" label="现价" width="80"/>
	<el-table-column prop="percentage" label="涨跌幅%" width="90"/>
	<el-table-column prop="amount" label="涨跌额" width="80"/>
	<el-table-column prop="volatility" label="振幅%" width="80"/>          
	<el-table-column prop="open" label="今开" width="80"/>
	<el-table-column prop="close" label="昨收" width="80"/>
	<el-table-column prop="high" label="最高" width="80"/>
	<el-table-column prop="low" label="最低" width="80"/>
	<el-table-column prop="volume" label="成交量" width="120"/>
	<el-table-column prop="turnover" label="成交额" width="140"/>
	<el-table-column prop="rate" label="换手率%" width="90"/>
	<el-table-column prop="date" label="行情日期" width="120"/>
	<el-table-column prop="updated" label="添加日期" width="120"/>
	</el-table>
	<personalized-create-form ref="PersonalizedCreateForm" :visibled="createFormVisibled" @closed="onCreateFormClosed" />
</div>
</template>
  
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { getPersonalized } from '@/api/quotes'
import PersonalizedCreateForm from './create_form.vue'
import { removePersonalized } from '@/api/quotes'

@Component({
name: 'Personsalized',
components: {
	PersonalizedCreateForm
}
})
export default class extends Vue {
private createFormVisibled: boolean = false
private itemSelected: boolean = false
private tableData: any[] = []
private selectedData: any[] = []

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
		id: item.id,
		code: item.code, //'<a>item.code</a>',
		name: item.name,
		updated: item.updated,
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

private onCreateFormClosed(args: any) {
	this.createFormVisibled = false

	if (args.code === 0)
		this.loadPersonalized()
}

private onCodeClick(code: string) {
	this.$router.push({name: 'DataStock', params: {stockSymbol: code}})
}

private onSelectionChange(items: any[]) {
	this.itemSelected = items.length > 0
	this.selectedData = items;
}
	
private async onItemDeleteClick() {
	try {
		const ret = await this.$confirm(
			'Are you sure to delete selected item(s) ?',
			'Warning',
			{
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'			
			}
		)

		const ids: number[] = []
		this.selectedData.forEach(item => {
			ids.push(item.id)
		})

		const { data } = await removePersonalized({
			id: ids
		})

		this.loadPersonalized()
	} catch (e) {
		// console.log(e)
	}
}
}
</script>
