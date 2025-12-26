import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  getFeedbackTaskDetail,
  updateTaskStatus,
} from "../../services/FeedbackService";
import { toast } from "react-toastify";
import "./FeedbackDetail.css";

export default function FeedbackDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchTaskDetail();
  }, [id]);

  const fetchTaskDetail = async () => {
    try {
      const response = await getFeedbackTaskDetail(id);
      if (response && response.success) {
        setTask(response.data);
      } else {
        toast.error("Không thể tải thông tin feedback!");
        navigate("/admin/feedback");
      }
    } catch (error) {
      console.error("Error fetching task:", error);
      toast.error("Đã có lỗi xảy ra!");
      navigate("/admin/feedback");
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteTask = async () => {
    if (task.status === "Finished") {
      toast.info("Task này đã được hoàn thành rồi!");
      return;
    }

    setUpdating(true);
    try {
      const response = await updateTaskStatus(id, "Finished");
      if (response && response.success) {
        toast.success("Đã đánh dấu task hoàn thành!");
        setTimeout(() => {
          navigate("/admin/feedback");
        }, 1500);
      } else {
        toast.error("Không thể cập nhật trạng thái!");
      }
    } catch (error) {
      console.error("Error updating task:", error);
      toast.error("Đã có lỗi xảy ra!");
    } finally {
      setUpdating(false);
    }
  };

  const handleBack = () => {
    navigate("/admin/feedback");
  };

  if (loading) {
    return (
      <div className="feedback-detail-container">
        <div className="loading">Đang tải dữ liệu...</div>
      </div>
    );
  }

  if (!task) {
    return null;
  }

  const getScoreClass = (score) => {
    const negativeKeywords = ["Tệ", "Không", "Lâu"];
    return negativeKeywords.includes(score) ? "score-negative" : "score-positive";
  };

  return (
    <div className="feedback-detail-container">
      <div className="detail-header">
        <button className="btn-back" onClick={handleBack}>
          ← Quay lại
        </button>
        <h1 className="detail-title">Chi Tiết Feedback #{task.id}</h1>
      </div>

      <div className="detail-content">
        {/* Status và Email */}
        <div className="info-section">
          <div className="section-header">
            <h2 className="section-title">Thông tin chung</h2>
            <span
              className={`status-badge-large ${
                task.status === "Pending" ? "pending" : "finished"
              }`}
            >
              {task.status === "Pending" ? "Chờ xử lý" : "Đã hoàn thành"}
            </span>
          </div>

          <div className="info-grid">
            <div className="info-item">
              <span className="item-label">📧 Email khách hàng:</span>
              <span className="item-value">{task.customer_email}</span>
            </div>
            <div className="info-item">
              <span className="item-label">📅 Ngày tạo:</span>
              <span className="item-value">
                {new Date(task.created_at).toLocaleString("vi-VN")}
              </span>
            </div>
            {task.has_negative_feedback && (
              <div className="info-item full-width alert-negative">
                <span className="item-label">⚠️ Cảnh báo:</span>
                <span className="item-value">Feedback chứa đánh giá tiêu cực</span>
              </div>
            )}
          </div>
        </div>

        {/* Các điểm đánh giá */}
        <div className="info-section">
          <h2 className="section-title">📊 Đánh giá chi tiết</h2>
          <div className="scores-grid">
            {task.score_doctor_attitude && (
              <div className="score-card">
                <div className="score-question">
                  Thái độ thăm khám của Bác sĩ?
                </div>
                <div className={`score-answer ${getScoreClass(task.score_doctor_attitude)}`}>
                  {task.score_doctor_attitude}
                </div>
              </div>
            )}

            {task.score_doctor_clarity && (
              <div className="score-card">
                <div className="score-question">
                  Bác sĩ tư vấn có rõ ràng, dễ hiểu không?
                </div>
                <div className={`score-answer ${getScoreClass(task.score_doctor_clarity)}`}>
                  {task.score_doctor_clarity}
                </div>
              </div>
            )}

            {task.score_waiting_time && (
              <div className="score-card">
                <div className="score-question">
                  Thời gian chờ đợi có lâu không?
                </div>
                <div className={`score-answer ${getScoreClass(task.score_waiting_time)}`}>
                  {task.score_waiting_time}
                </div>
              </div>
            )}

            {task.score_procedure_speed && (
              <div className="score-card">
                <div className="score-question">
                  Thủ tục đăng ký/thanh toán có nhanh gọn không?
                </div>
                <div className={`score-answer ${getScoreClass(task.score_procedure_speed)}`}>
                  {task.score_procedure_speed}
                </div>
              </div>
            )}

            {task.score_cleanliness && (
              <div className="score-card">
                <div className="score-question">
                  Không gian phòng khám/bệnh viện có sạch sẽ không?
                </div>
                <div className={`score-answer ${getScoreClass(task.score_cleanliness)}`}>
                  {task.score_cleanliness}
                </div>
              </div>
            )}

            {task.score_staff_attitude && (
              <div className="score-card">
                <div className="score-question">
                  Đánh giá thái độ phục vụ của nhân viên tư vấn?
                </div>
                <div className={`score-answer ${getScoreClass(task.score_staff_attitude)}`}>
                  {task.score_staff_attitude}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Góp ý */}
        {task.customer_comment && (
          <div className="info-section">
            <h2 className="section-title">💬 Góp ý của khách hàng</h2>
            <div className="comment-box">
              <p>{task.customer_comment}</p>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="action-section">
          {task.status === "Pending" ? (
            <button
              className="btn-complete"
              onClick={handleCompleteTask}
              disabled={updating}
            >
              {updating ? "Đang xử lý..." : "✓ Hoàn thành Task"}
            </button>
          ) : (
            <div className="completed-message">
              ✅ Task này đã được hoàn thành
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
