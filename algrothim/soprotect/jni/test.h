#ifndef _TEST_H
#define _TEST_H 1

#include <jni.h>
// #include <string>
#include <android/log.h>
#include <elf.h> //elf file 
#define  LOG_TAG    "ubu"
#define  LOGI(...)  __android_log_print(ANDROID_LOG_INFO,LOG_TAG,__VA_ARGS__)
#define  LOGE(...)  __android_log_print(ANDROID_LOG_ERROR,LOG_TAG,__VA_ARGS__)



/**

#include <unistd.h> 
#include <sys/mmap.h> 
int mprotect(const void *start, size_t len, int prot); 
*/

//add decrypt function in the init_array
void decrypt_xor11()__attribute__((constructor));//decrypt memory data ,which would be encrypt by python

void
Java_com_demo_my_MainActivity_stringFromJNI2(
        JNIEnv *env,
        jobject *obj);
void print(char* msg );

#endif