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
  TextField,
  Avatar,
} from "@mui/material";
import user from "../../assests/user.png";
import { getDoctorById, getScheduleOfDoctor } from "../../services/DoctorServicce";
import { toast } from "react-toastify";
import { getPatientIdByUserId, postN8nScheduleOfPatient, postScheduleOfPatient } from "../../services/PatientService";
import "./BookingPage.css";

const BookingPage = () => {
  const params = useParams();
  const isloggedIn = sessionStorage.getItem("access_token");
  const userData = sessionStorage.getItem("user");
  const userObj = userData ? JSON.parse(userData) : null;
  const userId = userObj?.id;

  const [doctor, setDoctor] = useState(null);
  const [doctorSchedule, setDoctorSchedule] = useState([]);
  const [date, setDate] = useState(null);
  const [time, setTime] = useState(null);
  const [reason, setReason] = useState("");
  const [notes, setNotes] = useState("");
  const [isAvailable, setIsAvailable] = useState(false);
  const [id, setId] = useState(null);

  const disabledHours = () => {
    const hours = Array.from({ length: 24 }, (_, i) => i);
    const allowedHours = [8, 9, 10, 11, 14, 15, 16, 17];
    return hours.filter((hour) => !allowedHours.includes(hour));
  };

  const fetchDoctor = async () => {
    const res = await getDoctorById(params.id);
    if (res) setDoctor(res.data);
  };

  const fetchScheduleDoctor = async () => {
    const res = await getScheduleOfDoctor(params.id);
    if (res) setDoctorSchedule(res?.schedules ?? []);
  };

  const fetchPatient = async () => {
    const res = await getPatientIdByUserId(userId);
    if (res) setId(res.data.id);
  };

  useEffect(() => {
    fetchDoctor();
    fetchScheduleDoctor();
    fetchPatient();
  }, []);

  const appointment_date_convert = date
    ? moment(date, "DD-MM-YYYY").format("YYYY-MM-DD")
    : null;
  const time_slot_convert = time
    ? `${time}-${moment(time, "HH:mm").add(1, "hour").format("HH:mm")}`
    : null;

  const handleAvailability = () => {
    const isValidDate = doctorSchedule.some(
      (sch) => sch.work_date === appointment_date_convert
    );

    if (!isValidDate) {
      return toast.error("Vui lòng chọn đúng ngày làm việc");
    }

    if (!date || !time) {
      return message.error("Please select date and time.");
    }

    setIsAvailable(true);
    message.success("Slot Available!");
  };

  const handleBooking = async () => {
    const data = {
      patient: id,
      doctor: params.id,
      appointment_date: appointment_date_convert,
      time_slot: time_slot_convert,
      reason: reason,
      notes: notes,
    };

    try {
      const res = await postScheduleOfPatient(data);

      if (res?.success === true) {
        await postN8nScheduleOfPatient(data);
        toast.success(res.message);
      } else {
        toast.error(res?.data?.message || "Lỗi không xác định");
      }
    } catch (error) {
      const msg =
        error.response?.data?.errors?.non_field_errors?.[0] ||
        error.response?.data?.message ||
        "Đã xảy ra lỗi";
      toast.error(msg);
    }
  };

  if (!doctor) {
    return (
      <Box className="booking-page-container">
        <Typography variant="h5" sx={{ fontFamily: 'Poppins', color: '#667eea' }}>
          Loading...
        </Typography>
      </Box>
    );
  }

  return (
    <Box className="booking-page-container">
      <Card className="booking-card">
        <CardMedia className="booking-card-media">
          <Avatar src={user} className="doctor-avatar-large" />
        </CardMedia>

        <CardContent className="booking-card-content">
          <Typography className="doctor-title">{doctor.fullname}</Typography>
          <Typography className="doctor-subtitle">Medical Professional</Typography>

          <hr className="info-divider" />

          <div className="info-grid">
            <Typography className="info-item">
              <strong>Doctor ID:</strong> BS{doctor.id}
            </Typography>
            <Typography className="info-item">
              <strong>Phone:</strong> {doctor.user?.phone || "N/A"}
            </Typography>
            <Typography className="info-item">
              <strong>Specialization:</strong> {doctor.specialization}
            </Typography>
            <Typography className="info-item">
              <strong>Experience:</strong> {doctor.experience_years} years
            </Typography>
          </div>

          {doctorSchedule.map((schedule) => (
            <div key={schedule.id} className="schedule-grid">
              <Typography className="schedule-item">
                <strong>📅 Work Date:</strong> {schedule.work_date}
              </Typography>
              <Typography className="schedule-item">
                <strong>⏰ Shift:</strong> {schedule.start_time} → {schedule.end_time}
              </Typography>
            </div>
          ))}

          <hr className="info-divider" />

          <Typography className="booking-section-title">Book Your Appointment</Typography>

          {isloggedIn ? (
            <Box className="booking-form">
              <div className="datetime-picker-row">
                <DatePicker
                  format="DD-MM-YYYY"
                  onChange={(date) => setDate(date ? date.format("DD-MM-YYYY") : null)}
                  placeholder="Select Date"
                />
                <TimePicker
                  format="HH:mm"
                  onChange={(time) => setTime(time ? time.format("HH:mm") : null)}
                  disabledHours={disabledHours}
                  minuteStep={60}
                  placeholder="Select Time"
                />
              </div>

              <TextField
                label="Reason for Appointment"
                variant="outlined"
                fullWidth
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                className="booking-textfield"
              />

              <TextField
                label="Notes (Optional)"
                variant="outlined"
                fullWidth
                multiline
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="booking-textfield"
              />

              <div className="booking-actions">
                <button className="btn-check-availability" onClick={handleAvailability}>
                  Check Availability
                </button>

                {isAvailable && (
                  <button className="btn-book-now" onClick={handleBooking}>
                    Book Now
                  </button>
                )}
              </div>
            </Box>
          ) : (
            <Typography className="login-message">
              ⚠️ Please login to book an appointment
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default BookingPage;
