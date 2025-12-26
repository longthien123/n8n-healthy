import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getFeedbackTasks } from "../../services/FeedbackService";
import { toast } from "react-toastify";
import "./FeedbackTasks.css";

export default function FeedbackTasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("Pending"); // Pending hoặc Finished
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
  }, [filter]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await getFeedbackTasks(filter);

      if (response && response.success) {
        setTasks(response.data);
      } else {
        toast.error("Không thể tải danh sách feedback!");
      }
    } catch (error) {
      console.error("Error fetching tasks:", error);
      toast.error("Đã có lỗi xảy ra!");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetail = (taskId) => {
    navigate(`/admin/feedback/${taskId}`);
  };

  const getStatusBadge = (status) => {
    return status === "Pending" ? (
      <span className="feedback-status-badge pending">Chờ xử lý</span>
    ) : (
      <span className="feedback-status-badge finished">Đã hoàn thành</span>
    );
  };

  const getNegativeBadge = (hasNegative) => {
    return hasNegative ? (
      <span className="feedback-negative-badge">⚠️ Tiêu cực</span>
    ) : null;
  };

  if (loading) {
    return (
      <div className="feedback-tasks-container">
        <div className="loading-spinner">Đang tải dữ liệu...</div>
      </div>
    );
  }

  return (
    <div className="feedback-tasks-container">
      <div className="feedback-header">
        <h1 className="feedback-title">
          📋 Feedback Tasks
          <span className="task-count">({tasks.length})</span>
        </h1>

        <div className="feedback-filter">
          <button
            className={`filter-btn ${filter === "Pending" ? "active" : ""}`}
            onClick={() => setFilter("Pending")}
          >
            Chờ xử lý
          </button>
          <button
            className={`filter-btn ${filter === "Finished" ? "active" : ""}`}
            onClick={() => setFilter("Finished")}
          >
            Đã hoàn thành
          </button>
        </div>
      </div>

      {tasks.length === 0 ? (
        <div className="empty-state">
          <p>Không có feedback nào {filter === "Pending" ? "chờ xử lý" : "đã hoàn thành"}</p>
        </div>
      ) : (
        <div className="feedback-grid">
          {tasks.map((task) => (
            <div
              key={task.id}
              className={`feedback-card ${task.has_negative_feedback ? "has-negative" : ""}`}
              onClick={() => handleViewDetail(task.id)}
            >
              <div className="feedback-card-header">
                <div className="feedback-badges">
                  {getStatusBadge(task.status)}
                  {getNegativeBadge(task.has_negative_feedback)}
                </div>
                <span className="feedback-id">#{task.id}</span>
              </div>

              <div className="feedback-card-body">
                <div className="feedback-email">
                  <span className="email-icon">📧</span>
                  {task.customer_email}
                </div>

                <div className="feedback-scores">
                  {task.score_doctor_attitude && (
                    <div className="score-item">
                      <span className="score-label">Bác sĩ:</span>
                      <span className={`score-value ${task.score_doctor_attitude === "Tệ" ? "negative" : ""}`}>
                        {task.score_doctor_attitude}
                      </span>
                    </div>
                  )}
                  {task.score_waiting_time && (
                    <div className="score-item">
                      <span className="score-label">Thời gian chờ:</span>
                      <span className={`score-value ${task.score_waiting_time === "Lâu" ? "negative" : ""}`}>
                        {task.score_waiting_time}
                      </span>
                    </div>
                  )}
                  {task.score_cleanliness && (
                    <div className="score-item">
                      <span className="score-label">Vệ sinh:</span>
                      <span className={`score-value ${task.score_cleanliness === "Không" ? "negative" : ""}`}>
                        {task.score_cleanliness}
                      </span>
                    </div>
                  )}
                </div>

                {task.customer_comment && (
                  <div className="feedback-comment-preview">
                    <span className="comment-icon">💬</span>
                    <span className="comment-text">
                      {task.customer_comment.substring(0, 80)}
                      {task.customer_comment.length > 80 ? "..." : ""}
                    </span>
                  </div>
                )}
              </div>

              <div className="feedback-card-footer">
                <span className="feedback-date">
                  {new Date(task.created_at).toLocaleDateString("vi-VN", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
                <span className="view-detail-btn">Xem chi tiết →</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
