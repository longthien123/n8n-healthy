import React, { useEffect, useState } from "react";
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
  IconButton,
  Tooltip,
} from "@mui/material";
import "./PatientList.css";
import { useNavigate } from "react-router-dom";
import { deletePatient, getPatient } from "../../services/PatientService";
import { toast } from "react-toastify";

export default function PatientList() {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const getPatients = async () => {
    const res = await getPatient();
    if (res) setPatients(res.data);
  };

  useEffect(() => {
    getPatients();
  }, []);

  const handleDelete = async (id) => {
    const response = await deletePatient(id);
    if (response) {
      toast.success(response.message);
      navigate("admin/patient");
    }
  };

  const displayedPatients = patients.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <div className="Table">
      <div className="patient-container">
        <Typography variant="h4" className="title">
          Patients List
        </Typography>

        <Box className="table-wrapper">
          <TableContainer component={Paper} className="table-box">
            <Table>
              <TableHead>
                <TableRow className="table-header-row">
                  {[
                    "Patient No",
                    "Name",
                    "Date of Birth",
                    "Gender",
                    "Address",
                    "Blood",
                    "Action",
                  ].map((header) => (
                    <TableCell key={header} className="table-header">
                      {header}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>

              <TableBody>
                {displayedPatients.map((patient) => (
                  <TableRow key={patient.id} className="table-row">
                    <TableCell>BN{patient.id}</TableCell>
                    <TableCell>{patient.user.full_name}</TableCell>
                    <TableCell>{patient.date_of_birth}</TableCell>
                    <TableCell>{patient.gender}</TableCell>
                    <TableCell>{patient.address}</TableCell>
                    <TableCell>{patient.blood_type}</TableCell>

                    <TableCell>
                      <div className="action-buttons">
                        {/* EDIT BUTTON */}
                        <Button
                          variant="contained"
                          color="primary"
                          size="small"
                          onClick={() =>
                            navigate(`/admin/patient/${patient.id}`)
                          }
                        >
                          Edit
                        </Button>
                        <Button
                          variant="contained"
                          color="error"
                          size="small"
                          onClick={() => {
                            handleDelete(patient.id);
                          }}
                        >
                          Remove
                        </Button>
                      </div>
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
          count={patients.length}
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
          onClick={() => navigate("/info-patient")}
        >
          Add Patient
        </Button>
      </div>
    </div>
  );
}
