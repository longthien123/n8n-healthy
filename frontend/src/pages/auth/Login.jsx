import "./Login.css";
import image from "./Asset 1.png";
import { useState } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { postLogin } from "../../services/AuthService";

export default function LoginForm() {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const submitHandler = async (e) => {
    e.preventDefault();
    let data = await postLogin( username, password );
    
      if (data && data.success === true) {
        sessionStorage.setItem("access_token", data.data.session_id);
        sessionStorage.setItem(
          "user",
          JSON.stringify({
            id: data.data.user.id,
            role: data.data.user.role,
            name: data.data.user.full_name,
          })
        );
        if (data.data.user.role === "ADMIN") {
          navigate("/admin");
        } else if (data.data.user.role === "USER") {
          navigate("/");
        }
        toast.success(data.message);
      }
      if (data && data.success !== true) {
        toast.error("Đăng nhập thất bại!");
      }
  };

  return (
    <div className="login-container">
      <div className="login-card">

        <div className="left-side">
          <img src={image} alt="Login visual" className="login-image" />
        </div>

        <form onSubmit={submitHandler} className="right-side">
          <h2 className="title">WELCOME BACK</h2>
          <p className="subtitle">Please login to continue</p>

          <div className="form-group">
            <label>User Name</label>
            <input className="text"
              type="text"
              placeholder="Enter username"
              onChange={(e) => setUserName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter password"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className="btn-login">LOGIN</button>
        </form>

      </div>
    </div>
  );
}
