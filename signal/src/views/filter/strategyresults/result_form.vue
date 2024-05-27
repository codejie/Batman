<template>
    <el-dialog :title="getTitle()" :visible="visibled" :show-close="false" width="45%">
        <el-form label-position="right" label-width="80px">
            <!-- <el-form-item label="实例名称">
                {{ instance.title }}
            </el-form-item> -->
            <el-form-item label="策略名称">
                {{ getStrategy() }}
            </el-form-item>
            <el-form-item label="更新时间">
                {{ getLastUpdated() }}
            </el-form-item>            
            <el-form-item label="参数" style="margin-top: 10px;">
                <el-table :border="true" :data="getAlgorithmArgs()" style="width: 100%;">
                    <el-table-column label="名称" prop="name" width="120" />
                    <el-table-column label="描述" prop="desc" width="200" />          
                    <el-table-column label="单位" prop="unit" width="60" />
                    <el-table-column label="数值" width="100">
                        <template slot-scope="{row}">
                            {{ getArgumentValue(row) }}
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>            
            <el-form-item label="结果" style="margin-top: 10px;">
                <el-table max-height="350" :border="true" :data="results" style="width: 100%;">
                    <el-table-column label="代码" prop="code1" width="120">
                        <template slot-scope="{row}">
                            <el-button type="text" size="mini" @click="onCellClick(row.code1)" >{{ row.code1 }}</el-button>    
                        </template>
                    </el-table-column>
                    <el-table-column label="名称" prop="name1" width="120">
                        <template slot-scope="{row}">
                            <el-button type="text" size="mini" @click="onCellClick(row.code1)" >{{ row.name1 }}</el-button>    
                        </template>
                    </el-table-column>                        
                    <el-table-column label="代码" prop="code2" width="120">
                        <template slot-scope="{row}">
                            <el-button type="text" size="mini" @click="onCellClick(row.code2)" >{{ row.code2 }}</el-button>    
                        </template>
                    </el-table-column>                        
                    <el-table-column label="名称" prop="name2" width="120">
                        <template slot-scope="{row}">
                            <el-button type="text" size="mini" @click="onCellClick(row.code2)" >{{ row.name2 }}</el-button>    
                        </template>
                    </el-table-column>                                            
                </el-table>
            </el-form-item>            
        </el-form>
        <div style="text-align:right; margin-top:15px;">
          <el-button type="primary" @click="onOKClick">关闭</el-button>
          <!-- <el-button @click="onCancelClick">取消</el-button> -->
      </div>        
    </el-dialog>
</template>

<script lang="ts">
import { IAlgorithmInfo, IArgumentInfo, IInstanceInfo, IStrategyInfo } from '@/api/def/finder_strategy';
import { Component, Prop, Vue, Watch} from 'vue-property-decorator'

@Component({
    name: 'StrategyResultForm'
})
export default class extends Vue {
    @Prop({ required: true })
    private visibled: boolean = false
    @Prop({ required: true, default: undefined })
    private instance?: IInstanceInfo
    @Prop({ required: true, default: undefined })
    private strategy?: IStrategyInfo

    private results: {
        code1: string,
        name1: string,
        code2?: string,
        name2?: string
    }[] = []

    @Watch('instance')
    onInstanceChanged(newVal: IInstanceInfo, oldVal: IInstanceInfo) {
        this.results = []
        const items: any[] = newVal.result.items
        for (let index = 0; index < items.length; index += 2) {
            this.results.push({
                code1: items[index].code,
                name1: items[index].name,
                code2: items[index+1]?.code,
                name2: items[index+1]?.name,
            })
        }
    }

    private getInstance(): IInstanceInfo | undefined {
        return this.instance
    }

    private getTitle() {
        return this.instance?.title || ''
    }

    private getStrategy() {
        return this.instance?.strategy || ''
    }

    private getLastUpdated() {
        return this.instance?.lastUpdated || ''
    }

    private getAlgorithmArgs(): IArgumentInfo[] | undefined {
        return this.strategy?.algorithm.args
    }

    private getArgumentValue(row: any) {
        return this.instance?.args[row.name]
    }

    private onCellClick(code: string) {
        this.$emit('selected', { symbol: code})           
    }

    private async onOKClick() {
        this.$emit('closed', { code: 0})
    } 
}
</script>
