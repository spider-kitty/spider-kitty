from django.db import models
from django.utils import timezone
from datetime import datetime

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Added this field
    due_date = models.DateField()          # تاریخ سررسید
    due_time = models.TimeField()          # ساعت سررسید
    done = models.BooleanField(default=False)  # انجام شده یا نه
    
    def __str__(self):
        status = "done" if self.done else "undone"
        return f"{self.title} - {self.due_date} {self.due_time} ({status})"


    @classmethod
    def overdue_unfinished(cls):  # Renamed for clarity
        now = timezone.now()
        time_str = now.strftime('%H:%M:%S')  # تبدیل به رشته قابل فهم برای SQLite
        return cls.objects.filter(
            done=False
        ).extra(
            where=["(due_date < %s) OR (due_date = %s AND due_time < %s)"],
            params=[now.date(), now.date(), time_str]
        )