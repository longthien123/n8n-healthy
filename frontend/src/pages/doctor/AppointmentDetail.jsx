import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  getAppointmentDetail,
  completeAppointment,
} from "../../services/AppointmentService";
import { toast } from "react-toastify";
import "./AppointmentDetail.css";

export default function AppointmentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [appointment, setAppointment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  // Form state
  const [reason, setReason] = useState("");
  const [notes, setNotes] = useState("");
  const [webhookUrl, setWebhookUrl] = useState(
    "https://longthien.duckdns.org/webhook/kham-benh-hoan-thanh"
  ); // URL webhook production (workflow đã active)

  useEffect(() => {
    fetchAppointmentDetail();
  }, [id]);

  const fetchAppointmentDetail = async () => {
    try {
      const response = await getAppointmentDetail(id);
      if (response && response.success) {
        setAppointment(response.data);
        setReason(response.data.reason || "");
        setNotes(response.data.notes || "");
      } else {
        toast.error("Không thể tải thông tin lịch khám!");
        navigate("/doctor");
      }
    } catch (error) {
      console.error("Error fetching appointment:", error);
      toast.error("Đã có lỗi xảy ra!");
      navigate("/doctor");
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteAppointment = async (e) => {
    e.preventDefault();

    if (!reason.trim()) {
      toast.warning("Vui lòng nhập lý do khám!");
      return;
    }

    if (!notes.trim()) {
      toast.warning("Vui lòng nhập ghi chú khám bệnh!");
      return;
    }

    setUpdating(true);
    try {
      const data = {
        reason: reason,
        notes: notes,
        webhook_url: webhookUrl,
      };

      const response = await completeAppointment(id, data);

      if (response && response.success) {
        toast.success("Hoàn thành lịch khám thành công!");
        
        // Hiển thị thông báo về webhook
        if (response.webhook?.success) {
          toast.success("✅ " + response.webhook.message);
        } else if (response.webhook?.message) {
          toast.warning("⚠️ " + response.webhook.message);
        }

        // Quay lại dashboard sau 2 giây
        setTimeout(() => {
          navigate("/doctor");
        }, 2000);
      } else {
        toast.error("Không thể hoàn thành lịch khám!");
      }
    } catch (error) {
      console.error("Error completing appointment:", error);
      toast.error("Đã có lỗi xảy ra!");
    } finally {
      setUpdating(false);
    }
  };

  const handleBack = () => {
    navigate("/doctor");
  };

  if (loading) {
    return (
      <div className="appointment-detail">
        <div className="loading">Đang tải dữ liệu...</div>
      </div>
    );
  }

  if (!appointment) {
    return null;
  }

  const isCompleted = appointment.status === "COMPLETED";

  return (
    <div className="appointment-detail">
      <div className="detail-container">
        <div className="detail-header">
          <button className="btn-back" onClick={handleBack}>
            ← Quay lại
          </button>
          <h1 className="detail-title">Chi Tiết Lịch Khám</h1>
        </div>

        <div className="detail-content">
          {/* Thông tin bệnh nhân */}
          <div className="info-section">
            <h2 className="section-title">👤 Thông Tin Bệnh Nhân</h2>
            <div className="info-grid">
              <div className="info-item">
                <span className="item-label">Họ tên:</span>
                <span className="item-value">{appointment.patient.full_name}</span>
              </div>
              <div className="info-item">
                <span className="item-label">Ngày sinh:</span>
                <span className="item-value">{appointment.patient.date_of_birth}</span>
              </div>
              <div className="info-item">
                <span className="item-label">Giới tính:</span>
                <span className="item-value">
                  {appointment.patient.gender === "MALE" ? "Nam" : "Nữ"}
                </span>
              </div>
              <div className="info-item">
                <span className="item-label">Nhóm máu:</span>
                <span className="item-value">{appointment.patient.blood_type}</span>
              </div>
              <div className="info-item">
                <span className="item-label">Điện thoại:</span>
                <span className="item-value">{appointment.patient.phone}</span>
              </div>
              <div className="info-item">
                <span className="item-label">Email:</span>
                <span className="item-value">{appointment.patient.email}</span>
              </div>
              <div className="info-item full-width">
                <span className="item-label">Địa chỉ:</span>
                <span className="item-value">{appointment.patient.address}</span>
              </div>
              {appointment.patient.allergies && (
                <div className="info-item full-width alert">
                  <span className="item-label">⚠️ Dị ứng:</span>
                  <span className="item-value">{appointment.patient.allergies}</span>
                </div>
              )}
            </div>
          </div>

          {/* Thông tin lịch khám */}
          <div className="info-section">
            <h2 className="section-title">📋 Thông Tin Lịch Khám</h2>
            <div className="info-grid">
              <div className="info-item">
                <span className="item-label">Ngày khám:</span>
                <span className="item-value">{appointment.appointment_date}</span>
              </div>
              <div className="info-item">
                <span className="item-label">Khung giờ:</span>
                <span className="item-value">{appointment.time_slot}</span>
              </div>
              <div className="info-item">
                <span className="item-label">Trạng thái:</span>
                <span className={`status-badge status-${appointment.status.toLowerCase()}`}>
                  {appointment.status === "SCHEDULED" && "Đã đặt lịch"}
                  {appointment.status === "CONFIRMED" && "Đã xác nhận"}
                  {appointment.status === "COMPLETED" && "Hoàn thành"}
                  {appointment.status === "CANCELLED" && "Đã hủy"}
                </span>
              </div>
            </div>
          </div>

          {/* Form cập nhật (chỉ hiện khi chưa completed) */}
          {!isCompleted && (
            <div className="info-section form-section">
              <h2 className="section-title">✍️ Cập Nhật Thông Tin Khám</h2>
              <form onSubmit={handleCompleteAppointment}>
                <div className="form-group">
                  <label>Lý do khám *</label>
                  <textarea
                    rows="3"
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                    placeholder="Nhập lý do khám bệnh..."
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Ghi chú khám bệnh *</label>
                  <textarea
                    rows="5"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Nhập ghi chú chi tiết về tình trạng bệnh, chẩn đoán, kê đơn..."
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Webhook URL n8n (Tùy chọn)</label>
                  <input
                    type="url"
                    value={webhookUrl}
                    onChange={(e) => setWebhookUrl(e.target.value)}
                    placeholder="https://your-n8n-instance.com/webhook/..."
                  />
                  <small className="form-help">
                    Sau khi hoàn thành, hệ thống sẽ gửi thông tin bệnh nhân tới n8n để tạo hồ sơ.
                  </small>
                </div>

                <div className="form-actions">
                  <button
                    type="button"
                    className="btn-cancel"
                    onClick={handleBack}
                    disabled={updating}
                  >
                    Hủy
                  </button>
                  <button type="submit" className="btn-submit" disabled={updating}>
                    {updating ? "Đang xử lý..." : "Hoàn thành khám"}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Hiển thị thông tin đã hoàn thành */}
          {isCompleted && (
            <div className="info-section completed-section">
              <h2 className="section-title">✅ Thông Tin Khám Đã Hoàn Thành</h2>
              <div className="completed-info">
                <div className="info-item full-width">
                  <span className="item-label">Lý do khám:</span>
                  <span className="item-value">{appointment.reason}</span>
                </div>
                <div className="info-item full-width">
                  <span className="item-label">Ghi chú khám bệnh:</span>
                  <span className="item-value">{appointment.notes}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
