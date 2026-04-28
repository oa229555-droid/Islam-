#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Titan Islamic AI - التطبيق الإسلامي الذكي
إصدار 4.0.0 - للمهندس عمر عبدو
"""

import os
import sys
import threading
import asyncio
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

# إضافة المسار
sys.path.insert(0, os.path.dirname(__file__))

# استيراد المكونات
from core import TitanEngine, IslamicDatabase, CONFIG
from core.config import AppConfig
from ai.prayer_times import PrayerTimesManager
from utils.notifications import NotificationManager
from utils.constants import DEVELOPER_INFO, COLORS, DHIKR_TEXTS

# تحميل تصميم الواجهة
KV_CODE = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import COLORS utils.constants.COLORS

<CustomCard@MDCard>:
    orientation: 'vertical'
    padding: dp(12)
    spacing: dp(10)
    size_hint: 1, None
    height: self.minimum_height
    elevation: 2
    radius: [dp(15)]
    md_bg_color: get_color_from_hex(COLORS["secondary"])

<PrayerCard@MDCard>:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(10)
    size_hint: 1, None
    height: dp(280)
    md_bg_color: get_color_from_hex(COLORS["primary"])
    radius: [dp(20)]
    
    MDLabel:
        text: '🕌 مواقيت الصلاة'
        font_style: 'H6'
        halign: 'center'
        color: 1, 1, 1, 1
    
    GridLayout:
        cols: 2
        spacing: dp(12)
        padding: dp(10)
        size_hint_y: None
        height: dp(160)
        
        MDLabel:
            text: 'صلاة الفجر'
            halign: 'left'
        MDLabel:
            id: fajr_time
            text: '--:--'
            halign: 'right'
        
        MDLabel:
            text: 'صلاة الظهر'
            halign: 'left'
        MDLabel:
            id: dhuhr_time
            text: '--:--'
            halign: 'right'
        
        MDLabel:
            text: 'صلاة العصر'
            halign: 'left'
        MDLabel:
            id: asr_time
            text: '--:--'
            halign: 'right'
        
        MDLabel:
            text: 'صلاة المغرب'
            halign: 'left'
        MDLabel:
            id: maghrib_time
            text: '--:--'
            halign: 'right'
        
        MDLabel:
            text: 'صلاة العشاء'
            halign: 'left'
        MDLabel:
            id: isha_time
            text: '--:--'
            halign: 'right'
    
    MDLabel:
        id: next_prayer
        text: 'القادمة: --'
        halign: 'center'
        font_style: 'Caption'

<DeveloperCard@MDCard>:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(10)
    size_hint: 1, None
    height: dp(320)
    md_bg_color: get_color_from_hex(COLORS["secondary"])
    radius: [dp(20)]
    
    MDLabel:
        text: '👨‍💻 معلومات المطور'
        font_style: 'H6'
        halign: 'center'
    
    MDLabel:
        text: f'الاسم: {DEVELOPER_INFO["name"]}'
        font_style: 'Body1'
    
    MDLabel:
        text: f'رقم الهاتف: {DEVELOPER_INFO["phone"]}'
        font_style: 'Body1'
    
    MDLabel:
        text: f'البريد الإلكتروني: {DEVELOPER_INFO["email"]}'
        font_style: 'Body1'
    
    MDLabel:
        text: f'المنصب: {DEVELOPER_INFO["role"]}'
        font_style: 'Body1'
    
    MDLabel:
        text: f'الإصدار: v{DEVELOPER_INFO["version"]}'
        font_style: 'Caption'
        halign: 'center'
    
    BoxLayout:
        spacing: dp(10)
        size_hint_y: None
        height: dp(48)
        
        MDRaisedButton:
            text: '📞 اتصل'
            md_bg_color: get_color_from_hex('#25D366')
            on_release: app.call_developer()
        
        MDRaisedButton:
            text: '✉️ راسل'
            md_bg_color: get_color_from_hex('#128C7E')
            on_release: app.email_developer()

<ChatBubbleUser@BoxLayout>:
    orientation: 'vertical'
    size_hint_x: 0.7
    pos_hint: {'right': 1}
    
    MDLabel:
        text: root.text
        size_hint_y: None
        height: self.texture_size[1] + dp(20)
        padding: [dp(15), dp(10)]
        color: 1, 1, 1, 1
        font_size: dp(15)
        markup: True
        md_bg_color: get_color_from_hex(COLORS["accent"])
        radius: [dp(15), dp(5), dp(15), dp(15)]

<ChatBubbleBot@BoxLayout>:
    orientation: 'vertical'
    size_hint_x: 0.75
    
    MDLabel:
        text: root.text
        size_hint_y: None
        height: self.texture_size[1] + dp(20)
        padding: [dp(15), dp(10)]
        color: 1, 1, 1, 1
        font_size: dp(15)
        markup: True
        md_bg_color: get_color_from_hex(COLORS["primary"])
        radius: [dp(5), dp(15), dp(15), dp(15)]

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: 'تيتان إسلامي'
            md_bg_color: get_color_from_hex(COLORS["primary"])
            specific_text_color: 1, 1, 1, 1
            left_action_items: [['menu', lambda x: app.toggle_nav_drawer()]]
        
        MDBottomNavigation:
            panel_color: get_color_from_hex(COLORS["secondary"])
            
            MDBottomNavigationItem:
                name: 'chat'
                text: 'محادثة'
                icon: 'chat'
                
                BoxLayout:
                    orientation: 'vertical'
                    
                    ScrollView:
                        id: chat_scroll
                        do_scroll_x: False
                        
                        MDGridLayout:
                            id: chat_list
                            cols: 1
                            spacing: dp(10)
                            padding: dp(10)
                            size_hint_y: None
                            height: self.minimum_height
                    
                    BoxLayout:
                        size_hint_y: 0.12
                        padding: dp(8)
                        spacing: dp(8)
                        md_bg_color: get_color_from_hex(COLORS["secondary"])
                        
                        MDTextField:
                            id: message_input
                            hint_text: '✍️ اكتب سؤالك هنا...'
                            mode: 'round'
                            size_hint_x: 0.8
                            
                        MDRaisedButton:
                            text: '📤 إرسال'
                            size_hint_x: 0.2
                            md_bg_color: get_color_from_hex(COLORS["accent"])
                            on_release: app.send_message()
            
            MDBottomNavigationItem:
                name: 'prayer'
                text: 'صلاة'
                icon: 'mosque'
                
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(16)
                        spacing: dp(16)
                        size_hint_y: None
                        height: self.minimum_height
                        
                        PrayerCard:
                            id: prayer_card
                        
                        CustomCard:
                            size_hint_y: None
                            height: dp(300)
                            
                            MDLabel:
                                text: '🕋 الأذكار اليومية'
                                font_style: 'H6'
                                halign: 'center'
                            
                            GridLayout:
                                cols: 2
                                spacing: dp(12)
                                padding: dp(10)
                                size_hint_y: None
                                height: dp(200)
                                
                                MDRaisedButton:
                                    text: '🌅 الصباح'
                                    on_release: app.show_dhikr('morning')
                                MDRaisedButton:
                                    text: '🌙 المساء'
                                    on_release: app.show_dhikr('evening')
                                MDRaisedButton:
                                    text: '😴 النوم'
                                    on_release: app.show_dhikr('sleep')
                                MDRaisedButton:
                                    text: '🚪 الخروج'
                                    on_release: app.show_dhikr('leaving_home')
            
            MDBottomNavigationItem:
                name: 'worship'
                text: 'عبادات'
                icon: 'prayer-beads'
                
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(16)
                        spacing: dp(16)
                        size_hint_y: None
                        height: self.minimum_height
                        
                        CustomCard:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: dp(450)
                            
                            MDLabel:
                                text: '📿 تسجيل الصلوات'
                                font_style: 'H6'
                                halign: 'center'
                            
                            GridLayout:
                                cols: 2
                                spacing: dp(12)
                                size_hint_y: None
                                height: dp(250)
                                
                                MDRaisedButton:
                                    id: fajr_btn
                                    text: '🌅 الفجر'
                                    on_release: app.toggle_prayer('fajr')
                                MDRaisedButton:
                                    id: dhuhr_btn
                                    text: '☀️ الظهر'
                                    on_release: app.toggle_prayer('dhuhr')
                                MDRaisedButton:
                                    id: asr_btn
                                    text: '🌤️ العصر'
                                    on_release: app.toggle_prayer('asr')
                                MDRaisedButton:
                                    id: maghrib_btn
                                    text: '🌙 المغرب'
                                    on_release: app.toggle_prayer('maghrib')
                                MDRaisedButton:
                                    id: isha_btn
                                    text: '⭐ العشاء'
                                    on_release: app.toggle_prayer('isha')
                            
                            MDRaisedButton:
                                text: '💾 حفظ الصلوات'
                                md_bg_color: get_color_from_hex(COLORS["accent"])
                                on_release: app.save_prayers()
                        
                        CustomCard:
                            size_hint_y: None
                            height: dp(200)
                            
                            MDLabel:
                                text: '📖 إحصائياتك'
                                font_style: 'H6'
                                halign: 'center'
                            
                            MDProgressBar:
                                id: prayer_progress
                                value: 0
                                color: get_color_from_hex(COLORS["accent"])
                            
                            MDLabel:
                                id: stats_label
                                text: '--'
            
            MDBottomNavigationItem:
                name: 'profile'
                text: 'ملفي'
                icon: 'account'
                
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(16)
                        spacing: dp(16)
                        size_hint_y: None
                        height: self.minimum_height
                        
                        CustomCard:
                            size_hint_y: None
                            height: dp(250)
                            
                            MDLabel:
                                id: user_name
                                text: 'مرحباً بك'
                                font_style: 'H5'
                                halign: 'center'
                            
                            MDLabel:
                                id: emotional_status
                                text: 'حالتك النفسية: --'
                            
                            MDRaisedButton:
                                text: '📊 عرض التقرير'
                                on_release: app.show_report()
                                
                            MDRaisedButton:
                                text: '🔄 تحديث'
                                md_bg_color: get_color_from_hex('#FF9800')
                                on_release: app.update_profile()
                        
                        DeveloperCard:
                            id: developer_card

class MainScreen(MDScreenManager):
    pass
'''

class TitanIslamicApp(MDApp):
    """التطبيق الرئيسي"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None
        self.db = None
        self.user_id = "mobile_user"
        self.prayers_status = {}
        self.event_loop = None
        self.prayer_manager = PrayerTimesManager()
        self.notification_manager = NotificationManager()
    
    def build(self):
        """بناء التطبيق"""
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        
        self.root = Builder.load_string(KV_CODE)
        
        # تشغيل المحرك
        self.start_engine()
        
        # جدولة المهام
        Clock.schedule_interval(self.check_notifications, 30)
        Clock.schedule_interval(self.update_prayer_times, 60)
        Clock.schedule_once(lambda dt: self.fetch_prayer_times(), 1)
        Clock.schedule_once(lambda dt: self.update_profile(), 2)
        
        return self.root
    
    def start_engine(self):
        """تشغيل المحرك"""
        def run_engine():
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            self.engine = TitanEngine()
            self.db = IslamicDatabase()
            self.db.register_user(self.user_id)
            self.event_loop.run_forever()
        
        threading.Thread(target=run_engine, daemon=True).start()
    
    def fetch_prayer_times(self):
        """جلب مواقيت الصلاة"""
        self.prayer_manager.fetch_times()
        self.update_prayer_display()
    
    def update_prayer_display(self):
        """تحديث عرض مواقيت الصلاة"""
        times = self.prayer_manager.prayer_times
        next_prayer, next_time = self.prayer_manager.get_next_prayer()
        
        self.root.ids.fajr_time.text = times.get("Fajr", "--:--")
        self.root.ids.dhuhr_time.text = times.get("Dhuhr", "--:--")
        self.root.ids.asr_time.text = times.get("Asr", "--:--")
        self.root.ids.maghrib_time.text = times.get("Maghrib", "--:--")
        self.root.ids.isha_time.text = times.get("Isha", "--:--")
        
        prayer_ar = self.prayer_manager.get_prayer_name_ar(next_prayer)
        self.root.ids.next_prayer.text = f"🕌 القادمة: {prayer_ar} - {next_time}"
    
    def update_prayer_times(self, dt):
        """تحديث مواقيت الصلاة"""
        self.update_prayer_display()
    
    def check_notifications(self, dt):
        """التحقق من الإشعارات"""
        self.notification_manager.check_and_notify()
    
    def show_dhikr(self, dhikr_type):
        """عرض الأذكار"""
        from utils.constants import DHIKR_TEXTS
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        
        text = DHIKR_TEXTS.get(dhikr_type, "لا يوجد نص")
        titles = {"morning": "أذكار الصباح", "evening": "أذكار المساء",
                  "sleep": "أذكار النوم", "leaving_home": "أذكار الخروج"}
        
        dialog = MDDialog(title=titles.get(dhikr_type, "أذكار"),
                         text=text,
                         buttons=[MDFlatButton(text="إغلاق", on_release=lambda x: dialog.dismiss())])
        dialog.open()
    
    def call_developer(self):
        """الاتصال بالمطور"""
        from plyer import call
        try:
            call.makecall(DEVELOPER_INFO["phone"])
        except:
            from kivymd.uix.dialog import MDDialog
            dialog = MDDialog(title="رقم المطور", 
                             text=f"📞 {DEVELOPER_INFO['phone']}",
                             buttons=[MDFlatButton(text="إغلاق", on_release=lambda x: dialog.dismiss())])
            dialog.open()
    
    def email_developer(self):
        """مراسلة المطور"""
        import webbrowser
        webbrowser.open(f"mailto:{DEVELOPER_INFO['email']}")
    
    async def process_message_async(self, message):
        """معالجة الرسالة"""
        if self.engine:
            return await self.engine.process(message, self.user_id)
        return None
    
    def add_chat_message(self, text, is_user=True):
        """إضافة رسالة إلى الشات"""
        from kivy.lang import Builder
        from kivy.clock import Clock
        
        chat_list = self.root.ids.chat_list
        
        if is_user:
            bubble = Builder.load_string(f'''
<ChatBubbleUser@BoxLayout>:
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.7
        pos_hint: {{'right': 1}}
        
        MDLabel:
            text: '{text}'
            size_hint_y: None
            height: self.texture_size[1] + dp(20)
            padding: [dp(15), dp(10)]
            color: 1, 1, 1, 1
            font_size: dp(15)
            markup: True
            md_bg_color: get_color_from_hex(COLORS["accent"])
            radius: [dp(15), dp(5), dp(15), dp(15)]
''')
        else:
            bubble = Builder.load_string(f'''
<ChatBubbleBot@BoxLayout>:
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.75
        
        MDLabel:
            text: '{text}'
            size_hint_y: None
            height: self.texture_size[1] + dp(20)
            padding: [dp(15), dp(10)]
            color: 1, 1, 1, 1
            font_size: dp(15)
            markup: True
            md_bg_color: get_color_from_hex(COLORS["primary"])
            radius: [dp(5), dp(15), dp(15), dp(15)]
''')
        
        chat_list.add_widget(bubble)
        Clock.schedule_once(lambda dt: setattr(self.root.ids.chat_scroll, 'scroll_y', 0), 0.1)
    
    def send_message(self):
        """إرسال رسالة"""
        import threading
        
        message_input = self.root.ids.message_input
        message = message_input.text.strip()
        if not message:
            return
        
        self.add_chat_message(message, is_user=True)
        message_input.text = ""
        
        def handle_response():
            import asyncio
            future = asyncio.run_coroutine_threadsafe(
                self.process_message_async(message), self.event_loop
            )
            try:
                result = future.result(timeout=30)
                self.add_chat_message(result.response, is_user=False)
            except Exception as e:
                self.add_chat_message(f"حدث خطأ: {str(e)}", is_user=False)
        
        threading.Thread(target=handle_response, daemon=True).start()
    
    def toggle_prayer(self, prayer):
        """تبديل حالة الصلاة"""
        btn_id = f"{prayer}_btn"
        btn = self.root.ids.get(btn_id)
        if btn:
            current = self.prayers_status.get(prayer, False)
            self.prayers_status[prayer] = not current
            if self.prayers_status[prayer]:
                btn.md_bg_color = get_color_from_hex(COLORS["accent"])
                btn.text = f"✓ {btn.text}"
            else:
                btn.md_bg_color = get_color_from_hex(COLORS["primary"])
                btn.text = btn.text.replace("✓ ", "")
    
    def save_prayers(self):
        """حفظ الصلوات"""
        if self.db:
            self.db.save_worship(self.user_id, self.prayers_status)
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text="✅ تم حفظ الصلوات بنجاح").open()
            self.update_worship_display()
    
    def update_worship_display(self):
        """تحديث عرض العبادات"""
        if self.db:
            stats = self.db.get_worship_stats(self.user_id)
            total_prayers = stats.get('prayers_completed', 0)
            max_prayers = stats.get('total_days', 1) * 5
            if max_prayers > 0:
                self.root.ids.prayer_progress.value = total_prayers / max_prayers
            self.root.ids.stats_label.text = f"عدد الصلوات: {total_prayers} / {max_prayers}"
    
    def update_profile(self):
        """تحديث الملف الشخصي"""
        if self.db:
            user = self.db.get_user(self.user_id)
            emotional = self.db.get_emotional_trend(self.user_id)
            
            name = user.get('full_name', 'زائر') if user else 'زائر'
            self.root.ids.user_name.text = f"مرحباً {name}"
            self.root.ids.emotional_status.text = f"😊 حالتك النفسية: {emotional.get('most_common_emotion', 'محايد')}"
    
    def show_report(self):
        """عرض التقرير"""
        if self.db:
            report = self.db.get_user_report(self.user_id)
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDFlatButton
            
            if "error" in report:
                content = report['error']
            else:
                content = f"""
📋 تقرير حالتك:

😊 المشاعر السائدة: {report['emotional_summary']['most_common_emotion']}

🕌 متوسط الصلوات: {report['worship_summary']['prayers_completed'] / max(report['worship_summary']['total_days'], 1):.1f}/5
📖 إجمالي صفحات القرآن: {report['worship_summary']['total_quran_pages']}
🔄 إجمالي الأذكار: {report['worship_summary']['total_dhikr']}
🌙 أيام الصيام: {report['worship_summary']['fasting_days']}
"""
            dialog = MDDialog(title="تقرير الحالة", text=content,
                             buttons=[MDFlatButton(text="إغلاق", on_release=lambda x: dialog.dismiss())])
            dialog.open()
    
    def toggle_nav_drawer(self):
        """فتح القائمة الجانبية"""
        pass


if __name__ == "__main__":
    TitanIslamicApp().run()
