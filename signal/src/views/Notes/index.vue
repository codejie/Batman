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
const selectedNote = ref<NoteItem | null>(null) // For highlighting in the list
const editingNote = ref<NoteItem | null>(null) // For the editor's content and tags
const dialogVisible = ref(false)
const newTagName = ref('')
const isVditorEditable = ref(false)
const hasUnsavedChanges = ref(false)

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

const confirmSaveAndProceed = async (): Promise<boolean> => {
  if (!hasUnsavedChanges.value) {
    return true // No unsaved changes, proceed
  }
  try {
    await ElMessageBox.confirm('当前笔记有未保存的修改，是否保存？', '提示', {
      confirmButtonText: '保存',
      cancelButtonText: '不保存',
      distinguishCancelAndClose: true,
      type: 'warning'
    })
    // User clicked '保存'
    await saveNote()
    return true
  } catch (action) {
    if (action === 'cancel') {
      // User clicked '不保存'
      return true
    }
    // User clicked close button or other error
    return false
  }
}

const getNotesList = async () => {
  try {
    const res = await apiListNotes({})
    notes.value = res.result
    if (notes.value.length > 0) {
      // Select the first note if available
      // This will also set editingNote, vditor content, and enable editor
      selectNote(notes.value[0])
    } else {
      selectedNote.value = null
      editingNote.value = null
      vditor.value?.setValue('# 韭菜笔记\n\n请在左侧选择或创建一篇笔记。')
      isVditorEditable.value = false
      vditor.value?.disabled()
    }
    hasUnsavedChanges.value = false // No unsaved changes after loading list
  } catch (error) {
    ElMessage.error('获取笔记列表失败')
  }
}

const selectNote = async (note: NoteItem) => {
  if (selectedNote.value?.id === note.id) {
    return // Already selected
  }
  const proceed = await confirmSaveAndProceed()
  if (!proceed) {
    return // User cancelled or error during save
  }

  selectedNote.value = note // Highlight in the list
  editingNote.value = JSON.parse(JSON.stringify(note)) // Deep copy for editing
  vditor.value?.setValue(editingNote.value!.content)
  isVditorEditable.value = true // Enable editor when a note is selected
  vditor.value?.enable()
  hasUnsavedChanges.value = false // Reset unsaved changes flag
}

const extractTitleFromContent = (content: string): string => {  if (!content) {
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

const createNewNote = async () => {
  const proceed = await confirmSaveAndProceed()
  if (!proceed) {
    return // User cancelled or error during save
  }

  selectedNote.value = null // No item highlighted in the list
  editingNote.value = {
    id: undefined,
    title: '未命名笔记',
    tags: [],
    content: '# 新笔记',
    updated: new Date()
  }
  vditor.value?.setValue(editingNote.value.content)
  isVditorEditable.value = true // Enable editor for new note
  vditor.value?.enable()
  hasUnsavedChanges.value = false // Reset unsaved changes flag
}

const saveNote = async () => {
  if (!editingNote.value) {
    ElMessage.warning('没有可保存的笔记')
    return
  }

  try {
    const currentContent = vditor.value?.getValue() || ''
    editingNote.value.content = currentContent
    editingNote.value.title = extractTitleFromContent(currentContent) // Extract title from content

    if (!editingNote.value.id) {
      // Create new note
      await apiCreateNote(editingNote.value)
      ElMessage.success('创建成功')
    } else {
      // Update existing note
      await apiUpdateNote({
        id: editingNote.value.id,
        title: editingNote.value.title,
        tags: editingNote.value.tags,
        content: editingNote.value.content
      })
      ElMessage.success('保存成功')
    }
    hasUnsavedChanges.value = false // Reset unsaved changes flag after successful save
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
    hasUnsavedChanges.value = false // Reset unsaved changes flag after successful delete
  } catch (error) {
    // If error is 'cancel', it means user clicked cancel button
    if (error !== 'cancel') {
      ElMessage.error('删除笔记失败')
    }
  }
}

const handleTagClose = (tag: string) => {
  if (editingNote.value) {
    editingNote.value.tags = editingNote.value.tags.filter((t) => t !== tag)
    hasUnsavedChanges.value = true // Mark as unsaved
  }
}

const addNewTag = () => {
  if (!editingNote.value || !isVditorEditable.value) {
    ElMessage.warning('请先选择或创建一篇可编辑的笔记')
    return
  }
  newTagName.value = ''
  dialogVisible.value = true
}

const confirmAddNewTag = () => {
  const newTag = newTagName.value.trim()
  if (newTag && editingNote.value && !editingNote.value.tags.includes(newTag)) {
    editingNote.value.tags.push(newTag)
    hasUnsavedChanges.value = true // Mark as unsaved
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
    input: () => {
      hasUnsavedChanges.value = true
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
                <span class="note-date">{{ note.updated?.toLocaleDateString() }}</span>
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
            <div class="tags-display" v-if="editingNote">
              <ElTag
                v-for="tag in editingNote.tags"
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
