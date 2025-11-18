import React from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";

const SidebarData = [
  {
    title: "DashBoard",
    path: "/admin/dashboard",
    icon: <AiIcons.AiOutlineDashboard />,
    cName: "nav-text",
  },
  {
    title: "Patients",
    path: "/admin/patient",
    icon: <FaIcons.FaUserInjured />,
    cName: "nav-text",
  },
  {
    title: "Doctors",
    path: "/admin/doctor",
    icon: <FaIcons.FaUserNurse />,
    cName: "nav-text",
  },
];

export default SidebarData
