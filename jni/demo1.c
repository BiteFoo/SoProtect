#include "demo1.h"


void _init(void){}
int const dummy_to_make_this_compressible[100000] = {1,2,3};
int const dummy_to_make_this_compressible2[100000] = {1,2,3};
int des(int a, int b)
{
	int ret=0;
		if(a>b)
		{
				ret = a-b;
		}
		else
		{
			ret = b-a;
		}

	return ret;
}

/**
frida build commands
make core-android  ANDROID_NDK_ROOT=$LLVMr11c
*/
//com.demo.my

void
Java_com_demo_my_MainActivity_stringFromJNI2(
        JNIEnv *env,
        jobject  *obj ) {
    LOGI("be compressed by upx ");
  
}

