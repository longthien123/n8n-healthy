import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import Footer from "./Footer";
import "./Home.css";
import Slider from "./Slider"; 
import Navbar from "./NavBar";
import MessengerIcon from "./MessengerIcon";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <Navbar />
      <div className="background-wrapper"></div>
      <div className="home" id="home-div">
        <Outlet/>
      </div>
      {/* Messenger nổi cố định */}
      <div className="messenger-float">
        <MessengerIcon
          size={52}
          showBadge
          badgeCount={1}
          onClick={() => navigate("https://www.messenger.com/t/100472262897552")} // hoặc mở link Messenger
        />
      </div>
      <Footer />
    </div>
  );
}