import axios from 'axios'
const instance = axios.create({
  baseURL: 'http://localhost:5002',
  timeout: 15000,
  headers: {
    'Authorization': localStorage.getItem("credential") || null,
  }
})

// 添加响应拦截器
instance.interceptors.response.use(
  response => {
    const { data } = response
    return data
  },
  err => {
    console.log(err)
  }
)

export default instance
