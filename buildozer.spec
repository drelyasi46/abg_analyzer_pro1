[app]

title = ABG Analyzer Pro

package.name = abganalyzer
package.domain = drelyasibabak.ir

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,json
source.exclude_dirs = .git,.github,.buildozer,bin,venv,.venv,buildenv,__pycache__

version = 1.0

requirements = python3==3.11.5,kivy==2.2.1,kivymd==1.2.0

p4a.branch = v2024.01.21
p4a.commit = v2024.01.21

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 24
android.archs = arm64-v8a
android.enable_androidx = True
android.ndk_path = /mnt/c/Users/Emd/AppData/Local/Android/Sdk/ndk/30.0.15729638
android.accept_sdk_license = True

log_level = 2
warn_on_root = 0

[buildozer]

log_level = 2
android.sdk_path = /mnt/c/Users/Emd/AppData/Local/Android/Sdk
android.build_tools_version = 34.0.0
