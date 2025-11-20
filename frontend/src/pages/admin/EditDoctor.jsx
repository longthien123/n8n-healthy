import React, { useEffect, useState } from "react";
import "./AddDoctor.css";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@mui/material";
import { createNewDoctor, getDoctorById } from "../../services/DoctorServicce";

export default function EditDoctor() {
  const [doctor, setDoctor] = useState({
    fullname: "",
    email: "",
    username:"",
    password: "",
    phone: "",
    specialization: "",
    license_number: "",
    experience_years: "",
    shiftStart: "",
    shiftEnd: "",
    bio:""
  });
  const params = useParams()
  console.log(params.id);
  
    const fetchDoctor = async () => {
        try {
          const response = await getDoctorById(params.id);
          console.log(response);
          
          setDoctor({
            fullname: response.data.user.full_name,
    email: response.data.user.email,
    username:response.data.user.username,
    password: response.data.user.password,
    phone: response.data.user.phone,
    specialization: response.data.specialization,
    license_number: response.data.license_number,
    experience_years: response.data.experience_years,
    bio: response.data.bio,
            shiftStart: response.data.shiftStart || "",
            shiftEnd: response.data.shiftEnd || ""
          });
        } catch (error) {
          console.error("Error fetching doctor:", error);
        }
      };
      useEffect(() => {
        fetchDoctor()
      }, [])
  const navigate = useNavigate();

  const handleChangeHandler = (e) => {
    setDoctor({
      ...doctor,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async () => {
     const doctorData = {
    username: doctor.username,
    email: doctor.email,
    password: doctor.password,
    full_name: doctor.full_name,
    phone: doctor.phone || '',
    specialization: doctor.specialization || '',
    license_number: doctor.license_number || '',
    experience_years: doctor.experience_years || 0,
    bio: doctor.bio || ''
  };
  const response = await createNewDoctor(doctorData);
  console.log(response);
  
  };

  return (
    <div className="doctor-form">
      <div className="form-box">
        <h2>Edit Doctor</h2>

        <div className="form-grp">
          <label>Name:</label>
          <input
            type="text"
            name="fullname"
            value={doctor.fullname}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={doctor.email}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>UserName:</label>
          <input
            type="text"
            name="username"
            value={doctor.username}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={doctor.password}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>Contact</label>
          <input
            type="number"
            name="phone"
            value={doctor.phone}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>Specialization</label>
          <input
            type="text"
            name="specialization"
            value={doctor.specialization}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>License Number</label>
          <input
            type="number"
            name="license_number"
            value={doctor.license_number}
            onChange={handleChangeHandler}
          />
        </div>
        <div className="form-grp">
          <label>Bio</label>
          <input
            type="text"
            name="bio"
            value={doctor.bio}
            onChange={handleChangeHandler}
          />
        </div>
        {/* MỚI: Thêm ca vào và ra */}
        <div className="form-grp">
          <label>Shift Start (Check in):</label>
          <input
            type="datetime-local"
            name="shiftStart"
            value={doctor.shiftStart}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <label>Shift End (Checkout out):</label>
          <input
            type="datetime-local"
            name="shiftEnd"
            value={doctor.shiftEnd}
            onChange={handleChangeHandler}
          />
        </div>

        <div className="form-grp">
          <button type="submit" id="doc-submit" onClick={() => handleSubmit()}>
            Save Doctor
          </button>
        </div>
      </div>
    </div>
  );
}
