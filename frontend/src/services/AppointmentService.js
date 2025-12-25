import axios from "../utils/AxiosCustom.js";

// Lấy danh sách lịch khám của bác sĩ (theo doctor_id)
const getDoctorAppointments = (doctorId) => {
  return axios.get(`appointments/appointments/doctor/${doctorId}/`);
};

// Lấy chi tiết một lịch khám
const getAppointmentDetail = (appointmentId) => {
  return axios.get(`appointments/appointments/${appointmentId}/detail/`);
};

// Hoàn thành lịch khám và gọi webhook n8n
const completeAppointment = (appointmentId, data) => {
  return axios.post(`appointments/appointments/${appointmentId}/complete/`, data);
};

// Cập nhật lịch khám
const updateAppointment = (appointmentId, data) => {
  return axios.patch(`appointments/appointments/${appointmentId}/update/`, data);
};

export {
  getDoctorAppointments,
  getAppointmentDetail,
  completeAppointment,
  updateAppointment,
};
