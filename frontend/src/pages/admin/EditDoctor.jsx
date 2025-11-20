import React, { useEffect, useState } from "react";
import "./AddDoctor.css";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { getDoctorById, editDoctor, createSchedule } from "../../services/DoctorServicce";

export default function EditDoctor() {
  const [doctor, setDoctor] = useState({
    fullname: "",
    email: "",
    username: "",
    password: "",
    phone: "",
    specialization: "",
    license_number: "",
    experience_years: "",
    bio: "",
    startDate: "",
    shiftStart: "",
    shiftEnd: "",
  });

  const params = useParams();
  const navigate = useNavigate();

  const fetchDoctor = async () => {
    try {
      const response = await getDoctorById(params.id);
      const data = response.data;

      setDoctor({
        fullname: data.user.full_name,
        email: data.user.email,
        username: data.user.username,
        password: data.user.password,
        phone: data.user.phone,
        specialization: data.specialization,
        license_number: data.license_number,
        experience_years: data.experience_years,
        bio: data.bio,
      });
    } catch (error) {
      console.error("Error fetching doctor:", error);
    }
  };

  useEffect(() => {
    fetchDoctor();
  }, []);

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
      full_name: doctor.fullname,
      phone: doctor.phone,
      specialization: doctor.specialization,
      license_number: doctor.license_number,
      experience_years: doctor.experience_years,
      bio: doctor.bio,
    };

    const response = await editDoctor(doctorData, params.id);
    if (response && response.success === true) {
      toast.success(response.message);
      navigate("/admin/doctor");
    }
  };
  const handleSubmitSchedule = async () => {
    const data = {
        doctor: params.id,
        work_date: doctor.startDate,
        start_time: doctor.shiftStart,
        end_time: doctor.shiftEnd,
        status: "SCHEDULED",
        note: "lịch trình",
    }
    console.log(data, "data");
    
    const response = await createSchedule(data);
    if (response && response.success === true){
        toast.success(response.message)
        navigate("/admin/doctor-schedule")
    }
    
  }
  return (
    <div className="doctor-form">
      <div className="form-box form-grid">
        <div className="form-left">
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
            <label>Phone:</label>
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
        </div>

        {/* Right column */}
        <div className="form-right">
          <h3>Shift Information</h3>

          <div className="form-grp">
            <label>Ngày vào làm:</label>
            <input
              type="date"
              name="startDate"
              value={doctor.startDate}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>Giờ vào ca:</label>
            <input
              type="time"
              name="shiftStart"
              value={doctor.shiftStart}
              onChange={handleChangeHandler}
            />
          </div>

          <div className="form-grp">
            <label>Giờ ra ca:</label>
            <input
              type="time"
              name="shiftEnd"
              value={doctor.shiftEnd}
              onChange={handleChangeHandler}
            />
          </div>
<button id="doc-submit" onClick={handleSubmitSchedule}>
            Save
          </button>
        </div>

        <div className="form-grp submit-zone">
          <button id="doc-submit" onClick={handleSubmit}>
            Save Doctor
          </button>
        </div>
      </div>
    </div>
  );
}
