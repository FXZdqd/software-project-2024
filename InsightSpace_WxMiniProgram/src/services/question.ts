import { http } from '../utils/http'

type createQParams = {
  title: string
  content: string
  username: string
  tags: []
}
type qidParams = {
  q_id: number
  username: string
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
type followParams = {
  username: string
  q_id: number
}
type addVParams = {
  q_id: number
}
type likeQParams = {
  q_id: number
  username: string
}

type likeAParams = {
  a_id: number
  username: string
}
type reportQParams = {
  q_id: number
}
type reportAParams = {
  a_id: number
}
type usernameParams = {
  username: string
}
type answerParams = {
  q_id: number
  username: string
  content: string
}
type delQParams = {
  q_id: number
}
type delAParams = {
  a_id: number
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
export const followAPI = (data: likeQParams) => {
  return http({
    method: 'POST',
    url: '/follow',
    data,
  })
}
export const addVAPI = (data: addVParams) => {
  return http({
    method: 'POST',
    url: '/viewQuestion',
    data,
  })
}
export const likeQAPI = (data: likeQParams) => {
  return http({
    method: 'POST',
    url: '/likeQuestion',
    data,
  })
}
export const unlikeQAPI = (data: likeQParams) => {
  return http({
    method: 'POST',
    url: '/unlikeQuestion',
    data,
  })
}
export const unfollowAPI = (data: likeQParams) => {
  return http({
    method: 'POST',
    url: '/unfollow',
    data,
  })
}
export const likeAAPI = (data: likeAParams) => {
  return http({
    method: 'POST',
    url: '/likeAnswer',
    data,
  })
}
export const unlikeAAPI = (data: likeAParams) => {
  return http({
    method: 'POST',
    url: '/unlikeAnswer',
    data,
  })
}
export const reportQAPI = (data: reportQParams) => {
  return http({
    method: 'POST',
    url: '/reportQuestion',
    data,
  })
}
export const reportAAPI = (data: reportAParams) => {
  return http({
    method: 'POST',
    url: '/reportAnswer',
    data,
  })
}
export const getFollowQAPI = (data: usernameParams) => {
  return http({
    method: 'POST',
    url: '/user_follow',
    data,
  })
}
export const goAnswerAPI = (data: answerParams) => {
  return http({
    method: 'POST',
    url: '/goAnswer',
    data,
  })
}
export const delQAPI = (data: delQParams) => {
  return http({
    method: 'POST',
    url: '/delQuestion',
    data,
  })
}
export const delAAPI = (data: delAParams) => {
  return http({
    method: 'POST',
    url: '/delAnswer',
    data,
  })
}
