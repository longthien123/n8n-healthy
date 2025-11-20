import React, { useEffect, useState } from "react";
import "./PatientList.css";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  Box,
  Typography,
  Button,
  Stack
} from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { deleteDoctor, deleteDoctorSchedule, getAllDoctor, getSchedule } from "../../services/DoctorServicce";
import { toast } from "react-toastify";

export default function DoctorScheduleList() {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const fetchDoctors = async () => {
    try {
      const response = await getSchedule();
      setDoctors(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const displayedDoctors = doctors.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );
  const handleDelete = async (id) => {
    const response = await deleteDoctorSchedule(id);
    if (response) {
      toast.success(response.message)
      navigate("/admin/doctor-schedule")
    }
  }
  return (
    <Box sx={{ padding: "20px 5%", minHeight: "100vh", background: "#f5f6fa" }}>
      <Typography
        variant="h4"
        gutterBottom
        sx={{ fontWeight: "bold", color: "#060b26", mb: 3, textAlign: "center" }}
      >
        Doctors Schedule
      </Typography>

      <TableContainer component={Paper} sx={{ borderRadius: "12px", overflow: "hidden", boxShadow: 3 }}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow sx={{ backgroundColor: "#060b26" }}>
              {["ID Doctor","Name", "Day work", "CheckIn", "CheckOut", "Status", "Note", "Actions"].map((header) => (
                <TableCell
                  key={header}
                  sx={{ color: "white", fontWeight: "bold", textAlign: "center" }}
                >
                  {header}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
            {displayedDoctors.map((doctor) => (
              <TableRow
                key={doctor.doctorNo}
                sx={{
                  "&:nth-of-type(even)": { backgroundColor: "#f9f9f9" },
                  "&:hover": { backgroundColor: "#e3f2fd" },
                }}
              >
                <TableCell>{doctor.doctor}</TableCell>
                <TableCell>{doctor.doctor_name}</TableCell>
                <TableCell>{doctor.work_date}</TableCell>
                <TableCell>{doctor.start_time}</TableCell>
                <TableCell>{doctor.end_time}</TableCell>
                <TableCell>{doctor.status}</TableCell>
                <TableCell>{doctor.notes}</TableCell>
                <TableCell>
                  <Stack direction="row" spacing={1} justifyContent="center">
                    {/* <Button
                      variant="contained"
                      color="primary"
                      size="small"
                      onClick={() => navigate(`/admin/doctor/${doctor.id}`)}
                    >
                      Edit
                    </Button> */}
                    <Button
                      variant="contained"
                      color="error"
                      size="small"
                      onClick={() => {handleDelete(doctor.id)}}
                    >
                      Remove
                    </Button>
                  </Stack>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={doctors.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        sx={{ mt: 2 }}
      />

      <Button
        variant="contained"
        color="success"
        sx={{ mt: 3, float: "right" }}
        onClick={() => navigate("/admin/doctor")}
      >
        Add Schedule
      </Button>
    </Box>
  );
}
