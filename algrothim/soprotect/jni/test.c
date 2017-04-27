#include <stdio.h>  //fopen ,fgets()
#include "test.h"   //decrypt_xor
#include <unistd.h>  //mprotexct()  pagesize = getpagesize ()
#include <sys/mman.h>  //mmap()h
#include <stdlib.h> //strtoul()
#include <string.h> //strlen() strtok() 

__attribute__((section("hackme"))) void hello(void);
__attribute__((section("hackme_data"))) char *key = "xxxxx";

void hello(void)
{
        LOGI("here----->%s",key);
}


/**
strtoul() 函数源自于“string to unsigned long”，用来将字符串转换成无符号长整型数(unsigned long)，其原型为：
unsigned long strtoul (const char* str, char** endptr, int base);

*/


/**
get target .so file in the memory ,
1.getpit()
2.read maps
3.find target .so 
4.get name  and transformed string to unsigned long ,return it .

*/

unsigned long getLibAddr(){
	unsigned long ret = 0;
	char name[] ="libdemo1.so";
	//according to  the pid to get the target pid, where the target file in the mmap  
	char buf[4096],*tmp;
	int pid;//target process' pid
	FILE *fp;
	pid=getpid();
	sprintf(buf,"/proc/%d/maps",pid);
	fp=fopen(buf,"r");
	if(fp == NULL)
	{
		LOGE("fopen file %s failed",buf);
		goto _error;
	}
	while(fgets(buf,sizeof(buf),fp))
	{
		if(strstr(buf,name)){
			tmp=strtok(buf,"_");
			ret=strtoul(tmp,NULL,16);
			break;
		}
	}
	_error:
	fclose(fp);
	return ret;
}

/**
decrypt function 
*/
void decrypt_xor11(){
	LOGI("begin to decrypt mem ");
	char name[15];
	unsigned int nblock;
	unsigned int psize;
	unsigned  long  so_base;
	unsigned long text_addr;
	unsigned int i;
	Elf32_Ehdr *ehdr; //elf header
	Elf32_Shdr *shdr; //section header 
	so_base=getLibAddr();
	ehdr=(Elf32_Ehdr *)so_base;
	//get encrypted code areas;  //得到待解密节占用的页的大小
	text_addr = ehdr->e_shoff+so_base;//get section header addr
	LOGI("get section header addr so_base =%lx",text_addr);
	nblock=ehdr->e_entry;
	psize=ehdr->e_shoff /4096 +(ehdr->e_shoff %4096  == 0 ? 0:1);
	LOGI("get encrypt pagesize psize = %x",psize);
	LOGI("check privillege ");   
	// int pagesize = getpagesize ();
	//mprotect修改权限是以页为单位的，所以这里必须将起始地址设置为PAGE_SIZE的整数倍
	if(mprotect((void*)(text_addr / PAGE_SIZE *PAGE_SIZE),4096 * psize,PROT_READ|PROT_WRITE|PROT_EXEC != 0)) //
	{
		LOGE("mprotect can't get privillege !!");
	}
	//begin to decrypt
	LOGI("begin to decrypt ");
	for(i=0;i<nblock;i++)
	{
		char *addr=(char*)(text_addr + i);
		*addr = *addr ^ 11;
	}
	LOGI("decrypt  end ");
	if(mprotect((void*)(text_addr / PAGE_SIZE *PAGE_SIZE),4096 * psize,PROT_READ|PROT_WRITE|PROT_EXEC != 0))
	{
		LOGE(" mprotect can't get privillege !!");
	}

	LOGI(" decrypt success !! ^_^ ");
}


void
Java_com_demo_my_MainActivity_stringFromJNI2(
        JNIEnv *env,
        jobject *obj)
{

	hello();
	LOGI("testing encrypt section header...... ");
}
