import axios from "../utils/AxiosCustom.js";

// Lấy danh sách feedback tasks
const getFeedbackTasks = (status = null) => {
  const url = status ? `feedback/tasks/?status=${status}` : `feedback/tasks/`;
  return axios.get(url);
};

// Lấy chi tiết một feedback task
const getFeedbackTaskDetail = (taskId) => {
  return axios.get(`feedback/tasks/${taskId}/`);
};

// Cập nhật trạng thái task (Pending -> Finished)
const updateTaskStatus = (taskId, status) => {
  return axios.patch(`feedback/tasks/${taskId}/update-status/`, { status });
};

// Xóa feedback task
const deleteFeedbackTask = (taskId) => {
  return axios.delete(`feedback/tasks/${taskId}/delete/`);
};

export {
  getFeedbackTasks,
  getFeedbackTaskDetail,
  updateTaskStatus,
  deleteFeedbackTask,
};
