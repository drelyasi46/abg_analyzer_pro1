[app]

# (str) Title of your application
title = ABG Analyzer Pro

# (str) Package name
package.name = abganalyzer

# (str) Package domain
package.domain = drelyasibabak.ir

# (str) Application version
version = 1.3.0

# (str) Source code directory
source.dir = .

# (str) Source file extensions
source.include_exts = py,kv,png,jpg,jpeg,ttf,json,atlas,txt

# (str) Exclude directories
source.exclude_dirs = .git,.github,.buildozer,bin,venv,.venv,buildenv,__pycache__

# (list) Requirements
requirements = python3==3.11.5,kivy==2.2.1,kivymd==1.2.0,pyjnius

# Python-for-Android version pin
p4a.branch = v2024.01.21
p4a.commit = v2024.01.21

# (str) Orientation
orientation = portrait

# (bool) Enable fullscreen
fullscreen = 0

# Android API
android.api = 34

# Minimum Android API
android.minapi = 24

# Android architecture
android.archs = arm64-v8a

# Permissions
android.permissions = INTERNET

# Android package metadata
android.release_artifact = apk