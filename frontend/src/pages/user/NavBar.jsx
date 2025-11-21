import { useRef } from "react";
import { FaBars, FaTimes } from "react-icons/fa";
import "./Navbar.css";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const navRef = useRef();
  const isLoggedIn = sessionStorage.getItem("access_token");
  const showNavbar = () => {
    navRef.current.classList.toggle("responsive_nav");
  };
  const userData = sessionStorage.getItem("user");
  const user = userData ? JSON.parse(userData) : null;
  const name = user?.name;
  return (
    <header className="Nav-header">
      <h3>LOGO</h3>
      <nav ref={navRef}>
        <a href="/">Home</a>
        <a href="/doctors">Doctors</a>
        <a href="/#">Blog</a>
        <a href="/#">About me</a>
        <div className="navbar1">
          <span className="Nav-username">Hi, {name} </span>

          {isLoggedIn ? (
            <button
              className="Nav-login"
              style={{ background: "red", color: "white" }}
              onClick={() => {
                localStorage.clear();
                navigate("/login");
              }}
            >
              Logout
            </button>
          ) : (
            <button
              className="Nav-login"
              onClick={() => {
                navigate("/login");
              }}
            >
              Login
            </button>
          )}
        </div>

        <button className="nav-btn nav-close-btn" onClick={showNavbar}>
          <FaTimes />
        </button>
      </nav>
      <button className="nav-btn" onClick={showNavbar}>
        <FaBars />
      </button>
    </header>
  );
}

export default Navbar;
