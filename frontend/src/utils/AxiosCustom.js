import axios from "axios";
import nProgress from "nprogress";
const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/users/',
    // timeout: 1000,
    // headers: {'X-Custom-Header': 'foobar'}
});
instance.interceptors.request.use(function (config) {
  //lấy ra access token từ redux
//   const access_token = store?.getState()?.user?.account?.access_token
//   if (!config.url.includes("/auth/login")) {
//     config.headers['Authorization'] = "Bearer " + access_token;
//   }
// const access_token = sessionStorage.getItem("access_token");

// if (!config.url?.includes("/auth/login") && access_token) {
//   config.headers["Authorization"] = "Bearer " + access_token;
// }
  //trc khi gửi request đi thì bật thanh loading
  nProgress.start();
    // Do something before request is sent
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });

// Add a response interceptor
instance.interceptors.response.use(function (response) {
  nProgress.done();
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response && response.data ? response.data : response;
  }, function (error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    return Promise.reject(error);
  });
export default instance;