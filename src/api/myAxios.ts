import axios from "axios";
import { ElMessage } from "element-plus";

const myAxios = axios.create({
  baseURL: "http://39.109.126.173:39001",
  timeout: 60000,
});

myAxios.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    ElMessage.warning("网络连接异常,请稍后再试");
    return Promise.reject(error);
  }
);
myAxios.interceptors.response.use(
  (response) => {
    if (response.status === 200) {
      if (response.data["msg"] !== "success") {
        ElMessage.success(response.data["msg"]);
      }
      return Promise.resolve(response);
    } else {
      ElMessage.error(response.data["msg"]);
      return Promise.reject(response);
    }
  },
  (error) => {
    const { response } = error;
    if (response) {
      ElMessage.error(response.data["msg"]);
      return Promise.reject(response);
    } else {
      ElMessage.warning("网络连接异常,请稍后再试");
    }
  }
);

export default myAxios;
