export interface NoteItem {
  id?: number
  title: string
  tags: string[]
  content: string
  updated?: Date
  created?: Date
}

// Requests and Results
export interface ListNotesRequest {}
export type ListNotesResult = NoteItem[]

export interface CreateNoteRequest {
  title: string
  tags: string[]
  content: string
}
export type CreateNoteResult = number

export interface UpdateNoteRequest {
  id: number
  title: string
  tags: string[]
  content: string
}
export type UpdateNoteResult = number

export interface DeleteNoteRequest {
  id: number
}
export type DeleteNoteResult = number
