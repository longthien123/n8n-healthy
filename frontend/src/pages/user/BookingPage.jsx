import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { DatePicker, TimePicker, message } from "antd";
import moment from "moment";
import {
  Card,
  CardContent,
  CardActions,
  CardMedia,
  Button,
  Typography,
  Box,
  Grid,
  Divider,
  TextField,
} from "@mui/material";
import user from "../../assests/user.png";
import { getDoctorById, getScheduleOfDoctor } from "../../services/DoctorServicce";
import { toast } from "react-toastify";

const BookingPage = () => {
  const params = useParams();
  const isloggedIn = sessionStorage.getItem("access_token");
const userData = sessionStorage.getItem("user");
const user = userData ? JSON.parse(userData) : null;
const userId = user?.id;

  const [doctor, setDoctor] = useState(null);
  const [doctorSchedule, setDoctorSchedule] = useState({});
  const [date, setDate] = useState(null);
  const [time, setTime] = useState(null);
  const [reason, setReason] = useState("");
  const [notes, setNotes] = useState("");
  const [isAvailable, setIsAvailable] = useState(false);

  const disabledHours = () => {
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const allowedHours = [8, 9, 10, 11, 14, 15, 16, 17];

  return hours.filter(hour => !allowedHours.includes(hour));
  };

  const fetchDoctor = async () => {
    const res = await getDoctorById(params.id);
    if (res) setDoctor(res.data);
  };

  const fetchScheduleDoctor = async () => {
    const res = await getScheduleOfDoctor(params.id);
    console.log(res, "sche");
    
    if (res) setDoctorSchedule(res.data || {});
  };

  useEffect(() => {
    fetchDoctor();
    fetchScheduleDoctor();
  }, []);

  // Chuyển date + time sang format API
  const appointment_date_convert = date ? moment(date, "DD-MM-YYYY").format("YYYY-MM-DD") : null;
  const time_slot_convert = time
    ? `${time}-${moment(time, "HH:mm").add(1, "hour").format("HH:mm")}`
    : null;

  const handleAvailability = () => {
    console.log(date,doctorSchedule.work_date );
    
    if (appointment_date_convert !== doctorSchedule.work_date){
      return toast.error("Vui lòng chọn đúng ngày làm việc")
    }
    if (!date || !time) {
      return message.error("Please select date and time.");
    }
    const data = {
      patient: userId,
      doctor: params.id,
      appointment_date: appointment_date_convert,
      time_slot: time_slot_convert,
      reason: reason,
      notes: notes
    }
    console.log(data);
    
    setIsAvailable(true);
    message.success("Slot Available!");
    console.log({ appointment_date, time_slot, reason, notes });
  };

  const handleBooking = () => {
    if (!reason) return message.error("Please enter reason for appointment.");
    message.success("Appointment Booked Successfully!");
    console.log({
      appointment_date,
      time_slot,
      reason,
      notes,
    });
  };

  if (!doctor) {
    return <h2 style={{ textAlign: "center", marginTop: 50 }}>Loading...</h2>;
  }

  return (
    <Box
      sx={{
        minHeight: "90vh",
        display: "flex",
        justifyContent: "center",
        paddingTop: "5vh",
      }}
    >
      <Card
        sx={{
          maxWidth: 700,
          width: "100%",
          borderRadius: "18px",
          boxShadow: "0 6px 20px rgba(0,0,0,0.15)",
          paddingBottom: 3,
        }}
      >
        <CardMedia
          sx={{
            height: 220,
            backgroundSize: "contain",
            backgroundColor: "#f5f8ff",
          }}
          image={user}
        />

        <CardContent>
          <Typography
            variant="h4"
            sx={{ textAlign: "center", fontWeight: "bold", color: "#002D62" }}
          >
            {doctor.fullname}
          </Typography>

          <Typography
            variant="subtitle1"
            sx={{ textAlign: "center", color: "#555", mb: 2 }}
          >
            Doctor Profile
          </Typography>

          <Divider sx={{ mb: 3 }} />

          {/* Doctor Info */}
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography><strong>Doctor No:</strong> BS{doctor.id}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography><strong>Phone:</strong> {doctor.user?.phone || ""}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography><strong>Specialization:</strong> {doctor.specialization}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography><strong>Experience:</strong> {doctor.experience_years} years</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography><strong>Work Date:</strong> {doctorSchedule.work_date}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                <strong>Shift:</strong> {doctorSchedule.start_time} → {doctorSchedule.end_time}
              </Typography>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* Booking Form */}
          <Typography variant="h6" sx={{ color: "#002D62", mb: 1 }}>
            Book Appointment
          </Typography>

          {isloggedIn ? (
            <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
              <Box sx={{ display: "flex", gap: 2 }}>
                <DatePicker
                  format="DD-MM-YYYY"
                  onChange={(date) => setDate(date ? date.format("DD-MM-YYYY") : null)}
                />
                <TimePicker
                  format="HH:mm"
                  onChange={(time) => setTime(time ? time.format("HH:mm") : null)}
                  disabledHours={disabledHours}
                  minuteStep={60}
                />
              </Box>

              <TextField
                label="Reason for Appointment"
                variant="outlined"
                fullWidth
                value={reason}
                onChange={(e) => setReason(e.target.value)}
              />
              <TextField
                label="Notes (Optional)"
                variant="outlined"
                fullWidth
                multiline
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />

              <CardActions sx={{ mt: 1 }}>
                <Button
                  variant="contained"
                  sx={{
                    backgroundColor: "#005A9C",
                    "&:hover": { backgroundColor: "#003f6f" },
                  }}
                  onClick={handleAvailability}
                >
                  Check Availability
                </Button>

                {isAvailable && (
                  <Button
                    variant="contained"
                    color="success"
                    onClick={handleBooking}
                  >
                    Book Now
                  </Button>
                )}
              </CardActions>
            </Box>
          ) : (
            <Typography sx={{ mt: 2, color: "red" }}>
              Please login to book an appointment.
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default BookingPage;
