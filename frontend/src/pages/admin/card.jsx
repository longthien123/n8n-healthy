import { useState, useEffect } from "react";
import React from "react";
import "./card.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserDoctor, faHospitalUser, faChartLine } from "@fortawesome/free-solid-svg-icons";
import { getAllDoctor } from "../../services/DoctorServicce";
import { getPatient } from "../../services/PatientService";

export default function Card() {
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);

  const getDoctors = async () => {
    try {
      const response = await getAllDoctor();
      if (response && response.data) {
        setDoctors(response.data);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const getPatients = async () => {
    try {
      const response = await getPatient();
      if (response && response.data) {
        setPatients(response.data);
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getDoctors();
    getPatients();
  }, []);

  return (
    <div className="card-container">
      {/* PATIENTS CARD */}
      <div className="card">
        <div className="card__side card__side--front">
          <div className="card__decoration card__decoration-1"></div>
          <div className="card__decoration card__decoration-2"></div>
          <div className="card__theme">
            <div className="card__theme-box">
              <FontAwesomeIcon icon={faHospitalUser} className="card__icon" />
              <h2 className="card__title">Patients</h2>
              <p className="card__subtitle">Registered Patients</p>
            </div>
          </div>
        </div>

        <div className="card__side card__side--back">
          <div className="card__cover">
            <h4 className="card__heading">
              <span className="card__heading-span">Total Patients</span>
            </h4>
          </div>
          <div className="card__details">
            <ul>
              <li>
                <h2 className="card__count">{patients.length}</h2>
              </li>
              <li>
                <div className="card__stat">
                  <FontAwesomeIcon icon={faChartLine} className="card__stat-icon" />
                  <span>Active Records</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* DOCTORS CARD */}
      <div className="card">
        <div className="card__side card__side--front">
          <div className="card__decoration card__decoration-1"></div>
          <div className="card__decoration card__decoration-2"></div>
          <div className="card__theme">
            <div className="card__theme-box">
              <FontAwesomeIcon icon={faUserDoctor} className="card__icon" />
              <h2 className="card__title">Doctors</h2>
              <p className="card__subtitle">Medical Professionals</p>
            </div>
          </div>
        </div>

        <div className="card__side card__side--back">
          <div className="card__cover">
            <h4 className="card__heading">
              <span className="card__heading-span">Total Doctors</span>
            </h4>
          </div>
          <div className="card__details">
            <ul>
              <li>
                <h2 className="card__count">{doctors.length}</h2>
              </li>
              <li>
                <div className="card__stat">
                  <FontAwesomeIcon icon={faChartLine} className="card__stat-icon" />
                  <span>Active Staff</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* APPOINTMENTS CARD */}
      <div className="card">
        <div className="card__side card__side--front">
          <div className="card__decoration card__decoration-1"></div>
          <div className="card__decoration card__decoration-2"></div>
          <div className="card__theme">
            <div className="card__theme-box">
              <FontAwesomeIcon icon={faChartLine} className="card__icon" />
              <h2 className="card__title">Total</h2>
              <p className="card__subtitle">System Overview</p>
            </div>
          </div>
        </div>

        <div className="card__side card__side--back">
          <div className="card__cover">
            <h4 className="card__heading">
              <span className="card__heading-span">Overall Stats</span>
            </h4>
          </div>
          <div className="card__details">
            <ul>
              <li>
                <h2 className="card__count">{patients.length + doctors.length}</h2>
              </li>
              <li>
                <div className="card__stat">
                  <FontAwesomeIcon icon={faChartLine} className="card__stat-icon" />
                  <span>Total Users</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
