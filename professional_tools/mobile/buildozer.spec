
[app]

# (str) Title of your application
title = RAULI Mobile Assistant

# (str) Package name
package.name = rauli_mobile

# (str) Package domain (needed for android/ios packaging)
package.domain = com.rauli.mobile

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,kivymd,requests,opencv-python,numpy,pandas

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations (choose one)
# Valid options are: landscape, sensor, portrait
#orientation = portrait
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) Permissions
android.permissions = CAMERA, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, INTERNET, VIBRATE, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.renpy.android.PythonActivity

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in Gradle project)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

#
# iOS specific
#

# (str) Path to a custom kivy-ios directory
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# For more details about iOS signing please see the documentation
#ios.codesign.debug = ""

# (str) The development team identity to use for signing the debug version
#ios.codesign.development_team = ""

# (str) Path to a custom .mobileprovision file to use for signing the debug version
#ios.codesign.debug_mobileprovision = ""

#
# macOS specific
#

# (str) Path to a custom kivy-macos directory
#macos.kivy_macos_dir = ../kivy-macos

#
# Windows specific
#

# (str) Path to a custom kivy-windows directory
#windows.kivy_windows_dir = ../kivy-windows

#
# Linux specific
#

# (str) Command to start a custom X server
#linux.x_server_command = Xvfb :1

#
# Buildozer Environment
#

# (str) Buildozer command to execute
#buildozer.cmd = /usr/local/bin/buildozer

# (str) Environment variables to pass to buildozer
#buildozer.env = CUSTOM_VAR=value
