#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
قاعدة البيانات المركزية - إدارة بيانات المستخدمين والعبادات والمحادثات
"""

import sqlite3
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class IslamicDatabase:
    """قاعدة البيانات الرئيسية للتطبيق"""
    
    def __init__(self, db_path: str = "titan_islamic.db"):
        self.db_path = db_path
        self._init_tables()
        logger.info(f"✅ قاعدة البيانات متصلة: {db_path}")
    
    @contextmanager
    def _get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_tables(self):
        """إنشاء جميع الجداول"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    full_name TEXT,
                    phone TEXT,
                    email TEXT,
                    country TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP,
                    preferences TEXT DEFAULT '{}'
                )
            ''')
            
            # جدول العبادات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS worship_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    worship_date DATE,
                    fajr BOOLEAN DEFAULT 0,
                    dhuhr BOOLEAN DEFAULT 0,
                    asr BOOLEAN DEFAULT 0,
                    maghrib BOOLEAN DEFAULT 0,
                    isha BOOLEAN DEFAULT 0,
                    quran_pages INTEGER DEFAULT 0,
                    dhikr_count INTEGER DEFAULT 0,
                    fasting BOOLEAN DEFAULT 0,
                    sadaqah_amount REAL DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول الحالة النفسية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotional_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    emotion TEXT,
                    confidence REAL,
                    context TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول المحادثات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    query TEXT,
                    response TEXT,
                    query_type TEXT,
                    emotion TEXT,
                    confidence REAL,
                    response_time_ms REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول الإشعارات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    title TEXT,
                    message TEXT,
                    is_read BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # إنشاء الفهارس
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_worship_user_date ON worship_tracking(user_id, worship_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id, created_at)')
            
            logger.info("✅ جميع الجداول تم إنشاؤها")
    
    # ==================== عمليات المستخدم ====================
    
    def register_user(self, user_id: str, **kwargs) -> bool:
        """تسجيل مستخدم جديد"""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO users (user_id, full_name, phone, email, country, preferences)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, 
                  kwargs.get('full_name', ''),
                  kwargs.get('phone', ''),
                  kwargs.get('email', ''),
                  kwargs.get('country', ''),
                  kwargs.get('preferences', '{}')))
            conn.execute('UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?', (user_id,))
        return True
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """جلب بيانات المستخدم"""
        with self._get_connection() as conn:
            result = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return dict(result) if result else None
    
    # ==================== عمليات العبادات ====================
    
    def save_worship(self, user_id: str, worship_data: Dict) -> bool:
        """حفظ بيانات العبادات"""
        today = datetime.now().date().isoformat()
        
        with self._get_connection() as conn:
            existing = conn.execute('''
                SELECT id FROM worship_tracking 
                WHERE user_id = ? AND worship_date = ?
            ''', (user_id, today)).fetchone()
            
            if existing:
                conn.execute('''
                    UPDATE worship_tracking SET
                        fajr = COALESCE(?, fajr),
                        dhuhr = COALESCE(?, dhuhr),
                        asr = COALESCE(?, asr),
                        maghrib = COALESCE(?, maghrib),
                        isha = COALESCE(?, isha),
                        quran_pages = COALESCE(?, quran_pages),
                        dhikr_count = COALESCE(?, dhikr_count),
                        fasting = COALESCE(?, fasting),
                        sadaqah_amount = COALESCE(?, sadaqah_amount)
                    WHERE user_id = ? AND worship_date = ?
                ''', (
                    worship_data.get('fajr'),
                    worship_data.get('dhuhr'),
                    worship_data.get('asr'),
                    worship_data.get('maghrib'),
                    worship_data.get('isha'),
                    worship_data.get('quran_pages'),
                    worship_data.get('dhikr_count'),
                    worship_data.get('fasting'),
                    worship_data.get('sadaqah_amount'),
                    user_id, today
                ))
            else:
                conn.execute('''
                    INSERT INTO worship_tracking (user_id, worship_date, fajr, dhuhr, asr, maghrib, isha,
                        quran_pages, dhikr_count, fasting, sadaqah_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, today,
                      worship_data.get('fajr', 0),
                      worship_data.get('dhuhr', 0),
                      worship_data.get('asr', 0),
                      worship_data.get('maghrib', 0),
                      worship_data.get('isha', 0),
                      worship_data.get('quran_pages', 0),
                      worship_data.get('dhikr_count', 0),
                      worship_data.get('fasting', 0),
                      worship_data.get('sadaqah_amount', 0)))
        return True
    
    def get_worship_stats(self, user_id: str, days: int = 7) -> Dict:
        """إحصائيات العبادات"""
        with self._get_connection() as conn:
            results = conn.execute('''
                SELECT * FROM worship_tracking 
                WHERE user_id = ? AND worship_date >= date('now', ?)
                ORDER BY worship_date DESC
            ''', (user_id, f'-{days} days')).fetchall()
            
            stats = {
                "total_days": len(results),
                "prayers_completed": 0,
                "total_quran_pages": 0,
                "total_dhikr": 0,
                "fasting_days": 0,
            }
            
            for row in results:
                prayers = sum([row['fajr'], row['dhuhr'], row['asr'], row['maghrib'], row['isha']])
                stats["prayers_completed"] += prayers
                stats["total_quran_pages"] += row['quran_pages'] or 0
                stats["total_dhikr"] += row['dhikr_count'] or 0
                stats["fasting_days"] += 1 if row['fasting'] else 0
            
            return stats
    
    # ==================== عمليات المحادثات ====================
    
    def save_conversation(self, user_id: str, query: str, response: str,
                          query_type: str, emotion: str, confidence: float,
                          response_time_ms: float) -> int:
        """حفظ المحادثة"""
        with self._get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO conversations (user_id, query, response, query_type, emotion, confidence, response_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, query[:500], response[:500], query_type, emotion, confidence, response_time_ms))
            return cursor.lastrowid
    
    def save_emotional_state(self, user_id: str, emotion: str, confidence: float, context: str = "") -> bool:
        """حفظ الحالة النفسية"""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT INTO emotional_state (user_id, emotion, confidence, context)
                VALUES (?, ?, ?, ?)
            ''', (user_id, emotion, confidence, context[:500]))
        return True
    
    def get_emotional_trend(self, user_id: str, days: int = 30) -> Dict:
        """اتجاه الحالة النفسية"""
        with self._get_connection() as conn:
            results = conn.execute('''
                SELECT emotion, COUNT(*) as count FROM emotional_state 
                WHERE user_id = ? AND recorded_at >= datetime('now', ?)
                GROUP BY emotion
                ORDER BY count DESC
            ''', (user_id, f'-{days} days')).fetchall()
            
            emotion_counts = {r['emotion']: r['count'] for r in results}
            most_common = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral"
            
            return {
                "total_records": sum(emotion_counts.values()),
                "emotion_distribution": emotion_counts,
                "most_common_emotion": most_common
            }
    
    def get_user_report(self, user_id: str) -> Dict:
        """تقرير شامل عن المستخدم"""
        user = self.get_user(user_id)
        if not user:
            return {"error": "المستخدم غير موجود"}
        
        worship_stats = self.get_worship_stats(user_id)
        emotional_trend = self.get_emotional_trend(user_id)
        
        return {
            "user": user,
            "worship_summary": worship_stats,
            "emotional_summary": emotional_trend,
            "generated_at": datetime.now().isoformat()
      }
