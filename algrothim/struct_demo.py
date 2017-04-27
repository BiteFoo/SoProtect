# -*- coding: utf-8 -*-
import struct
import binascii


def strct():

#struct.unpack(fmt,ident_data+data)
	values=(1,"abc",'zhou')
	fmt="I16s5s"
	s=struct.Struct(fmt)
	# print'', *values
	ss=s.pack(*values)
	value=s.unpack(ss)

	print value

if __name__ == '__main__':
	strct()