from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import requests

from appointments.models import Appointment

def is_morning(time_slot: str) -> bool:
    start_hour = int(time_slot.split('-')[0].split(':')[0])
    return 8 <= start_hour < 12

def is_afternoon(time_slot: str) -> bool:
    start_hour = int(time_slot.split('-')[0].split(':')[0])
    return 14 <= start_hour < 18

class Command(BaseCommand):
    help = "Check appointments and send reminders to n8n"

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Chạy test mode - gửi webhook ngay lập tức'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset reminder_enabled về False để test lại'
        )

    def handle(self, *args, **options):
        # Reset reminder_enabled nếu có flag --reset
        if options['reset']:
            reset_count = Appointment.objects.filter(
                reminder_enabled=True
            ).update(reminder_enabled=False)
            self.stdout.write(
                self.style.SUCCESS(f"🔄 Đã reset {reset_count} lịch hẹn về reminder_enabled=False")
            )
            return

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        if options['test']:
            # TEST MODE - gửi webhook ngay
            self.stdout.write(self.style.SUCCESS("🧪 CHẠY TEST MODE"))
            self.test_all_reminders(today, tomorrow)
        else:
            # PRODUCTION MODE - chỉ gửi đúng giờ
            now = timezone.localtime()
            current_hour = now.hour
            
            self.stdout.write(f"🕐 Thời gian hiện tại: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            self.stdout.write(f"⏰ Kiểm tra giờ: {current_hour}h")
            
            if current_hour == 20:
                self.stdout.write("🌆 Đúng 20h - Gửi nhắc lịch buổi sáng ngày mai")
                self.send_morning_reminders(tomorrow)
            elif current_hour == 7:
                self.stdout.write("🌅 Đúng 7h - Gửi nhắc lịch buổi chiều hôm nay")
                self.send_afternoon_reminders(today)
            else:
                self.stdout.write(f"⏭️ Không phải giờ gửi nhắc (hiện tại: {current_hour}h, cần: 7h hoặc 20h)")
                return

    def test_all_reminders(self, today, tomorrow):
        """Test mode - gửi tất cả reminders"""
        # Test nhắc buổi sáng
        self.stdout.write("📅 Test nhắc lịch buổi SÁNG ngày mai:")
        morning_appointments = self.get_morning_appointments(tomorrow)
        if morning_appointments:
            self.send_batch_reminders(morning_appointments, "morning")
        else:
            self.stdout.write("  ℹ️ Không có lịch buổi sáng nào")

        # Test nhắc buổi chiều  
        self.stdout.write("\n🌅 Test nhắc lịch buổi CHIỀU hôm nay:")
        afternoon_appointments = self.get_afternoon_appointments(today)
        if afternoon_appointments:
            self.send_batch_reminders(afternoon_appointments, "afternoon")
        else:
            self.stdout.write("  ℹ️ Không có lịch buổi chiều nào")

    def send_morning_reminders(self, tomorrow):
        """Gửi nhắc lịch buổi sáng lúc 20h"""
        self.stdout.write("📅 Gửi nhắc lịch buổi sáng ngày mai...")
        appointments = self.get_morning_appointments(tomorrow)
        if appointments:
            self.send_batch_reminders(appointments, "morning")

    def send_afternoon_reminders(self, today):
        """Gửi nhắc lịch buổi chiều lúc 7h"""
        self.stdout.write("🌅 Gửi nhắc lịch buổi chiều hôm nay...")
        appointments = self.get_afternoon_appointments(today)
        if appointments:
            self.send_batch_reminders(appointments, "afternoon")

    def get_morning_appointments(self, date):
        """Lấy lịch hẹn buổi sáng chưa nhắc"""
        appointments = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).filter(
            appointment_date=date,
            status="SCHEDULED",
            reminder_enabled=False  # Chỉ lấy lịch chưa nhắc
        )
        
        return [appt for appt in appointments if is_morning(appt.time_slot)]

    def get_afternoon_appointments(self, date):
        """Lấy lịch hẹn buổi chiều chưa nhắc"""
        appointments = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).filter(
            appointment_date=date,
            status="SCHEDULED",
            reminder_enabled=False  # Chỉ lấy lịch chưa nhắc
        )
        
        return [appt for appt in appointments if is_afternoon(appt.time_slot)]

    def send_batch_reminders(self, appointments, reminder_type):
        """Gửi một mảng lịch hẹn đến webhook"""
        if not appointments:
            return

        # Chuẩn bị dữ liệu gửi
        appointments_data = []
        appointment_ids = []
        
        for appt in appointments:
            appointment_ids.append(appt.id)
            appointments_data.append({
                "id": appt.id,
                "date": str(appt.appointment_date),
                "time_slot": appt.time_slot,
                "status": appt.status,
                "patient_name": appt.patient.user.full_name,
                "patient_email": appt.patient.user.email,
                "patient_phone": appt.patient.user.phone,
                "doctor_name": appt.doctor.user.full_name,
                "reason": appt.reason or "Không có ghi chú",
                "notes": appt.notes or "",
            })

        payload = {
            "reminder_type": reminder_type,
            "total_appointments": len(appointments_data),
            "appointments": appointments_data,
            "timestamp": timezone.now().isoformat()
        }

        self.stdout.write(f"📤 Đang gửi {len(appointments_data)} lịch hẹn đến webhook...")
        self.stdout.write("⏳ Đang chờ n8n xử lý và trả về response...")
        
        # Gửi webhook và nhận response
        webhook_response = self.send_to_n8n(payload)
        
        # Kiểm tra response từ webhook
        if webhook_response is not None:
            success = webhook_response.get('output', False)
            
            if success:
                # Cập nhật reminder_enabled = True cho tất cả lịch đã gửi
                updated_count = Appointment.objects.filter(
                    id__in=appointment_ids
                ).update(reminder_enabled=True)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ n8n trả về success=True! Đã cập nhật reminder_enabled=True cho {updated_count} lịch hẹn"
                    )
                )
                
                # In chi tiết các lịch đã cập nhật
                self.stdout.write("\n📋 Chi tiết các lịch hẹn đã xử lý:")
                for appt in appointments:
                    self.stdout.write(
                        f"  ✉️  ID {appt.id}: {appt.patient.user.full_name} ({appt.patient.user.email}) - {appt.time_slot}"
                    )
            else:
                # n8n trả về success=False
                error_message = webhook_response.get('message', 'Không có thông tin lỗi')
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ n8n trả về success=False: {error_message}\n"
                        f"   Không cập nhật reminder_enabled"
                    )
                )
                
                # In danh sách các lịch không xử lý được
                self.stdout.write("\n📋 Các lịch hẹn KHÔNG được xử lý:")
                for appt in appointments:
                    self.stdout.write(
                        f"  ❌ ID {appt.id}: {appt.patient.user.full_name} ({appt.patient.user.email})"
                    )
        else:
            # Không nhận được response từ webhook
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Không nhận được response từ webhook\n"
                    f"   Không cập nhật reminder_enabled"
                )
            )

    def send_to_n8n(self, payload):
        """
        Gửi dữ liệu đến n8n webhook và nhận response
        Trả về: dict response từ webhook hoặc None nếu lỗi
        """
        url = "http://localhost:5678/webhook/send-reminders"
        
        try:
            # Tăng timeout lên 120 giây để chờ n8n xử lý (gửi email)
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                self.stdout.write(f"  ✅ Nhận được response từ webhook - Status: {response.status_code}")
                
                try:
                    # Parse JSON response từ webhook
                    response_data = response.json()
                    self.stdout.write(f"  📥 Response data: {response_data}")
                    return response_data
                    
                except ValueError:
                    self.stdout.write(
                        self.style.WARNING("  ⚠️ Webhook không trả về JSON hợp lệ")
                    )
                    return None
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠️ Webhook lỗi - Status: {response.status_code}, Response: {response.text}"
                    )
                )
                return None
                
        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.ERROR(
                    "  ❌ Timeout: Webhook không phản hồi trong 120 giây\n"
                    "     n8n có thể đang xử lý nhưng mất quá nhiều thời gian"
                )
            )
            return None
            
        except requests.exceptions.ConnectionError:
            self.stdout.write(
                self.style.ERROR(
                    f"  ❌ Lỗi kết nối: Không thể kết nối đến webhook\n"
                    f"     Kiểm tra n8n có đang chạy không? URL: {url}"
                )
            )
            return None
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f"  ❌ Lỗi request webhook: {str(e)}")
            )
            return None
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"  ❌ Lỗi không xác định: {str(e)}")
            )
            return None

