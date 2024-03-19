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

/**
 * 小程序登录
 * @param data 请求参数
 * @returns
 */
/* export const postLoginWxMinAPI = (data: LoginParams) => {
  return http({
    method: 'POST',
    url: '/login/wxMin',
    data,
  })
} */
export const postLoginWxMinAPI = (data: LoginParams) => {
  return http({
    method: 'POST',
    url: '/login',
    data,
  })
}
export const postRegisterWxMinAPI = (data: RegisterParams) => {
  return http({
    method: 'POST',
    url: '/register',
    data,
  })
}
