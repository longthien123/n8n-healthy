import React, { useState } from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from "react-router-dom";
import "./Navbar.css";
import { IconContext } from "react-icons";
import { useNavigate } from "react-router-dom";
import SidebarData from "./SidebarData";

function Navbar() {
  const [sidebar, setSidebar] = useState(false);
  const navigate = useNavigate();

  const showSidebar = () => setSidebar(!sidebar);

  return (
    <>
      <IconContext.Provider value={{ color: "#fff" }}>
        <div className="navbar">
          <Link to="#" className="menu-bars">
            <FaIcons.FaBars onClick={showSidebar} />
          </Link>

          <button
            className="logout-btn"
            onClick={() => {
              localStorage.clear();
              navigate("/login");
            }}
          >
            Log Out
          </button>
        </div>

        <nav className={sidebar ? "nav-menu active" : "nav-menu"}>
          <ul className="nav-menu-items">
            <li className="navbar-toggle">
              <AiIcons.AiOutlineClose className="close-icon" onClick={showSidebar} />
            </li>

            <h2 className="sidebar-title">ADMIN PANEL</h2>

            {SidebarData.map((item, index) => (
              <li key={index} className="nav-text">
                <Link to={item.path}>
                  {item.icon}
                  <span>{item.title}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </IconContext.Provider>
    </>
  );
}

export default Navbar;
