import axios from 'axios'
import request from '@/axios'
import { DbExportRequest,  DbImportRequest, DbImportResult } from './types'
import { PATH_URL } from '@/axios/service';

export const apiDbExport = (data: DbExportRequest) => {
  // return request.get({ url: '/system/db/export', data, responseType: 'blob' })

  axios({
    baseURL: PATH_URL,
    url: '/system/db/export',
    method: 'POST',
    responseType: 'blob', // 表示服务器响应的数据类型
    data
  })
  .then((response) => {
    // 尝试从Content-Disposition头中获取文件名
    console.log('response', response)
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'export.zip';
    if (contentDisposition) {
      const matches = contentDisposition.match(/filename="([^"]+)"/);
      if (matches.length === 2) {
        filename = matches[1];
      }
    }
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
  })
  .catch((error) => {
    console.error(error);
  });  
}

export const urlDbImport = `${PATH_URL}/system/db/import`

export const apiDbImport = (data: DbImportRequest): Promise<IResponse<DbImportResult>> => {
  return request.post({ url: '/system/db/import', data })
}