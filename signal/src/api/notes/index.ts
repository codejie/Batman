import request from '@/axios'
import * as Types from './types'

// Assuming IResponse is a generic wrapper used in the project
// e.g., interface IResponse<T = any> { code: number; message: string; result: T }

export * from './types'

export const apiListNotes = (
  data: Types.ListNotesRequest
): Promise<IResponse<Types.ListNotesResult>> => {
  return request.post({ url: '/notes/list', data })
}

export const apiCreateNote = (
  data: Types.CreateNoteRequest
): Promise<IResponse<Types.CreateNoteResult>> => {
  return request.post({ url: '/notes/create', data })
}

export const apiUpdateNote = (
  data: Types.UpdateNoteRequest
): Promise<IResponse<Types.UpdateNoteResult>> => {
  return request.post({ url: '/notes/update', data })
}

export const apiDeleteNote = (
  data: Types.DeleteNoteRequest
): Promise<IResponse<Types.DeleteNoteResult>> => {
  return request.post({ url: '/notes/delete', data })
}
