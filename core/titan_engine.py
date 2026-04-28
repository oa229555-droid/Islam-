#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
محرك Titan-Omega AI - الذكاء الاصطناعي للتطبيق الإسلامي
"""

import json
import random
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class QueryType(Enum):
    """أنواع الاستعلامات"""
    FATWA = "fatwa"
    QURAN = "quran"
    HADITH = "hadith"
    DUA = "dua"
    GENERAL = "general"
    EMOTIONAL = "emotional"


@dataclass
class QueryResult:
    """نتيجة معالجة الاستعلام"""
    success: bool
    query: str
    response: str
    query_type: QueryType
    emotion: str
    confidence: float
    response_time_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    references: List[Dict] = field(default_factory=list)


class IslamicDatabaseCore:
    """قاعدة البيانات الإسلامية المركزية"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.quran = self._load_json("quran.json")
        self.hadith = self._load_json("hadith.json")
        self.duas = self._load_json("duas.json")
        self.cache = {}
    
    def _load_json(self, filename: str) -> Dict:
        """تحميل ملف JSON"""
        import os
        filepath = os.path.join(self.data_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_data(filename)
    
    def _get_default_data(self, filename: str) -> Dict:
        """بيانات افتراضية"""
        if filename == "quran.json":
            return {
                "1:1": {"text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "surah": "الفاتحة", "verse": 1},
                "2:255": {"text": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ", "surah": "البقرة", "verse": 255, "name": "آية الكرسي"},
                "94:5": {"text": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "surah": "الشرح", "verse": 5},
            }
        elif filename == "hadith.json":
            return {
                "bukhari_1": {"text": "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ", "book": "صحيح البخاري", "grade": "صحيح"},
                "muslim_1": {"text": "لا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ", "book": "صحيح مسلم", "grade": "صحيح"},
            }
        elif filename == "duas.json":
            return {
                "morning": {"text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ", "occasion": "الصباح"},
                "evening": {"text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ", "occasion": "المساء"},
                "anxiety": {"text": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ", "occasion": "القلق"},
            }
        return {}


class EmotionalAnalyzer:
    """تحليل المشاعر من النص"""
    
    def __init__(self):
        self.emotion_keywords = {
            "sad": ["حزين", "زعلان", "بكيت", "مكتئب", "حزن"],
            "anxious": ["قلق", "خائف", "متوتر", "خوف", "هلع"],
            "happy": ["سعيد", "فرحان", "مبسوط", "سعادة", "فرح"],
            "angry": ["غضبان", "معصب", "غيظ", "غضب"],
            "grateful": ["الحمد لله", "شكراً", "نعمة", "فضل"],
        }
        
        self.recommendations = {
            "sad": {"ayah": "94:5", "advice": "لا تحزن إن الله معنا"},
            "anxious": {"ayah": "2:255", "advice": "قل: حسبي الله ونعم الوكيل"},
            "happy": {"ayah": "1:2", "advice": "احمد الله واشكره على نعمه"},
            "angry": {"advice": "توضأ فإن الغضب من الشيطان"},
            "grateful": {"advice": "الزيادة في النعمة بالشكر"},
        }
    
    def analyze(self, text: str) -> Dict:
        """تحليل المشاعر"""
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[primary_emotion] / 5, 0.95)
        else:
            primary_emotion = "neutral"
            confidence = 0.3
        
        recommendation = self.recommendations.get(primary_emotion, self.recommendations.get("sad"))
        
        return {
            "primary_emotion": primary_emotion,
            "scores": emotion_scores,
            "confidence": confidence,
            "recommendation": recommendation
        }


class FatwaEngine:
    """محرك الفتاوى الذكي"""
    
    def __init__(self):
        self.patterns = {
            "prayer": {
                "keywords": ["صلاة", "صليت", "فجر", "ظهر", "عصر", "مغرب", "عشاء"],
                "answer": "الصلاة عمود الإسلام، يجب المحافظة عليها في أوقاتها.",
                "evidence": "قال الله تعالى: {إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَوْقُوتًا}"
            },
            "interest": {
                "keywords": ["ربا", "فائدة", "بنك", "قرض", "فوائد"],
                "answer": "الربا محرم تحريماً قاطعاً في القرآن والسنة والإجماع.",
                "evidence": "قال الله تعالى: {وَأَحَلَّ اللَّهُ الْبَيْعَ وَحَرَّمَ الرِّبَا}"
            },
            "fasting": {
                "keywords": ["صوم", "صيام", "رمضان", "فطر"],
                "answer": "الصيام ركن من أركان الإسلام، يبطل بالأكل والشرب عمداً.",
                "evidence": "قال الله تعالى: {كُتِبَ عَلَيْكُمُ الصِّيَامُ}"
            },
            "tawba": {
                "keywords": ["توبة", "استغفار", "ذنب", "ندم"],
                "answer": "باب التوبة مفتوح حتى تطلع الشمس من مغربها.",
                "evidence": "قال الله تعالى: {وَتُوبُوا إِلَى اللَّهِ جَمِيعًا أَيُّهَ الْمُؤْمِنُونَ}"
            }
        }
    
    def answer(self, question: str) -> Dict:
        """الإجابة على السؤال"""
        question_lower = question.lower()
        
        for topic, pattern in self.patterns.items():
            if any(kw in question_lower for kw in pattern["keywords"]):
                return {
                    "topic": topic,
                    "answer": pattern["answer"],
                    "evidence": pattern["evidence"],
                    "confidence": 0.9
                }
        
        return {
            "topic": "general",
            "answer": "جزاك الله خيراً على سؤالك. يُفضل سؤال أهل العلم للتفصيل.",
            "evidence": "",
            "confidence": 0.5
        }


class TitanEngine:
    """المحرك الرئيسي"""
    
    def __init__(self):
        self.db_core = IslamicDatabaseCore()
        self.emotional_ai = EmotionalAnalyzer()
        self.fatwa_ai = FatwaEngine()
        self.stats = {"queries": 0, "total_time": 0}
    
    async def process(self, query: str, user_id: str = None) -> QueryResult:
        """معالجة الاستعلام"""
        start_time = time.time()
        self.stats["queries"] += 1
        
        # تحليل المشاعر
        emotional = self.emotional_ai.analyze(query)
        
        # تحديد نوع الاستعلام
        query_type = self._classify_query(query)
        
        # الحصول على الرد
        if query_type == QueryType.FATWA:
            response_data = self.fatwa_ai.answer(query)
            response = self._format_fatwa_response(response_data, emotional)
        elif query_type == QueryType.QURAN:
            response = self._get_quran_response(query)
        elif query_type == QueryType.HADITH:
            response = self._get_hadith_response(query)
        elif query_type == QueryType.DUA:
            response = self._get_dua_response(emotional)
        else:
            response = self._get_general_response(emotional)
        
        elapsed_ms = (time.time() - start_time) * 1000
        self.stats["total_time"] += elapsed_ms
        
        return QueryResult(
            success=True,
            query=query,
            response=response,
            query_type=query_type,
            emotion=emotional["primary_emotion"],
            confidence=emotional["confidence"],
            response_time_ms=elapsed_ms
        )
    
    def _classify_query(self, query: str) -> QueryType:
        """تصنيف الاستعلام"""
        q = query.lower()
        if any(word in q for word in ["حكم", "يجوز", "حرام", "حلال"]):
            return QueryType.FATWA
        elif any(word in q for word in ["سورة", "آية", "قرآن"]):
            return QueryType.QURAN
        elif any(word in q for word in ["حديث", "رسول", "نبوي"]):
            return QueryType.HADITH
        elif any(word in q for word in ["دعاء", "أذكار", "اللهم"]):
            return QueryType.DUA
        elif any(word in q for word in ["حزين", "قلق", "خائف"]):
            return QueryType.EMOTIONAL
        return QueryType.GENERAL
    
    def _get_quran_response(self, query: str) -> str:
        """رد من القرآن"""
        import random
        ayah_key = random.choice(list(self.db_core.quran.keys()))
        ayah = self.db_core.quran[ayah_key]
        return f"📖 {ayah['text']}\n\n({ayah['surah']}:{ayah['verse']})"
    
    def _get_hadith_response(self, query: str) -> str:
        """رد من الحديث"""
        import random
        hadith_key = random.choice(list(self.db_core.hadith.keys()))
        hadith = self.db_core.hadith[hadith_key]
        return f"📚 قال رسول الله ﷺ: {hadith['text']}"
    
    def _get_dua_response(self, emotional: Dict) -> str:
        """رد من الأدعية"""
        dua_key = "morning"
        if emotional["primary_emotion"] == "sad":
            dua_key = "anxiety"
        elif emotional["primary_emotion"] == "anxious":
            dua_key = "anxiety"
        
        dua = self.db_core.duas.get(dua_key, self.db_core.duas.get("morning"))
        return f"🤲 {dua['text']}\n\n📌 المناسبة: {dua.get('occasion', 'عامة')}"
    
    def _get_general_response(self, emotional: Dict) -> str:
        """رد عام"""
        emotion = emotional["primary_emotion"]
        rec = emotional["recommendation"]
        
        openings = {
            "sad": "أخي الحبيب، لا تحزن إن الله معنا 🤲",
            "anxious": "لا تخف، الله معك ويهديك 🕊️",
            "happy": "الحمد لله على نعمة الفرح 🌸",
            "angry": "هدئ بالك واستغفر الله 😌",
            "neutral": "جزاك الله خيراً على سؤالك 🌙"
        }
        
        opening = openings.get(emotion, openings["neutral"])
        return f"{opening}\n\n💡 {rec.get('advice', '')}"
    
    def get_stats(self) -> Dict:
        """إحصائيات الأداء"""
        avg_time = self.stats["total_time"] / self.stats["queries"] if self.stats["queries"] > 0 else 0
        return {
            "queries_processed": self.stats["queries"],
            "avg_response_time_ms": round(avg_time, 2),
            "status": "running"
      }
