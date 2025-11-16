import React from "react";
import "./home.css";
// import PatientList from "./patientList";
// import axios from "axios";
import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";


export default function Home() {
  // useEffect(() => {
  //   if (!localStorage.getItem("token")) {
  //     navigate("/");
  //   }
  // }, []);

  return (
    <div className="container">
      <div className="background-wrapper"></div>
            <Navbar />
      <div className="home">
          <Outlet/>
     </div>
    </div>
  );
}
