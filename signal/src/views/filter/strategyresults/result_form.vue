<template>
    <el-dialog :title="instance.title" :visible="visibled" width="40%">
        <el-form label-position="right" label-width="80px">
            <!-- <el-form-item label="实例名称">
                {{ instance.title }}
            </el-form-item> -->
            <el-form-item label="策略名称">
                {{ instance.strategy }}
            </el-form-item>
            <el-form-item label="参数" style="margin-top: 15px;">
                <el-table :border="true" :data="strategy.algorithm.args">
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
            <el-form-item>
                <el-table :border="true" :data="instance.result.items">
                    <el-table-column label="代码" prop="code" width="120" />
                    <el-table-column label="名称" prop="name" width="120" />
                </el-table>
            </el-form-item>            
        </el-form>
        <div style="text-align:right; margin-top:15px;">
          <el-button type="primary" @click="onOKClick">确认</el-button>
          <el-button @click="onCancelClick">取消</el-button>
      </div>        
    </el-dialog>
</template>

<script lang="ts">
import { IInstanceInfo, IStrategyInfo } from '@/api/def/finder_strategy';
import { Component, Prop, Vue, Watch} from 'vue-property-decorator'

@Component({
    name: 'StrategyResultForm'
})
export default class extends Vue {
    @Prop({ required: true })
    private visibled: boolean = false
    @Prop({ required: true })
    private instance?: IInstanceInfo
    @Prop({ required: true })
    private strategy?: IStrategyInfo

    @Watch('instance')
    onInstanceChanged(newVal: IInstanceInfo, oldVal: IInstanceInfo) {
        // console.log('instance changed')
        // console.log(newVal)
    }

    private getArgumentValue(row: any) {
        return this.instance?.args[row.name]
    }
    private async onOKClick() {

    this.$emit('closed', { code: 0})
  }

  private onCancelClick() {
    this.$emit('closed', { code: -1})
  }    
}
</script>
