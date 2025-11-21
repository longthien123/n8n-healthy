import axios from "../utils/AxiosCustom.js";

const getPatient = () => {
  return axios.get(`users/patients/`);
};
const getPatientById = (id) => {
  return axios.get(`users/patients/${id}/`);
};
const editPatient = (data, id) => {
  return axios.put(`users/patients/${id}/update/`, {
    username: data.username,
    email: data.email,
    password: data.password,
    full_name: data.full_name,
    phone: data.phone || "",
    patient_code: data.patient_code,
    date_of_birth: data.date_of_birth,
    gender: data.gender,
    address: data.address,
    blood_type: data.blood_type,
  });
};
const deletePatient = (id) => {
  return axios.delete(`users/patients/${id}/delete/`);
};
export { getPatient, getPatientById, editPatient, deletePatient };
