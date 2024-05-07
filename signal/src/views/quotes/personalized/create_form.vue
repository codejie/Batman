<template>
    <el-dialog :visible.sync="dlgVisable" title="Input the code..." width="45%">
        <el-form :model="form">
            <el-form-item label="Code:">
                <el-input v-model="form.code" />
            </el-form-item>
        </el-form>
        <template>
            <div style="text-align:right; margin-top: 10px;">
                <el-button @click="dlgVisable = false">Cancel</el-button>
                <el-button type="primary" @click="onCreate">Create</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { creatPersonalized } from '@/api/quotes'

@Component({
    name: 'PersonalizedCreateForm'
})

export default class extends Vue {
    private dlgVisable: boolean = false
    private form = { code: ''}

    private async onCreate() {
        const form = this.form
        const { data } = await creatPersonalized({
            code: form.code
        })

        this.dlgVisable = false
        this.$parent.loadPersonalized()
    }

    private init() {
        this.dlgVisable = true        
    }
}

</script>

<style lang="scss">
</style>