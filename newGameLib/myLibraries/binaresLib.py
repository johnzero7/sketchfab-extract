import bpy
import struct
import os
import traceback
import io
import itertools
from itertools import *
import array

"""
byte=0x2
byte = bin(byte)[2:].rjust(8, '0')
print(byte)
"""
# self.xorKey = [0x33, 0x56 ...]


class Loop:
	def __init__(self):
		pass

blendDir=os.path.dirname(bpy.context.blend_data.filepath)

class BinaryUnpacker():
	def __init__(self, data,log=None):
		self.endian='<'
		self.offset=0
		self.data=data
		self.len=len(data)-self.offset
		self.log=True
		self.logData=""

	def ShowError(self):
		fp = StringIO.StringIO()
		traceback.print_exc(file=fp)
		message = fp.getvalue()
		print(message)


	def saveLog(self,openLog=False):
		if (self.log):
			print("Begin log")
			with open("log.txt","w") as Log:
				Log.write(self.logData+"offset:"+str(self.offset)+"\n")
			if (openLog==True):
				os.system(blendDir+os.sep+"tools"+os.sep+"Notepad++"+os.sep+"notepad++.exe"+" "+"log.txt")
			print("End log")

	def WriteToFile(self,path):
		file=open(path,'wb')
		file.write(self.data)
		file.close

	def WriteToLog(self,text):
		if self.log:self.logData+=str(text)+":"


	def q(self,n):
		data=struct.unpack(self.endian+n*'q',self.data[self.offset:self.offset+(n*8)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*8
		return data

	def i(self,n):
		data=struct.unpack(self.endian+n*'i',self.data[self.offset:self.offset+(n*4)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*4
		return data

	def I(self,n):
		data=struct.unpack(self.endian+n*'I',self.data[self.offset:self.offset+(n*4)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*4
		return data

	def B(self,n):
		data=struct.unpack(self.endian+n*'B',self.data[self.offset:self.offset+(n*1)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*1
		return data

	def b(self,n):
		data=struct.unpack(self.endian+n*'b',self.data[self.offset:self.offset+(n*1)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*1
		return data

	def h(self,n):
		data=struct.unpack(self.endian+n*'h',self.data[self.offset:self.offset+(n*2)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*2
		return data

	def H(self,n):
		data=struct.unpack(self.endian+n*'H',self.data[self.offset:self.offset+(n*2)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*2
		return data

	def f(self,n):
		data=struct.unpack(self.endian+n*'f',self.data[self.offset:self.offset+(n*4)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*4
		return data

	def d(self,n):
		data=struct.unpack(self.endian+n*'d',self.data[self.offset:self.offset+(n*8)] )
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		self.offset+=n*8
		return data

	def half(self,n,h='h'):
		data = []
		for id in range(n):
			data.append(converthalf2float(struct.unpack(self.endian+h,self.data[self.offset:self.offset+2])[0]))
			self.offset+=2
		if self.log:self.logData+=str(self.offset-n*2)+' '+str(data)+'\n'
		return data

	def short(self,n,h='h',exp=12):
		data = []
		for id in range(n):
			data.append(struct.unpack(self.endian+h,self.data[self.offset:self.offset+2])*2**-exp)
		if self.log:self.logData+=str(self.offset-n*2)+' '+str(data)+'\n'
		return data


	def seek(self,off,a=0):
		if a==0:self.offset=off
		if a==1:self.offset+=off

	def dataSize(self):
		return len(self.data)

	def read(self,len=0):
		if len==0:len=self.len
		return self.data[self.offset:self.offset+len]

	def readString(self,n=0):
		data=''
		if (n==0):
			while(True):
				lit =  struct.unpack('c',self.data[self.offset:self.offset+1] )[0]
				self.offset+=1
				if (ord(lit)!=0):
					data+=lit
				else:break
		else:
			for m in range(n):
				lit =  struct.unpack('c',self.data[self.offset:self.offset+1] )[0]
				self.offset+=1
				if (ord(lit)!=0):
					data+=lit
		if self.log:self.logData+=str(self.offset)+' '+str(data)+'\n'
		return data


	def unpack(self,values):
		count=""
		type=None
		out=[]
		for value in values:
			if (value.isdigit()==True):
				count+=value
			else:
				type=value
			if (type):
				if len(count)==0:count=1
				else:count=int(count)
				if type=='i':out.extend(self.i(count))
				elif type=='I':out.extend(self.I(count))
				elif type=='h':out.extend(self.h(count))
				elif type=='H':out.extend(self.H(count))
				elif type=='f':out.extend(self.f(count))
				elif type=='b':out.extend(self.b(count))
				elif type=='B':out.extend(self.B(count))
				elif type=='d':out.extend(self.d(count))
				elif type=='q':out.extend(self.q(count))
				elif type=='half':out.extend(self.half(count))
				elif type=='short':out.extend(self.short(count))
				elif type=='_':self.seek(count,1)
				else:
					print('are you sure ?:',type)
				type=None
				count=""
		return out

	def loop(self,values,count):
		for m in range(count):
			self.unpack(values)




	def tell(self):
		return self.offset

def getDataFromFile(filename):
	data=''
	if (os.path.exists(filename)==True):
		file=open(filename,'rb')
		data=file.read()
	return data



def WriteDataToFile(path,data):
	dirname=os.path.dirname(path)
	if os.path.exists(dirname)==False:os.makedirs(dirname)
	File=open(path,'wb')
	File.write(data)
	File.close()


def GxtToPng(path):
	command=os.path.dirname(bpy.context.blend_data.filepath)+os.sep+"GXTConvert.exe"+' "'+path+'"'
	os.system(command)


def HalfToFloat(h):
	s = int((h >> 15) & 0x00000001) # sign
	e = int((h >> 10) & 0x0000001f) # exponent
	f = int(h & 0x000003ff)  # fraction

	if (e == 0):
		if (f == 0):
			return int(s << 31)
		else:
			while not (f & 0x00000400):
				f <<= 1
				e -= 1
			e += 1
			f &= ~0x00000400
			#print(s,e,f)
	elif (e == 31):
		if (f == 0):
			return int((s << 31) | 0x7f800000)
		else:
			return int((s << 31) | 0x7f800000 | (f << 13))

	e = e + (127 -15)
	f = f << 13
	return int((s << 31) | (e << 23) | f)


def converthalf2float(h):
	id = HalfToFloat(h)
	str = struct.pack('I',id)
	return struct.unpack('f', str)[0]


class BinaryReader():
	"""general BinaryReader
	"""
	def __init__(self, inputFile):
		self.inputFile=inputFile
		self.endian='<'
		self.debug=False
		self.stream={}
		self.logfile=None
		self.log=False
		self.dirname=os.path.dirname(self.inputFile.name)
		basename, ext=os.path.split(self.dirname)
		self.basename=basename
		self.ext=ext
		self.xorKey=None
		self.xorOffset=0
		self.xorData=''
		self.logskip=False
		self.ARRAY=False

	def close(self):
		self.inputFile.close()

	def XOR(self,data):
			self.xorData=''
			for m in range(len(data)):
				ch=ord(	chr(data[m] ^ self.xorKey[self.xorOffset])	)
				self.xorData+=struct.pack('B',ch)
				if (self.xorOffset==len(self.xorKey)-1):
					self.xorOffset=0
				else:
					self.xorOffset+=1

	def logOpen(self):
		logDir='log'
		if (os.path.exists(logDir)==False):
			os.makedirs(logDir)
		self.log=True
		self.logfile=open(os.path.join(logDir, os.path.basename(self.inputFile.name)+'.log'),'w')

	def logClose(self):
		self.log=False
		if (self.logfile is not None):
			self.logfile.close()

	def logWrite(self,data):
		if (self.logfile is not None):
			self.logfile.write(str(data)+'\n')
		else:
			print('WARNING: no log')

	def dirname(self):
		return os.path.dirname(self.inputFile.name)

	def basename(self):
		return os.path.split(os.path.basename(self.inputFile.name))[0]

	def ext(self):
		return os.path.split(os.path.basename(self.inputFile.name))[1]

	def q(self,n):
		offset=self.inputFile.tell()
		data=struct.unpack(self.endian+n*'q',self.inputFile.read(n*8))
		if (self.debug==True):
			print('q',data)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
		return data

	def i(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				if (self.ARRAY==False):
					data=struct.unpack(self.endian+n*'i',self.inputFile.read(n*4))
				else:
					data = array.array('i')
					data.fromfile(self.inputFile, n)
					if (self.endian == ">"):
						data.byteswap()
			else:
				data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*4))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'i',self.xorData)

			if (self.debug==True):
				print('i',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'i',n[m])
				self.inputFile.write(data)

	def I(self,n):
		offset=self.inputFile.tell()
		if (self.xorKey is None):
			data=struct.unpack(self.endian+n*'I',self.inputFile.read(n*4))
		else:
			data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*4))
			self.XOR(data)
			data=struct.unpack(self.endian+n*'I',self.xorData)
		if (self.debug==True):
			print('I',data)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
		return data

	def B(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				if (self.ARRAY==False):
					data=struct.unpack(self.endian+n*'B',self.inputFile.read(n))
				else:
					data = array.array('B')
					data.fromfile(self.inputFile, n)
					if (self.endian == ">"):
						data.byteswap()
			else:
				data=struct.unpack(self.endian+n*'B',self.inputFile.read(n))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'B',self.xorData)
			if (self.debug==True):
				print('B',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'B',n[m])
				self.inputFile.write(data)

	def b(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				if (self.ARRAY==False):
					data=struct.unpack(self.endian+n*'b',self.inputFile.read(n))
				else:
					data = array.array('b')
					data.fromfile(self.inputFile, n)
					if (self.endian == ">"):
						data.byteswap()
			else:
				data=struct.unpack(self.endian+n*'b',self.inputFile.read(n))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'b',self.xorData)
			if (self.debug==True):
				print('b',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'b',n[m])
				self.inputFile.write(data)
	def h(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				if (self.ARRAY==False):
					data=struct.unpack(self.endian+n*'h',self.inputFile.read(n*2))
				else:
					data = array.array('h')
					data.fromfile(self.inputFile, n)
					if (self.endian == ">"):
						data.byteswap()
			else:
				data=struct.unpack(self.endian+n*2*'B',self.inputFile.read(n*2))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'h',self.xorData)
			if (self.debug==True):
				print('h',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'h',n[m])
				self.inputFile.write(data)
	def H(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				if (self.ARRAY==False):
					data=struct.unpack(self.endian+n*'H',self.inputFile.read(n*2))
				else:
					data = array.array('H')
					data.fromfile(self.inputFile, n)
					if (self.endian == ">"):
						data.byteswap()
			else:
				data=struct.unpack(self.endian+n*2*'B',self.inputFile.read(n*2))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'H',self.xorData)
			if (self.debug==True):
				print('H',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'H',n[m])
				self.inputFile.write(data)
	def f(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				if (self.ARRAY==False):
					data=struct.unpack(self.endian+n*'f',self.inputFile.read(n*4))
				else:
					data = array.array('f')
					data.fromfile(self.inputFile, n)
					if (self.endian == ">"):
						data.byteswap()

			else:
				data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*4))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'f',self.xorData)
			if (self.debug==True):
				print('f',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'f',n[m])
				self.inputFile.write(data)
	def d(self,n):
		if (self.inputFile.mode=='rb'):
			offset=self.inputFile.tell()
			if (self.xorKey is None):
				data=struct.unpack(self.endian+n*'d',self.inputFile.read(n*8))
			else:
				data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*8))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'d',self.xorData)
			if (self.debug==True):
				print('d',data)
			if (self.log==True):
				if (self.logfile is not None and self.logskip is not True):
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if (self.inputFile.mode=='wb'):
			for m in range(len(n)):
				data=struct.pack(self.endian+'d',n[m])
				self.inputFile.write(data)
	def half(self,n,h='h'):
		array = []
		offset=self.inputFile.tell()
		for id in range(n):
			#array.append(converthalf2float(struct.unpack(self.endian+'H',self.inputFile.read(2))[0]))
			array.append(converthalf2float(struct.unpack(self.endian+h,self.inputFile.read(2))[0]))
		if (self.debug==True):
			print('half',array)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(offset)+'	'+str(array)+'\n')
		return array

	def short(self,n,h='h',exp=12):
		array = []
		offset=self.inputFile.tell()
		for id in range(n):
			array.append(struct.unpack(self.endian+h,self.inputFile.read(2))[0]*2**-exp)
			#array.append(self.H(1)[0]*2**-exp)
		if (self.debug==True):
			print('short',array)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(offset)+'	'+str(array)+'\n')
		return array

	def i12(self,n):
		array = []
		offset=self.inputFile.tell()
		for id in range(n):
			if (self.endian=='>'):
				var='\x00'+self.inputFile.read(3)
			if (self.endian=='<'):
				var=self.inputFile.read(3)+'\x00'
			array.append(struct.unpack(self.endian+'i',var)[0])
		if (self.debug==True):
			print(array)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(offset)+'	'+str(array)+'\n')
		return array

	def find(self,values="\x00",size=100,all=None):
		list=[]
		start=self.inputFile.tell()
		s=""
		while(True):
			data=self.inputFile.read(size+len(values))
			off=data.find(values)
			if (off>=0):
				s+=data[:off]
				self.inputFile.seek(start+off+len(values))
				break
			else:
				self.inputFile.seek(-len(values),1)
				s+=data
				start+=size
			if self.inputFile.tell()>=self.fileSize():break




		if (self.debug==True):
			pass#print(s)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(start)+'	'+s+'\n')
		return s

	def getValue(self,values="\x00",size=100,all=None):
		list=[]
		start=self.inputFile.tell()
		mam=0
		while(True):
			data=self.inputFile.read(size+len(values))
			off=data.find(values)
			if (off>=0):
				self.inputFile.seek(start+off+len(values))
				mam=1
				break
			else:
				self.inputFile.seek(-len(values),1)
				start+=size
			if (self.inputFile.tell()>=self.fileSize()):
				print('dziala')
				break
		return mam


	def find1(self,var,size=999):

		start=self.inputFile.tell()
		s=''
		while(True):
			data=self.inputFile.read(size)
			off=data.find(var)
			#print(off)
			if (off>=0):
				s+=data[:off]
				self.inputFile.seek(start+off+len(var))
				#print('Found',var,'offset=',self.inputFile.tell())
				break
			else:
				s+=data
				start+=size
			#print(self.inputFile.tell()	,self.fileSize())
			if (self.inputFile.tell()>=self.fileSize()):
				break
		if (self.debug==True):
			print(s)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(start)+'	'+s+'\n')
		return s

	def string(self,values="\x00",size=100):
		list=[]
		start=self.inputFile.tell()
		s=""
		while(True):
			data=self.inputFile.read(size+len(values))
			off=data.find(values)
			if (off>=0):
				s+=data[:off]
				self.inputFile.seek(start+off+len(values))
				break
			else:
				self.inputFile.seek(-len(values),1)
				s+=data
				start+=size
			if (self.inputFile.tell()>=self.fileSize()):
				break

		if (self.debug==True):
			pass#print(s)
		if (self.log==True):
			if (self.logfile is not None and self.logskip is not True):
				self.logfile.write('offset '+str(start)+'	'+s+'\n')
		return s

	def findAll(self,var,size=100):
		list=[]
		while(True):
			start=self.inputFile.tell()
			data=self.inputFile.read(size)
			off=data.find(var)
			#print(off,self.inputFile.tell())
			if (off>=0):
				list.append(start+off)
				#print(start+off)
				self.inputFile.seek(start+off+len(var))
				#if (self.debug==True):
				#	print(start+off)
			else:
				start+=size
				self.inputFile.seek(start)
			if (	self.inputFile.tell()>self.fileSize()):
				break
		return list




	def fileSize(self):
		back=self.inputFile.tell()
		self.inputFile.seek(0,2)
		tell=self.inputFile.tell()
		#self.inputFile.seek(0)
		self.inputFile.seek(back)
		return tell

	def seek(self,off,a=0):
		self.inputFile.seek(off,a)

	def seekpad(self,pad,type=0):
		''' 16-byte chunk alignment'''
		size=self.inputFile.tell()
		seek = (pad - (size % pad)) % pad
		if (type==1):
			if (seek==0):
				seek+=pad
		self.inputFile.seek(seek, 1)

	def read(self,count):
		back=self.inputFile.tell()
		if (self.xorKey is None):
			return self.inputFile.read(count)
		data=struct.unpack(self.endian+count*'B',self.inputFile.read(count))
		self.XOR(data)
		return self.xorData

	def bytes(self,count):
		back=self.inputFile.tell()
		if (self.xorKey is None):
			return self.inputFile.read(count)
		data=struct.unpack(self.endian+count*'B',self.inputFile.read(count))
		self.XOR(data)
		return self.xorData

	def unpack(self,values):
		#"5i6hi"
		count=""
		type=None
		#print(values)
		out=[]
		for value in values:
			#print(value,value.isdigit())
			if (value.isdigit()==True):
				count+=value
			else:
				type=value
			if (type):
				if len(count)==0:
					count=1
				else:
					count=int(count)
				if type=='i':out.extend(self.i(count))
				elif type=='I':out.extend(self.I(count))
				elif type=='h':out.extend(self.h(count))
				elif type=='H':out.extend(self.H(count))
				elif type=='f':out.extend(self.f(count))
				elif type=='b':out.extend(self.b(count))
				elif type=='B':out.extend(self.B(count))
				elif type=='d':out.extend(self.d(count))
				elif type=='q':out.extend(self.q(count))
				elif type=='half':out.extend(self.half(count))
				elif type=='short':out.extend(self.short(count))
				elif type=='_':self.seek(count,1)
				#elif type=='i':self.i(count)
				else:
					print('are you sure ?:',type)
				type=None
				count=""
		return out



	def write(self,string):
		self.inputFile.write(string)

	def tell(self):
		val=self.inputFile.tell()
		if (self.debug==True):
			print('current offset is',val)
		return val

	def word(self,long):
		if (long<10000):
			if (self.inputFile.mode=='rb'):
				offset=self.inputFile.tell()
				s=''
				for j in range(0,long):
					if (self.xorKey is None):
						lit =  struct.unpack('c',self.inputFile.read(1))[0]
					else:
						data=struct.unpack(self.endian+'B',self.inputFile.read(1))
						self.XOR(data)
						lit=struct.unpack(self.endian+'c',self.xorData)[0]
					if (ord(lit)!=0):
						s+=lit
				if (self.debug==True):
					print(s)
				if (self.log==True):
					if (self.logfile is not None and self.logskip is not True):
						self.logfile.write('offset '+str(offset)+'	'+s+'\n')
				return s
			if (self.inputFile.mode=='wb'):
				self.inputFile.write(long)
		else:
			if (self.debug==True):
				print('WARNING:too long')

	def decode(self,list):
		litery='qwertyuiopasdfghjklzxcvbnm'
		new=[]
		for item in list:
			if (chr(item).lower() in litery):
				new.append(chr(item))
			else:
				new.append(item)
		return new


class New:
	def __init__(self,basename,mode,sys):
		self.mode=mode
		self.path=None
		self.basename=basename
		self.file=None
		self.sys=sys
		self.data=None
	def open(self):
		drive,tail=os.path.splitdrive(self.basename)
		g=None

		if (len(drive)==0 and len(tail)!=0):
			self.path=os.path.join(self.sys.dir, self.sys.base+'_files', self.basename)
			#print(path)
			dirpath=os.path.dirname(self.path)
			os.makedirs(dirpath, exist_ok=True)

		if (len(drive)!=0 and len(tail)!=0):
			dirpath=os.path.dirname(self.basename)
			self.path=self.basename
			if (os.path.exists(dirpath)==False):
				os.makedirs(dirpath)

		self.file=open(self.path,self.mode)
		if (self.mode=='wb'):
			g=BinaryReader(self.file)
		if (self.mode=='rb'):
			g=BinaryReader(self.file)
		if (self.mode=='w'):
			g=self.file
		return g

	def close(self):
		if self.file:self.file.close()


class Sys1(object):
	def __init__(self,input):
		self.input=input.lower()
		#if (os.path.exists(self.input)):
		self.dir=os.path.dirname(self.input)
		self.base=os.path.basename(self.input)
		if ('.' in os.path.basename(self.input)):
			self.ext=os.path.basename(self.input).split('.')[-1].lower()
			self.base=self.base.split(self.ext)[0].replace('.','')
		else:
			self.ext=None
		self.blendPath=bpy.context.blend_data.filepath
		self.log=False
		self.newFile=None

	#def new(self,path,mode):
	#	self.newFile=New(path,mode,self)
	#	g=self.newFile.open()
	#	return g

	#def close(self):
	#	if self.newFile:self.newFile.close()

	def	addDir(self,name):
		newDir=self.dir+os.sep+name
		if (os.path.exists(newDir)==False):
			os.makedirs(newDir)

	def getFiles(self,what,part=None):
		search=Searcher()
		search.dir=self.dir
		search.what=what
		search.part=part
		search.run()
		if (self.log==True):
			print('Found',len(search.list),what)
		return search.list



	def parseFile(self,function,mode='rb',log=0):
		#os.system('cls')
		if (os.path.exists(self.input)==True):
			if (mode=='rb'):
				readFile=open(self.input,'rb')
				g=BinaryReader(readFile)
				if log==True:g.logOpen()
				try:function(self.input,g)
				except:
					fp = StringIO.StringIO()
					traceback.print_exc(file=fp)
					message = fp.getvalue()
					print(message)
					values=message.split('File ')
					lines=values[-1].replace('\n','|')
					Blender.Draw.PupMenu(lines)
				if log==True:g.logClose()
				readFile.close()
			if (mode=='r'):
				function(self.input)
		else:

			Blender.Draw.PupMenu('ten plik nie istnieje'+'|'+self.input)


	def parseFiles(self,function,files,mode='rb',log=0):
		for i,filePath in enumerate(files):
			if (self.log==True):
				print('file:',i,'from',len(files),os.path.basename(filePath))
			if (mode=='rb'):
				#os.system('cls')
				readFile=open(filePath,'rb')
				g=BinaryReader(readFile)
				if log==True:g.logOpen()
				function(filePath,g)
				if log==True:g.logClose()
				readFile.close()

	def join(self,path):
		returnDir=None
		path=path.lower()
		if (os.path.isabs(path)==False):
			path=os.path.relpath(path)
			splitpath=os.path.split(path)
			print
			if (len(splitpath[0])!=0):
				returnDir=self.input.split(splitpath[0])[0]+path
			else:
				returnDir=self.dir+os.sep+path
		else:
			drive,tail=os.path.splitdrive(path)
			if (len(drive)>0 and os.path.exists(path)==True):
				returnDir=path
			elif (len(drive)==0):
				returnDir=os.path.normpath(self.dir+os.sep+tail)
		return returnDir


class Searcher():
	def __init__(self):
		self.dir=None
		self.list=[]
		self.part=None#ext,dir,base
		self.what=None
	def run(self):
		dir=self.dir
		def tree(dir):
			listDir = os.listdir(dir)
			olddir = dir
			for file in listDir:
				if (self.part=='ext'):
					if (self.what.lower() in file.lower().split('.')[-1]):
						if (os.path.isfile(olddir+os.sep+file)==True):
							self.list.append(olddir+os.sep+file)

				else:
					if (self.what.lower() in file.lower()):
						if (os.path.isfile(olddir+os.sep+file)==True):
							self.list.append(olddir+os.sep+file)

				if (os.path.isdir(olddir+os.sep+file)==True):
					dir = olddir+os.sep+file
					tree(dir)
		tree(dir)



class Sys(object):
	def __init__(self,input):
		self.input=input.lower()
		#if (os.path.exists(self.input)):
		self.dir=os.path.dirname(self.input)
		self.base=os.path.basename(self.input)
		if ('.' in os.path.basename(self.input)):
			self.ext=os.path.basename(self.input).split('.')[-1].lower()
			#self.base=self.base.split(self.ext)[0].replace('.','')
		else:
			self.ext=None
		self.blendPath=bpy.context.blend_data.filepath
		self.log=False
		self.newFile=None

	#def new(self,path,mode):
	#	self.newFile=New(path,mode,self)
	#	g=self.newFile.open()
	#	return g

	#def close(self):
	#	if self.newFile:self.newFile.close()

	def	addDir(self,name):
		newDir=self.dir+os.sep+name
		if (os.path.exists(newDir)==False):
			os.makedirs(newDir)

	def getFiles(self,what,part=None):
		search=Searcher()
		search.dir=self.dir
		search.what=what
		search.part=part
		search.run()
		if (self.log==True):
			print('Found',len(search.list),what)
		#if len(search.list)==1;
		#	return search.list[0]
		if (len(search.list)==0):
			return None
		else:
			return search.list



	def parseFile(self,function,mode='rb',log=0):
		#os.system('cls')
		if (os.path.exists(self.input)==True):
			if (mode=='rb'):
				readFile=open(self.input,'rb')
				g=BinaryReader(readFile)
				if log==True:g.logOpen()
				function(self.input,g)
				if log==True:g.logClose()
				readFile.close()
			if (mode=='r'):
				g=open(self.input,'r')
				function(self.input,g)
				g.close()
		else:

			Blender.Draw.PupMenu('ten plik nie istnieje'+'|'+self.input)


	def parseFiles(self,function,files,mode='rb',log=0):
		for i,filePath in enumerate(files):
			if (self.log==True):
				print('file:',i,'from',len(files),os.path.basename(filePath))
			if (mode=='rb'):
				#os.system('cls')
				readFile=open(filePath,'rb')
				g=BinaryReader(readFile)
				if log==True:g.logOpen()
				try:function(filePath,g)
				except:pass
				if log==True:g.logClose()
				readFile.close()

	def join(self,path):
		returnPath=None
		if (os.path.exists(path)==False):
			if (path is not None):
				path=path.lower()
				if (os.path.isabs(path)==False):
					path=os.path.relpath(path)
					split2=path.split(os.sep)
					split1=self.dir.split(os.sep)
					#print(split2)
					#print(split1)
					for m in range(len(split1)):
						#result1=combinations(split1,m+1)
						for item1 in combinations(split1,m+1):
							for n in range(len(split2)):
								#result2=combinations(split2,n+1)
								for item2 in combinations(split2,n+1):
									path=str(item1+item2).replace("('",'').replace("')",'').replace("', '",os.sep)
									#print(path)
									if (os.path.exists(path)==True and split2[-1] in path):
										print(path,'True')
										returnPath=path


					#returnPath=self.input.split(splitpath[0])[0]+os.sep+path
				else:
					drive,tail=os.path.splitdrive(path)
					if (len(drive)>0 and os.path.exists(path)==True):
						returnDir=path
					elif (len(drive)==0):
						returnPath=os.path.normpath(self.dir+os.sep+tail)
		else:
			returnPath=path
		return returnPath

