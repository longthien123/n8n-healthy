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
  Stack,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { deleteDoctor, getAllDoctor } from "../../services/DoctorServicce";
import { toast } from "react-toastify";

export default function DoctorList() {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const fetchDoctors = async () => {
    try {
      const response = await getAllDoctor();
      setDoctors(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this doctor?")) {
      const response = await deleteDoctor(id);
      if (response) {
        toast.success(response.message);
        fetchDoctors();
      }
    }
  };

  const displayedDoctors = doctors.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <div className="Table">
      <div className="patient-container">
        <Typography variant="h4" className="title" sx={{
          '&::before': {
            content: '"👨‍⚕️"',
            WebkitTextFillColor: 'initial'
          }
        }}>
          Doctors Management
        </Typography>

        <Box className="table-wrapper">
          <TableContainer component={Paper} className="table-box">
            <Table>
              <TableHead>
                <TableRow className="table-header-row">
                  {[
                    "Doctor Name",
                    "Email",
                    "Phone",
                    "Experience",
                    "License",
                    "Specialization",
                    "Actions",
                  ].map((header) => (
                    <TableCell key={header} className="table-header">
                      {header}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>

              <TableBody>
                {displayedDoctors.map((doctor) => (
                  <TableRow key={doctor.id} className="table-row">
                    <TableCell>{doctor.user.full_name}</TableCell>
                    <TableCell>{doctor.user.email}</TableCell>
                    <TableCell>{doctor.user.phone}</TableCell>
                    <TableCell>
                      <span style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        fontWeight: '600'
                      }}>
                        {doctor.experience_years} years
                      </span>
                    </TableCell>
                    <TableCell>{doctor.license_number}</TableCell>
                    <TableCell>
                      <span style={{
                        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        fontWeight: '600'
                      }}>
                        {doctor.specialization}
                      </span>
                    </TableCell>
                    <TableCell>
                      <Stack direction="row" spacing={1} justifyContent="center" className="action-buttons">
                        <Button
                          variant="contained"
                          color="primary"
                          size="small"
                          onClick={() => navigate(`/admin/doctor/${doctor.id}`)}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="contained"
                          color="error"
                          size="small"
                          onClick={() => handleDelete(doctor.id)}
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
        </Box>

        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={doctors.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={(e, p) => setPage(p)}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
        />

        <Button
          variant="contained"
          color="success"
          sx={{ mt: 3, float: "right" }}
          onClick={() => navigate("/admin/add-doctor")}
        >
          ➕ Add New Doctor
        </Button>
      </div>
    </div>
  );
}
