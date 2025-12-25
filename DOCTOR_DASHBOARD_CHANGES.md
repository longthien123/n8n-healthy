# DOCTOR DASHBOARD - TỔNG HỢP THAY ĐỔI

## 📝 Tóm tắt
Đã thêm tính năng **Doctor Dashboard** để bác sĩ xem danh sách lịch khám và hoàn thành khám bệnh, kết hợp với n8n webhook để tạo hồ sơ bệnh tự động.

## 🔧 Backend - Những gì đã THÊM MỚI

### 1. File: `backend/appointments/views.py`
**Thêm 2 functions mới (dòng cuối file):**

```python
# ===== DOCTOR DASHBOARD VIEWS (THÊM MỚI) =====

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor_appointments(request, doctor_id):
    """
    API lấy danh sách lịch khám của bác sĩ (theo doctor_id)
    Sắp xếp theo ngày khám và khung giờ
    """
    # ... (code đã thêm)

@api_view(['POST'])
@permission_classes([AllowAny])
def complete_appointment(request, pk):
    """
    API hoàn thành lịch khám - Cập nhật status, reason, notes
    Sau khi cập nhật xong sẽ gọi webhook n8n
    """
    # ... (code đã thêm)
```

### 2. File: `backend/appointments/urls.py`
**Thêm 2 routes mới (cuối file, trước `]`):**

```python
# Doctor Dashboard endpoints (THÊM MỚI)
path('appointments/doctor/<int:doctor_id>/', views.get_doctor_appointments, name='get_doctor_appointments'),
path('appointments/<int:pk>/complete/', views.complete_appointment, name='complete_appointment'),
```

---

## 🎨 Frontend - Những gì đã THÊM MỚI

### 1. File: `frontend/src/services/AppointmentService.js`
**File mới - Service để gọi API:**
- `getDoctorAppointments(doctorId)` - Lấy danh sách lịch khám
- `getAppointmentDetail(appointmentId)` - Lấy chi tiết lịch khám
- `completeAppointment(appointmentId, data)` - Hoàn thành khám + gọi webhook
- `updateAppointment(appointmentId, data)` - Cập nhật lịch khám

### 2. File: `frontend/src/Layout.jsx`
**Thêm import (đầu file):**
```jsx
// THÊM MỚI: Import trang Doctor Dashboard
import DoctorDashboard from "./pages/doctor/DoctorDashboard";
import AppointmentDetail from "./pages/doctor/AppointmentDetail";
```

**Thêm routes (trước dòng `{/* <Route path="*" element={<NotFound />}></Route>  */}`):**
```jsx
{/* THÊM MỚI: Doctor Dashboard Routes */}
<Route path="/doctor" element={<DoctorDashboard />} />
<Route path="/doctor/appointment/:id" element={<AppointmentDetail />} />
```

### 3. File: `frontend/src/pages/auth/Login.jsx`
**ĐÃ CÓ SẴN** - Logic redirect bác sĩ:
```jsx
else if (data.data.user.role === "DOCTOR") {
  navigate("/doctor");
}
```

### 4. Các file components mới (ĐÃ TỒN TẠI):
- `frontend/src/pages/doctor/DoctorDashboard.jsx` - Trang dashboard bác sĩ
- `frontend/src/pages/doctor/DoctorDashboard.css` - CSS cho dashboard
- `frontend/src/pages/doctor/AppointmentDetail.jsx` - Trang chi tiết lịch khám
- `frontend/src/pages/doctor/AppointmentDetail.css` - CSS cho chi tiết

---

## 🚀 Cách sử dụng

### 1. Đăng nhập bác sĩ
- Username: `doctor01` hoặc `toan`
- Password: (cần biết password)
- Sau khi login → Tự động vào `/doctor`

### 2. Xem danh sách lịch khám
- Dashboard hiển thị tất cả lịch khám
- Có filter theo status: Tất cả, Đã đặt lịch, Đã xác nhận, Hoàn thành

### 3. Hoàn thành khám bệnh
- Click vào card lịch khám
- Điền "Lý do khám" và "Ghi chú khám bệnh"
- Nhập URL webhook n8n (hoặc để mặc định)
- Click "Hoàn thành khám"
- Hệ thống sẽ:
  - Cập nhật status = COMPLETED
  - Gọi webhook n8n với đầy đủ thông tin bệnh nhân
  - Hiển thị toast notification kết quả

---

## 🔗 API Endpoints mới

### 1. Lấy lịch khám của bác sĩ
```
GET /api/appointments/appointments/doctor/<doctor_id>/
```
Response:
```json
{
  "success": true,
  "data": [...],
  "count": 5
}
```

### 2. Hoàn thành lịch khám
```
POST /api/appointments/appointments/<appointment_id>/complete/
```
Body:
```json
{
  "reason": "Khám da liễu",
  "notes": "Chẩn đoán...",
  "webhook_url": "https://n8n.com/webhook/..."
}
```

Response:
```json
{
  "success": true,
  "message": "Hoàn thành lịch khám thành công",
  "data": {...},
  "webhook": {
    "success": true,
    "message": "Webhook đã được gọi thành công"
  }
}
```

---

## 📦 Dữ liệu gửi tới n8n webhook

```json
{
  "appointment_id": 1,
  "patient": {
    "id": 1,
    "user_id": 2,
    "full_name": "Trần Thị Bình",
    "email": "email@example.com",
    "phone": "0123456789",
    "date_of_birth": "1990-01-01",
    "gender": "FEMALE",
    "blood_type": "O+",
    "address": "123 Đường ABC",
    "allergies": "Dị ứng...",
    "emergency_contact": "0987654321"
  },
  "doctor": {
    "id": 1,
    "full_name": "Nguyễn Văn An",
    "specialization": "Bác sĩ y khoa"
  },
  "appointment": {
    "date": "2025-11-28",
    "time_slot": "08:00-09:00",
    "status": "COMPLETED",
    "reason": "Khám da liễu",
    "notes": "Chẩn đoán chi tiết...",
    "created_at": "2025-11-20T10:00:00",
    "updated_at": "2025-12-24T15:30:00"
  }
}
```

---

## ⚠️ Lưu ý quan trọng

1. **Code cũ KHÔNG bị ảnh hưởng** - Chỉ thêm mới, không sửa code hiện tại
2. **n8n webhook URL** - Cần thay URL mặc định bằng URL thật của bạn
3. **Permission** - Hiện tại dùng `AllowAny` cho dễ test, nên đổi thành `IsAuthenticated` khi deploy
4. **Doctor ID** - Lấy từ `user.id` trong sessionStorage (giả sử user.id = doctor.id)

---

## 🎯 Testing checklist

- [ ] Backend server chạy: `python manage.py runserver`
- [ ] Frontend server chạy: `npm run dev`
- [ ] Đăng nhập bác sĩ thành công
- [ ] Dashboard hiển thị danh sách lịch khám
- [ ] Filter theo status hoạt động
- [ ] Click vào lịch khám → Vào trang chi tiết
- [ ] Form hoàn thành khám hiển thị đúng
- [ ] Submit form → Cập nhật DB thành công
- [ ] Webhook n8n được gọi thành công
- [ ] Toast notification hiển thị kết quả

---

**Tác giả:** GitHub Copilot  
**Ngày tạo:** 24/12/2025  
**Branch:** feature/finishMedicalExamination
