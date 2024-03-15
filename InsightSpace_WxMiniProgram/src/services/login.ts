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
<<<<<<< HEAD
} */
export const postLoginWxMinAPI = (data: LoginParams) => {
  return http({
    method: 'POST',
    url: '/login/',
    data,
  })
}
=======
}
>>>>>>> 65e75a388728ab4a51c493fb81e9c81f00d883b2
