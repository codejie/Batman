<template>
    <el-card>
        <div slot="header">
            <span>{{ code }}</span>
        </div>
        <div>
            other info
        </div>
    </el-card>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from 'vue-property-decorator'

@Component({
    name: 'StockInfoPanel'
})
export default class extends Vue {
    @Prop({required: true})
    private symbol?: string

    private code: string = '000001'

    @Watch('symbol')
    onSymbolChanged(newVal: string, oldVal: string) {
        this.code = this.symbol || '000001'
    }

    private fetchInfo(code: string) {

    }

    private fetchHistory() {
        
    }
}
</script>

<style lang="scss" scoped>
</style>