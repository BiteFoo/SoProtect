#
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE    := demo1
LOCAL_SRC_FILES := test.c \
					

# LOCAL_CFLAGS += -Wl,-init=my_init

#-mllvm -sub -mllvm -fla -mllvm -bcf
# LOCAL_CFLAGS := -O0  -mllvm -sub
# LOCAL_ARM_MODE := arm
# LOCAL_CFLAGS := -O0  -mllvm -fla -mllvm -bcf -mllvm -sub

LOCAL_LDLIBS :=-llog
include $(BUILD_SHARED_LIBRARY)

