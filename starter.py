import newGameLib
from newGameLib import *
import Blender

import array
import subprocess


htm1="""
<head>
   <script type="text/javascript" src="https://static.sketchfab.com/api/sketchfab-viewer-1.3.0.js"></script>

   <script type="text/javascript" src="https://cdn.jsdelivr.net/gh/shaderbytes/Sketchfab-Viewer-API-Utility@v2.0.0.7/SketchfabAPIUtility.js"></script>

</head>

<body>
  <div class="center-div">
	<iframe id="api-frame" width="1000" height="550"	 allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
  </div>

  <script>
	  function onSketchfabUtilityReady(){
		 sketchfabAPIUtilityInstance.removeEventListener(sketchfabAPIUtilityInstance.EVENT_INITIALIZED, onSketchfabUtilityReady);
		 //some code here..
	  };
	  var sketchfabAPIUtilityInstance = new SketchfabAPIUtility("###"""
htm2="""af528e3df5f766ca012f5e065c7cb812"""
htm3="""", document.getElementById("api-frame"), {"autostart": 1 });
	  sketchfabAPIUtilityInstance.addEventListener(sketchfabAPIUtilityInstance.EVENT_INITIALIZED, onSketchfabUtilityReady);
	  sketchfabAPIUtilityInstance.create();
   </script>

</body>
"""



class BinaryReader(file):
	"""general BinaryReader
	"""
	def __init__(self, inputFile):
		self.inputFile=inputFile
		self.endian='<'
		self.debug=False
		self.stream={}
		self.logfile=None
		self.log=False
		self.dirname=Blender.sys.dirname(self.inputFile.name)
		self.basename=Blender.sys.basename(self.inputFile.name).split('.')[0]
		self.ext=Blender.sys.basename(self.inputFile.name).split('.')[-1]
		self.xorKey=None
		self.xorOffset=0
		self.xorData=''
		self.logskip=False

	def close(self):
		self.inputFile.close()

	def XOR(self,data):
			self.xorData=''
			for m in range(len(data)):
				ch=ord(	chr(data[m] ^ self.xorKey[self.xorOffset])	)
				self.xorData+=struct.pack('B',ch)
				if self.xorOffset==len(self.xorKey)-1:
					self.xorOffset=0
				else:
					self.xorOffset+=1


	def logOpen(self):
		logDir='log'
		if os.path.exists(logDir)==False:os.makedirs(logDir)
		self.log=True
		self.logfile=open(logDir+os.sep+os.path.basename(self.inputFile.name)+'.log','w')
	def logClose(self):
		self.log=False
		if self.logfile is not None:
			self.logfile.close()
	def logWrite(self,data):
		if self.logfile is not None:
			self.logfile.write(str(data)+'\n')
		else:
			print 'WARNING: no log'

	def dirname(self):
		return Blender.sys.dirname(self.inputFile.name)
	def basename(self):
		return Blender.sys.basename(self.inputFile.name).split('.')[0]
	def ext(self):
		return Blender.sys.basename(self.inputFile.name).split('.')[-1]


	def q(self,n):
		offset=self.inputFile.tell()
		data=struct.unpack(self.endian+n*'q',self.inputFile.read(n*8))
		if self.debug==True:
			print 'q',data
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
		return data

	def i(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				#data=struct.unpack(self.endian+n*'i',self.inputFile.read(n*4))

				data = array.array('i')
				data.fromfile(self.inputFile, n)
				if self.endian == ">": data.byteswap()


			else:
				data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*4))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'i',self.xorData)

			if self.debug==True:
				print 'i',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'i',n[m])
				self.inputFile.write(data)

	def I(self,n):
		offset=self.inputFile.tell()
		if self.xorKey is None:
			data=struct.unpack(self.endian+n*'I',self.inputFile.read(n*4))
		else:
			data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*4))
			self.XOR(data)
			data=struct.unpack(self.endian+n*'I',self.xorData)
		if self.debug==True:
			print 'I',data
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
		return data

	def B(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				#data=struct.unpack(self.endian+n*'B',self.inputFile.read(n))

				data = array.array('B')
				data.fromfile(self.inputFile, n)
				if self.endian == ">": data.byteswap()


			else:
				data=struct.unpack(self.endian+n*'B',self.inputFile.read(n))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'B',self.xorData)
			if self.debug==True:
				print 'B',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'B',n[m])
				self.inputFile.write(data)
	def b(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				#data=struct.unpack(self.endian+n*'b',self.inputFile.read(n))
				data = array.array('b')
				data.fromfile(self.inputFile, n)
				if self.endian == ">": data.byteswap()
			else:
				data=struct.unpack(self.endian+n*'b',self.inputFile.read(n))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'b',self.xorData)
			if self.debug==True:
				print 'b',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'b',n[m])
				self.inputFile.write(data)
	def h(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				#data=struct.unpack(self.endian+n*'h',self.inputFile.read(n*2))

				data = array.array('h')
				data.fromfile(self.inputFile, n)
				if self.endian == ">": data.byteswap()


			else:
				data=struct.unpack(self.endian+n*2*'B',self.inputFile.read(n*2))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'h',self.xorData)
			if self.debug==True:
				print 'h',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'h',n[m])
				self.inputFile.write(data)
	def H(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				#data=struct.unpack(self.endian+n*'H',self.inputFile.read(n*2))

				data = array.array('H')
				data.fromfile(self.inputFile, n)
				if self.endian == ">": data.byteswap()


			else:
				data=struct.unpack(self.endian+n*2*'B',self.inputFile.read(n*2))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'H',self.xorData)
			if self.debug==True:
				print 'H',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'H',n[m])
				self.inputFile.write(data)
	def f(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				#data=struct.unpack(self.endian+n*'f',self.inputFile.read(n*4))

				data = array.array('f')
				data.fromfile(self.inputFile, n)
				if self.endian == ">": data.byteswap()

			else:
				data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*4))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'f',self.xorData)
			if self.debug==True:
				print 'f',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'f',n[m])
				self.inputFile.write(data)
	def d(self,n):
		if self.inputFile.mode=='rb':
			offset=self.inputFile.tell()
			if self.xorKey is None:
				data=struct.unpack(self.endian+n*'d',self.inputFile.read(n*8))
			else:
				data=struct.unpack(self.endian+n*4*'B',self.inputFile.read(n*8))
				self.XOR(data)
				data=struct.unpack(self.endian+n*'d',self.xorData)
			if self.debug==True:
				print 'd',data
			if self.log==True:
				if self.logfile is not None and self.logskip is not True:
					self.logfile.write('offset '+str(offset)+'	'+str(data)+'\n')
			return data
		if self.inputFile.mode=='wb':
			for m in range(len(n)):
				data=struct.pack(self.endian+'d',n[m])
				self.inputFile.write(data)
	def half(self,n,h='h'):
		array = []
		offset=self.inputFile.tell()
		for id in range(n):
			#array.append(converthalf2float(struct.unpack(self.endian+'H',self.inputFile.read(2))[0]))
			array.append(converthalf2float(struct.unpack(self.endian+h,self.inputFile.read(2))[0]))
		if self.debug==True:
			print 'half',array
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(offset)+'	'+str(array)+'\n')
		return array

	def short(self,n,h='h',exp=12):
		array = []
		offset=self.inputFile.tell()
		for id in range(n):
			array.append(struct.unpack(self.endian+h,self.inputFile.read(2))[0]*2**-exp)
			#array.append(self.H(1)[0]*2**-exp)
		if self.debug==True:
			print 'short',array
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(offset)+'	'+str(array)+'\n')
		return array

	def i12(self,n):
		array = []
		offset=self.inputFile.tell()
		for id in range(n):
			if self.endian=='>':
				var='\x00'+self.inputFile.read(3)
			if self.endian=='<':
				var=self.inputFile.read(3)+'\x00'
			array.append(struct.unpack(self.endian+'i',var)[0])
		if self.debug==True:
			print array
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(offset)+'	'+str(array)+'\n')
		return array



	def find(self,var):
		start=self.inputFile.tell()
		s=''
		while(True):
			c=self.inputFile.read(1)
			#print c
			if c==var[0]:
				if len(var)>1:
					for m in range(1,len(var)):
						c=self.inputFile.read(1)
						if c!=var[m]:
							break
					if m==len(var)-1:
						break
				else:
					break
			else:
				s+=c





		#if self.log==True:
		#	if self.logfile is not None and self.logskip is not True:
		#		self.logfile.write('offset '+str(start)+'	'+s+'\n')
		return s

	def find1(self,var,size=999):

		start=self.inputFile.tell()
		s=''
		while(True):
			data=self.inputFile.read(size)
			off=data.find(var)
			#print off
			if off>=0:
				s+=data[:off]
				self.inputFile.seek(start+off+len(var))
				#print 'znaleziono',var,'offset=',self.inputFile.tell()
				break
			else:
				s+=data
				start+=size
			#print self.inputFile.tell()	,self.fileSize()
			if self.inputFile.tell()>=self.fileSize():break
		if self.debug==True:
			print s
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(start)+'	'+s+'\n')
		return s

	def find10(self,var):

		start=self.inputFile.tell()
		s=''
		data=self.inputFile.read()
		off=data.find(var)
		if off>=0:
			s+=data[:off]
			self.inputFile.seek(start+off+len(var))
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write('offset '+str(start)+'	'+s+'\n')
		return s

	def findAll(self,var,size=100):
		list=[]
		while(True):
			start=self.inputFile.tell()
			data=self.inputFile.read(size)
			off=data.find(var)
			#print off,self.inputFile.tell()
			if off>=0:
				list.append(start+off)
				#print start+off
				self.inputFile.seek(start+off+len(var))
				#if self.debug==True:
				#	print start+off
			else:
				start+=size
				self.inputFile.seek(start)
			if	self.inputFile.tell()>self.fileSize():
				break
		return list


	def findchar(self,var):
		offset=self.inputFile.find(var)
		if self.debug==True:
			print var,'znaleziono',offset
		if self.log==True:
			if self.logfile is not None and self.logskip is not True:
				self.logfile.write(var+' znaleziono '+str(offset)+'\n')
		return offset


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
		if type==1:
			if seek==0:
				seek+=pad
		self.inputFile.seek(seek, 1)

	def read(self,count):
		back=self.inputFile.tell()
		if self.xorKey is None:
			return self.inputFile.read(count)
		else:
			data=struct.unpack(self.endian+count*'B',self.inputFile.read(count))
			self.XOR(data)
			return self.xorData



	def write(self,string):
		self.inputFile.write(string)

	def tell(self):
		val=self.inputFile.tell()
		if self.debug==True:
			print 'current offset is',val
		return val

	def word(self,long):
		if long<10000:
			if self.inputFile.mode=='rb':
				offset=self.inputFile.tell()
				s=''
				for j in range(0,long):


					if self.xorKey is None:
						lit =  struct.unpack('c',self.inputFile.read(1))[0]
						#data=struct.unpack(self.endian+n*'i',self.inputFile.read(n*4))
					else:
						data=struct.unpack(self.endian+'B',self.inputFile.read(1))
						self.XOR(data)
						lit=struct.unpack(self.endian+'c',self.xorData)[0]

						#lit =	struct.unpack('c',self.inputFile.read(1))[0]



					if ord(lit)!=0:
						s+=lit
				if self.debug==True:
					print s
				if self.log==True:
					if self.logfile is not None and self.logskip is not True:
						self.logfile.write('offset '+str(offset)+'	'+s+'\n')
				return s
			if self.inputFile.mode=='wb':
				#data=self.inputFile.read(long)
				self.inputFile.write(long)
			#return 0
		else:
			if self.debug==True:
				print 'WARNING:too long'
			#return 1



	def s(self,long):
		if long<10000:
			if self.inputFile.mode=='rb':
				offset=self.inputFile.tell()
				s=''
				for j in range(0,long):


					if self.xorKey is None:
						lit =  struct.unpack('c',self.inputFile.read(1))[0]
						#data=struct.unpack(self.endian+n*'i',self.inputFile.read(n*4))
					else:
						data=struct.unpack(self.endian+'B',self.inputFile.read(1))
						self.XOR(data)
						lit=struct.unpack(self.endian+'c',self.xorData)[0]

						#lit =	struct.unpack('c',self.inputFile.read(1))[0]



					if ord(lit)!=0:
						s+=lit
				if self.debug==True:
					print s
				if self.log==True:
					if self.logfile is not None and self.logskip is not True:
						self.logfile.write('offset '+str(offset)+'	'+s+'\n')
				return s
			if self.inputFile.mode=='wb':
				#data=self.inputFile.read(long)
				self.inputFile.write(long)
			#return 0
		else:
			if self.debug==True:
				print 'WARNING:too long'
			#return 1


	def Stream(self,stream_name,element_count,element_size):
		self.inputFile.seek(element_count*element_size,1)
		self.stream[stream_name]['offset']=offset
		self.stream[stream_name]['element_count']=element_count
		self.stream[stream_name]['element_size']=element_size




def getMatName(ys,parent):
	#print 'getMatName'
	matName=None
	if	matName not in MATERIALS.keys():
		UniqueID=ys.get(parent,'"UniqueID"')
		if UniqueID:
			values=ys.values(UniqueID[0].header,'s')
			if len(values)>1:
				if '"' in values[1] and '_' in values[1]:
					matName=values[1].split('"')[3].split('_')[-2]

	rgba=None
	AttributeList=ys.get(parent,'"AttributeList"')
	if AttributeList:
		values=ys.values(AttributeList[0].header,':')
		UniqueID=ys.getValue(values,'"UniqueID"','i')
		Diffuse=ys.get(parent,'"Diffuse"')
		if Diffuse:
			rgba=ys.values(Diffuse[0].data,'f')
		if	matName not in MATERIALS.keys():
			Material=ys.get(AttributeList[0],'"osg.Material"')
			if Material:
				for a in Material[0].children:
					if '"Name"' in a.header:
						splits=a.header.split('"')
						if len(splits)>4:
							matName=splits[5]
							if ':' in matName:
								matName=matName.replace(':','')
							model.matList[UniqueID]=matName

	if	matName not in MATERIALS.keys():
		StateSet=ys.get(parent,'"StateSet"')
		if StateSet:
			osgStateSet=ys.get(StateSet[0],'"osg.StateSet"')
			if osgStateSet:
				if len(osgStateSet[0].children)>0:
					for child in osgStateSet[0].children:
						values=ys.values(child.header,':')
						if '"UniqueID"' in values and '"Name"' in values:
							UniqueID=ys.getValue(values,'"UniqueID"','i')
							matName=ys.getValue(values,'"Name"','""')
							model.matList[UniqueID]=matName
				else:
					values=ys.values(osgStateSet[0].data,':')
					if '"AttributeList"' not in values:
						UniqueID=ys.getValue(values,'"UniqueID"','i')
						if UniqueID in model.matList:
							matName=model.matList[UniqueID]

	if	matName:
		if	len(matName)==0:
			matName='RootNode'
		if '\xef' in matName:
			matName=matName.split('\xef')[0]
	diffuse=None
	normal=None
	specular=None
	trans=None
	ao=None
	rgbCol=None
	rgbSpec=None





	if len(MATERIALS.keys())==1:
			key=MATERIALS.keys()[0]
			for imageType in MATERIALS[key]:
				if MATERIALS[key][imageType][0]=='texture':
					hash=MATERIALS[key][imageType][1]
					if hash in IMAGES.keys():
						if IMAGES[hash]['RGB']:
							path,exists,quality=IMAGES[hash]['RGB']
							if exists==1:
								if imageType=='Opacity':trans=path
								if imageType=='AlbedoPBR':diffuse=path
								if imageType=='DiffuseColor':diffuse=path
								if imageType=='NormalMap':normal=path
								if imageType=='SpecularColor':specular=path
								if imageType=='DiffusePBR':diffuse=path
								if imageType=='SpecularF0':specular=path
								if imageType=='SpecularColor':specular=path
								if imageType=='DiffuseIntensity':ao=path
						if IMAGES[hash]['A']:
							path,exists,quality=IMAGES[hash]['A']
							if exists==1:
								trans=path
						if IMAGES[hash]['N']:
							path,exists,quality=IMAGES[hash]['N']
							if exists==1:
								if imageType=='NormalMap':normal=path
								if imageType=='BumpMap':normal=path
						if IMAGES[hash]['R']:
							path,exists,quality=IMAGES[hash]['R']
							if exists==1:
								if imageType=='Opacity':trans=path
								if imageType=='SpecularF0':specular=path
								if imageType=='AOPBR':ao=path
								if imageType=='RoughnessPBR':specular=path
								if imageType=='GlossinessPBR':specular=path
								if imageType=='BumpMap':normal=path
								if imageType=='SpecularColor':specular=path
								if imageType=='DiffuseIntensity':ao=path
				if MATERIALS[key][imageType][0]=='color':
					if imageType=='DiffuseColor':
						rgbCol=MATERIALS[key][imageType][1]

	else:
		for key in MATERIALS.keys():
			if key==matName:
				for imageType in MATERIALS[key]:
					if MATERIALS[key][imageType][0]=='texture':
						hash=MATERIALS[key][imageType][1]
						if hash in IMAGES.keys():
							if IMAGES[hash]['RGB']:
								path,exists,quality=IMAGES[hash]['RGB']
								if exists==1:
									if imageType=='AlbedoPBR':diffuse=path
									if imageType=='DiffuseColor':diffuse=path
									if imageType=='DiffusePBR':diffuse=path
									if imageType=='NormalMap':normal=path
									if imageType=='EmitColor':diffuse=path
									if imageType=='SpecularPBR':specular=path
									if imageType=='Opacity':trans=path
									if imageType=='SpecularF0':specular=path
									if imageType=='SpecularColor':specular=path
									if imageType=='DiffuseIntensity':ao=path
							if IMAGES[hash]['A']:
								path,exists,quality=IMAGES[hash]['A']
								if exists==1:
									trans=path
							if IMAGES[hash]['N']:
								path,exists,quality=IMAGES[hash]['N']
								if exists==1:
									if imageType=='NormalMap':normal=path
									if imageType=='BumpMap':normal=path
							if IMAGES[hash]['R']:
								path,exists,quality=IMAGES[hash]['R']
								if exists==1:
									if imageType=='Opacity':trans=path
									if imageType=='SpecularF0':specular=path
									if imageType=='AOPBR':ao=path
									if imageType=='RoughnessPBR':specular=path
									if imageType=='GlossinessPBR':specular=path
									if imageType=='BumpMap':normal=path
									if imageType=='SpecularColor':specular=path
									if imageType=='DiffuseIntensity':ao=path
					if MATERIALS[key][imageType][0]=='color':
						if imageType=='DiffuseColor':
							rgbCol=MATERIALS[key][imageType][1]

	TextureAttributeList=ys.get(parent,'"TextureAttributeList"')
	if TextureAttributeList:
			#print 'here'
			osg_Texture=ys.get(parent,'"osg.Texture"')
			if osg_Texture:
				values=ys.values(osg_Texture[0].data,':')
				hash=ys.getValue(values,'"File"','""')
				if hash:
					if '/' in hash:
						hash=hash.split('/')[1]
						#print hash
						if hash in IMAGES.keys():
							if IMAGES[hash]['RGB']:
								path,exists,quality=IMAGES[hash]['RGB']
								if exists==1:
									diffuse=path
							if IMAGES[hash]['A']:
								path,exists,quality=IMAGES[hash]['A']
								if exists==1:
									trans=path
							if IMAGES[hash]['N']:
								path,exists,quality=IMAGES[hash]['N']
								if exists==1:
									if imageType=='NormalMap':normal=path
									if imageType=='BumpMap':normal=path

	return matName,diffuse,specular,normal,ao,trans,rgbCol,rgbSpec,rgba


def getSplitName(name,what,which):
	a=None
	if what in name:
		a=''
		splits=name.split(what)
		if which<0:
			num=len(splits)+which-1
		else:
			num=which
		if num<0:
			a=name
		else:
			if which<len(splits):
				for m in range(num):
					a+=splits[m]+what
				a+=splits[num]
			else:
				a=name
	return a


def etap1(input,ItemSize):
	n=len(input)/ItemSize
	r=0
	output=[0]*len(input)
	while(r<n):
		a=r*ItemSize
		s=0
		while(s<ItemSize):
			output[a+s]=input[r+n*s]
			s+=1
		r+=1
	return output

def etap2(input,ItemSize,atributes):
	i=[atributes['"bx"'],atributes['"by"'],atributes['"bz"']]
	n=[atributes['"hx"'],atributes['"hy"'],atributes['"hz"']]
	a=len(input)/ItemSize
	s=0
	output=[0]*len(input)
	while(s<a):
		o=s*ItemSize
		u=0
		while(u<ItemSize):
			output[o+u]=i[u]+input[o+u]*n[u];
			u+=1
		s+=1
	return output




def etap3(input,ItemSize):
	i=ItemSize|1
	n=1
	r=len(input)/i
	while(n<r):
		a=(n-1)*i
		s=n*i
		o=0
		while(o<i):
			input[s+o]+=input[a+o]
			o+=1
		n+=1
	return input

def etap4(input):
	e=1
	i=len(input)/4
	while(e<i):
		n=4*(e-1)
		r=4*e
		a=input[n]
		s=input[n+1]
		o=input[n+2]
		u=input[n+3]
		l=input[r]
		h=input[r+1]
		c=input[r+2]
		d=input[r+3]
		input[r]=a*d+s*c-o*h+u*l
		input[r+1]=-a*c+s*d+o*l+u*h
		input[r+2]=a*h-s*l+o*d+u*c
		input[r+3]=-a*l-s*h-o*c+u*d
		e+=1
	return	input



def int3float4(input,atributes,ItemSize):
	c=4
	d=atributes['"epsilon"']
	p=int(atributes['"nphi"'])
	e=[0]*len(input)*4
	i=1.57079632679
	n=6.28318530718
	r=3.14159265359
	a=0.01745329251
	s=0.25
	o=720
	u=832
	l=47938362584151635e-21
	h={}
	f=True

	d=d or s
	p=p or o
	g=math.cos(d*a)
	m=0
	v=0
	_=[]

	v=(p+1)*(u+1)*3
	_=[None]*v

	b=r/float(p-1)
	x=i/float(p-1)

	if f:y=3
	else:y=2


	m=0
	v=len(input)/y
	while(m<v):
		A=m*c
		S=m*y
		C=input[S]
		w=input[S+1]
		if c==0:
			if f==0:
				if (C&-1025)!=4:
					e[A+3]=-1
				else:
					e[A+3]=1
		M=None
		T=None
		E=None
		I=3*(C+p*w)
		M=_[I]
		if	M==None:
			N=C*b
			k=cos(N)
			F=sin(N)
			N+=x
			D=(g-k*cos(N))/float(max(1e-5,F*sin(N)))
			if D>1:D=1
			else:
				if D<-1:D=-1
			P=w*n/float(math.ceil(r/float(max(1e-5,math.acos(D)))))
			M=_[I]=F*math.cos(P)
			T=_[I+1]=F*math.sin(P)
			E=_[I+2]=k
		else:
			T=_[I+1]
			E=_[I+2]
		if f:
			R=input[S+2]*l
			O=math.sin(R)
			e[A]=O*M
			e[A+1]=O*T
			e[A+2]=O*E
			e[A+3]=math.cos(R)
			#write(log,[A,e[A],e[A+1],e[A+2],e[A+3]],0)
		else:
			e[A]=M
			e[A+1]=T
			e[A+2]=E
		m+=1

	return e


def getAnimation(ys,A,n):
	action=Action()
	action.BONESPACE=True
	#action.ARMATURESPACE=True
	action.FRAMESORT=True
	action.skeleton=skeleton.name
	n+=4
	Channels=ys.get(A,'"Channels"')
	boneList={}
	if Channels:
		values=ys.values(Channels[0].header,':')
		Name=ys.getValue(values,'"Name"')
		action.name=Name
		new=New(Name.replace('"','').replace('|','')+'.action','wb',sys).open()
		for a in  Channels[0].children:
			Vec3LerpChannel=ys.get(a,'"osgAnimation.Vec3LerpChannel"')
			if Vec3LerpChannel:
				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					name=getSplitName(TargetName,'_',-1)
					if Name=='"translate"':
						bone=None
						if TargetName in boneIndeksList:
							name=boneIndeksList[TargetName]
							if name not in boneList.keys():
								bone=ActionBone()
								action.boneList.append(bone)
								bone.name=name
								boneList[name]=bone
							bone=boneList[name]
						else:
							print 'skiped translate bone:',TargetName


						Key=ys.get(a,'"Key"')
						if Key:
							values=ys.values(Key[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')
							Float32Array=ys.get(Key[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"')
								Offset=ys.getValue(values,'"Offset"')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)

								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path)==True:
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									if bone:
										new.write(bone.name+'\x00')
										new.write('translate'+'\x00')
										new.i([int(Size)])
									for m in range(int(Size)):
										value=g.f(ItemSize)
										#write(log,value,n+8)
										if bone:
											new.f(value)
											boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
											matrix=VectorMatrix(value)#*boneMatrix
											bone.posKeyList.append(matrix)
									file.close()
							else:print 'unknow array type'
						else:print 'no key'

						Time=ys.get(a,'"Time"')
						if Time:
							values=ys.values(Time[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')
							Float32Array=ys.get(Time[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"')
								Offset=ys.getValue(values,'"Offset"')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)


								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									if bone:new.i([int(Size)])
									for m in range(int(Size)):
										value=g.f(ItemSize)
										if ItemSize==1:value=value[0]
										#write(log,[value],n+8)
										if bone:
											new.f([value])
											bone.posFrameList.append(int(value*33))
									file.close()
							else:print 'unknow array type'
						else:print 'no time'




					if Name=='"scale"':
						bone=None
						if TargetName in boneIndeksList:
							name=boneIndeksList[TargetName]
							if name not in boneList.keys():
								bone=ActionBone()
								action.boneList.append(bone)
								bone.name=name
								boneList[name]=bone
							bone=boneList[name]
						else:
							print 'skiped scale bone:',TargetName


						Key=ys.get(a,'"Key"')
						if Key:
							values=ys.values(Key[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')
							Float32Array=ys.get(Key[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"')
								Offset=ys.getValue(values,'"Offset"')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)

								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path)==True:
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									if bone:
										new.write(bone.name+'\x00')
										new.write('size'+'\x00')
										new.i([int(Size)])
									for m in range(int(Size)):
										value=g.f(ItemSize)
										#write(log,value,n+8)
										if bone:
											new.f(value)
											boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
											matrix=VectorMatrix(value)#*boneMatrix
											bone.sizeKeyList.append(matrix)
									file.close()
							else:print 'unknow array type'
						else:print 'no key'

						Time=ys.get(a,'"Time"')
						if Time:
							values=ys.values(Time[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')
							Float32Array=ys.get(Time[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"')
								Offset=ys.getValue(values,'"Offset"')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)


								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									if bone:new.i([int(Size)])
									for m in range(int(Size)):
										value=g.f(ItemSize)
										if ItemSize==1:value=value[0]
										#write(log,[value],n+8)
										if bone:
											new.f([value])
											bone.sizeFrameList.append(int(value*33))
									file.close()
							else:print 'unknow array type'
						else:print 'no time'

			Vec3LerpChannelCompressedPacked=ys.get(a,'"osgAnimation.Vec3LerpChannelCompressedPacked"')
			if Vec3LerpChannelCompressedPacked:

				atributes={}
				UserDataContainer=ys.get(Vec3LerpChannelCompressedPacked[0],'"UserDataContainer"')
				if UserDataContainer:
					Values=ys.get(UserDataContainer[0],'"Values"')
					if Values:
						for child in Values[0].children:
							values=ys.values(child.data,':')
							Name=ys.getValue(values,'"Name"')
							Value=ys.getValue(values,'"Value"','"f"')
							#write(log,[Name,Value],n+4)
							atributes[Name]=Value

				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					#write(log,['Vec3LerpChannelCompressedPacked:',Name,'TargetName:',TargetName],n+4)
					name=getSplitName(TargetName,'_',-1)
					if Name=='"translate"':
						bone=None
						if TargetName in boneIndeksList:
							#new.write(TargetName+'\x00')
							#new.write('translate'+'\x00')
							name=boneIndeksList[TargetName]
							if name not in boneList.keys():
								bone=ActionBone()
								action.boneList.append(bone)
								bone.name=name
								boneList[name]=bone
							bone=boneList[name]
						else:
							print 'skiped translate bone:',TargetName

						Key=ys.get(a,'"Key"')
						if Key:
							values=ys.values(Key[0].data,':')
							ItemSize=int(ys.getValue(values,'"ItemSize"'))
							Uint16Array=ys.get(Key[0],'"Uint16Array"')
							type="Uint16Array"
							if Uint16Array:
								values=ys.values(Uint16Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=int(ys.getValue(values,'"Size"'))
								Offset=int(ys.getValue(values,'"Offset"'))
								Encoding=ys.getValue(values,'"Encoding"')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'ItemSize:',ItemSize],n+4)


								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)

									list=decodeVarint(g,Offset,Size*ItemSize,type)
									list1=etap1(list,ItemSize)
									out=etap2(list1,ItemSize,atributes)
									list2=[atributes['"ox"'],atributes['"oy"'],atributes['"oz"']]
									list2.extend(out)
									list3=etap3(list2,ItemSize)
									if bone:
										new.write(bone.name+'\x00')
										new.write('translate'+'\x00')
										new.i([Size])
									for m in range(Size):
										value=list3[m*3:m*3+3]
										#write(log,value,n+8)
										if bone:
											new.f(value)
											if bone.name in skeleton.object.getData().bones.keys():
												boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
												#boneMatrix*=VectorMatrix(value)
												matrix=VectorMatrix(value)#*boneMatrix
												bone.posKeyList.append(matrix)

									file.close()
							else:print 'unknow array type'
						else:print 'no key'

						Time=ys.get(a,'"Time"')
						if Time:
							values=ys.values(Time[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')
							Float32Array=ys.get(Time[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"','i')
								Offset=ys.getValue(values,'"Offset"','i')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)



								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									list=g.f(Size*ItemSize)
									list1=etap1(list,ItemSize)
									#out=etap2(list1,ItemSize,atributes)
									list2=[atributes['"ot"']]
									list2.extend(list1)
									list3=etap3(list2,ItemSize)
									#write(log,list3,0)
									if bone:new.i([Size])
									for m in range(Size):
										value=list3[m]
										if bone:
											new.f([value])
											bone.posFrameList.append(int(value*33))
									file.close()
							else:print 'unknow array type'
						else:print 'no time'



			QuatSlerpChannel=ys.get(a,'"osgAnimation.QuatSlerpChannel"')
			if QuatSlerpChannel:
				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					#write(log,['QuatSlerpChannel:',Name,'TargetName:',TargetName],n+4)
					name=getSplitName(TargetName,'_',-1)
					bone=None
					if TargetName in boneIndeksList:
						name=boneIndeksList[TargetName]
						if name not in boneList.keys():
							bone=ActionBone()
							action.boneList.append(bone)
							bone.name=name
							boneList[name]=bone
						bone=boneList[name]
					else:
						print 'skiped quaternion bone:',TargetName



					Key=ys.get(a,'"Key"')
					if Key:
						values=ys.values(Key[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"')
						Float32Array=ys.get(Key[0],'"Float32Array"')
						if Float32Array:
							values=ys.values(Float32Array[0].data,':')
							File=ys.getValue(values,'"File"')
							Size=ys.getValue(values,'"Size"')
							Offset=ys.getValue(values,'"Offset"')
							#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)


							path=os.path.dirname(filename)+os.sep+File.split('"')[1]
							if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
								cmd=Cmd()
								cmd.input=path
								cmd.ZIP=True
								cmd.run()
							path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
							if os.path.exists(path)==False:
								path+='.gz.txt'

							if os.path.exists(path):
								file=open(path,'rb')
								g=BinaryReader(file)
								g.seek(int(Offset))
								if bone:
									new.write(bone.name+'\x00')
									new.write('quaternion'+'\x00')
									new.i([int(Size)])
								for m in range(int(Size)):
									value=g.f(4)
									if bone:
										new.f(value)
									value=Quaternion(value)
									if bone:
										#new.f(value)
										boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
										#bone.rotKeyList.append(boneMatrix*QuatMatrix(value).resize4x4())
										matrix=QuatMatrix(value).resize4x4()#*boneMatrix
										bone.rotKeyList.append(matrix)
								file.close()

					Time=ys.get(a,'"Time"')
					if Time:
						values=ys.values(Time[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"','i')
						Float32Array=ys.get(Time[0],'"Float32Array"')
						if Float32Array:
							values=ys.values(Float32Array[0].data,':')
							File=ys.getValue(values,'"File"')
							Size=ys.getValue(values,'"Size"')
							Offset=ys.getValue(values,'"Offset"')
							#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)


							path=os.path.dirname(filename)+os.sep+File.split('"')[1]
							if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
								cmd=Cmd()
								cmd.input=path
								cmd.ZIP=True
								cmd.run()
							path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
							if os.path.exists(path)==False:
								path+='.gz.txt'

							if os.path.exists(path):
								file=open(path,'rb')
								g=BinaryReader(file)
								g.seek(int(Offset))
								if bone:new.i([int(Size)])
								for m in range(int(Size)):
									value=g.f(ItemSize)
									if ItemSize==1:value=value[0]
									if bone:
										new.f([value])
										bone.rotFrameList.append(int(value*33))
								file.close()


			QuatSlerpChannelCompressedPacked=ys.get(a,'"osgAnimation.QuatSlerpChannelCompressedPacked"')
			if QuatSlerpChannelCompressedPacked:
				TargetName=None
				try:

					atributes={}
					UserDataContainer=ys.get(QuatSlerpChannelCompressedPacked[0],'"UserDataContainer"')
					if UserDataContainer:
						Values=ys.get(UserDataContainer[0],'"Values"')
						if Values:
							for child in Values[0].children:
								values=ys.values(child.data,':')
								Name=ys.getValue(values,'"Name"')
								Value=ys.getValue(values,'"Value"','"f"')
								#write(log,[Name,Value],n+4)
								atributes[Name]=Value

					KeyFrames=ys.get(a,'"KeyFrames"')
					if KeyFrames:
						values=ys.values(KeyFrames[0].header,':')
						Name=ys.getValue(values,'"Name"')
						TargetName=ys.getValue(values,'"TargetName"','""')
						#write(log,['QuatSlerpChannelCompressedPacked:',Name,'TargetName:',TargetName],n+4)
						name=getSplitName(TargetName,'_',-1)
						#print TargetName
						bone=None
						#print TargetName
						#print atributes
						if TargetName in boneIndeksList:
							name=boneIndeksList[TargetName]
							if name not in boneList.keys():
								bone=ActionBone()
								action.boneList.append(bone)
								bone.name=name
								boneList[name]=bone
							bone=boneList[name]
						else:
							print 'skiped quaternion bone:',TargetName

						Key=ys.get(a,'"Key"')
						if Key:
							values=ys.values(Key[0].data,':')
							ItemSize=int(ys.getValue(values,'"ItemSize"'))
							Uint16Array=ys.get(Key[0],'"Uint16Array"')
							type="Uint16Array"
							if Uint16Array:
								values=ys.values(Uint16Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=int(ys.getValue(values,'"Size"'))
								Offset=int(ys.getValue(values,'"Offset"'))
								Encoding=ys.getValue(values,'"Encoding"')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'ItemSize:',ItemSize],n+4)


								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)

									list=decodeVarint(g,Offset,Size*ItemSize,type)
									#write(log,list,0)
									list1=etap1(list,ItemSize)
									#write(log,list1,0)
									if '"ox"' in atributes:
										list2=int3float4(list1,atributes,ItemSize)
										#write(log,list2,0)
										list3=[atributes['"ox"'],atributes['"oy"'],atributes['"oz"'],atributes['"ow"']]
										list3.extend(list2)
										list4=etap4(list3)
										#write(log,list4,0)

										if bone:
											new.write(bone.name+'\x00')
											new.write('quaternion'+'\x00')
											new.i([Size])
										for m in range(Size):
											value=list4[m*4:m*4+4]
											if bone:
												new.f(value)
											value=Quaternion(value)
											#write(log,value,n+8)
											if bone:
												#new.f(value)
												boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
												##bone.rotKeyList.append((boneMatrix.rotationPart()*QuatMatrix(value)).resize4x4())
												matrix=QuatMatrix(value).resize4x4()#*boneMatrix
												bone.rotKeyList.append(matrix)
									file.close()

						Time=ys.get(a,'"Time"')
						if Time:
							values=ys.values(Time[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')
							Float32Array=ys.get(Time[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"','i')
								Offset=ys.getValue(values,'"Offset"','i')
								#write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)


								path=os.path.dirname(filename)+os.sep+File.split('"')[1]
								if os.path.exists(path)==True and os.path.exists(path.split('.gz')[0])==False:
									cmd=Cmd()
									cmd.input=path
									cmd.ZIP=True
									cmd.run()
								path=os.path.dirname(filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path)==False:
									path+='.gz.txt'

								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									list=g.f(Size*ItemSize)
									list1=etap1(list,ItemSize)
									#out=etap2(list1,ItemSize,atributes)
									if '"ot"' in atributes:
										list2=[atributes['"ot"']]
										list2.extend(list1)
										list3=etap3(list2,ItemSize)
										#write(log,list3,0)
										if bone:new.i([Size])
										for m in range(Size):
											value=list2[m]
											if bone:
												new.f([value])
												bone.rotFrameList.append(int(value*33))
									file.close()
				except:
					print 'niepowodzenie:QuatSlerpChannelCompressedPacked:',TargetName

			#if bone:
			#	print name,bone.name
		new.close()
	#action.draw()
	#action.setContext()


def decodeVarint(g,offset,size,type):
	g.seek(offset)
	n=[0]*size
	a=0
	s=0
	while(a!=size):
		shift = 0
		result = 0
		while True:
			byte = g.B(1)[0]
			result |= (byte & 127) << shift
			shift += 7
			if not (byte & 0x80):break
		n[a]=result
		a+=1
	if type[0]!='U':
		l=0
		while(l<size):
			h=n[l]
			n[l]=h>>1^-(1&h)
			l+=1
	return n



def decodeDelta(t,e):
	i=e|0
	n=len(t)
	if i>=len(t):r=None
	else:r=t[i]
	a=i+1
	while(a<n):
		s=t[a]
		r=t[a]=r+(s>>1^-(1&s))
		a+=1
	return t


def decodeImplicit(input,n):
	IMPLICIT_HEADER_LENGTH=3
	IMPLICIT_HEADER_MASK_LENGTH=1
	IMPLICIT_HEADER_PRIMITIVE_LENGTH=0
	IMPLICIT_HEADER_EXPECTED_INDEX=2
	highWatermark=2

	t=input
	e=[0]*t[IMPLICIT_HEADER_PRIMITIVE_LENGTH]
	a=t[IMPLICIT_HEADER_EXPECTED_INDEX]
	s=t[IMPLICIT_HEADER_MASK_LENGTH]
	o=t[IMPLICIT_HEADER_LENGTH:s+IMPLICIT_HEADER_LENGTH]
	r=highWatermark
	u=32*s-len(e)
	l=1<<31
	h=0
	while(h<s):
		c=o[h]
		d=32
		p=h*d
		if h==s-1:f=u
		else:f=0
		g1=f
		while(g1<d):
			if c&l>>g1:
				e[p]=t[n]
				n+=1
			else:
				if r:
					e[p]=a
				else:
					e[p]=a
					a+=1
			g1+=1
			p+=1
		h+=1
	return e


def decodeWatermark(t,e,i):
	n=i[0]
	r=len(t)
	a=0
	while(a<r):
		s=n-t[a]
		e[a]=s
		if n<=s:n=s+1
		a+=1
	return e,n


def decodeQuantize(input,s,a,itemsize):
	x=[0]*len(input)
	id=0
	for r in range(len(input)/itemsize):
		for l in range(itemsize):
			x[id]=s[l]+input[id]*a[l]
			id+=1
	return x


def decodePredict(indices,input,itemsize):
	t=input
	if len(indices)>0:
		t=input
		e=itemsize
		i=indices
		n=len(t)/e
		r=[0]*n
		a=len(i)-1
		r[i[0]]=1
		r[i[1]]=1
		r[i[2]]=1
		s=2
		while(s<a):
			o=s-2
			u=i[o]
			l=i[o+1]
			h=i[o+2]
			c=i[o+3]
			if 1!=r[c]:
				r[c]=1
				u*=e
				l*=e
				h*=e
				c*=e
				d=0
				while(d<e):
					t[c+d]=t[c+d]+t[l+d]+t[h+d]-t[u+d]
					d+=1
			s+=1
	return t



class Node:
	def __init__(self):
		self.name=None
		self.children=[]
		self.osgChildren=[]
		self.offset=None
		self.start=None
		self.end=None
		self.header=''
		self.data=''
		self.parent=None

class Yson:
	def __init__(self):
		self.input=None
		self.filename=None
		self.root=Node()
		self.log=False
	def parse(self):
		global offset,string,txt
		if self.filename is not None:
			file=open(self.filename,'rb')
			self.input=file.read().replace('\x20','').replace('\x0A','').replace('&#34;','"')

			line=self.input
			if self.log==True:txt=open(self.filename+'.ys','w')

			if line is not None and len(line)>0:
				offset=0
				n=0
				string=[]
				if self.input[offset]=='{':
					if self.log==True:
						txt.write('\n')
						txt.write(' '*n+'header:'+str(None))
						txt.write(' { '+str(offset))
						txt.write(' '*(n+4))
				if self.input[offset]=='[':
					if self.log==True:
						txt.write('\n')
						txt.write(' '*n+'header:'+str(None))
						txt.write(' [ '+str(offset))
						txt.write(' '*(n+4))
				self.tree(self.root,n)
				if self.log==True:
					txt.write(' '*n)

			file.close()

		if self.log==True:txt.close()

	def getTree1(self,parent,list,key):
		for child in parent.children:
			if key in child.header:
				list.append(child)
			self.getTree(child,list,key)


	def getTree(self,parent,list,key):
		if key in parent.header or key in parent.data:
			list.append(parent)
		for child in parent.children:
			self.getTree(child,list,key)

	def values(self,data,type):
		list={}
		A=data.split(',')
		if type==':':
			for a in A:
				if ':' in a:
					c=0
					alist=[]
					string=''
					for b in a:
						if b=='"' and c==0:
							if len(string)>0:alist.append(string)
							string=''
							string+=b
							c=1
						elif b=='"' and c==1:
							string+=b
							if len(string)>0:alist.append(string)
							string=''
							c=0
						elif b==':':
							pass
						else:string+=b
					if len(string)>0:alist.append(string)
					if len(alist)==2:
						list[alist[0]]=alist[1]
					if len(alist)==1:
						list[alist[0]]='None'



					#if a.count(':')>1:
		if type=='f':
			list=map(float,A)
		if type=='i':
			list=map(int,A)
		if type=='s':
			list=A
		return list

	def getValue(self,values,name,type=None):
		if name in values:
			if type=='"f"':
				return float(values[name].split('"')[1])
			elif type=='"i"':
				return int(values[name].split('"')[1])
			elif type=='i':
				#print name,values[name]
				if values[name]!='None':

					return int(values[name])
				else:
					return None
			elif type=='""':
				return values[name].split('"')[1]
			else:
				return values[name]
		else:
			return None

	def get(self,node,key):
		list=[]
		self.getTree(node,list,key)
		if len(list)>0:
			return list
		else:
			return None

	def tree(self,parentNode,n):
		global offset,string
		n+=4
		offset+=1
		while(True):
			if	offset>=len(self.input):break
			value=self.input[offset]
			if value=='}':
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'data:'+self.input[string[0]:offset])
					else:
						txt.write(' '*n+'data:None')
					txt.write('\n'+' '*n+' } '+str(offset))
				if len(string)>0:
					parentNode.data=self.input[string[0]:offset]
				string=[]
				offset+=1
				break

			elif value=='{':
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'header:'+self.input[string[0]:offset])
					else:
						txt.write(' '*n+'header:None')
					txt.write(' { '+str(offset))
					txt.write(' '*(n+4))
				#print round(100*offset/float(len(self.input)),3),'procent'
				node=Node()
				node.parent=parentNode
				parentNode.children.append(node)
				node.offset=offset
				if len(string)>0:
					node.header=self.input[string[0]:offset]
				string=[]
				self.tree(node,n)
				if self.log==True:
					txt.write(' '*n)

			elif value==']':
				if len(string)>0:
					parentNode.data=self.input[string[0]:offset]

				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'data:'+self.input[string[0]:offset]+'\n')
					else:
						txt.write(' '*n+'data:None')
					txt.write(' '*n+' ] '+str(offset))

				offset+=1
				string=[]
				break

			elif value=='[':
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'header:'+self.input[string[0]:offset])
					else:
						txt.write(' '*n+'header:None')
					txt.write(' [ '+str(offset))
					txt.write(' '*(n+4))
				#print round(100*offset/float(len(self.input)),3),'procent'
				node=Node()
				node.parent=parentNode
				parentNode.children.append(node)
				node.offset=offset
				node.name=string
				if len(string)>0:
					node.header=self.input[string[0]:offset]
				else:
					node.header=''
				string=[]
				self.tree(node,n)
				if self.log==True:
					txt.write(' '*n)
			else:
				#string+=value
				if len(string)==0:
					string.append(offset)
				offset+=1

def getUniqueID(ys,data):
	UniqueID=None
	values=ys.values(data,':')
	if '"UniqueID"' in values:
		UniqueID=ys.getValue(values,'"UniqueID"','i')
	return UniqueID


class NewNode:
	def __init__(self):
		self.node=None
		self.parent=None
		self.children=[]
		self.UniqueID=None

def getIDTree(ys,parentNode,n,parentNewNode):
	if len(parentNode.header)!=0 and parentNode.header!=',':
		n+=4
	UniqueID=getUniqueID(ys,parentNode.data)
	if UniqueID:
		parentNewNode.UniqueID=UniqueID
	for child in parentNode.children:
		if len(child.header)!=0 and child.header!=',':
			newNode=NewNode()
			UniqueID=getUniqueID(ys,child.header)
			if UniqueID:
				parentNewNode.UniqueID=UniqueID
			newNode.node=child
			parentNewNode.children.append(newNode)
			newNodeList.append(newNode)
			newNode.parent=parentNode
			parentNewNode1=newNode
			getIDTree(ys,child,n,parentNewNode1)
		else:
			getIDTree(ys,child,n,parentNewNode)


def getPath(File):
	path=os.path.dirname(filename)+os.sep+File.split('.gz')[0]
	if os.path.exists(path)==False:path=os.path.dirname(filename)+os.sep+File+'.txt'
	if os.path.exists(path)==False:path=os.path.dirname(filename)+os.sep+File
	if os.path.exists(path)==True:return path
	else:return None


def Vertex(ys,b):
	n=20
	Size=None
	Offset=None
	Encoding=None
	ItemSize=None
	type=None
	vertexArray=[]
	values=ys.values(b.data,':')
	if '"ItemSize"' in values:
		ItemSize=int(values['"ItemSize"'])
		Int32Array=ys.get(b,'"Int32Array"')
		if Int32Array:
			type='Int32Array'
			values=ys.values(Int32Array[0].data,':')
			Size=ys.getValue(values,'"Size"','i')
			Offset=ys.getValue(values,'"Offset"','i')
			File=ys.getValue(values,'"File"','""')
			Encoding=ys.getValue(values,'"Encoding"')
			#write(log,[type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding],n)
			if Encoding=='"varint"':
				path=getPath(File)
				if path:
					file=open(path,'rb')
					g=BinaryReader(file)
					bytes=decodeVarint(g,Offset,Size*ItemSize,type)
					vertexArray.append([bytes,Encoding,ItemSize])
					file.close()

		Float32Array=ys.get(b,'"Float32Array"')
		if Float32Array:
			type='Float32Array'
			#print mode,type
			values=ys.values(Float32Array[0].data,':')
			Size=ys.getValue(values,'"Size"','i')
			Offset=ys.getValue(values,'"Offset"','i')
			File=ys.getValue(values,'"File"','""')
			Encoding=ys.getValue(values,'"Encoding"')
			#write(log,[type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding],n)
			if Encoding!='"varint"':
				path=getPath(File)
				if path:
					file=open(path,'rb')
					g=BinaryReader(file)
					g.seek(Offset)
					bytes=g.f(Size*ItemSize)
					list=[]
					for m in range(Size):
						list.append(bytes[m*ItemSize:m*ItemSize+ItemSize])
					vertexArray.append([list,Encoding])
					file.close()
	return vertexArray

def TexCoord(ys,b):
	n=20
	Size=None
	Offset=None
	Encoding=None
	ItemSize=None
	type=None
	TexCoordArray=[]
	values=ys.values(b.data,':')
	if '"ItemSize"' in values:
		ItemSize=int(values['"ItemSize"'])
		Int32Array=ys.get(b,'"Int32Array"')
		if Int32Array:
			type='Int32Array'
			values=ys.values(Int32Array[0].data,':')
			Size=ys.getValue(values,'"Size"','i')
			Offset=ys.getValue(values,'"Offset"','i')
			File=ys.getValue(values,'"File"','""')
			Encoding=ys.getValue(values,'"Encoding"')
			if Encoding=='"varint"':
				path=getPath(File)
				if path:
					file=open(path,'rb')
					g=BinaryReader(file)
					bytes=decodeVarint(g,Offset,Size*ItemSize,type)
					TexCoordArray.append([bytes,Encoding,ItemSize])
					file.close()

		Float32Array=ys.get(b,'"Float32Array"')
		if Float32Array:
			type='Float32Array'
			values=ys.values(Float32Array[0].data,':')
			Size=ys.getValue(values,'"Size"','i')
			Offset=ys.getValue(values,'"Offset"','i')
			File=ys.getValue(values,'"File"','""')
			Encoding=ys.getValue(values,'"Encoding"')
			if Encoding!='"varint"':
				path=getPath(File)
				if path:
					file=open(path,'rb')
					g=BinaryReader(file)
					g.seek(Offset)
					bytes=g.f(Size*ItemSize)
					list=[]
					for m in range(Size):
						u,v=bytes[m*ItemSize:m*ItemSize+ItemSize]
						list.append([u,1-v])
					TexCoordArray.append([list,Encoding])
					file.close()
	return TexCoordArray

def Color(ys,b):
	n=20
	Size=None
	Offset=None
	Encoding=None
	ItemSize=None
	type=None
	values=ys.values(b.data,':')
	colorArray=[]
	if '"ItemSize"' in values:
		ItemSize=int(values['"ItemSize"'])
		Uint8Array=ys.get(b,'"Uint8Array"')
		if Uint8Array:
			type="Uint8Array"
			values=ys.values(Uint8Array[0].data,':')
			Size=ys.getValue(values,'"Size"','i')
			Offset=ys.getValue(values,'"Offset"','i')
			Encoding=ys.getValue(values,'"Encoding"','""')
			File=ys.getValue(values,'"File"','""')
			path=getPath(File)
			if path:
				if Encoding!='"varint"':
					file=open(path,'rb')
					g=BinaryReader(file)
					g.seek(Offset)
					bytes=g.B(Size*ItemSize)
					list=[]
					for m in range(Size):
						list.append(bytes[m*ItemSize:m*ItemSize+ItemSize])
					colorArray=list
					file.close()
		Float32Array=ys.get(b,'"Float32Array"')
		if Float32Array:
			type="Float32Array"
			values=ys.values(Float32Array[0].data,':')
			Size=ys.getValue(values,'"Size"','i')
			Offset=ys.getValue(values,'"Offset"','i')
			Encoding=ys.getValue(values,'"Encoding"','""')
			File=ys.getValue(values,'"File"','""')
			path=getPath(File)
			if path:
				if Encoding!='"varint"':
					file=open(path,'rb')
					g=BinaryReader(file)
					g.seek(Offset)
					bytes=g.f(Size*ItemSize)
					list=[]
					for m in range(Size):
						items=bytes[m*ItemSize:m*ItemSize+ItemSize]
						A=[]
						for item in items:
							A.append(int(item*256))
						list.append(A)
					colorArray=list
					file.close()
	return colorArray



def getIndices(itemsize,size,offset,type,g,mode,magic):
	if type!="Uint8Array":bytes=decodeVarint(g,offset,size*itemsize,type)
	else:
		g.seek(offset)
		bytes=list(g.B(size*itemsize))
	write(log,[magic,mode,type],0)
	write(log,bytes,0)

	IMPLICIT_HEADER_LENGTH=3
	IMPLICIT_HEADER_MASK_LENGTH=1
	IMPLICIT_HEADER_PRIMITIVE_LENGTH=0
	IMPLICIT_HEADER_EXPECTED_INDEX=2
	highWatermark=2

	MissingCondition=skipdecode
	if MissingCondition!=1:

		if mode=='"TRIANGLE_STRIP"':
					k=IMPLICIT_HEADER_LENGTH+bytes[IMPLICIT_HEADER_MASK_LENGTH]
					bytes=decodeDelta(bytes,k)
					#write(log,[magic,k],0)
					#write(log,bytes,0)
					bytes=decodeImplicit(bytes,k)
					#write(log,[magic,k],0)
					#write(log,bytes,0)
					i=[magic]
					bytes,magic=decodeWatermark(bytes,bytes,i)
					#write(log,[magic],0)
					#write(log,bytes,0)

		elif mode=='"TRIANGLES"':
					k=0
					bytes=decodeDelta(bytes,k)
					#write(log,[magic],0)
					#write(log,bytes,0)
					i=[magic]
					bytes,magic=decodeWatermark(bytes,bytes,i)
					#write(log,[magic],0)
					#write(log,bytes,0)




	return magic,bytes


def PrimitiveSetList(ys,child):
	global magic
	mode=None
	magic=0
	n=16
	indiceArray=[]
	for child in child.children:
		b=child.node
		if '"DrawElementsUInt"' in b.header:
			values=ys.values(b.data,':')
			mode=values['"Mode"']
			Size=None
			Offset=None
			Encoding=None
			ItemSize=None
			type=None
			if mode!='"LINES"':
				Indices=ys.get(b,'"Indices"')
				if Indices:
					values=ys.values(Indices[0].data,':')
					ItemSize=ys.getValue(values,'"ItemSize"','i')
					Uint32Array=ys.get(Indices[0],'"Uint32Array"')
					type="Uint32Array"
					#print "DrawElementsUInt",type
					if Uint32Array:
						values=ys.values(Uint32Array[0].data,':')
						Size=ys.getValue(values,'"Size"','i')
						Offset=ys.getValue(values,'"Offset"','i')
						Encoding=ys.getValue(values,'"Encoding"','""')
						#write(log,['Indice:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'magic:',magic],n)
						if Encoding=='varint':
							path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
							if os.path.exists(path)==True:
								file=open(path,'rb')
								g=BinaryReader(file)
								magic,indiceList=getIndices(ItemSize,Size,Offset,type,g,mode,magic)
								indiceArray.append([indiceList,mode])
								file.close()
			#else:
			#	print 'LINES'

		if '"DrawElementsUShort"' in b.header:
			values=ys.values(b.data,':')
			mode=values['"Mode"']
			Size=None
			Offset=None
			Encoding=None
			ItemSize=None
			type=None
			if mode!='"LINES"':
				Indices=ys.get(b,'"Indices"')
				if Indices:
					values=ys.values(Indices[0].data,':')
					ItemSize=ys.getValue(values,'"ItemSize"','i')
					Uint16Array=ys.get(Indices[0],'"Uint16Array"')
					type="Uint16Array"
					#print "DrawElementsUShort",type
					if Uint16Array:
						values=ys.values(Uint16Array[0].data,':')
						Size=ys.getValue(values,'"Size"','i')
						Offset=ys.getValue(values,'"Offset"','i')
						Encoding=ys.getValue(values,'"Encoding"','""')
						#write(log,['Indice:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'magic:',magic],n)
						#print Encoding
						if Encoding=='varint':
							path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
							if os.path.exists(path)==True:
								file=open(path,'rb')
								g=BinaryReader(file)
								magic,indiceList=getIndices(ItemSize,Size,Offset,type,g,mode,magic)
								indiceArray.append([indiceList,mode])
								file.close()
						else:
							path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
							if os.path.exists(path)==True:
								file=open(path,'rb')
								g=BinaryReader(file)
								g.seek(Offset)
								indiceList=g.H(ItemSize*Size)
								indiceArray.append([indiceList,mode])
								file.close()
			#else:
			#	print 'LINES'

		if '"DrawElementsUByte"' in b.header:
			values=ys.values(b.data,':')
			mode=values['"Mode"']
			Size=None
			Offset=None
			Encoding=None
			ItemSize=None
			type=None
			if mode!='"LINES"':
				Indices=ys.get(b,'"Indices"')
				if Indices:
					values=ys.values(Indices[0].data,':')
					ItemSize=ys.getValue(values,'"ItemSize"','i')
					Uint8Array=ys.get(Indices[0],'"Uint8Array"')
					type="Uint8Array"
					#print "DrawElementsUByte",type
					if Uint8Array:
						values=ys.values(Uint8Array[0].data,':')
						Size=ys.getValue(values,'"Size"','i')
						Offset=ys.getValue(values,'"Offset"','i')
						Encoding=ys.getValue(values,'"Encoding"','""')
						#write(log,['Indice:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'magic:',magic],n)
						path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
						if os.path.exists(path)==True:
							file=open(path,'rb')
							g=BinaryReader(file)
							magic,indiceList=getIndices(ItemSize,Size,Offset,type,g,mode,magic)
							indiceArray.append([indiceList,mode])
							file.close()
			#else:
			#	print 'LINES'

	return indiceArray



def Bones(ys,b):
	n=20
	bones=[]
	values=ys.values(b.data,':')
	ItemSize=ys.getValue(values,'"ItemSize"','i')
	Uint16Array=ys.get(b,'"Uint16Array"')
	if Uint16Array:
		type="Uint16Array"
		values=ys.values(Uint16Array[0].data,':')
		File=ys.getValue(values,'"File"','""')
		Size=ys.getValue(values,'"Size"','i')
		Offset=ys.getValue(values,'"Offset"','i')
		Encoding=ys.getValue(values,'"Encoding"','""')

		if Encoding=='varint':
			path=getPath(File)
			if path:
				file=open(path,'rb')
				g=BinaryReader(file)
				list=decodeVarint(g,Offset,Size*ItemSize,type)
				for m in range(Size):
					bones.append(list[m*ItemSize:m*ItemSize+ItemSize])
				file.close()
	return bones

def Weights(ys,b):
	n=20
	weights=[]
	values=ys.values(b.data,':')
	ItemSize=ys.getValue(values,'"ItemSize"','i')
	Float32Array=ys.get(b,'"Float32Array"')
	if Float32Array:
		values=ys.values(Float32Array[0].data,':')
		File=ys.getValue(values,'"File"','""')
		Size=ys.getValue(values,'"Size"','i')
		Offset=ys.getValue(values,'"Offset"','i')
		Encoding=ys.getValue(values,'"Encoding"','""')

		if Encoding=='varint':
			path=getPath(File)
			if path:
				file=open(path,'rb')
				g=BinaryReader(file)
				list=decodeVarint(g,Offset,Size*ItemSize,type)
				file.close()
		else:
			path=getPath(File)
			if path:
				file=open(path,'rb')
				g=BinaryReader(file)
				g.seek(Offset)
				list=g.f(Size*ItemSize)
				for m in range(Size):
					weights.append(list[m*ItemSize:m*ItemSize+ItemSize])
				file.close()
	return weights

def BoneMap(ys,b):
	BoneMap={}
	values=ys.values(b.data,':')
	for value in values:
		id=ys.getValue(values,value,'i')
		name=value.split('"')[1]
		BoneMap[name]=id
	return BoneMap


def osgAnimationRigGeometry(ys,parentNewNode):

	mesh=Mesh()
	mesh.vertexArray=[]
	mesh.indiceArray=[]
	mesh.TexCoord0Array=[]
	mesh.TexCoord1Array=[]
	mesh.TexCoord3Array=[]
	mesh.TexCoord5Array=[]
	mesh.TexCoord6Array=[]
	mesh.colorArray=[]
	mesh.morphArray={}
	mesh.Bones=[]
	mesh.Weights=[]
	mesh.BoneMap={}
	mesh.atributes={}
	mesh.parentNode=parentNewNode.node
	for child in parentNewNode.children:
		#write(log,[child.node.header],4)
		if '"SourceGeometry"' in child.node.header:
			for child in child.children:
				#write(log,[child.node.header],8)
				if '"osgAnimation.MorphGeometry"' in child.node.header:
					for child in child.children:
						#write(log,[child.node.header],12)
						if '"VertexAttributeList"' in child.node.header:
							for child in child.children:
								if '"Vertex"' in child.node.header:
									mesh.vertexArray=Vertex(ys,child.node)
								if '"TexCoord0"' in child.node.header:
									mesh.TexCoord0Array=TexCoord(ys,child.node)
								if '"TexCoord1"' in child.node.header:
									mesh.TexCoord1Array=TexCoord(ys,child.node)
								if '"TexCoord3"' in child.node.header:
									mesh.TexCoord3Array=TexCoord(ys,child.node)
								if '"TexCoord5"' in child.node.header:
									mesh.TexCoord5Array=TexCoord(ys,child.node)
								if '"TexCoord6"' in child.node.header:
									mesh.TexCoord6Array=TexCoord(ys,child.node)
								if '"Color"' in child.node.header:
									mesh.colorArray=Color(ys,child.node)
						if '"PrimitiveSetList"' in child.node.header:
							mesh.indiceArray=PrimitiveSetList(ys,child)
						if '"UserDataContainer"' in child.node.header:
							mesh.atributes=UserDataContainer(ys,child)
						if '"MorphTargets"' in child.node.header:
							print "MorphTargets"
							for child in child.children:
								#write(log,[child.node.header],16)
								if '"osg.Geometry"' in child.node.header:
									Name=None
									for child in child.children:
										#write(log,[child.node.header],20)
										if '"VertexAttributeList"' in child.node.header:
											for child in child.children:
												if '"Vertex"' in child.node.header:
													if Name:
														mesh.morphArray[Name]=Vertex(ys,child.node)
										if '"UniqueID"' in child.node.header:
											values=ys.values(child.node.header,':')
											UniqueID=ys.getValue(values,'"UniqueID"','i')
											Name=ys.getValue(values,'"Name"','""')
											#write(log,[UniqueID,Name],24)
				if '"osg.Geometry"' in child.node.header:
					for child in child.children:
						if '"VertexAttributeList"' in child.node.header:
							for child in child.children:
								if '"Vertex"' in child.node.header:
									mesh.vertexArray=Vertex(ys,child.node)
								if '"TexCoord0"' in child.node.header:
									mesh.TexCoord0Array=TexCoord(ys,child.node)
								if '"TexCoord1"' in child.node.header:
									mesh.TexCoord1Array=TexCoord(ys,child.node)
								if '"TexCoord3"' in child.node.header:
									mesh.TexCoord3Array=TexCoord(ys,child.node)
								if '"TexCoord5"' in child.node.header:
									mesh.TexCoord5Array=TexCoord(ys,child.node)
								if '"TexCoord6"' in child.node.header:
									mesh.TexCoord6Array=TexCoord(ys,child.node)
								if '"Color"' in child.node.header:
									mesh.colorArray=Color(ys,child.node)
						if '"PrimitiveSetList"' in child.node.header:
							mesh.indiceArray=PrimitiveSetList(ys,child)
						if '"UserDataContainer"' in child.node.header:
							mesh.atributes=UserDataContainer(ys,child)


		if '"VertexAttributeList"' in child.node.header:
			for child in child.children:
				if '"Bones"' in child.node.header:
					mesh.Bones=Bones(ys,child.node)
				if '"Weights"' in child.node.header:
					mesh.Weights=Weights(ys,child.node)
		if '"BoneMap"' in child.node.header:
			mesh.BoneMap=BoneMap(ys,child.node)

	return mesh

def osgGeometry(ys,parentNewNode):

	mesh=Mesh()
	mesh.vertexArray=[]
	mesh.indiceArray=[]
	mesh.TexCoord0Array=[]
	mesh.TexCoord1Array=[]
	mesh.TexCoord3Array=[]
	mesh.TexCoord5Array=[]
	mesh.TexCoord6Array=[]
	mesh.colorArray=[]
	mesh.morphArray={}
	mesh.Bones=[]
	mesh.Weights=[]
	mesh.BoneMap={}
	mesh.atributes={}
	mesh.parentNode=parentNewNode.node
	for child in parentNewNode.children:
		#write(log,[child.node.header],4)
		if '"VertexAttributeList"' in child.node.header:
			for child in child.children:
				#write(log,[child.node.header],8)
				if '"Vertex"' in child.node.header:
					mesh.vertexArray=Vertex(ys,child.node)
				if '"TexCoord0"' in child.node.header:
					mesh.TexCoord0Array=TexCoord(ys,child.node)
				if '"TexCoord1"' in child.node.header:
					mesh.TexCoord1Array=TexCoord(ys,child.node)
				if '"TexCoord3"' in child.node.header:
					mesh.TexCoord3Array=TexCoord(ys,child.node)
				if '"TexCoord5"' in child.node.header:
					mesh.TexCoord5Array=TexCoord(ys,child.node)
				if '"TexCoord6"' in child.node.header:
					mesh.TexCoord6Array=TexCoord(ys,child.node)
				if '"Color"' in child.node.header:
					mesh.colorArray=Color(ys,child.node)
		if '"PrimitiveSetList"' in child.node.header:
			mesh.indiceArray=PrimitiveSetList(ys,child)
		if '"UserDataContainer"' in child.node.header:
			mesh.atributes=UserDataContainer(ys,child)
	return mesh


def osgAnimationMorphGeometry(ys,parentNewNode):

	mesh=Mesh()
	mesh.vertexArray=[]
	mesh.indiceArray=[]
	mesh.TexCoord0Array=[]
	mesh.TexCoord1Array=[]
	mesh.TexCoord3Array=[]
	mesh.TexCoord5Array=[]
	mesh.TexCoord6Array=[]
	mesh.colorArray=[]
	mesh.morphArray={}
	mesh.Bones=[]
	mesh.Weights=[]
	mesh.BoneMap={}
	mesh.atributes={}
	mesh.parentNode=parentNewNode.node
	for child in parentNewNode.children:
		if '"MorphTargets"' in child.node.header:
			print "MorphTargets"
			for child in child.children:
				#write(log,[child.node.header],16)
				if '"osg.Geometry"' in child.node.header:
					Name=None
					for child in child.children:
						#write(log,[child.node.header],20)
						if '"VertexAttributeList"' in child.node.header:
							for child in child.children:
								if '"Vertex"' in child.node.header:
									if Name:
										mesh.morphArray[Name]=Vertex(ys,child.node)
						if '"UniqueID"' in child.node.header:
							values=ys.values(child.node.header,':')
							UniqueID=ys.getValue(values,'"UniqueID"','i')
							Name=ys.getValue(values,'"Name"','""')
							#write(log,[UniqueID,Name],24)
		if '"VertexAttributeList"' in child.node.header:
			for child in child.children:
				#print child.node.header
				if '"Vertex"' in child.node.header:
					mesh.vertexArray=Vertex(ys,child.node)
				if '"TexCoord0"' in child.node.header:
					mesh.TexCoord0Array=TexCoord(ys,child.node)
				if '"TexCoord1"' in child.node.header:
					mesh.TexCoord1Array=TexCoord(ys,child.node)
				if '"TexCoord3"' in child.node.header:
					mesh.TexCoord3Array=TexCoord(ys,child.node)
				if '"TexCoord5"' in child.node.header:
					mesh.TexCoord5Array=TexCoord(ys,child.node)
				if '"TexCoord6"' in child.node.header:
					mesh.TexCoord6Array=TexCoord(ys,child.node)
				if '"Color"' in child.node.header:
					mesh.colorArray=Color(ys,child.node)
		if '"PrimitiveSetList"' in child.node.header:
			mesh.indiceArray=PrimitiveSetList(ys,child)
		if '"UserDataContainer"' in child.node.header:
			mesh.atributes=UserDataContainer(ys,child)



	return mesh


def drawMesh(ys,mesh):
	diffuse=None
	normal=None
	specular=None
	trans=None
	ao=None
	rgbCol=None
	rgbSpec=None
	rgba=None
	mode=None



	matName,diffuse,specular,normal,ao,trans,rgbCol,rgbSpec,rgba=getMatName(ys,mesh.parentNode)
	#print 'matName:',matName,diffuse
	if len(mesh.indiceArray)>0:
		for [indices,mode] in mesh.indiceArray:
			mat=Mat()
			mat.matName=matName
			mat.rgbCol=rgbCol
			mat.diffuse=diffuse
			mat.normal=normal
			mat.specular=specular
			mat.trans=trans
			if trans:
				mat.ZTRANS=True
			#mat.ao=ao
			if rgba:mat.rgba=rgba
			mesh.matList.append(mat)
			mat.IDStart=len(mesh.indiceList)
			mat.IDCount=len(indices)
			mesh.indiceList.extend(indices)
			if mode=='"TRIANGLE_STRIP"':mat.TRISTRIP=True
			if mode=='"TRIANGLES"':mat.TRIANGLE=True

		indices=mesh.indiceArray[0][0]
		mode=mesh.indiceArray[0][1]
	if len(mesh.vertexArray)==1:
		if mesh.vertexArray[0][1]=='"varint"':
			if mode:
				bytes=mesh.vertexArray[0][0]
				ItemSize=mesh.vertexArray[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(mesh.atributes['vtx_bbl_x'])
				s2=float(mesh.atributes['vtx_bbl_y'])
				s3=float(mesh.atributes['vtx_bbl_z'])
				s=[s1,s2,s3]
				a1=float(mesh.atributes['vtx_h_x'])
				a2=float(mesh.atributes['vtx_h_y'])
				a3=float(mesh.atributes['vtx_h_z'])
				a=[a1,a2,a3]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				mesh.vertPosList=[floats[m:m+ItemSize]for m in range(0,len(floats),3)]
				#print mesh.vertPosList
				#mesh.indi
				#mesh.draw()
		else:
			list=mesh.vertexArray[0][0]
			mesh.vertPosList=list

	if len(mesh.TexCoord0Array)==1:
		if mesh.TexCoord0Array[0][1]=='"varint"':
			if mode:
				bytes=mesh.TexCoord0Array[0][0]
				ItemSize=mesh.TexCoord0Array[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(mesh.atributes['uv_0_bbl_x'])
				s2=float(mesh.atributes['uv_0_bbl_y'])
				s=[s1,s2]
				a1=float(mesh.atributes['uv_0_h_x'])
				a2=float(mesh.atributes['uv_0_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
		else:
			list=mesh.TexCoord0Array[0][0]
			mesh.vertUVList=list
	elif len(mesh.TexCoord1Array)==1:
		if mesh.TexCoord1Array[0][1]=='"varint"':
			if mode:
				bytes=mesh.TexCoord1Array[0][0]
				ItemSize=mesh.TexCoord1Array[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(mesh.atributes['uv_1_bbl_x'])
				s2=float(mesh.atributes['uv_1_bbl_y'])
				s=[s1,s2]
				a1=float(mesh.atributes['uv_1_h_x'])
				a2=float(mesh.atributes['uv_1_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
		else:
			list=mesh.TexCoord1Array[0][0]
			mesh.vertUVList=list
	elif len(mesh.TexCoord3Array)==1:
		if mesh.TexCoord3Array[0][1]=='"varint"':
			if mode:
				bytes=mesh.TexCoord3Array[0][0]
				ItemSize=mesh.TexCoord3Array[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(mesh.atributes['uv_3_bbl_x'])
				s2=float(mesh.atributes['uv_3_bbl_y'])
				s=[s1,s2]
				a1=float(mesh.atributes['uv_3_h_x'])
				a2=float(mesh.atributes['uv_3_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
		else:
			list=mesh.TexCoord3Array[0][0]
			mesh.vertUVList=list
	elif len(mesh.TexCoord5Array)==1:
		if mesh.TexCoord5Array[0][1]=='"varint"':
			if mode:
				bytes=mesh.TexCoord5Array[0][0]
				ItemSize=mesh.TexCoord5Array[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(mesh.atributes['uv_5_bbl_x'])
				s2=float(mesh.atributes['uv_5_bbl_y'])
				s=[s1,s2]
				a1=float(mesh.atributes['uv_5_h_x'])
				a2=float(mesh.atributes['uv_5_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
		else:
			list=mesh.TexCoord5Array[0][0]
			mesh.vertUVList=list
	elif len(mesh.TexCoord6Array)==1:
		if mesh.TexCoord6Array[0][1]=='"varint"':
			if mode:
				bytes=mesh.TexCoord6Array[0][0]
				ItemSize=mesh.TexCoord6Array[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(mesh.atributes['uv_6_bbl_x'])
				s2=float(mesh.atributes['uv_6_bbl_y'])
				s=[s1,s2]
				a1=float(mesh.atributes['uv_6_h_x'])
				a2=float(mesh.atributes['uv_6_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
		else:
			list=mesh.TexCoord6Array[0][0]
			mesh.vertUVList=list
	if len(mesh.colorArray)>0:
		mesh.vertColList=mesh.colorArray




def UserDataContainer(ys,b):
	atributes={}
	Values=ys.get(b.node,'"Values"')
	if Values:
		for a in Values[0].children:
			values=ys.values(a.data,':')
			Name=ys.getValue(values,'"Name"','""')
			Value=ys.getValue(values,'"Value"','""')
			#if Name:write(log,[Name,Value],n+4)
			if Name:atributes[Name]=Value
	return atributes

def osgNode(ys,parentNewNode,parentBone):
	for child in parentNewNode.children:
		for child in child.children:
			if '"osg.Geometry"' in child.node.header:
				mesh=osgGeometry(ys,child)
				mesh.parentBone=parentBone
				model.meshList.append(mesh)
			if '"osgAnimation.RigGeometry"' in child.node.header:
				mesh=osgAnimationRigGeometry(ys,child)
				mesh.parentBone=parentBone
				model.meshList.append(mesh)
			if '"osgAnimation.MorphGeometry"' in child.node.header:
				mesh=osgAnimationMorphGeometry(ys,child)
				mesh.parentBone=parentBone
				model.meshList.append(mesh)


def osgMatrixTransform(ys,parentNewNode,parentBone):
	bone=Bone()
	bone.Name=None
	bone.UpdateName=None
	bone.matrix=Matrix().resize4x4()#.invert()
	if parentBone:bone.parentName=parentBone.name
	skeleton.boneList.append(bone)
	for child in parentNewNode.children:
		if '"Matrix"' in child.node.header:
			values=ys.values(child.node.data,'f')
			bone.matrix=Matrix4x4(values)
			if parentBone:bone.matrix*=parentBone.matrix
		if '"UniqueID"' in child.node.header:
			values=ys.values(child.node.header,':')
			UniqueID=ys.getValue(values,'"UniqueID"','i')
			bone.name='UniqueID_'+str(UniqueID)
		if '"Name"' in child.node.header:
			values=ys.values(child.node.header,':')
			Name=ys.getValue(values,'"Name"','""')
			#bindBone.Name=Name
			bone.Name=Name
		if '"UpdateCallbacks"' in child.node.header:
			for child in child.children:
				if '"osgAnimation.UpdateMatrixTransform"' in child.node.header:
					for child in child.children:
						if '"Name"' in child.node.header:
							values=ys.values(child.node.header,':')
							Name=ys.getValue(values,'"Name"','""')
							#bindBone.UpdateName=Name
							bone.UpdateName=Name
	return bone


def osgAnimationBone(ys,parentNewNode,parentBone):
	bone=Bone()
	skeleton.boneList.append(bone)
	bone.matrix=Matrix().resize4x4()#.invert()
	bindBone=Bone()
	bindBone.matrix=Matrix().resize4x4()#.invert()
	bindBone.Name=None
	bone.Name=None
	bone.UpdateName=None
	bindBone.UpdateName=None
	for child in parentNewNode.children:
		if '"InvBindMatrixInSkeletonSpace"' in child.node.header:
			values=ys.values(child.node.data,'f')
			matrix=Matrix4x4(values)
			bindBone.matrix=matrix.invert()
			bindskeleton.boneList.append(bindBone)
		if '"UniqueID"' in child.node.header:
			values=ys.values(child.node.header,':')
			UniqueID=ys.getValue(values,'"UniqueID"','i')
			bindBone.name='UniqueID_'+str(UniqueID)
			bone.name='UniqueID_'+str(UniqueID)
		if '"Name"' in child.node.header:
			values=ys.values(child.node.header,':')
			Name=ys.getValue(values,'"Name"','""')
			bindBone.Name=Name
			bone.Name=Name
			#boneIndeksList[Name]=bone.name
		if '"Matrix"' in child.node.header:
			values=ys.values(child.node.data,'f')
			bone.matrix=Matrix4x4(values)
			if parentBone:
				if 'MatrixTransform' not in parentBone.name:
					bone.parentName=parentBone.name
				bone.matrix*=parentBone.matrix
		if '"UpdateCallbacks"' in child.node.header:
			for child in child.children:
				if '"osgAnimation.UpdateBone"' in child.node.header:
					for child in child.children:
						if '"Name"' in child.node.header:
							values=ys.values(child.node.header,':')
							Name=ys.getValue(values,'"Name"','""')
							bindBone.UpdateName=Name
							bone.UpdateName=Name
	return bone

def getNewNodeTree(ys,parentNewNode,n,parentBone,data):

	if '"osgAnimation.Skeleton"' in parentNewNode.node.header:
		parentBone=osgAnimationBone(ys,parentNewNode,parentBone)
		bindskeleton.parentBone=parentBone
	if '"osg.Node"' in parentNewNode.node.header:
		osgNode(ys,parentNewNode,parentBone)
	if '"osg.MatrixTransform"' in parentNewNode.node.header:
		parentBone=osgMatrixTransform(ys,parentNewNode,parentBone)
	if '"osgAnimation.Bone"' in parentNewNode.node.header:
		parentBone=osgAnimationBone(ys,parentNewNode,parentBone)
	n+=4
	for child in parentNewNode.children:
		#write(log,[child.node.header,child.UniqueID],n)
		getNewNodeTree(ys,child,n,parentBone,data)

def osgParser(filename):
	global skeleton,bindskeleton,model,boneIndeksList,firstmatrix,newNodeList
	#RigGeometry=False
	boneIndeksList={}
	model=Model(filename)
	model.matList={}
	skeleton=Skeleton()
	skeleton.ARMATURESPACE=True
	bindskeleton=Skeleton()
	bindskeleton.parentBone=None
	bindskeleton.ARMATURESPACE=True
	UniqueIDList={}
	ys=Yson()
	ys.log=True
	ys.filename=filename
	ys.parse()

	root=ys.root
	n=0
	newNodeList=[]
	newRoot=NewNode()
	newRoot.node=ys.root
	newNodeList.append(newRoot)
	getIDTree(ys,ys.root,n,newRoot)

	root=newRoot
	getNewNodeTree(ys,root,n,None,None)

#def sss():

	skeleton.draw()
		#for bone in bindskeleton.boneList:
		#	bone.matrix*=bindskeleton.parentBone.matrix
	if len(bindskeleton.boneList)>0:
		bindskeleton.draw()
	if bindskeleton.parentBone and bindskeleton.object:
		bindskeleton.object.setMatrix(bindskeleton.parentBone.matrix)
	#boneNameList=[]

	for bone in skeleton.boneList:
		if bone.UpdateName:
			#Name=getSplitName(bone.Name,'_',-1)
			boneIndeksList[bone.UpdateName]=bone.name
			#print Name,bone.name

	n=0
	result=2
	Animations=ys.get(ys.root,'"osgAnimation.Animation"')
	if Animations:
		result=Blender.Draw.PupMenu("export animations as *.action?%t|Yes|No")
		if result==1:
			for animation in Animations:
				getAnimation(ys,animation,n)





	for mesh in model.meshList:
		mesh.BINDSKELETON=skeleton.name
		drawMesh(ys,mesh)

	#model.getMat()
	result=2
	result=Blender.Draw.PupMenu("Send meshes to startpose?%t|Yes|No")

	result10=1
	if len(model.meshList)>10:
		result10=Blender.Draw.PupMenu("import "+str(len(model.meshList))+" meshes "+"?%t|Yes|No")

	if result10==1:
		for i1,mesh in enumerate(model.meshList):
			print i1,'vert:',len(mesh.vertPosList),'col:',len(mesh.vertColList),'uv:',len(mesh.vertUVList),'indice:',len(mesh.indiceList),'mat:',len(mesh.matList),'skin:',len(mesh.skinList)#,matName
			Blender.Window.DrawProgressBar(float((i1)/float(len(model.meshList))),str(len(model.meshList)-1-i1))

			mesh.BINDSKELETON=skeleton.name
			if len(mesh.vertPosList)>0:
				if len(mesh.Bones)>0 and len(mesh.Weights)>0:
					skin=Skin()
					skin.boneMap=[0]*len(mesh.BoneMap)
					mesh.boneNameList=['']*len(mesh.BoneMap)
					for boneName in mesh.BoneMap:
						for bone in skeleton.boneList:
							if bone.Name==boneName:
								id=mesh.BoneMap[boneName]
								skin.boneMap[id]=id
								mesh.boneNameList[id]=bone.name
								break
					mesh.skinList.append(skin)
					mesh.skinIndiceList=mesh.Bones
					mesh.skinWeightList=mesh.Weights

				if bindskeleton.object and skeleton.object:
					if mesh.parentBone and len(mesh.skinList)>0:
						mesh.draw()
						mesh.object.getData(mesh=1).transform(mesh.parentBone.matrix)
						mesh.object.getData(mesh=1).update()
						#mesh.object.setMatrix(mesh.parentBone.matrix)
						if result==1:
							bindPose(bindskeleton.object,skeleton.object,mesh.object)
						skeleton.object.makeParentDeform([mesh.object],1,0)
					elif mesh.parentBone and len(mesh.skinList)==0:
						mesh.setSkin(mesh.parentBone.name)
						mesh.draw()
						mesh.object.getData(mesh=1).transform(mesh.parentBone.matrix)
						mesh.object.getData(mesh=1).update()
						skeleton.object.makeParentDeform([mesh.object],1,0)
				else:
					if mesh.parentBone:
						if len(mesh.skinList)==0:
							mesh.setSkin(mesh.parentBone.name)
						mesh.draw()
						mesh.object.getData(mesh=1).transform(mesh.parentBone.matrix)
						mesh.object.getData(mesh=1).update()
						#mesh.object.setMatrix(mesh.parentBone.matrix)
						#skeleton.object.makeParentBone([mesh.object],mesh.parentBone.name,0,0)
						if skeleton.object and skeleton.object:
							skeleton.object.makeParentDeform([mesh.object],1,0)
					else:
						#print len(mesh.vertPosList)
						#print mesh.indiceList
						#mesh.indiceList=[]
						mesh.draw()
						#mesh.object.getData(mesh=1).transform(mesh.parentBone.matrix)
						#mesh.object.getData(mesh=1).update()
						#mesh.object.setMatrix(mesh.parentBone.matrix)

				"""
				if len(mesh.morphArray)>0:
					name=mesh.object.name
					action=Action()
					action.MESHSPACE=True
					action.name=name
					for i,morph in enumerate(mesh.morphArray):
						#morphMesh=Mesh()
						#morphMesh.vertPosList=mesh.morphArray[morph][0][0]
						#print morph
						#morphMesh.draw()
						vertList=mesh.morphArray[morph][0][0]
						frame=i*5
						action.shapeFrameList.append(frame)
						action.shapeKeyList.append(vertList)
					action.draw()
					action.setContext()
					"""





		model.set()











		#for i,mesh in enumerate(model.meshList):
		#	Blender.Window.DrawProgressBar(float(i/float(len(model.meshList)+1)),str(-1+len(model.meshList)-i))
		#print 'result:',result
		if result!=2:
			if	bindskeleton.object:
				scene = bpy.data.scenes.active
				scene.objects.unlink(bindskeleton.object)

def htmParser(filename):
	ys=Yson()
	ys.log=True
	ys.filename=filename
	ys.parse()
	##os.system('cls')


	#szukam ikony
	print 'szukam ikony'
	#print ys.root
	THUMBNAILS=ys.get(ys.root,'"thumbnails"')
	print THUMBNAILS
	ikona=None
	SIZE=0
	if THUMBNAILS:
		for thumbnails in THUMBNAILS:
			#print thumbnails.header
			URL=ys.get(thumbnails,'"url"')
			for a in URL:
				values=ys.values(a.data,':')
				url=ys.getValue(values,'"url"','""')
				size=ys.getValue(values,'"size"','i')
				if url:
					basename=os.path.basename(url)
					if '.jpeg' in basename:path=sys.dir+os.sep+os.path.basename(url)+'.jpg'
					else:path=sys.dir+os.sep+os.path.basename(url)
					exists=os.path.exists(path)
					#print 'ikona',exists,os.path.basename(url)+'.jpg'
					if exists==True:
						if size>SIZE:
							SIZE=size
							ikona=path

	if ikona:
		#print ikona
		for file in os.listdir(sys.dir):
			if '.htm' in file:
				if os.path.exists(sys.dir+os.sep+file+".thumb.10.png")==False:
					if os.path.exists(ikona):
						os.rename(ikona,sys.dir+os.sep+file+".thumb.10.png")
				else:
					if os.path.exists(sys.dir+os.sep+file+".thumb.11.png")==False:
						if os.path.exists(ikona):
							os.rename(ikona,sys.dir+os.sep+file+".thumb.11.png")




	RESULTS=ys.get(ys.root,'"results"')
	if RESULTS:
		for results in RESULTS:
			write(log,["results"],0)
			UIDS=ys.get(results,'"uid"')
			if UIDS:
				for UID in UIDS:
					#write(log,[UID.header],4)
					uid=None
					values=None
					if '"uid"' in UID.header:values=ys.values(UID.header,':')
					if '"uid"' in UID.data:values=ys.values(UID.data,':')
					if values:uid=ys.getValue(values,'"uid"','""')
					write(log,['uid:',uid],4)
					if uid:
						formats=ys.get(UID,'"format"')
						if formats:
							IMAGES[uid]={}
							IMAGES[uid]['A']=[None,None,100]
							IMAGES[uid]['RGB']=[None,None,100]
							IMAGES[uid]['N']=[None,None,100]
							IMAGES[uid]['R']=[None,None,100]
							for formatNode in formats:
								write(log,['image'],8)
								values=None
								format=None
								if '"format"' in formatNode.header:values=ys.values(formatNode.header,':')
								if '"format"' in formatNode.data:values=ys.values(formatNode.data,':')
								if values:format=ys.getValue(values,'"format"','""')
								write(log,['format:',format],12)
								values=None
								quality=None
								if '"quality"' in formatNode.header:values=ys.values(formatNode.header,':')
								if '"quality"' in formatNode.data:values=ys.values(formatNode.data,':')
								if values:quality=ys.getValue(values,'"quality"','i')
								write(log,['quality:',quality],12)
								values=None
								url=None
								if '"url"' in formatNode.header:values=ys.values(formatNode.header,':')
								if '"url"' in formatNode.data:values=ys.values(formatNode.data,':')
								if values:url=ys.getValue(values,'"url"','""')
								#write(log,['url:',url],12)
								if not url:
									if '"url"' in formatNode.parent.header:values=ys.values(formatNode.parent.header,':')
									if '"url"' in formatNode.parent.data:values=ys.values(formatNode.parent.data,':')
									if values:url=ys.getValue(values,'"url"','""')
								if url:
									basename=os.path.basename(url)
									if '.jpeg' in basename:path=sys.dir+os.sep+os.path.basename(url)+'.jpg'
									else:path=sys.dir+os.sep+os.path.basename(url)
									exists=os.path.exists(path)
									write(log,['path:',path,exists],12)

									if format not in IMAGES[uid].keys():
										print 'NOWY FORMAT:',format
										IMAGES[uid][format]=[path,exists,quality]
									else:
										if quality and format:
											if quality<=IMAGES[uid][format][2] and exists==True:
												IMAGES[uid][format]=[path,exists,quality]








	allImagePaths=[]


	usedImagePaths=[]
	for key in IMAGES:
		#write(log,[key],0)
		for item in IMAGES[key]:
			#write(log,[item,':',IMAGES[key][item]],4)
			if IMAGES[key][item][0]:
				if IMAGES[key][item][0] not in usedImagePaths:
					usedImagePaths.append(IMAGES[key][item][0])

	for image in allImagePaths:
		if image not in usedImagePaths:
			if os.path.exists(image)==True:
				print 'usuwam:',image
				#os.remove(image)

	materials=ys.get(ys.root,'"materials"')
	if materials:
		for a in materials:
			for b in a.children:
				matName=None
				if '"name"' in b.data:
					values=ys.values(b.data,':')
					matName=ys.getValue(values,'"name"','""').replace(':','')
					matName=matName.replace(':','')
					if '\\' in matName:matName=matName.split('\\')[0]
					MATERIALS[matName]={}
				else:
					for c in b.children:
						if '"name"' in c.header:
							values=ys.values(c.header,':')
							matName=ys.getValue(values,'"name"','""')
							MATERIALS[matName]={}
				#print matName
				write(log,[matName],0)
				if	matName:
					#matName=matName.replace(':','')
					#if '\\' in matName:matName=matName.split('\\')[0]
					channels=ys.get(b,'"channels"')
					if channels:
						for c in channels[0].children:
							MATERIALS[matName][c.header.split('"')[1]]=['',[],[]]
							values=ys.values(c.data,':')
							enable=ys.getValue(values,'"enable"','s')
							if enable:
								if enable=='true':
									for d in c.children:
										dvalues=ys.values(d.header,':')
										#print dvalues
										if '"texture"' in d.header:
											if '"uid"' in d.data:
												values=ys.values(d.data,':')
												uid=ys.getValue(values,'"uid"','""')
												write(log,[uid],4)
												if uid in IMAGES.keys():
													for format in IMAGES[uid]:
														write(log,[format,IMAGES[uid][format]],8)
														pass
												else:
													write(log,['MISSING:',uid],8)
													pass

												MATERIALS[matName][c.header.split('"')[1]]=['texture',uid]
												uid=MATERIALS[matName][c.header.split('"')[1]][1]
												#print IMAGES[uid]
										if '"color"' in d.header:
											values=ys.values(d.data,'f')
											MATERIALS[matName][c.header.split('"')[1]]=['color',values]
							else:
									for d in c.children:

										values=ys.values(d.header,':')
										enable=ys.getValue(values,'"enable"','s')
										if enable:

											if enable=='true':

													dvalues=ys.values(d.header,':')
													#print dvalues
													if '"texture"' in d.header:
														if '"uid"' in d.data:
															values=ys.values(d.data,':')
															uid=ys.getValue(values,'"uid"','""')
															write(log,[uid],4)
															if uid in IMAGES.keys():
																for format in IMAGES[uid]:
																	write(log,[format,IMAGES[uid][format],enable],8)
																	pass
															else:
																write(log,['MISSING:',uid],8)
																pass

															MATERIALS[matName][c.header.split('"')[1]]=['texture',uid]
															uid=MATERIALS[matName][c.header.split('"')[1]][1]
															#print IMAGES[uid]
													if '"color"' in d.header:
														values=ys.values(d.data,'f')
														MATERIALS[matName][c.header.split('"')[1]]=['color',values]



def actionParser(filename,g):
	action=Action()
	action.BONESPACE=True
	action.BONESORT=True
	while(True):
		if g.tell()>=g.fileSize():break
		bone=ActionBone()
		action.boneList.append(bone)
		bone.name=g.find('\x00')
		type=g.find('\x00')
		#print bone.name,type,g.tell()
		if type=='size':
			count=g.i(1)[0]
			#print count
			for m in safe(count):
				matrix=VectorScaleMatrix(g.f(3))
				bone.sizeKeyList.append(matrix)
			count=g.i(1)[0]
			#print count
			for m in safe(count):
				frame=int(g.f(1)[0]*33)
				bone.sizeFrameList.append(frame)
		if type=='translate':
			count=g.i(1)[0]
			#print count
			for m in safe(count):
				matrix=VectorMatrix(g.f(3))
				bone.posKeyList.append(matrix)
			count=g.i(1)[0]
			#print count
			for m in safe(count):
				frame=int(g.f(1)[0]*33)
				bone.posFrameList.append(frame)
		if type=='quaternion':
			count=g.i(1)[0]
			#print count
			for m in safe(count):
				quat=Quaternion(g.f(4))
				matrix=QuatMatrix(quat).resize4x4()
				bone.rotKeyList.append(matrix)
			count=g.i(1)[0]
			#print count
			for m in safe(count):
				frame=int(g.f(1)[0]*33)
				bone.rotFrameList.append(frame)
	action.draw()
	action.setContext()



def getCanonical(filename):
	file=open(filename,'r')
	data=file.read()
	#print data
	canonical=None
	if '"canonical"' in data:
		canonical=data.split('"canonical"')[1].split('"')[1].split('/')[4]
		#('<link rel="canonical" href="https://sketchfab.com/3d-models/')[1].split('">')[0]
		if "-" in canonical:
			canonical=canonical.split("-")[-1]
	#if
	file.close()
	return canonical

def Parser(path):
	global sys,MATERIALS,IMAGES,LASTNODENAME,log,skipdecode,filename
	log=open('log.txt','w')
	LASTNODENAME=None
	MATERIALS={}
	IMAGES={}


	filename=path
	sys=Sys(filename)
	os.system("cls")
	ext=filename.split('.')[-1].lower()
	if ext=='gz':
		osg=sys.dir+os.sep+'file.osgjs'
		if os.path.exists(osg)==False:
			cmd=Cmd()
			cmd.input=filename
			cmd.ZIP=True
			cmd.run()
			model=sys.dir+os.sep+'model_file.bin.gz'
			if os.path.exists(model)==True:
				cmd=Cmd()
				cmd.input=model
				cmd.ZIP=True
				cmd.run()
			osgParser(filename.split('.gz')[0])

	if ext=='osgjs':
		osgParser(filename)
	if ext=='txt':
		osgParser(filename)
	if ext in ['htm','html']:
		osg=sys.dir+os.sep+'file.osgjs.gz'
		if os.path.exists(osg)==True:
			cmd=Cmd()
			cmd.input=osg
			cmd.ZIP=True
			cmd.run()
			model=sys.dir+os.sep+'model_file.bin.gz'
		else:
			osg=sys.dir+os.sep+'file.osgjs.gz.txt'
		model=sys.dir+os.sep+'model_file.bin.gz'
		if os.path.exists(model)==True:
			cmd=Cmd()
			cmd.input=model
			cmd.ZIP=True
			cmd.run()
		else:
			model=sys.dir+os.sep+'model_file.bin.gz.txt'
		if os.path.exists(model):

			result=1
			result=Blender.Draw.PupMenu("Sketchfab Viewer ?%t|Yes|No")
			if result==1:
				canonical=getCanonical(filename)
				chromeExe="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
				#os.system(chromeExe)
				#subprocess.Popen([chromeExe,filename]).wait()
				#txt=htm1+htm2+htm3
				txt=open("sketchfab.html","w")
				txt.write(htm1.replace("#",""))
				if canonical is not None:

					txt.write(canonical)
				else:
					#txt.write(htm2)
					txt.write(os.path.dirname(filename).split(os.sep)[-1])
				txt.write(htm3)
				txt.close()
				subprocess.Popen([chromeExe,blendDir+os.sep+"sketchfab.html"])#.wait()
			else:


				result=1
				fileSize=os.path.getsize(model)
				result=Blender.Draw.PupMenu("import "+str(round(fileSize/1000000.0,1))+" Mb ?%t|Yes|No")

				htmParser(filename)
				if result==1:
					skipdecode=0

					result=1
					result=Blender.Draw.PupMenu("indice problem"+" ?%t|Yes|No")
					if result==1:
						skipdecode=1



					osgPath=sys.dir+os.sep+'file.osgjs'
					if os.path.exists(osgPath)==True:
						osgParser(osgPath)
						pass
					else:
						osgPath=sys.dir+os.sep+'file.osgjs.gz.txt'
						if os.path.exists(osgPath)==True:
							osgParser(osgPath)
							pass

	if ext=='action':
		file=open(filename,'rb')
		g=BinaryReader(file)
		actionParser(filename,g)
		file.close()
	log.close()




Blender.Window.FileSelector(Parser,'import','htm files: *.... - model')
