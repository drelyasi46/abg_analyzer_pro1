#!/bin/bash

PROJECT=$HOME/abg_analyzer_pro
LOG=$PROJECT/auto_machine.log

echo "===== AUTO BUILD MACHINE START =====" | tee $LOG

cd $PROJECT || exit 1


repair_libwebp(){

echo "[FIX] libwebp" | tee -a $LOG

SDL=$(find .buildozer -type d -name SDL2_image | head -1)

if [ -z "$SDL" ]; then
    echo "SDL2_image not found"
    return
fi

cd "$SDL/external" || exit

rm -rf libwebp

git clone --depth 1 \
https://github.com/webmproject/libwebp.git libwebp

cd $PROJECT

}



repair_sdl_ndk(){

echo "[FIX] SDL NDK compatibility" | tee -a $LOG

sed -i 's/android.ndk = .*/android.ndk = 25b/' buildozer.spec

rm -rf .buildozer/android/platform/build-arm64-v8a

}



repair_clean_build(){

echo "[FIX] clean build cache" | tee -a $LOG

rm -rf .buildozer/android/platform/build-arm64-v8a

}



while true
do

echo "===== BUILD TRY =====" | tee -a $LOG

buildozer android debug 2>&1 | tee -a $LOG


if grep -q "libwebp/Android.mk" $LOG
then
    repair_libwebp
    continue
fi


if grep -q "ALooper_pollAll" $LOG
then
    repair_sdl_ndk
    continue
fi


if grep -q "No APK/AAB artifact found" $LOG
then
    repair_clean_build
    continue
fi


if grep -q "BUILD SUCCESS" $LOG
then
    echo "SUCCESS"
    break
fi


echo "Unknown error. STOP"
break


done
