import React, { useEffect, useState } from "react";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Avatar,
  Box,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import maleAvatar from "../../assests/male-avatar.jpg";
import femaleAvatar from "../../assests/female-avatar.jpg";
import { getAllDoctor } from "../../services/DoctorServicce";

const DoctorGrid = () => {
  const navigate = useNavigate();
  const [doctorData, setDoctorData] = useState([]);

  const fetchDoctor = async () => {
    const res = await getAllDoctor();
    console.log(res);
    
    if (res) {
      setDoctorData(res.data);
    }
  };

  useEffect(() => {
    fetchDoctor();
  }, []);

  const getAvatarSrc = (gender) => (gender === "MALE" ? maleAvatar : maleAvatar);

  return (
    <Box sx={{ padding: "30px" }}>
      <Typography
        variant="h4"
        sx={{ fontWeight: "bold", color: "#002D62", mb: 3, textAlign: "center" }}
      >
        Doctors Directory
      </Typography>

      <Grid container spacing={3}>
        {doctorData.map((doctor) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={doctor.doctorNo}>
            <Card
              sx={{
                borderRadius: "15px",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                padding: "20px",
                textAlign: "center",
                transition: "0.3s",
                "&:hover": {
                  transform: "translateY(-7px)",
                  boxShadow: "0 8px 20px rgba(0,0,0,0.2)",
                },
              }}
            >
              <Avatar
                src={getAvatarSrc(doctor.Gender)}
                alt="Doctor Avatar"
                sx={{
                  width: 90,
                  height: 90,
                  margin: "0 auto",
                  border: "3px solid #002D62",
                  mb: 2,
                }}
              />

              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: "bold", color: "#002D62" }}>
                  {doctor.user.full_name}
                </Typography>

                <Typography variant="body2" sx={{ mt: 1, color: "#444" }}>
                  📞 {doctor.user.phone}
                </Typography>

                <Typography
                  variant="body2"
                  sx={{ mt: 1, color: "#1F75FE", fontWeight: "bold" }}
                >
                  🩺 {doctor.specialization}
                </Typography>

                <Button
                  variant="contained"
                  sx={{
                    mt: 2,
                    backgroundColor: "#04619f",
                    padding: "6px 20px",
                    borderRadius: "10px",
                    textTransform: "none",
                    fontWeight: "bold",
                    "&:hover": { backgroundColor: "#002D62" },
                  }}
                  onClick={() =>
                    navigate(`/doctors/book-appointment/${doctor.id}`)
                  }
                >
                  View Details
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
