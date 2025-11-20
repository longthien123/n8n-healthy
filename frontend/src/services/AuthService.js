import axios from "../utils/AxiosCustom.js";
const postLogin = (userName, password) => {  
  return axios.post(`login/`, {
    username: userName,
    password: password,
  });
};
export {
    postLogin,
}