#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
إعدادات التطبيق المركزية
"""

import os
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AppConfig:
    """إعدادات التطبيق الرئيسية"""
    
    # معلومات التطبيق
    APP_NAME: str = "Titan Islamic AI"
    APP_VERSION: str = "4.0.0"
    APP_BUILD: int = 100
    
    # معلومات المطور
    DEVELOPER_NAME: str = "Omar Abdo"
    DEVELOPER_PHONE: str = "01289411976"
    DEVELOPER_EMAIL: str = "omar.abdo@titan.com"
    DEVELOPER_ROLE: str = "مطور رئيسي"
    
    # إعدادات قاعدة البيانات
    DATABASE_PATH: str = "titan_islamic.db"
    
    # إعدادات مواقيت الصلاة
    DEFAULT_CITY: str = "Cairo"
    DEFAULT_COUNTRY: str = "EG"
    PRAYER_API_URL: str = "http://api.aladhan.com/v1/timingsByCity"
    PRAYER_METHOD: int = 5  # طريقة حساب مواقيت الصلاة
    
    # إعدادات الإشعارات
    NOTIFICATIONS_ENABLED: bool = True
    NOTIFICATION_INTERVAL: int = 30  # ثانية
    
    # إعدادات الأذكار التلقائية
    DHIKR_TIMES: Dict[str, str] = None
    
    # إعدادات العرض
    THEME_STYLE: str = "Dark"
    PRIMARY_PALETTE: str = "Teal"
    
    def __post_init__(self):
        if self.DHIKR_TIMES is None:
            self.DHIKR_TIMES = {
                "morning_dhikr": "06:00",
                "evening_dhikr": "18:00",
                "duha_prayer": "08:00",
                "istighfar": "12:00",
                "night_dhikr": "21:00",
            }
    
    @classmethod
    def get_instance(cls):
        """الحصول على نسخة واحدة من الإعدادات (Singleton)"""
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance


# نسخة عالمية من الإعدادات
CONFIG = AppConfig.get_instance()
