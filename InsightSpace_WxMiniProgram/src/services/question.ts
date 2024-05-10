import { http } from '../utils/http'

type createQParams = {
  title: string
  content: string
  username: string
}
type qidParams = {
  q_id: number
}
type tagParams = {
  tag_name: string
  sort_questions_by: string
  sort_questions_order: string
  sort_answers_by: string
  sort_answers_order: string
}
type keyParams = {
  keyword: string
  sort_questions_by: string
  sort_questions_order: string
  sort_answers_by: string
  sort_answers_order: string
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
export const getTAGQAPI = (data: tagParams) => {
  return http({
    method: 'POST',
    url: '/getQuestionByTag',
    data,
  })
}
export const getKeywordQAPI = (data: keyParams) => {
  return http({
    method: 'POST',
    url: '/getQuestionByKeyword',
    data,
  })
}