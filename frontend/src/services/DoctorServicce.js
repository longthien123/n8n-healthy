import axios from "../utils/AxiosCustom.js";

const getAllDoctor = () => {
    return axios.get("doctors/")
}
const createNewDoctor = (doctorData) => {
    return axios.post(`doctors/create/`, {
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
     return axios.put(`doctors/${id}/update/`, {
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
    return axios.get(`doctors/${id}`)
}
const deleteDoctor = (id) => {
    return axios.delete(`doctors/${id}/delete/`)
}
export {
    getAllDoctor,
    createNewDoctor,
    getDoctorById,
    editDoctor,
    deleteDoctor
}