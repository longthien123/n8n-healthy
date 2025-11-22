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
const getPatientIdByUserId = (id) => {
    return axios.get(`users/patient/user/${id}`)
}
//đặt lịch
const postScheduleOfPatient = (data) => {
    return axios.post(`/appointments/appointments/create/`, {
        patient: data.patient,
      doctor: data.doctor,
      appointment_date: data.appointment_date,
      time_slot: data.time_slot,
      reason: data.reason,
      notes: data.notes
    })
}
//xác nhận đặt lịch 
const postN8nScheduleOfPatient = (data) => {
    return axios.post(`n8n/book/`, {
       patient: data.patient,
      doctor: data.doctor,
      appointment_date: data.appointment_date,
      time_slot: data.time_slot,
      reason: data.reason,
      notes: data.notes
    })
}
export { getPatient, getPatientById, editPatient, deletePatient, postScheduleOfPatient, getPatientIdByUserId, postN8nScheduleOfPatient };
