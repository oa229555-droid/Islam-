#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام الإشعارات التلقائية للأذكار والصلوات
"""

from plyer import notification
from datetime import datetime
from typing import Dict, Optional


class NotificationManager:
    """مدير الإشعارات التلقائية"""
    
    def __init__(self):
        self.dhikr_reminders = {
            "morning": {"time": "06:00", "title": "🌸 أذكار الصباح", 
                       "message": "قل: أصبحنا وأصبح الملك لله"},
            "evening": {"time": "18:00", "title": "🌙 أذكار المساء",
                       "message": "قل: أمسينا وأمسى الملك لله"},
            "duha": {"time": "08:00", "title": "☀️ صلاة الضحى",
                    "message": "حان وقت صلاة الضحى - ركعتان"},
            "istighfar": {"time": "12:00", "title": "🕌 أذكار الظهيرة",
                         "message": "استغفر الله العظيم"},
            "night": {"time": "21:00", "title": "✨ أذكار النوم",
                     "message": "قل: باسمك اللهم أموت وأحيا"},
            "quran": {"time": "10:00", "title": "📖 تذكير بالقرآن",
                     "message": "خصص ورداً يومياً من القرآن"},
            "sadaqah": {"time": "14:00", "title": "🤲 ذكرى الصدقة",
                       "message": "ولو بتمرة، فإن الله يجزي بها"},
        }
        self.last_notifications = {}
    
    def check_and_notify(self) -> Optional[Dict]:
        """التحقق من الوقت وإرسال الإشعارات"""
        now = datetime.now().strftime("%H:%M")
        
        for key, reminder in self.dhikr_reminders.items():
            if reminder["time"] == now:
                if key not in self.last_notifications or \
                   self.last_notifications[key] != datetime.now().date():
                    self.send_notification(reminder["title"], reminder["message"])
                    self.last_notifications[key] = datetime.now().date()
                    return reminder
        return None
    
    def send_notification(self, title: str, message: str):
        """إرسال إشعار"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Titan Islamic",
                timeout=10,
                ticker="تذكير إسلامي"
            )
        except Exception as e:
            print(f"فشل إرسال الإشعار: {e}")
    
    def send_prayer_notification(self, prayer_name: str, prayer_time: str):
        """إرسال إشعار بموعد الصلاة"""
        title = f"🕌 أذان {prayer_name}"
        message = f"حان الآن موعد صلاة {prayer_name} - {prayer_time}"
        self.send_notification(title, message)
