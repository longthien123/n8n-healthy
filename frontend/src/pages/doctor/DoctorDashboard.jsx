import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDoctorAppointments } from "../../services/AppointmentService";
import { toast } from "react-toastify";
import "./DoctorDashboard.css";

export default function DoctorDashboard() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("ALL"); // ALL, SCHEDULED, CONFIRMED, COMPLETED
  const navigate = useNavigate();

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const user = JSON.parse(sessionStorage.getItem("user"));
      if (!user || user.role !== "DOCTOR") {
        toast.error("Bạn không có quyền truy cập trang này!");
        navigate("/login");
        return;
      }

      // Lấy doctor_id từ user (giả sử user.id là doctor_id)
      // Nếu cần, bạn có thể lưu doctor_id riêng trong sessionStorage khi login
      const response = await getDoctorAppointments(user.id);
      
      if (response && response.success) {
        setAppointments(response.data);
      } else {
        toast.error("Không thể tải danh sách lịch khám!");
      }
    } catch (error) {
      console.error("Error fetching appointments:", error);
      toast.error("Đã có lỗi xảy ra!");
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      SCHEDULED: { text: "Đã đặt lịch", class: "status-scheduled" },
      CONFIRMED: { text: "Đã xác nhận", class: "status-confirmed" },
      COMPLETED: { text: "Hoàn thành", class: "status-completed" },
      CANCELLED: { text: "Đã hủy", class: "status-cancelled" },
      NO_SHOW: { text: "Không đến", class: "status-no-show" },
    };
    const info = statusMap[status] || { text: status, class: "" };
    return <span className={`status-badge ${info.class}`}>{info.text}</span>;
  };

  const filteredAppointments = appointments.filter((apt) => {
    if (filter === "ALL") return true;
    return apt.status === filter;
  });

  const handleViewDetail = (appointmentId) => {
    navigate(`/doctor/appointment/${appointmentId}`);
  };

  const handleLogout = () => {
    sessionStorage.clear();
    navigate("/login");
    toast.success("Đăng xuất thành công!");
  };

  if (loading) {
    return (
      <div className="doctor-dashboard">
        <div className="loading">Đang tải dữ liệu...</div>
      </div>
    );
  }

  return (
    <div className="doctor-dashboard">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Lịch Khám Bệnh</h1>
          <p className="dashboard-subtitle">
            Xin chào, BS. {JSON.parse(sessionStorage.getItem("user"))?.name}
          </p>
        </div>
        <button className="btn-logout" onClick={handleLogout}>
          Đăng xuất
        </button>
      </div>

      <div className="filter-tabs">
        <button
          className={`filter-tab ${filter === "ALL" ? "active" : ""}`}
          onClick={() => setFilter("ALL")}
        >
          Tất cả ({appointments.length})
        </button>
        <button
          className={`filter-tab ${filter === "SCHEDULED" ? "active" : ""}`}
          onClick={() => setFilter("SCHEDULED")}
        >
          Đã đặt lịch
        </button>
        <button
          className={`filter-tab ${filter === "CONFIRMED" ? "active" : ""}`}
          onClick={() => setFilter("CONFIRMED")}
        >
          Đã xác nhận
        </button>
        <button
          className={`filter-tab ${filter === "COMPLETED" ? "active" : ""}`}
          onClick={() => setFilter("COMPLETED")}
        >
          Hoàn thành
        </button>
      </div>

      <div className="appointments-grid">
        {filteredAppointments.length === 0 ? (
          <div className="no-data">Không có lịch khám nào.</div>
        ) : (
          filteredAppointments.map((apt) => (
            <div
              key={apt.id}
              className="appointment-card"
              onClick={() => handleViewDetail(apt.id)}
            >
              <div className="card-header">
                <h3 className="patient-name">{apt.patient.full_name}</h3>
                {getStatusBadge(apt.status)}
              </div>

              <div className="card-body">
                <div className="info-row">
                  <span className="label">📅 Ngày khám:</span>
                  <span className="value">{apt.appointment_date}</span>
                </div>
                <div className="info-row">
                  <span className="label">🕒 Khung giờ:</span>
                  <span className="value">{apt.time_slot}</span>
                </div>
                <div className="info-row">
                  <span className="label">📞 Điện thoại:</span>
                  <span className="value">{apt.patient.phone}</span>
                </div>
                {apt.reason && (
                  <div className="info-row reason">
                    <span className="label">💬 Lý do:</span>
                    <span className="value">{apt.reason}</span>
                  </div>
                )}
              </div>

              <div className="card-footer">
                <button className="btn-view-detail">Xem chi tiết →</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
