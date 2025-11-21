# Tạo file: /home/longthien/VKU/n8n-health/backend/n8n/management/commands/test_reminders.py
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
    help = "Test reminders - gửi webhook ngay lập tức"

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='all',
            choices=['morning', 'afternoon', 'all'],
            help='Loại reminder cần test: morning/afternoon/all'
        )

    def handle(self, *args, **options):
        self.stdout.write("🚀 Bắt đầu test reminders...")
        
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        reminder_type = options['type']

        # Test nhắc lịch buổi sáng (như lúc 20h hôm trước)
        if reminder_type in ['morning', 'all']:
            self.stdout.write("\n📅 Test nhắc lịch buổi SÁNG ngày mai:")
            appointments = Appointment.objects.filter(
                appointment_date=tomorrow,
                status="SCHEDULED"
            )
            
            morning_count = 0
            for appt in appointments:
                if is_morning(appt.time_slot):
                    self.process_appointment(appt, "Nhắc buổi sáng")
                    morning_count += 1
            
            self.stdout.write(f"📊 Đã xử lý {morning_count} lịch hẹn buổi sáng")

        # Test nhắc lịch buổi chiều (như lúc 7h sáng)
        if reminder_type in ['afternoon', 'all']:
            self.stdout.write("\n🌅 Test nhắc lịch buổi CHIỀU hôm nay:")
            appointments = Appointment.objects.filter(
                appointment_date=today,
                status="SCHEDULED"
            )
            
            afternoon_count = 0
            for appt in appointments:
                if is_afternoon(appt.time_slot):
                    self.process_appointment(appt, "Nhắc buổi chiều")
                    afternoon_count += 1
                    
            self.stdout.write(f"📊 Đã xử lý {afternoon_count} lịch hẹn buổi chiều")

        self.stdout.write("\n✅ Test hoàn thành!")

    def process_appointment(self, appointment, reminder_type):
        patient_name = appointment.patient.user.full_name
        doctor_name = appointment.doctor.user.full_name
        
        self.stdout.write(f"🔍 Kiểm tra: {patient_name} - BS.{doctor_name} - {appointment.time_slot}")
        
        if appointment.reminder_enabled:
            self.stdout.write(f"⏭️  Bỏ qua (reminder_enabled = True)")
        else:
            self.stdout.write(f"📤 Gửi webhook ({reminder_type})")
            self.send_to_n8n(appointment, reminder_type)

    def send_to_n8n(self, appointment, reminder_type):
        url = "http://localhost:5678/webhook/send-reminders"
        
        payload = {
            "id": appointment.id,
            "date": str(appointment.appointment_date),
            "time_slot": appointment.time_slot,
            "status": appointment.status,
            "patient_name": appointment.patient.user.full_name,
            "doctor_name": appointment.doctor.user.full_name,
            "reminder_type": reminder_type,
            "source": "test_command"
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"  ✅ Webhook thành công"))
                appointment.reminder_enabled = True 
                appointment.save(update_fields=['reminder_enabled'])
            else:
                self.stdout.write(self.style.WARNING(f"  ⚠️ Webhook lỗi: {response.status_code}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Lỗi kết nối: {str(e)}"))