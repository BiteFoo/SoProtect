#ifndef _DEMO1_H
#define _DEMO1_H 1

#include <jni.h>
// #include <string>
#include <android/log.h>

#define  LOG_TAG    "ubu"
#define  LOGI(...)  __android_log_print(ANDROID_LOG_INFO,LOG_TAG,__VA_ARGS__)
#define  LOGE(...)  __android_log_print(ANDROID_LOG_ERROR,LOG_TAG,__VA_ARGS__)
int des(int a,int b);

void
Java_com_demo_my_MainActivity_stringFromJNI2(
        JNIEnv *env,
        jobject *obj);
void print(char* msg );

#endif //JNIDEMO_ASE_H