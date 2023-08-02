import axios from 'axios'
const instance = axios.create({
  // baseURL: 'https://gonelist.cugxuan.cn/onedrive/',
  timeout: 15000
})

// 添加响应拦截器
axios.interceptors.response.use(
  response => {
    const { data } = response
    console.log(data)
    return data
  },
  err => {
    console.log(err)
  }
)

export default instance
