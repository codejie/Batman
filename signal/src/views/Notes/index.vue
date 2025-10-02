<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import { ContentWrap } from '@/components/ContentWrap'
import {
  ElRow,
  ElCol,
  ElInput,
  ElSelect,
  ElOption,
  ElCard,
  ElTag,
  ElButton,
  ElDialog,
  ElMessage,
  ElMessageBox
} from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  type NoteItem,
  apiListNotes,
  apiCreateNote,
  apiUpdateNote,
  apiDeleteNote
} from '@/api/notes'

const notes = ref<NoteItem[]>([])
const vditor = ref<Vditor | null>(null)
const searchQuery = ref('')
const filterType = ref('title') // 'title' or 'tags'
const selectedNote = ref<NoteItem | null>(null)
const dialogVisible = ref(false)
const newTagName = ref('')
const isVditorEditable = ref(false)

const filteredNotes = computed(() => {
  if (!searchQuery.value) {
    return notes.value
  }
  return notes.value.filter((note) => {
    const query = searchQuery.value.toLowerCase()
    if (filterType.value === 'title') {
      return note.title.toLowerCase().includes(query)
    } else {
      return note.tags.some((tag) => tag.toLowerCase().includes(query))
    }
  })
})

const getNotesList = async () => {
  try {
    const res = await apiListNotes({})
    notes.value = res.result
    if (notes.value.length > 0) {
      selectNote(notes.value[0])
      isVditorEditable.value = true
      vditor.value?.enable()
    } else {
      selectedNote.value = null
      vditor.value?.setValue('# 韭菜笔记\n\n请在左侧选择或创建一篇笔记。')
      isVditorEditable.value = false
      vditor.value?.disabled()
    }
  } catch (error) {
    ElMessage.error('获取笔记列表失败')
  }
}

const selectNote = (note: NoteItem) => {
  selectedNote.value = note
  vditor.value?.setValue(note.content)
  isVditorEditable.value = true // Enable editor when a note is selected
  vditor.value?.enable()
}

const extractTitleFromContent = (content: string): string => {
  if (!content) {
    return '未命名笔记'
  }
  const firstLine = content.split('\n')[0].trim()
  // Remove leading '#' characters and then strip whitespace
  const title = firstLine.replace(/^#+\s*/, '').trim()
  if (!title) {
    return '未命名笔记'
  }
  return title
}

const createNewNote = () => {
  selectedNote.value = {
    id: undefined,
    title: '未命名笔记',
    tags: [],
    content: '# 新笔记',
    updated: new Date()
  }
  vditor.value?.setValue(selectedNote.value.content)
  isVditorEditable.value = true // Enable editor for new note
  vditor.value?.enable()
}

const saveNote = async () => {
  if (!selectedNote.value) {
    ElMessage.warning('没有选中的笔记')
    return
  }

  try {
    const currentContent = vditor.value?.getValue() || ''
    const noteToSave: NoteItem = {
      ...selectedNote.value,
      content: currentContent,
      title: extractTitleFromContent(currentContent) // Extract title from content
    }

    if (!noteToSave.id) {
      // Create new note
      await apiCreateNote(noteToSave)
      ElMessage.success('创建成功')
    } else {
      // Update existing note
      await apiUpdateNote(noteToSave)
      ElMessage.success('保存成功')
    }
    await getNotesList() // Refresh to get new ID/timestamp and data
  } catch (error) {
    ElMessage.error('保存笔记失败')
  }
}

const deleteNote = async () => {
  if (!selectedNote.value || !selectedNote.value.id) {
    ElMessage.warning('没有选中的笔记')
    return
  }
  try {
    await ElMessageBox.confirm('确定要删除这篇笔记吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await apiDeleteNote({ id: selectedNote.value.id })
    ElMessage.success('删除成功')
    await getNotesList()
  } catch (error) {
    // If error is 'cancel', it means user clicked cancel button
    if (error !== 'cancel') {
      ElMessage.error('删除笔记失败')
    }
  }
}

const handleTagClose = (tag: string) => {
  if (selectedNote.value) {
    selectedNote.value.tags = selectedNote.value.tags.filter((t) => t !== tag)
    // saveNote() will be called by the '保存' button
  }
}

const addNewTag = () => {
  if (!selectedNote.value || !isVditorEditable.value) {
    ElMessage.warning('请先选择或创建一篇可编辑的笔记')
    return
  }
  newTagName.value = ''
  dialogVisible.value = true
}

const confirmAddNewTag = () => {
  const newTag = newTagName.value.trim()
  if (newTag && selectedNote.value && !selectedNote.value.tags.includes(newTag)) {
    selectedNote.value.tags.push(newTag)
    // saveNote() will be called by the '保存' button
  }
  dialogVisible.value = false
}

onMounted(() => {
  vditor.value = new Vditor('vditor', {
    height: '100%',
    minHeight: 400,
    preview: {
      maxWidth: 10000
    },
    after: () => {
      getNotesList()
    }
  })
})
</script>

<template>
  <ContentWrap title="韭菜笔记">
    <ElRow :gutter="24">
      <!-- Left Column -->
      <ElCol :span="6">
        <ElCard shadow="never" class="left-panel">
          <!-- Search Area -->
          <div class="search-area">
            <ElRow :gutter="10">
              <ElCol :span="16">
                <ElInput v-model="searchQuery" placeholder="检索笔记..." clearable />
              </ElCol>
              <ElCol :span="8">
                <ElSelect v-model="filterType">
                  <ElOption label="标题" value="title" />
                  <ElOption label="标签" value="tags" />
                </ElSelect>
              </ElCol>
            </ElRow>
          </div>

          <!-- Notes List -->
          <div class="notes-list">
            <div
              v-for="note in filteredNotes"
              :key="note.id"
              class="note-item"
              :class="{ active: selectedNote?.id === note.id }"
              @click="selectNote(note)"
            >
              <div class="note-title">
                <span class="title-text">{{ note.title }}</span>
                <span class="note-date">{{ new Date(note.updated).toLocaleDateString() }}</span>
              </div>
              <div class="note-tags">
                <ElTag v-for="tag in note.tags" :key="tag" size="small" type="info">{{ tag }}</ElTag>
              </div>
            </div>
          </div>
        </ElCard>
      </ElCol>

      <!-- Right Column -->
      <ElCol :span="18">
        <ElCard shadow="never" class="right-panel vditor-card">
          <!-- Action Bar -->
          <div class="action-bar">
            <ElButton type="primary" @click="saveNote" :disabled="!isVditorEditable">保存</ElButton>
            <div class="tags-display" v-if="selectedNote">
              <ElTag
                v-for="tag in selectedNote.tags"
                :key="tag"
                effect="plain"
                class="ml-10px"
                closable
                @close="handleTagClose(tag)"
              >
                {{ tag }}
              </ElTag>
              <ElButton
                :icon="Plus"
                circle
                size="small"
                @click="addNewTag"
                class="ml-10px"
                :disabled="!isVditorEditable"
              />
            </div>
            <div style="flex-grow: 1;"></div>
            <ElButton @click="createNewNote">新建</ElButton>
            <ElButton type="danger" @click="deleteNote" :disabled="!selectedNote?.id">删除</ElButton>
          </div>
          <!-- Vditor Editor -->
          <div id="vditor" />
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- Add Tag Dialog -->
    <ElDialog v-model="dialogVisible" title="添加新标签" width="30%">
      <ElInput v-model="newTagName" placeholder="请输入标签名称" @keyup.enter="confirmAddNewTag" />
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="confirmAddNewTag">确认</ElButton>
        </span>
      </template>
    </ElDialog>
  </ContentWrap>
</template>

<style scoped>
.left-panel,
.right-panel {
  height: calc(100vh - 200px);
}

.left-panel > :deep(.el-card__body) {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.right-panel.vditor-card > :deep(.el-card__body) {
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.search-area {
  padding-bottom: 15px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.notes-list {
  flex: 1;
  overflow-y: auto;
  margin-top: 15px;
}

.note-item {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.note-item:hover {
  background-color: var(--el-color-primary-light-9);
}

.note-item.active {
  background-color: var(--el-color-primary-light-8);
}

.note-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* margin-bottom: 5px; */
  width: 100%;
}

.title-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 16px;
  /* font-weight: 500; */
}

.note-date {
  font-size: 12px;
  color: #999;
  flex-shrink: 0;
  margin-left: 10px;
}

.note-tags .el-tag {
  margin-right: 5px;
}

.action-bar {
  display: flex;
  align-items: center;
  padding: 10px 20px 15px 20px;
  margin-bottom: 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

#vditor {
  flex: 1;
  border: none;
}
</style>
