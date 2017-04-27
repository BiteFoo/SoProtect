#-*-coding: utf-8 -*-
import sys
import struct
"""
Name       Size Alignment Purpose
Elf32_Addr    4    4      Unsigned program address
Elf32_Half    2    2      Unsigned medium integer
Elf32_Off     4    4      Unsigned file offset
Elf32_Sword   4    4      Signed large integer
Elf32_Word    4    4      Unsigned large integer
unsigned char 1    1      Unsigned small integer
Elf64_Addr    8    8      Unsigned program address
Elf64_Off     8    8      Unsigned file offset
Elf64_Half    2    2      Unsigned medium integer
Elf64_Word    4    4      Unsigned integer
Elf64_Sword   4    4      Signed integer
Elf64_Xword   8    8      Unsigned long integer
Elf64_Sxword  8    8      Signed long integer
unsigned char 1    1      Unsigned small integer

#define EI_NIDENT 16

typedef struct {
  unsigned char e_ident[EI_NIDENT];     16  16B
  Elf32_Half e_type;                    18    H
  Elf32_Half e_machine;                 20    H
  Elf32_Word e_version;                 24    I
  Elf32_Addr e_entry;                   28    I
  Elf32_Off e_phoff;                    32    I
  Elf32_Off e_shoff;                    36    I
  Elf32_Word e_flags;                   40    I
  Elf32_Half e_ehsize;                  42    H
  Elf32_Half e_phentsize;               44    H
  Elf32_Half e_phnum;                   46    H
  Elf32_Half e_shentsize;               48    H
  Elf32_Half e_shnum;                   50    H
  Elf32_Half e_shstrndx;                52    H
} Elf32_Ehdr;

typedef struct {
  unsigned char   e_ident[EI_NIDENT];
  Elf64_Half      e_type;        2  H
  Elf64_Half      e_machine;     2  H
  Elf64_Word      e_version;     4  I
  Elf64_Addr      e_entry;       8  Q
  Elf64_Off       e_phoff;       8  Q
  Elf64_Off       e_shoff;       8  Q
  Elf64_Word      e_flags;       4  I
  Elf64_Half      e_ehsize;      2  H
  Elf64_Half      e_phentsize;   2  H
  Elf64_Half      e_phnum;       2  H
  Elf64_Half      e_shentsize;   2  H
  Elf64_Half      e_shnum;       2  H
  Elf64_Half      e_shtrndx;     2  H
} Elf64_Ehdr;
"""
def readElfHeader(f):
  global elf_class
  global end_char
  fmt_ident = '16s'
  fmt32 = 'HHIIIIIHHHHHH'
  fmt64 = 'HHIQQQIHHHHHH'
  fields = ['e_ident', 'e_type', 'e_machine', 'e_version', 'e_entry',
    'e_phoff', 'e_shoff', 'e_flags', 'e_ehsize', 'e_phentsize',
    'e_phnum', 'e_shentsize', 'e_shnum', 'e_shstrndx']
  f.seek(0) #adjust position 
  ident_data = f.read(struct.calcsize(fmt_ident))
  fmt = None
  if ord(ident_data[4]) == 1:
    elf_class = 32
    fmt = fmt32
    data = f.read(struct.calcsize(fmt32))
  elif ord(ident_data[4]) == 2:
    elf_class = 64
    fmt = fmt64
    data = f.read(struct.calcsize(fmt64))
  if ord(ident_data[5]) == 1: #little-endian
    fmt = '<' + fmt_ident + fmt
    end_char = '<'
  elif ord(ident_data[5]) == 2: #big-endian
    fmt = '>' + fmt_ident + fmt
    end_char = '>'
  return dict(zip(fields,struct.unpack(fmt,ident_data+data)))

"""

typedef struct {
  Elf32_Word      sh_name;        I
  Elf32_Word      sh_type;        I
  Elf32_Word      sh_flags;       I
  Elf32_Addr      sh_addr;        I
  Elf32_Off       sh_offset;      I
  Elf32_Word      sh_size;        I
  Elf32_Word      sh_link;        I
  Elf32_Word      sh_info;        I
  Elf32_Word      sh_addralign;   I
  Elf32_Word      sh_entsize;     I
} Elf32_Shdr;
"""
def readShHeaders(f,elf_hdr):
  print ' [===]  read section header...\n'
  fmt = '@IIIIIIIIII'
  fmt32 = 'IIIIIIIIII'
  fmt64 = 'IIQQQQIIQQ'
  fields = [  'sh_name_idx', 'sh_type', 'sh_flags', 'sh_addr', 'sh_offset', 
              'sh_size', 'sh_link', 'sh_info', 'sh_addralign', 'sh_entsize' ]

  sh_hdrs = []
  f.seek(elf_hdr['e_shoff'])
  for shentid in range(elf_hdr['e_shnum']):
    data = f.read(elf_hdr['e_shentsize'])
    sh_hdrs.append(dict(zip(fields,struct.unpack(fmt,data))))
  shstrndx_hdr = sh_hdrs[elf_hdr['e_shstrndx']]
  f.seek(shstrndx_hdr['sh_offset'])
  shstr = f.read(shstrndx_hdr['sh_size'])
  idx = 0
  for hdr in sh_hdrs:
    offset = hdr['sh_name_idx']
    hdr['sh_name'] = shstr[offset:offset+shstr[offset:].index(chr(0x0))]
    global shidx_strtab
    if '.strtab' == hdr['sh_name']:
      shidx_strtab = idx
    idx += 1
  print " [===]  read section header over ..\n"
  return sh_hdrs

def printElfHeader(hdr):
    print "ELF Header:"
    for s in hdr:
        print "%s:%s" %(s, hdr[s])

def printShHeaders(shdr):
    print "Section Header Table"
    print "fuck"
    # mdic={}
    for h in shdr:
        for s in h:
          # mdic.setdefault(s,h[s])
          print "%s:%s" %(s, h[s]),
        print
    # print mdic

#---------encrypt code section header by init_array -----------------------------------
'''
encode section header data
'''
def encrypt(content):
  encontent=[]
  for item in content:
    print "chr(ord(item))",chr(ord(item))
    encontent.append(chr(ord(item)) ^ 11)
  return encontent

def encryptSH(fd,elf_hdr,shdr,sname):
  print "begin encrypt .... "
  sh_hdr={}
  for s in shdr:
    if s['sh_name'] == sname:
      sh_hdr=s
      break
  offset = sh_hdr['sh_offset']
  size=sh_hdr['sh_size']
  fd.seek(24)
  fd.write(struct.pack("I",size))
  fd.seek(32)
  fd.write(struct.pack("I",offset))
  fd.seek(offset)
  content=fd.read(size)
  encontent=encrypt(content)
  fd.seek(offset)
  fd.write(''.join(encontent))
  print "encrypt complete .."
  fd.close()
  print "fd close ... "
#-------------------------------------------------

#*********************
def show_section_name(shdr):
  for sh_name in shdr:
    print '==='
    print sh_name # this is dic ,so we can iterator it 
    for key in sh_name.keys():
      if key == '.shstrstab':
        print 'find it ',key
        
      print "-----"
      print "key :",key,' value : ',sh_name.get(key)
      print '-----'
    print '==='
#******************

if __name__=='__main__':
    if len(sys.argv) != 2:
        print "usage: python readELF.py ELFname"
        sys.exit()
    elif len(sys.argv) == 2:
        fname = sys.argv[1]    
    fd = open(fname,'rb+')
    
    hdr = readElfHeader(fd)
    printElfHeader(hdr)
    shdr = readShHeaders(fd,hdr) 
    #call encrypt
    # encryptSH(fd,hdr,shdr,".data")
    show_section_name(shdr)

    # printShHeaders(shdr)