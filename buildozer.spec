[app]

# (str) Title of your application
title = ABG Analyzer Pro

# (str) Package name
package.name = abganalyzer

# (str) Package domain
package.domain = drelyasibabak.ir

# (str) Application version
version = 1.2.0


# (str) Source code directory
source.dir = .

# (str) Source file extensions
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,txt


# (list) Requirements
requirements = python3,kivy==2.2.1,pyjnius


# (str) Orientation
orientation = portrait


# (bool) Enable fullscreen
fullscreen = 0


# (str) Android API
android.api = 34

# (str) Minimum Android API
android.minapi = 24

# (str) NDK version
android.ndk = 25.2.9519653


# (list) Architectures
android.archs = arm64-v8a


# (bool) AndroidX
android.enable_androidx = True


# (str) Entry point
android.entrypoint = org.kivy.android.PythonActivity


# (str) Presplash
# presplash.filename = %(source.dir)s/data/presplash.png


# (str) Icon
# icon.filename = %(source.dir)s/data/icon.png


# (bool) Copy libraries
android.copy_libs = 1


# (str) Release artifact
android.release_artifact = aab


# (bool) Accept SDK licenses
android.accept_sdk_license = True



[buildozer]

# Log level
log_level = 2


# Warn about deprecated options
warn_on_root = 1
