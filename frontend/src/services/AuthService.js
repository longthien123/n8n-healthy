import axios from "../utils/AxiosCustom.js";
const postLogin = (userName, password) => {  
  return axios.post(`users/login/`, {
    username: userName,
    password: password,
  });
};
const register = (dataAuth) => {
  return axios.post(`users/create/`, {
    username: dataAuth.userName,
    email: dataAuth.email,
    password: dataAuth.password,
    password_confirm: dataAuth.password_confirm,
    full_name: dataAuth.full_name,
    phone: dataAuth.phone,
    role: dataAuth.role
  })
}
const patientRegister = (data) => {
  return axios.post(`users/patients/create/`, {
    username: data.userName,
    email: data.email,
    password: data.password,
    full_name: data.full_name,
    phone: data.phone,
    date_of_birth: data.date_of_birth,
    gender: data.gender,
    address: data.address,
    blood_type: data.blood_type,
    patient_code: "PN" + Math.floor(100000 + Math.random() * 900000)
  })
}
export {
    postLogin,
    register,
    patientRegister
}