import { http } from '../utils/http'

/* type LoginParams = {
  code: string
  encryptedData: string
  iv: string
} */
type LoginParams = {
  username: string,
  password: string,
  is_admin: boolean,
}
type RegisterParams = {
  username: string,
  password: string,
  password_re: string,
  phone: number
}
type usernameParams = {
  username: string
}
type setAvatarParams = {
  username: string,
  photo: string
}
type rePwd = {
  username: string,
  old_password: string,
  new_password: string,
  new_password_re: string
}
type reUsernameParams = {
  old_username: string,
  new_username: string
}
type setUserInfoParams = {
  username: string,
  gender: string,
  grade: string,
  department: string
}
type deleteUserParams = {
  username: string,
  password: string
}

/**
 * 小程序登录
 * @param data 请求参数
 * @returns
 */
export const postLoginWxMinAPI = (data: LoginParams) => {
  return http({
    method: 'POST',
    url: '/login',
    data,
  })
}

/**
 * 注册
 * @param data 
 * @returns 
 */
export const postRegisterWxMinAPI = (data: RegisterParams) => {
  return http({
    method: 'POST',
    url: '/register',
    data,
  })
}

export const getAvatarAPI = (data: usernameParams) => {
  return http({
    method: 'POST',
    url: '/getAvatar',
    data,
  })
}

export const setAvatarAPI = (data: setAvatarParams) => {
  return http({
    method: 'POST',
    url: '/setAvatar',
    data,
  })
}

export const getUserProfileAPI = (data: usernameParams) => {

}

export const resetPasswordAPI = (data: rePwd) => {
  return http({
    method: 'POST',
    url: '/resetPassword',
    data,
  })
}

export const reUsernameAPI = (data: reUsernameParams) => {
  return http({
    method: 'POST',
    url: '/resetUsername',
    data,
  })
}

export const getUserAPI = (data: usernameParams) => {
  return http({
    method: 'POST',
    url: '/getUser',
    data,
  })
}

export const setUserInfoAPI = (data: setUserInfoParams) => {
  return http({
    method: 'POST',
    url: '/setUserInfo',
    data,
  })
}

export const deleteUserAPI = (data: usernameParams) => {
  return http({
    method: 'POST',
    url: '/deleteUser',
    data,
  })
}
/**
 * 我的提问
 * @param data 
 * @returns 
 */
export const getQuestionAskedByUserAPI = (data: usernameParams) => {
  return http({
    method: 'POST',
    url: '/getQuestionAskedByUser',
    data,
  })
}

/**
 * 我的回答
 * @param data 
 * @returns 
 */
export const getQuestionAnsweredByUserAPI = (data: usernameParams) => {
  return http({
    method: 'POST',
    url: '/getQuestionAnsweredByUser',
    data,
  })
}