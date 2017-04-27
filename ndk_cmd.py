# -*- coding: UTF-8 -*-


'''
auther:
      Loopher

source :
http://www.qingpingshan.com/rjbc/az/222774.html

http://zke1ev3n.me/2016/01/18/%E5%9F%BA%E4%BA%8ELLVM%E7%9A%84%E4%BB%A3%E7%A0%81%E6%B7%B7%E6%B7%86/

'''
import sys,os
import re
import fileinput

###
TOOL_TAG=r"NDK_TOOLCHAIN_VERSION := "
LOCAL_CFLAGS=r"LOCAL_CFLAGS := "

###
FLAG=r":="

##
APP_MK="Application.mk"
Androi_MK="Android.mk"

###
llvm_flag_dict={"fla":"-mllvm -fla",
			"sub":"-mllvm -sub",
			"bcf":"-mllvm -bcf"

}

##
llvm_percent_dict={
	
	"preFLA":"-mllvm -perFLA=20",
	"loop":"-mllvm -boguscf-loop=3",
	"prob":"-mllvm -boguscf-prob=40"
	}

llvm_flagpercent_dict={	
	        "fla":"-mllvm -fla",
			"sub":"-mllvm -sub",
			"bcf":"-mllvm -bcf",
			"preFLA":"-mllvm -perFLA=20",
	        "loop":"-mllvm -boguscf-loop=3",
	        "prob":"-mllvm -boguscf-prob=40"
}	


all_obfuscator_dict={
			"1":llvm_flag_dict,
			"2":llvm_percent_dict,
			"3":llvm_flagpercent_dict

		}



'''
do main job for me 

'''
class NDK(object):
	def __init__(self,num="0"):
		self.num=num
		self.items=["1","2","3"]
		self.flag=False
		self.flag_app=False
		self.flag_android=False
		self.fileList=[]
		self.root_path=""
		self.app_list=[]
		self.android_list=[]

	def find_ndk_root(self):
		print "check NDK_ROOT... "
		ndk_root_path=os.getenv("LLVMr11c")
		return ndk_root_path
	def execut_cmd(self):
		ndk_path = self.find_ndk_root()
		if not ndk_path:
			print "not found $NDK_ROOT,check it  ~~"
			return
		#get item  
		#
		
		# print "fileList ",self.fileList
		# self.read_srcfile_tolist(self.fileList)
		self.ready_files()# ready files 
		if self.num in self.items:
			print "find num ,and use num for ndk-build ",self.num
			self.changeContent()
			self.execCmd()


		#default 
		else:
			#do change and execute cmd
			print "use default item not add toolchain for building  ~~~"
			# self.do_modified_() 
			for file in self.fileList:
				self.read_list_tosrcfile(file)
			self.execCmd()
							
	def read_list_tosrcfile(self,file):
		try:
			name = os.path.basename(file)
			fp=open(file,"w+")
			if name ==  APP_MK:
				for e in self.app_list:
					fp.write(e)
			if name == Androi_MK:
				for e in self.android_list:
					fp.write(e)

			fp.close()
			print "write back to files ok"
			self.flag=True

		except Exception as e:
			raise e
		

# record src content 
	def read_srcfile_tolist(self,fileList):
		try:
			for file in fileList:
				name=os.path.basename(file)
				fp=open(file,"r")
				if name == APP_MK:
					
					self.app_list= fp.readlines()
					fp.close()
				if name == Androi_MK:
					self.android_list=fp.readlines()
					fp.close()
			#print "".join(str(e) for e in self.app_list)
			print "**" * 10
			#print "".join(str(e) for e in self.android_list)

		except Exception as e:
			raise e

	#use self.num for  modified Application.mk Android.mk

	def changeContent(self):
		self.change_file_content(self.fileList)
		# self.flag=True
		if self.flag_android and self.flag_app:
			self.flag=True		
				
					
	def ready_files(self):
		current_path = os.getcwd()		
		dirs=os.listdir(current_path)
		for sub_dir in dirs:
			if sub_dir == "jni":
				print "--" * 10
				print "find jni ... ready to change Application.mk,Android.mk file ~~"
				print "--" * 10
				self.fileList=self.scan_file(sub_dir,postfix=".mk")
				#copy src file 
				self.read_srcfile_tolist(self.fileList)
				
				break
			else:
				print "--" * 10
				print "not found jni ,plz create jni and try  again ~~~"
				break

				

	def execCmd(self):
		
		if self.flag:
			print "*****" * 10 
			os.system("ndk-build -B")
			print "build project ok ~~~~~"
			self.write_back_srcContent()
			
			print "*****" * 10
		else:
			print "modified Application.mk and Android.mk was failed . "

	def write_back_srcContent(self):
		if self.fileList:
			if self.app_list and self.android_list:
				for file in self.fileList:
					#print "write file "
					fp=open(file,"w+")
					name = os.path.basename(file)
					#print "write file ",name

					if name == APP_MK:
						for line in self.app_list:
							fp.writelines(line)
					if name == Androi_MK:
						for line in self.android_list:
							fp.writelines(line)
					fp.close()
					print "write back !!! "

	def scan_file(self,directory,prefix=None,postfix=None):
		print "scanning file "
		file_list=[]
		for root,sub_dirs,files in os.walk(directory):
			for special_file in files:
				if postfix:
					if special_file.endswith(postfix):
						file_list.append(os.path.join(root,special_file))
				elif prefix:
					if special_file.startswith(prefix):
						file_list.append(os.path.join(root,special_file))
				else:
					file_list.append(os.path.join(root,special_file))
					current_path=os.path.join(root,special_file)
					self.root_path=root

			return file_list

	def change_file_content(self,files):
		fileName=""
		if not files:
			#print "file list is None"
			return
		for file in files:
			fileName=os.path.basename(file)
			#print "file name --- ", fileName
			if fileName == APP_MK:
				#print "App.mk "
				# self.chang_App_text(file)
				self.create_ApplicationMK(file)

				#
			if fileName == Androi_MK:
				#print "Android.mk !!! "
				# self.change_android_text(file)
				mlist=self.create_mlist()
				#print "get list ",mlist
				if not mlist:
					#print "command list is None ~"
					return
				self.create_AndroidMk(file,mlist)


	def create_mlist(self):
		tmp_list=[]
		for key in all_obfuscator_dict.keys():
			print "key",key 
			if key == self.num:
				# print "dict key ",key
				mdict=all_obfuscator_dict.get(key)
				for mkey in mdict.keys():
					tmp_list.append(mdict.get(mkey))
			else:
				continue

			return tmp_list

#default TOOL_TAG :obfuscator3.6
	def create_ApplicationMK(self,file,obftype="obfuscator3.6"):
		mpath=""
		toolchain=TOOL_TAG+ " "+obftype
		try:
			
			#print " pp ",os.path.join(file)
			mpath=  os.path.join(self.root_path,file)#os.getcwd()
			#print "666 ",mpath 
			flag=0
			newfile=mpath
			srcfp=open(file,"r")
			lines=srcfp.readlines()

			# print "src android .mk -------------- ",lines

			dstfp=open(os.path.join(newfile),"w+")
			for line in lines:
				# print "** ------ --- ---- ** "
				if line.startswith(TOOL_TAG):
					#print "find ************"
					dstfp.writelines(toolchain)
					flag=1
				else:
					# print "writing "
					dstfp.writelines(line)

			#print "flag ",flag

			if not flag:
				#print "add "
				dstfp.writelines(toolchain)
				#print "add "
			
			srcfp.close()
			dstfp.close()
			print"file Application.mk  create ok"
			self.flag_app=True
		except Exception as e:
			print"create Application.mk failed exception", e

	def create_AndroidMk(self,file,mlist):

		include ="include $(BUILD_SHARED_LIBRARY)"
		tmp_list=mlist
		flag=False
		strflag1=" ".join(str(e) for e in tmp_list)
		# print "strflag1 ",strflag1
		strflag2=LOCAL_CFLAGS+" ".join(str(e) for e in tmp_list)
		# print "strflag2 ",strflag2
		position=0
		try:
			mpath=os.path.join(self.root_path,file)
			srcfile=open(file,"r")
			lines=srcfile.readlines()
			# print "andrid .mk ======== ",lines
			newfile=mpath
			dstfile=open(os.path.join(newfile),"w+")	

			for line in lines:

				#add text into tail 
				# print"android line ",line
				if line.startswith(LOCAL_CFLAGS):
					print "write local_cflags "
					line=line.strip("\n")
					if line[-1] =="\\":
						dstfile.writelines(line)
						dstfile.writelines("\n"+strflag1)
						dstfile.writelines("\n")
						flag =True
					else:
						dstfile.writelines(line +" \\")	
						dstfile.writelines("\n"+strflag1)
						dstfile.writelines("\n")
						flag =True					
					# dstfile.writelines("\n")						
					
				#add text 
				elif  not flag and line.startswith(include):
					print "not found local cflags"
					dstfile.writelines("\n")
					dstfile.writelines(strflag2)
					dstfile.writelines("\n")
					dstfile.writelines(include)
					dstfile.writelines("\n")
			
				else:# normal write
					dstfile.writelines(line)

			srcfile.close()
			dstfile.close()
			print"create Android.mk ok "
			self.flag_android=True
		except Exception as e:
			print "create Android.mk was failed ,exception ",e


def execut_cmd(ndk_path):
	if  ndk_path:
		print " path is ok "
		os.system(" ndk-build -v ")
	else:
		print " path not ok "

def find_ndk_root():
	print "executing ~~"
	ndk_root_path=os.getenv("LLVMr11c")
	print "HOME =%s "%(os.getenv("HOME"))
	return ndk_root_path



def main():
	print "*" *10
 	current_path=os.getcwd()
 	print "current_path" ,current_path
 	
	path=find_ndk_root()
	execut_cmd(path)
	iterator_dir(current_path)
	panduan()

if __name__ == '__main__':
	# main()

	print "--**--"
	print "if you want to build obfuscator by ollvm ,"\
	"Firs of all,you should set ndk to the PAHT variable as 'LLVMr11c =path/android-ndk-r11c ' "\
	"and check the ndk path call 'ndk-build -v' "\
	"you also need install Python 2.7.x or highset level, "\
	" and keep the script with jni directory as same directory "\
	"if everything is ok ,now you can run script as 'python ndk_cmd.py '"\
	"please enter the number 1-3,the others number will"\
	" be select to the  default \n"\
	"1 : -mllvm -fla -mllvm -sub -mllvm -bcf\n"\
	"2 : -mllvm -perFLA=20 -mllvm -boguscf-loop=3 -mllvm -boguscf-prob=40 \n"\
	"3 : both 1 and 2 \n"
	print "--**--"
	
	num = raw_input("please enter the number(1-3) :" )
	mtype=str(num)

	ndk=NDK(mtype)
	ndk.execut_cmd()