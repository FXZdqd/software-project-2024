import { http } from '../utils/http'

type createQParams = {
  title: string,
  content: string,
  username: string
}

/**
 * 提问，添加问题
 * @param data 
 * @returns 
 */
export const createQAPI = (data: createQParams) => {
  return http({
    method: 'POST',
    url: '/addQuestion',
    data,
  })
}