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
import { deleteDoctorSchedule, getSchedule } from "../../services/DoctorServicce";
import { toast } from "react-toastify";

export default function DoctorScheduleList() {
  const navigate = useNavigate();
  const [schedules, setSchedules] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const fetchSchedules = async () => {
    try {
      const response = await getSchedule();
      setSchedules(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this schedule?")) {
      const response = await deleteDoctorSchedule(id);
      if (response) {
        toast.success(response.message);
        fetchSchedules();
      }
    }
  };

  const displayedSchedules = schedules.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <div className="Table">
      <div className="patient-container">
        <Typography variant="h4" className="title" sx={{
          '&::before': {
            content: '"📅"',
            WebkitTextFillColor: 'initial'
          }
        }}>
          Doctors Schedule
        </Typography>

        <Box className="table-wrapper">
          <TableContainer component={Paper} className="table-box">
            <Table>
              <TableHead>
                <TableRow className="table-header-row">
                  {[
                    "Doctor ID",
                    "Doctor Name",
                    "Work Date",
                    "Check In",
                    "Check Out",
                    "Status",
                    "Notes",
                    "Actions",
                  ].map((header) => (
                    <TableCell key={header} className="table-header">
                      {header}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>

              <TableBody>
                {displayedSchedules.map((schedule) => (
                  <TableRow key={schedule.id} className="table-row">
                    <TableCell>BS{schedule.doctor}</TableCell>
                    <TableCell>{schedule.doctor_name}</TableCell>
                    <TableCell>
                      <span style={{
                        background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        fontWeight: '600'
                      }}>
                        {schedule.work_date}
                      </span>
                    </TableCell>
                    <TableCell>{schedule.start_time}</TableCell>
                    <TableCell>{schedule.end_time}</TableCell>
                    <TableCell>
                      <span style={{
                        background: schedule.status === 'ACTIVE' 
                          ? 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'
                          : 'linear-gradient(135deg, #ee5a6f 0%, #f093fb 100%)',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        fontWeight: '600'
                      }}>
                        {schedule.status}
                      </span>
                    </TableCell>
                    <TableCell>{schedule.notes || "—"}</TableCell>
                    <TableCell>
                      <Stack direction="row" spacing={1} justifyContent="center" className="action-buttons">
                        <Button
                          variant="contained"
                          color="error"
                          size="small"
                          onClick={() => handleDelete(schedule.id)}
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
          count={schedules.length}
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
          onClick={() => navigate("/admin/doctor")}
        >
          ➕ Add New Schedule
        </Button>
      </div>
    </div>
  );
}
