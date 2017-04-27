#include <stdio.h>  //fopen ,fgets()
#include "demo.h"   //decrypt_xor
#include <unistd.h>  //mprotexct()  pagesize = getpagesize ()
#include <sys/mman.h>  //mmap()h
#include <stdlib.h> //strtoul()
#include <string.h> //strlen() strtok() 

__attribute__((section("hackme"))) void hello(void);
__attribute__((section("hackme_data"))) char *key = "xxxxx";

void _init(void){}
int const dummy_to_make_this_compressible[100000] = {1,2,3};
int const dummy_to_make_this_compressible2[100000] = {1,2,3};

void hello(void)
{
        LOGI("here----->%s",key);
}


unsigned long getLibAddr(){
        unsigned long ret = 0;
        char name[] = "libdemo1.so";
        char buf[4096], *temp;
        int pid;
        FILE *fp;
        pid = getpid();
        sprintf(buf, "/proc/%d/maps", pid);
        fp = fopen(buf, "r");
        if(fp == NULL)
        {
                puts("open failed");
                goto _error;
        }
        while(fgets(buf, sizeof(buf), fp)){
                if(strstr(buf, name)){
                        temp = strtok(buf, "-");
                        ret = strtoul(temp, NULL, 16);
                        break;
                }
        }
        _error:
        fclose(fp);
        return ret;
}

void init_getString(){
        char name[15];
        unsigned int nblock;
        unsigned int psize;
        unsigned long base;
        unsigned long text_addr;
        unsigned int i;
        Elf32_Ehdr *ehdr;
        Elf32_Shdr *shdr;

        base = getLibAddr();    //得到"libdemo.so"在进程中的地址

        ehdr = (Elf32_Ehdr *)base;
        text_addr = ehdr->e_shoff + base;     //得到待解密节的内存地址

        __android_log_print(ANDROID_LOG_INFO, "JNITag", "base =  0x%lx", text_addr);

        nblock = ehdr->e_entry;
        psize  = ehdr->e_shoff / 4096 + (ehdr->e_shoff % 4096 == 0 ? 0 : 1);    //得到待解密节占用的页的大小

        __android_log_print(ANDROID_LOG_INFO, "JNITag", "psize =  0x%x", psize);

        if(mprotect((void *)(text_addr / PAGE_SIZE * PAGE_SIZE), 4096 * psize, PROT_READ | PROT_EXEC | PROT_WRITE) != 0){   //mprotect修改权限是以页为单位的，所以这里必须将起始地址设置为PAGE_SIZE的整数倍
                __android_log_print(ANDROID_LOG_INFO, "JNITag", "mem privilege change failed");
        }

        for(i=0;i< nblock; i++){
                char *addr = (char*)(text_addr + i);
                *addr = (*addr) ^ 11;
        }

        if(mprotect((void *)(text_addr / PAGE_SIZE * PAGE_SIZE), 4096 * psize, PROT_READ | PROT_EXEC) != 0){
                __android_log_print(ANDROID_LOG_INFO, "JNITag", "mem privilege change failed");
        }
        __android_log_print(ANDROID_LOG_INFO, "JNITag", "Decrypt success");
}

void
Java_com_demo_my_MainActivity_stringFromJNI2(
        JNIEnv *env,
        jobject *obj)
{

        hello();
        LOGI("testing encrypt section header...... ");
}
