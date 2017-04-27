# -*- coding: UTF-8 -*-

import sys
import struct

'''
format  c type         python type       
c   == char 			bytes of length 
b   == signed char
B   == unsigned char 
?  	== _Bool

H   unsigned short    integer  2 
I    unsigned int     integer   4
Q   unsiged long long  integer  8


struct.pack(fmt, v1, v2, ...)
Return a bytes object containing the values
 v1, v2, ... packed according to the format string fmt. The arguments must match the values required by the format exactly.

struct.calcsize(fmt)
Return the size of the struct (and hence of the bytes object produced by pack(fmt, ...)) corresponding to the format string fmt.

first of all, get elf header information

fileds =
[
'e_ident','e_type','e_machine','e_version',
'e_entry','e_phoff','e_shoff','e_flags','e_ehsize',
'e_phensize','e_phnum','e_shensize','e_shnum',
'e_shstrndx'

]

fmt32 = 
fmt64 = 


'''

def getElfHead(elf):
	print 'get elf header'


def getProgrammHeader():
	print "get elf programm header"

def getSectionHeader():
	print 'get section header '

def main(file):
	elf = open(file,'rb')
	if elf ==None :
		print 'can not open %s'%(file)
		return
	getElfHead(elf)


if __name__=='__main__':
	if len(sys.argv) != 2:
		print "usage:"
		print "python myreadelf.py ELFNAME"
	elif len(sys.argv) == 2:
		main(sys.argv[1])