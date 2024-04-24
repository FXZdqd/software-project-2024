import { http } from '../utils/http'

type createQParams = {
  title: string
  content: string
  username: string
}
type qidParams = {
  q_id: number
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
export const getAllQAPI = () => {
  return http({
    method: 'POST',
    url: '/getAllQuestion',
  })
}
export const getQAPI = (data: qidParams) => {
  return http({
    method: 'POST',
    url: '/getQuestion',
    data,
  })
}
