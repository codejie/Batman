<script lang="ts">
interface CreateForm {
  type: string
  title: string
  code: string
}

interface UpdateTargetForm {
  id: number
  target: number
}

interface Item {
  record: RecordsItem
  calc?: CustomizedCalcItem
}
</script>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  ElDialog,
  ElText,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElTable,
  ElTableColumn,
  ElMessageBox,
  ElSelect,
  ElOption,
  ElMessage,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
  ElCheckbox
} from 'element-plus'
import { apiCreate, apiRecords, RecordsItem, apiRemove, apiUpdateTarget } from '@/api/customized'
import { apiGetName, apiGetSpotData, TYPE_INDEX, TYPE_STOCK, apiGetItemInfo } from '@/api/data'
import { ContentWrap } from '@/components/ContentWrap'
import { calcCustomizedData, CustomizedCalcItem } from '@/calc/customized'
import { KLineDialog } from '@/components/KLine'
import { HoldingRecordItem } from '@/api/holding'
import { useWebSocket, UseWebSocketOptions } from '@vueuse/core'
import { useUserStoreWithOut } from '@/store/modules/user'
import { formatNumberString } from '@/utils/fmtUtil'
import { PATH_URL } from '@/axios/service'
import ItemSearchDialog from '@/views/Common/components/ItemSearchDialog.vue'

const connected = ref<boolean>(false)

function onConnected(ws: WebSocket) {
  connected.value = true
  ElMessage.success('连接成功')
}

function onDisconnected(ws: WebSocket) {
  connected.value = false
  ElMessage.error('连接关闭')
}

function onError(ws: WebSocket, event: Event) {
  ElMessage.error('连接异常')
}

function onMessage(ws: WebSocket, event: MessageEvent) {
  onWebSocketData(JSON.parse(event.data))
}

const opts: UseWebSocketOptions = {
  autoConnect: false,
  immediate: false,
  autoClose: true,
  autoReconnect: false,
  onConnected: onConnected,
  onDisconnected: onDisconnected,
  onError: onError,
  onMessage: onMessage
}
const WS_URL_SPOT_DATA = `ws://${PATH_URL}/services/ws/spot_data?token=${useUserStoreWithOut().getTokenKey}`
const { open, close } = useWebSocket(WS_URL_SPOT_DATA, opts)

const createDialogVisible = ref<boolean>(false)
const createForm = ref<CreateForm>({
  type: '股票',
  title: '',
  code: ''
})
const updateTargetDialogVisible = ref<boolean>(false)
const updateTargetForm = ref<UpdateTargetForm>({
  id: 0,
  target: 0
})
const itemSearchDialogVisible = ref<boolean>(false)

function onSearchChanged(target: 'create') {
  const form = createForm.value
  form.code = ''
}
async function searchItem(key: string, target: 'create') {
  if (key) {
    const form = createForm.value
    const type = form.type == '股票' ? TYPE_STOCK : TYPE_INDEX
    const ret = await apiGetItemInfo({
      type: type,
      key: key
    })
    if (ret.result) {
      form.title = `${ret.result.name}/${ret.result.code}`
      form.code = ret.result.code
    } else {
      ElMessage.warning('Not Found')
    }
  }
}

const data = ref<Item[]>([])
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})
const fetchTime = ref<string>()
const useHistory = ref<boolean>(true)

function onWebSocketData(wd: any) {
  const records: RecordsItem[] = data.value.map((item) => item.record)
  data.value = []

  for (const record of records) {
    if (record.type === TYPE_STOCK) {
      const stock = wd.stocks.find((s: any) => s.代码 === record.code)
      if (stock) {
        data.value.push({
          record: record,
          calc: calcCustomizedData(stock)
        })
      }
    } else if (record.type === TYPE_INDEX) {
      const index = wd.indexes.find((s: any) => s.代码 === record.code)
      if (index) {
        data.value.push({
          record: record,
          calc: calcCustomizedData(index)
        })
      }
    }
  }

  fetchTime.value = wd.index
}

async function fetchData() {
  const ret = await apiRecords({})
  data.value = []
  for (const item of ret.result) {
    data.value.push({
      record: item,
      calc: undefined
    })
  }
}

async function fetchStockData() {
  for (const item of data.value) {
    item.calc = undefined
  }

  const stocks = data.value
    .filter((item) => item.record.type === TYPE_STOCK)
    .map((item) => item.record.code)
  if (stocks.length > 0) {
    const stockRet = await apiGetSpotData({
      type: TYPE_STOCK,
      codes: stocks,
      useHistory: useHistory.value
    })
    for (const item of stockRet.result) {
      const dataItem = data.value.find(
        (i) => i.record.type === TYPE_STOCK && i.record.code === item.代码
      )
      if (dataItem) {
        dataItem.calc = calcCustomizedData(item)
      }
    }
  }
  const indexes = data.value
    .filter((item) => item.record.type === TYPE_INDEX)
    .map((item) => item.record.code)
  if (indexes.length > 0) {
    const indexRet = await apiGetSpotData({
      type: TYPE_INDEX,
      codes: indexes,
      useHistory: useHistory.value
    })
    for (const item of indexRet.result) {
      const dataItem = data.value.find(
        (i) => i.record.type === TYPE_INDEX && i.record.code === item.代码
      )
      if (dataItem) {
        dataItem.calc = calcCustomizedData(item)
      }
    }
  }

  const now = new Date()
  fetchTime.value = `${now?.getHours()}:${now.getMinutes()}:${now.getSeconds()}`
}

async function fetch() {
  await fetchData()
  await fetchStockData()
}

async function onAdd() {
  await apiCreate({
    type: createForm.value.type == '股票' ? TYPE_STOCK : TYPE_INDEX,
    code: createForm.value.code
  })
  createDialogVisible.value = false
  await fetch()
}

function onQuickViewConfirm(item: any) {
  reqParam.value = {
    code: item.code,
    name: item.name,
    type: item.type
  }
  klineDialogVisible.value = true
}

async function onRemove(id: number) {
  const confirm = await ElMessageBox.confirm('是否确认删除?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
  if (confirm) {
    await apiRemove({
      id: id
    })
    data.value = data.value.filter((item) => item.record.id !== id)
    await fetchStockData()
  }
}

function onRecordClick(row: HoldingRecordItem) {
  reqParam.value = {
    code: row.code,
    name: row.name,
    type: row.type
  }
  klineDialogVisible.value = true
}

function onTarget(id: number) {
  updateTargetForm.value.id = id
  updateTargetDialogVisible.value = true
}
async function submitUpdateTarget() {
  updateTargetDialogVisible.value = false
  await apiUpdateTarget({
    id: updateTargetForm.value.id,
    target: updateTargetForm.value.target
  })
  await fetch()
}

onMounted(async () => {
  await fetch()
})

async function onWebSocketClick() {
  if (connected.value) {
    await close()
  } else {
    await open()
  }
}
</script>

<template>
  <ContentWrap>
    <div class="my-4">
      <ElButton type="primary" @click="createDialogVisible = true">增加自选</ElButton>
      <ElButton @click="itemSearchDialogVisible = true">快速查看</ElButton>
      <ElCheckbox v-model="useHistory" style="margin-left: 16px" label="使用历史数据接口" />
      <ElDropdown
        style="float: right"
        :split-button="true"
        type="primary"
        @click="fetchStockData()"
      >
        刷新{{ connected ? ' - On' : '' }}
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem @click="onWebSocketClick">{{
              connected ? 'WebSocket Off' : 'WebSocket On'
            }}</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>
      <ElText tag="b" style="float: right; margin-top: 4px; margin-right: 16px">{{
        fetchTime
      }}</ElText>
    </div>
    <div>
      <ElTable
        :data="data"
        :border="true"
        stripe
        :default-sort="{ prop: 'record.updated', order: 'descending' }"
      >
        <ElTableColumn type="index" width="40" />
        <ElTableColumn prop="record.holding" label="持有" width="60">
          <template #header>
            <ElText>持有</ElText>
          </template>
          <template #default="{ row }">
            {{ row.record.holding ? '是' : '否' }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="record.code" label="名称/代码" min-width="90">
          <template #header>
            <div><ElText>名称/代码</ElText></div>
          </template>
          <template #default="{ row }">
            <div @click="onRecordClick(row.record)">
              <div
                ><ElText>{{ row.record.name }}/{{ row.record.code }}</ElText></div
              >
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="120">
          <template #header>
            <div><ElText>最新价/目标价/差值</ElText></div>
          </template>
          <template #default="{ row }">
            <div>
              <ElText>{{ formatNumberString(row.calc?.最新价) }}</ElText>
              <ElText v-if="row.record.target">
                / {{ formatNumberString(row.record.target) }}</ElText
              >
              <ElText
                v-if="row.record.target"
                :class="row.calc?.最新价 - row.record.target >= 0 ? 'red-text' : 'green-text'"
              >
                / {{ formatNumberString(row.calc?.最新价 - row.record.target) }}</ElText
              >
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="100">
          <template #header>
            <div><ElText>昨收/今开</ElText></div>
          </template>
          <template #default="{ row }">
            <div
              ><ElText
                >{{ formatNumberString(row.calc?.昨收) }} /
                {{ formatNumberString(row.calc?.今开) }}</ElText
              ></div
            >
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="150">
          <template #header>
            <div><ElText>最高价/最低价/差值</ElText></div>
          </template>
          <template #default="{ row }">
            <div>
              <ElText
                >{{ formatNumberString(row.calc?.最高) }} /
                {{ formatNumberString(row.calc?.最低) }}</ElText
              >
              <ElText> / {{ formatNumberString(row.calc?.涨跌额) }}</ElText>
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="100">
          <template #header>
            <div><ElText>涨跌幅/振幅</ElText></div>
          </template>
          <template #default="{ row }">
            <div
              ><ElText :class="row.calc?.涨跌幅 >= 0 ? 'red-text' : 'green-text'"
                >{{ formatNumberString(row.calc?.涨跌幅) }}% /
                {{ formatNumberString(row.calc?.振幅) }}%</ElText
              ></div
            >
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="100">
          <template #header>
            <div><ElText>量比/换手率</ElText></div>
          </template>
          <template #default="{ row }">
            <div v-if="row.record.type == TYPE_STOCK"
              ><ElText
                >{{ formatNumberString(row.calc?.量比) }} /
                {{ formatNumberString(row.calc?.换手率) }}%</ElText
              ></div
            >
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="100">
          <template #header>
            <div><ElText>5分钟涨跌/涨速</ElText></div>
          </template>
          <template #default="{ row }">
            <div v-if="row.record.type == TYPE_STOCK"
              ><ElText
                >{{ formatNumberString(row.calc?.涨跌5分钟) }} /
                {{ formatNumberString(row.calc?.涨速) }}</ElText
              ></div
            >
          </template>
        </ElTableColumn>
        <ElTableColumn min-width="120">
          <template #header>
            <div><ElText>60日/年初至今涨跌幅</ElText></div>
          </template>
          <template #default="{ row }">
            <div v-if="row.record.type == TYPE_STOCK"
              ><ElText
                >{{ formatNumberString(row.calc?.涨跌幅60日) }}% /
                {{ formatNumberString(row.calc?.年初至今涨跌幅) }}%</ElText
              ></div
            >
          </template>
        </ElTableColumn>
        <ElTableColumn prop="action" label="操作" min-width="140">
          <template #header>
            <ElText>操作</ElText>
          </template>
          <template #default="{ row }">
            <ElButton @click="onTarget(row.record.id)">设置目标价</ElButton>
            <ElButton @click="onRemove(row.record.id)">删除</ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </div>
    <ElDialog v-model="createDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">新增自选..</ElText>
      </template>
      <template #default>
        <ElForm :model="createForm" label-position="right" label-width="auto">
          <ElFormItem label="类型">
            <ElSelect v-model="createForm.type">
              <ElOption label="股票" value="股票" />
              <ElOption label="指数" value="指数" />
            </ElSelect>
          </ElFormItem>
          <ElFormItem label="名称/代码">
            <ElInput
              v-model="createForm.title"
              placeholder="请输入代码或名称"
              :maxlength="6"
              @change="onSearchChanged('create')"
            >
              <template #append>
                <ElButton
                  :disabled="createForm.title === ''"
                  @click="searchItem(createForm.title, 'create')"
                  >搜索</ElButton
                >
              </template>
            </ElInput>
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="createDialogVisible = false">取消</ElButton>
        <ElButton type="primary" :disabled="createForm.code === ''" @click="onAdd">确定</ElButton>
      </template>
    </ElDialog>
    <ItemSearchDialog v-model:visible="itemSearchDialogVisible" @confirm="onQuickViewConfirm" />
    <ElDialog v-model="updateTargetDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText>设置目标价格</ElText>
      </template>
      <template #default>
        <ElForm :model="updateTargetForm" label-position="right" label-width="auto">
          <ElFormItem label="目标价格">
            <ElInput v-model="updateTargetForm.target" type="number">
              <template #append>元</template>
            </ElInput>
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="updateTargetDialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="submitUpdateTarget">确定</ElButton>
      </template>
    </ElDialog>
    <KLineDialog
      :visible="klineDialogVisible"
      :req-param="reqParam"
      @update:on-close="klineDialogVisible = false"
      width="60%"
    />
  </ContentWrap>
</template>
<style lang="css" scoped>
.green-text {
  color: green;
}

.red-text {
  color: red;
}
</style>
