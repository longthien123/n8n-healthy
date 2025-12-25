import React, { useEffect, useState } from "react";
import "./AddDoctor.css";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import {
  getDoctorById,
  editDoctor,
  createSchedule,
} from "../../services/DoctorServicce";
import { editPatient, getPatientById } from "../../services/PatientService";

export default function EditPatient() {
  const [patient, setPatient] = useState({
    fullname: "",
    email: "",
    username: "",
    password: "",
    phone: "",
    patient_code: "",
    date_of_birth: "",
    gender: "",
    address: "",
    blood_type: "",
  });

  const params = useParams();
  const navigate = useNavigate();

  const fetchPatient = async () => {
    try {
      const response = await getPatientById(params.id);
      const data = response.data;

      setPatient({
        fullname: data.user.full_name,
        email: data.user.email,
        username: data.user.username,
        password: data.user.password,
        phone: data.user.phone,
        patient_code: data.patient_code,
        date_of_birth: data.date_of_birth,
        gender: data.gender,
        address: data.address,
        blood_type: data.blood_type,
      });
    } catch (error) {
      console.error("Error fetching patient:", error);
    }
  };

  useEffect(() => {
    fetchPatient();
  }, []);

  const handleChangeHandler = (e) => {
    setPatient({
      ...patient,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async () => {
    const data = {
      username: patient.username,
      email: patient.email,
      password: patient.password,
      full_name: patient.fullname,
      phone: patient.phone,
      patient_code: patient.patient_code,
      date_of_birth: patient.date_of_birth,
      gender: patient.gender,
      address: patient.address,
      blood_type: patient.blood_type,
    };

    const response = await editPatient(data, params.id);
    if (response && response.success === true) {
      toast.success(response.message);
      navigate("/admin/patient");
    }
  };
  return (
    <div className="doctor-form">
      <div className="form-box">
        <div className="">
          <h2>Edit Patient</h2>

          <div className="form-grp">
            <label>Name:</label>
            <input
              type="text"
              name="fullname"
              value={patient.fullname}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={patient.email}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>UserName:</label>
            <input
              readOnly
              type="text"
              name="username"
              value={patient.username}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>Password:</label>
            <input
              readOnly
              type="password"
              name="password"
              value={patient.password}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>Phone:</label>
            <input
              type="number"
              name="phone"
              value={patient.phone}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>Patient No</label>
            <input
              type="text"
              name="patient_code"
              value={patient.patient_code}
              onChange={handleChangeHandler}
            />
          </div>
          <div className="form-grp">
            <label>Date of Birth</label>
            <input
              type="date"
              name="date_of_birth"
              value={patient.date_of_birth}
              onChange={handleChangeHandler}
            />
          </div>
          <div className="form-grp">
            <label>Gender</label>
            <input
              type="text"
              name="gender"
              value={patient.gender}
              onChange={handleChangeHandler}
            />
          </div>
          <div className="form-grp">
            <label>Address</label>
            <input
              type="text"
              name="address"
              value={patient.address}
              onChange={handleChangeHandler}
            />
          </div>
          <div className="form-grp">
            <label>Blood</label>
            <input
              type="text"
              name="blood"
              value={patient.blood_type}
              onChange={handleChangeHandler}
            />
          </div>
        </div>
        <div className="form-grp submit-zone">
          <button id="doc-submit" onClick={handleSubmit}>
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
