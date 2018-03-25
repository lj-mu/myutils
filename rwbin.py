import numpy as np
import struct
import os.path
import sys

def readbin(filename,size,precision='real*4',skip=0,endianness='ieee-be'):
#
# write a ndarray into binary file for MITgcm.
#
#         'filename'  :   Prefix of the output file name
#         'size'      :   data size
#         'precision' :  'real*4'(default) or 'real*8'
#	        'skip'      :   skip data (default 0)
#	        'endianness':  'ieee-be'(default) or 'ieee-le'
#
# Example: 
#         from rwbin import readbin
#
# --->    data=readbin('sst_1979.bin',[2,3])
#	    or
#         data=readbin('sst_1979.bin',[2,3],'real*8',6,'ieee-be')
#
# Date: 29-04-2017
# by mlj
#

# data format
	if endianness == 'ieee-be': 
		df_part1='>'
	elif endianness == 'ieee-le': 
		df_part1='<'
	else:
		print('Error endianness!')
		sys.exit(1)

	if precision == 'real*4': 
		df_part2='f'
		length=4
	elif precision == 'real*8': 
		df_part2='d'
		length=8
	else:
		print('Error precision!')
		sys.exit(1)
	
	dataformat=df_part1+str(np.prod(size))+df_part2
# read
	fout=open(filename,"rb")
	if skip!=0 : fout.seek(length*skip*np.prod(size))
	data=struct.unpack(dataformat, fout.read(length*np.prod(size)))
	fout.close()	
	return np.reshape(data,size,order='F')




def writebin(filename,ndarray,precision='real*4',skip=0,endianness='ieee-be'):
#
# write a ndarray into binary file for MITgcm.
#
#         'filename'  :   Prefix of the output file name
#         'ndarray'   :   data
#         'precision' :  'real*4'(default) or 'real*8'
#	        'skip'      :   skip data (default 0)
#	        'endianness':  'ieee-be'(default) or 'ieee-le'
#
# Example: 
#         from rwbin import writebin
#         import numpy as np
#
#         sst=np.array([[1.5898,1.6778,1.9928],[1.7736,2.82828,3.98282]])
#	
# --->    writebin('sst_1979.bin',sst)
#	   or
#         writebin('sst_1979.bin',sst,'real*8',3,'ieee-be')
#
# Date: 29-04-2017
# by mlj

# data preparation
	size=np.prod(ndarray.shape)
	arrayCol=np.reshape(ndarray,(size,1),order='F')
# data format
	if endianness == 'ieee-be': 
		df_part1='>'
	elif endianness == 'ieee-le': 
		df_part1='<'
	else:
		print('Error endianness!')
		sys.exit(1)

	if precision == 'real*4': 
		df_part2='f'
		length=4
	elif precision == 'real*8': 
		df_part2='d'
		length=8
	else:
		print('Error precision!')
		sys.exit(1)
	
	dataformat=df_part1+str(size)+df_part2

# write
	if os.path.isfile(filename) :
		fout=open(filename,"r+b")
	else:
		fout=open(filename,"wb")

	fout.seek(skip*length*size,0)
	fout.write(struct.pack(dataformat,*arrayCol))
	fout.close()
