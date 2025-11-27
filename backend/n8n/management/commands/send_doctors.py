from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import requests

from appointments.models import Appointment

def is_morning(time_slot: str) -> bool:
    """Kiểm tra khung giờ buổi sáng (7h-12h)"""
    start_hour = int(time_slot.split('-')[0].split(':')[0])
    return 7 <= start_hour < 12

def is_afternoon(time_slot: str) -> bool:
    """Kiểm tra khung giờ buổi chiều (13h-18h)"""
    start_hour = int(time_slot.split('-')[0].split(':')[0])
    return 13 <= start_hour < 18

class Command(BaseCommand):
    help = "Gửi lịch khám của bác sĩ lúc 7h30 sáng và 12h30 trưa"

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Chạy test mode - gửi webhook ngay lập tức'
        )

    def handle(self, *args, **options):
        today = timezone.localdate()

        if options['test']:
            # TEST MODE - gửi webhook ngay
            self.stdout.write(self.style.SUCCESS("🧪 CHẠY TEST MODE"))
            self.test_all_schedules(today)
        else:
            # PRODUCTION MODE - chỉ gửi đúng giờ
            now = timezone.localtime()
            current_hour = now.hour
            current_minute = now.minute
            
            self.stdout.write(f"🕐 Thời gian hiện tại: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Kiểm tra 7h30 sáng
            if current_hour == 7 and current_minute == 30:
                self.stdout.write("🌅 Đúng 7h30 sáng - Gửi lịch buổi sáng cho bác sĩ")
                self.send_morning_schedules(today)
            # Kiểm tra 12h30 trưa
            elif current_hour == 12 and current_minute == 30:
                self.stdout.write("🌆 Đúng 12h30 trưa - Gửi lịch buổi chiều cho bác sĩ")
                self.send_afternoon_schedules(today)
            else:
                self.stdout.write(f"⏭️ Không phải giờ gửi lịch (hiện tại: {current_hour}h{current_minute:02d}, cần: 7h30 hoặc 12h30)")
                return

    def test_all_schedules(self, today):
        """Test mode - gửi tất cả lịch khám"""
        # Test lịch buổi sáng
        self.stdout.write("📅 Test lịch khám buổi SÁNG:")
        self.send_morning_schedules(today)

        # Test lịch buổi chiều  
        self.stdout.write("\n🌅 Test lịch khám buổi CHIỀU:")
        self.send_afternoon_schedules(today)

    def send_morning_schedules(self, date):
        """Gửi lịch khám buổi sáng cho bác sĩ lúc 7h30"""
        self.stdout.write("📅 Lấy lịch khám buổi sáng...")
        appointments = self.get_morning_appointments(date)
        
        if appointments:
            doctors_schedules = self.group_by_doctor(appointments)
            self.send_to_webhook(doctors_schedules, "morning")
        else:
            self.stdout.write("  ℹ️ Không có lịch khám buổi sáng nào")

    def send_afternoon_schedules(self, date):
        """Gửi lịch khám buổi chiều cho bác sĩ lúc 12h30"""
        self.stdout.write("🌅 Lấy lịch khám buổi chiều...")
        appointments = self.get_afternoon_appointments(date)
        
        if appointments:
            doctors_schedules = self.group_by_doctor(appointments)
            self.send_to_webhook(doctors_schedules, "afternoon")
        else:
            self.stdout.write("  ℹ️ Không có lịch khám buổi chiều nào")

    def get_morning_appointments(self, date):
        """Lấy lịch hẹn buổi sáng"""
        appointments = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).filter(
            appointment_date=date,
            status="SCHEDULED"
        )
        
        return [appt for appt in appointments if is_morning(appt.time_slot)]

    def get_afternoon_appointments(self, date):
        """Lấy lịch hẹn buổi chiều"""
        appointments = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).filter(
            appointment_date=date,
            status="SCHEDULED"
        )
        
        return [appt for appt in appointments if is_afternoon(appt.time_slot)]

    def group_by_doctor(self, appointments):
        """Nhóm lịch khám theo bác sĩ"""
        doctors_dict = {}
        
        for appt in appointments:
            doctor_id = appt.doctor.id
            
            if doctor_id not in doctors_dict:
                doctors_dict[doctor_id] = {
                    "doctor_id": doctor_id,
                    "doctor_name": appt.doctor.user.full_name,
                    "doctor_email": appt.doctor.user.email,
                    "doctor_phone": appt.doctor.user.phone,
                    "appointments": []
                }
            
            doctors_dict[doctor_id]["appointments"].append({
                "appointment_id": appt.id,
                "patient_name": appt.patient.user.full_name,
                "time_slot": appt.time_slot,
                "appointment_date": str(appt.appointment_date),
                "reason": appt.reason or "Không có ghi chú",
                "notes": appt.notes or ""
            })
        
        # Chuyển dict thành list
        return list(doctors_dict.values())

    def send_to_webhook(self, doctors_schedules, schedule_type):
        """Gửi dữ liệu đến n8n webhook"""
        payload = {
            "schedule_type": schedule_type,
            "total_doctors": len(doctors_schedules),
            "doctors": doctors_schedules,
            "timestamp": timezone.now().isoformat()
        }

        self.stdout.write(f"📤 Đang gửi lịch khám của {len(doctors_schedules)} bác sĩ đến webhook...")
        
        # In chi tiết
        for doctor in doctors_schedules:
            self.stdout.write(
                f"  👨‍⚕️ BS. {doctor['doctor_phone']} - {len(doctor['appointments'])} lịch khám"
            )
        
        # Gửi webhook (không cần đợi response)
        self.send_to_n8n(payload)
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Đã gửi lịch khám của {len(doctors_schedules)} bác sĩ đến n8n!")
        )

    def send_to_n8n(self, payload):
        """Gửi dữ liệu đến n8n webhook - không đợi response"""
        url = "https://longthien.duckdns.org/webhook/send-doctor-schedules"
        
        try:
            # Gửi request và không đợi response (timeout ngắn)
            requests.post(url, json=payload, timeout=2)
            self.stdout.write(f"  ✅ Đã gửi request đến webhook")
            
        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.WARNING("  ⚠️ Request timeout nhưng dữ liệu có thể đã được gửi")
            )
            
        except requests.exceptions.ConnectionError:
            self.stdout.write(
                self.style.ERROR(f"  ❌ Lỗi kết nối đến webhook: {url}")
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"  ⚠️ Lỗi khi gửi: {str(e)}")
            )