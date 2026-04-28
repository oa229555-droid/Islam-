[app]

# اسم التطبيق
title = Titan Islamic
package.name = titanislamic
package.domain = com.titan.islamic

# الإصدار
version = 4.0.0
version.release = 4

# المتطلبات
requirements = python3,kivy==2.2.1,kivymd==1.1.1,sqlite3,plyer,requests,pillow,numpy

# الأذونات
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,VIBRATE,FOREGROUND_SERVICE

# إصدارات SDK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# الأيقونات
icon.filename = assets/icon.png
presplash.filename = assets/splash.png

# اللغة
android.manifest.application_icon = assets/icon.png
android.manifest.application_presplash = assets/splash.png

# الإعدادات
fullscreen = 0
orientation = portrait

# التوقيع
# android.keystore = /path/to/keystore.jks
# android.keystore_alias = myalias

[buildozer]
log_level = 2
warn_on_root = 1
