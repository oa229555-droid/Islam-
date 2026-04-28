#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مواقيت الصلاة - جلب من API مع تخزين محلي
"""

import requests
import json
from datetime import datetime
from typing import Dict, Tuple


class PrayerTimesManager:
    """مدير مواقيت الصلاة"""
    
    def __init__(self, city: str = "Cairo", country: str = "EG"):
        self.city = city
        self.country = country
        self.prayer_times: Dict[str, str] = {}
        self.last_update = None
        self.api_url = "http://api.aladhan.com/v1/timingsByCity"
    
    def fetch_times(self) -> bool:
        """جلب مواقيت الصلاة من API"""
        try:
            params = {
                "city": self.city,
                "country": self.country,
                "method": 5  # طريقة رابطة العالم الإسلامي
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                timings = data.get("data", {}).get("timings", {})
                
                self.prayer_times = {
                    "Fajr": timings.get("Fajr", "05:00"),
                    "Sunrise": timings.get("Sunrise", "06:00"),
                    "Dhuhr": timings.get("Dhuhr", "12:00"),
                    "Asr": timings.get("Asr", "15:00"),
                    "Maghrib": timings.get("Maghrib", "18:00"),
                    "Isha": timings.get("Isha", "19:00"),
                }
                self.last_update = datetime.now()
                return True
        except Exception as e:
            print(f"خطأ في جلب مواقيت الصلاة: {e}")
        
        # بيانات افتراضية
        self.prayer_times = {
            "Fajr": "05:00", "Sunrise": "06:00", "Dhuhr": "12:00",
            "Asr": "15:00", "Maghrib": "18:00", "Isha": "19:00"
        }
        return False
    
    def get_next_prayer(self) -> Tuple[str, str]:
        """جلب أقرب صلاة قادمة"""
        now = datetime.now().strftime("%H:%M")
        
        prayers_order = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
        
        for prayer in prayers_order:
            if prayer in self.prayer_times:
                time_str = self.prayer_times[prayer]
                if time_str > now:
                    return prayer, time_str
        
        return "Fajr", self.prayer_times.get("Fajr", "05:00")
    
    def get_prayer_name_ar(self, prayer: str) -> str:
        """ترجمة اسم الصلاة للعربية"""
        names = {
            "Fajr": "الفجر", "Sunrise": "الشروق",
            "Dhuhr": "الظهر", "Asr": "العصر",
            "Maghrib": "المغرب", "Isha": "العشاء"
        }
        return names.get(prayer, prayer)
