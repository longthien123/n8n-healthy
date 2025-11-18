import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import Footer from "./Footer";
import "./Home.css";
import Slider from "./Slider"; 
import Navbar from "./Navbar";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <Navbar />
      <div className="background-wrapper"></div>
      <div className="home" id="home-div">
        <Outlet/>
      </div>
      <Footer />
    </div>
  );
}