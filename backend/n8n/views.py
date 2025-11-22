from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

# gọi n8n send email khi đặt lịch thành công
@api_view(["POST"])
def send_booking_to_n8n(request):
    data = request.data  # Nhận dữ liệu từ frontend
    doctor_id = data.get("doctor")
    patient_id = data.get("patient")

    if not doctor_id or not patient_id:
        return Response(
            {"error": "Missing doctor or patient id"},
            status=status.HTTP_400_BAD_REQUEST
        )
    print(data, "requesst")
     # ================================
    # 1️⃣ Lấy thông tin doctor từ API
    # ================================
    try:
        doctor_res = requests.get(f"http://127.0.0.1:8000/api/users/doctors/{doctor_id}/")
        doctor_res.raise_for_status()
        doctor_data = doctor_res.json()
    except Exception as e:
        return Response(
            {"error": "Cannot fetch doctor info", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # ================================
    # 2️⃣ Lấy thông tin patient từ API
    # ================================
    try:
        patient_res = requests.get(f"http://127.0.0.1:8000/api/users/patients/{patient_id}/")
        patient_res.raise_for_status()
        patient_data = patient_res.json()
    except Exception as e:
        return Response(
            {"error": "Cannot fetch patient info", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # ================================
    # 3️⃣ Payload gửi lên n8n
    # ================================
    payload = {
        "appointment": {
            "appointment_date": data.get("appointment_date"),
            "time_slot": data.get("time_slot"),
            "reason": data.get("reason"),
            "notes": data.get("notes"),
        },
        "doctor": doctor_data,
        "patient": patient_data,
    }

    # Gọi webhook n8n
    try:
        response = requests.post(
            "https://son-ardeid-dobsonfly.ngrok-free.dev/webhook-test/421354db-d81c-4145-aa7d-d24f7a601000",  # Thay bằng URL của bạn
            json=payload,
            timeout=5
        )
        response.raise_for_status()  # Raise lỗi nếu n8n trả về lỗi

    except requests.exceptions.RequestException as e:
        return Response({"error": "Cannot send data to n8n", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Data sent to n8n successfully"}, status=status.HTTP_200_OK)
