import React, { useEffect, useState } from "react";
import { Grid, Card, CardContent, Typography, Button, Avatar, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import maleAvatar from "../../assests/male-avatar.jpg";
import femaleAvatar from "../../assests/female-avatar.jpg";
import { getAllDoctor } from "../../services/DoctorServicce";
import "./DoctorCard.css";

const DoctorGrid = () => {
  const navigate = useNavigate();
  const [doctorData, setDoctorData] = useState([]);

  const fetchDoctor = async () => {
    const res = await getAllDoctor();
    if (res) {
      setDoctorData(res.data);
    }
  };

  useEffect(() => {
    fetchDoctor();
  }, []);

  const getAvatarSrc = (gender) => (gender === "MALE" ? maleAvatar : femaleAvatar);

  return (
    <Box className="doctor-grid-container">
      <Typography className="doctor-grid-title">
        👨‍⚕️ Our Medical Team
      </Typography>

      <Grid container spacing={4}>
        {doctorData.map((doctor) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={doctor.id}>
            <Card className="doctor-card" elevation={0}>
              <Avatar
                src={getAvatarSrc(doctor.Gender)}
                alt={doctor.user.full_name}
                className="doctor-avatar"
              />

              <CardContent sx={{ padding: 0, flex: 1, display: 'flex', flexDirection: 'column' }}>
                <Typography className="doctor-name">
                  {doctor.user.full_name}
                </Typography>

                <Typography className="doctor-info">
                  📞 {doctor.user.phone}
                </Typography>

                <Typography className="doctor-specialization">
                  🩺 {doctor.specialization}
                </Typography>

                <Typography className="doctor-experience">
                  💼 {doctor.experience_years} years experience
                </Typography>

                <Button
                  className="doctor-view-btn"
                  onClick={() => navigate(`/doctors/book-appointment/${doctor.id}`)}
                >
                  📅 Book Appointment
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default DoctorGrid;
