# -*- coding: UTF-8 -*-
import sys
import struct

class SO_Header:
    def __init__(self):
        self.e_ident = ""
        self.e_type = 0
        self.e_machine = ""
        self.e_version = ""
        self.e_entry = 0 #对so而言无用 
        self.e_phoff = 0 
        self.e_shoff = 0 #section header table的偏移( 偏移32，4字节 )
        self.e_flags = ""
        self.e_ehsize = 0 #elf头部大小(偏移40，2字节)
        self.e_phentsize = 0 
        self.e_phnum = 0
        self.e_shentsize = 0 #section header table中每个表项的大小 （偏移46，2字节）
        self.e_shnum = 0 #section header table表项数目 （偏移48，2字节）
        self.e_shstrndx = 0 #name section的索引 (偏移50，2字节)


#每个item为40字节，其中每个字段都为4字节
class SectionTableItem:
    def __init__(self):
        self.sh_name = "" #section的名字（索引） 
        self.sh_type = ""
        self.sh_flags = ""
        self.sh_addr = 0 #在内存中的偏移
        self.sh_offset = 0 #该section相对于elf文件头的偏移
        self.sh_size = 0 #该section的总大小
        self.sh_link = 0
        self.sh_info = ""
        self.sh_addralign = 0
        self.sh_entsize = 0
        

class SO:
    def __init__(self,path):
        self.so = open(path,'rw')
        self.elf32_ehdr = SO_Header()
        self.section_header_table = []
        self.section_name_table = ""
        
        self.ReadELFHeader()
        self.ReadSectionTable()
        
    
    #只读出与加壳有关的关键数据
    def ReadELFHeader(self):
        self.so.seek(32)  
        # print 'so.seek(32) :',struct.unpack("I",self.so.read(4))[0]
        self.elf32_ehdr.e_shoff = struct.unpack("I",self.so.read(4))[0]
        self.so.seek(40)
        # print 'so.seek(40) :',struct.unpack("h",self.so.read(2))
        self.elf32_ehdr.e_ehsize = struct.unpack("h",self.so.read(2))[0]
        self.so.seek(46)  
        # print 'so.seek(46) :',struct.unpack("h",self.so.read(2))
        self.elf32_ehdr.e_shentsize = struct.unpack("h",self.so.read(2))[0]
        self.elf32_ehdr.e_shnum = struct.unpack("h",self.so.read(2))[0]
        # print 'self32_ehdr.e_shnum :',struct.unpack("h",self.so.read(2))[0]
        self.elf32_ehdr.e_shstrndx = struct.unpack("h",self.so.read(2))[0]  


    #读取section table 只读与加壳有关的数据
    def ReadSectionTable(self):
        self.so.seek(self.elf32_ehdr.e_shoff)
        num = self.elf32_ehdr.e_shnum

        #esize = self.elf32_ehdr.e_shentsize
        
        #print self.elf32_ehdr.e_shoff,num
        
        for i in xrange(num):
            sectionitem = SectionTableItem()
            sectionitem.sh_name = struct.unpack("I",self.so.read(4))[0]
            self.so.seek(8,1)
            sectionitem.sh_addr = struct.unpack("I",self.so.read(4))[0]
            sectionitem.sh_offset = struct.unpack("I",self.so.read(4))[0]
            sectionitem.sh_size = struct.unpack("I",self.so.read(4))[0]
            self.section_header_table.append(sectionitem)
            self.so.seek(16,1)            

        # print 'section header tab ',self.section_header_table
        for item in self.section_header_table:
            print 'key:',type(item)
        
        name_section_offset = self.section_header_table[self.elf32_ehdr.e_shstrndx].sh_offset        
                
        self.so.seek(name_section_offset)
        l = self.section_header_table[self.elf32_ehdr.e_shstrndx].sh_size
        self.section_name_table = self.so.read(l)

        #读取所有section名
        for i in xrange(num):
            idx = self.section_header_table[i].sh_name
            name = []
            while True:
                if self.section_name_table[idx] != '\0':
                    name.append(self.section_name_table[idx])
                else:
                    break
                idx+=1
            print "".join(name)

 

if __name__ == "__main__":

    if len(sys.argv) !=2:
        print "python elfEncrypt.py ELFNAME"

    elif len(sys.argv) == 2:
        print 'so ',sys.argv[1]
        df = SO(sys.argv[1])