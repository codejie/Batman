<template>
    <el-dialog :visable.sync="visabled" width="40%" @opened="onOpened">
    </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue} from 'vue-property-decorator'

@Component({
    name: 'TriggerEditForm'
})
export default class extends Vue {
    @Prop({ required: true })
    private visabled: boolean = false
    
    private onOpened() {

    }
}
</script>

<style lang="scss">
</style>