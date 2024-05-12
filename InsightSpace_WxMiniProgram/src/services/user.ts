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
type setAvatarParams = {
  username: string
}
type rePwd = {
  username: string,
  new_password: string,
  new_password_re:string
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

export const getAvatarAPI = (data: setAvatarParams) => {
  return http({
    method: 'POST',
    url: '/getAvatar',
    data,
  })
}

export const setAvatarAPI = () => {

}

export const getUserProfileAPI = (data: setAvatarParams)=>{

}

export const resetPasswordAPI = (data: rePwd)=>{
  return http({
    method: 'POST',
    url: '/resetPassword',
    data,
  })
}