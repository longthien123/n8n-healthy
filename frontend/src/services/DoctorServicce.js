import axios from "../utils/AxiosCustom.js";

const getAllDoctor = () => {
    return axios.get("users/doctors/")
}
const createNewDoctor = (doctorData) => {
    return axios.post(`users/doctors/create/`, {
        username: doctorData.username,
        email: doctorData.email,
        password: doctorData.password,
        full_name: doctorData.full_name,
        phone: doctorData.phone || '',
        specialization: doctorData.specialization || '',
        license_number: doctorData.license_number || '',
        experience_years: doctorData.experience_years || 0,
        bio: doctorData.bio || ''
    });
}
const editDoctor = (doctorData, id) => {
     return axios.put(`users/doctors/${id}/update/`, {
        username: doctorData.username,
        email: doctorData.email,
        password: doctorData.password,
        full_name: doctorData.full_name,
        phone: doctorData.phone || '',
        specialization: doctorData.specialization || '',
        license_number: doctorData.license_number || '',
        experience_years: doctorData.experience_years || 0,
        bio: doctorData.bio || ''
    });
}
const getDoctorById = (id) => {
    return axios.get(`users/doctors/${id}`)
}
const deleteDoctor = (id) => {
    return axios.delete(`users/doctors/${id}/delete/`)
}
const deleteDoctorSchedule = (id) => {
    return axios.delete(`appointments/schedules/${id}/delete/`)
}

const getSchedule = () => {
    return axios.get(`appointments/schedules/`)
}

const createSchedule = (doctorData) => {
    console.log(doctorData);
    
    return axios.post(`appointments/schedules/create/`, {
        doctor: doctorData.doctor,
        work_date: doctorData.work_date,
        start_time: doctorData.start_time,
        end_time: doctorData.end_time,
        status: doctorData.status,
        note: doctorData.note,
    })
}
const getScheduleOfDoctor = (id) => {
    return axios.get(`appointments/schedules/${id}/`)
}
export {
    getAllDoctor,
    createNewDoctor,
    getDoctorById,
    editDoctor,
    deleteDoctor,
    getSchedule,
    deleteDoctorSchedule,
    createSchedule,
    getScheduleOfDoctor
}