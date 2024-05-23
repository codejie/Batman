<template>
    <el-dialog :visible.sync="visibled" title="Input the code..." width="30%">
        <el-form :model="form">
            <el-form-item label="Code:">
                <el-input v-model="form.code" />
            </el-form-item>
        </el-form>
        <template>
            <div style="text-align:right; margin-top: 10px;">
                <el-button @click="onCancel">Cancel</el-button>
                <el-button type="primary" @click="onCreate">Create</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { creatPersonalized } from '@/api/quotes'

@Component({
    name: 'PersonalizedCreateForm'
})

export default class extends Vue {
    @Prop({ required: true})
    private visibled: boolean = false

    private form = { code: ''}

    private async onCreate() {
        const form = this.form
        const { data } = await creatPersonalized({
            code: form.code
        })

        this.$emit('closed', { code: 0 })
    }

    private onCancel() {
        this.$emit('closed', { code: 1 })
    }
}

</script>

<style lang="scss">
</style>