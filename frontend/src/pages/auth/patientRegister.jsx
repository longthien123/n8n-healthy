import React, { useState } from "react";
import "./PatientRegister.css";
import axios from "axios";
import { patientRegister } from "../../services/AuthService";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

export default function PatientRegister() {
    const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password_confirm: "",
    full_name: "",
    phone: "",
    patient_code: "",
    date_of_birth: "",
    gender: "",
    address: "",
    blood_type: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
        userName: formData.username,
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
        phone: formData.phone,
        date_of_birth: formData.date_of_birth,
        gender: formData.gender,
        address: formData.address,
        blood_type: formData.blood_type
    }
    
    const res = await patientRegister(data);    
      if (res && res.success === true) {
            toast.success("Đăng ký thành công!");
            navigate("/login");
          } else {
            toast.error(res?.message || "Đăng ký thất bại!");
          }
  };

  return (
    <div className="register-container">
      <form className="register-box" onSubmit={handleSubmit}>
        <h2 className="x">Fill the form to register your account</h2>

        <div className="form-row">
          {/* Cột 1 */}
          <div className="col">
            <div className="form-grp">
              <label>Username</label>
              <input
                type="text"
                name="username"
                placeholder="patient01"
                onChange={handleChange}
              />
            </div>

            <div className="form-grp">
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="patient@example.com"
                onChange={handleChange}
              />
            </div>

            <div className="form-grp">
              <label>Password</label>
              <input
                type="password"
                name="password"
                placeholder="password!"
                onChange={handleChange}
              />
            </div>

            <div className="form-grp">
              <label>FullName</label>
              <input
                type="text"
                name="full_name"
                placeholder="fullName"
                onChange={handleChange}
              />
            </div>

            <div className="form-grp">
              <label>Phone</label>
              <input
                type="text"
                name="phone"
                placeholder="phone"
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Cột 2 */}
          <div className="col">
            <div className="form-grp">
              <label>Date of Birth</label>
              <input
                type="date"
                name="date_of_birth"
                onChange={handleChange}
              />
            </div>

            <div className="form-grp">
              <label>Gender</label>
              <select name="gender" onChange={handleChange}>
                <option value="">-- select --</option>
                <option value="MALE">MALE</option>
                <option value="FEMALE">FEMALE</option>
                <option value="OTHER">OTHER</option>
              </select>
            </div>

            <div className="form-grp">
              <label>Address</label>
              <input
                type="text"
                name="address"
                placeholder="address"
                onChange={handleChange}
              />
            </div>

            <div className="form-grp">
              <label>Blood</label>
              <select name="blood_type" onChange={handleChange}>
                <option value="">-- Select --</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
              </select>
            </div>
          </div>
        </div>

        <button id="reg-submit">Register</button>
        <p className="login-link">
            Đã có tài khoản?{" "}
            <span onClick={() => navigate("/login")}>Đăng nhập</span>
          </p>
      </form>
    </div>
  );
}
