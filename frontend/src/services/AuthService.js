import axios from "../utils/AxiosCustom.js";
const postLogin = (userName, password) => {  
  return axios.post(`users/login/`, {
    username: userName,
    password: password,
  });
};
export {
    postLogin,
}