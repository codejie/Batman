import { HistroyRequest, HistroyResult } from "./types"

export const apiHistory = (data: HistroyRequest): Promise<IResponse<HistroyResult>> => {
  // return request.post({ url: '/holding/list', data })
  return Promise.resolve({
    code: 0,
    result: [
      { price: 0 }
    ]
  } as IResponse<HistroyResult>)
}