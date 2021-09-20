import bpy
from mathutils import *
from .myFunction import *
from .commandLib import *
import random
import os





def setBox(box,meshList):
	E=[[],[],[]]
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			E[0].append(x)
			E[1].append(y)
			E[2].append(z)
	skX=(box[3]-box[0])/(max(E[0])-min(E[0]))
	skY=(box[4]-box[1])/(max(E[1])-min(E[1]))
	skZ=(box[5]-box[2])/(max(E[2])-min(E[2]))
	sk=min(skX,skY,skZ)
	trX1=(box[3]+box[0])/2#-(max(E[0])+min(E[0]))/2
	trY1=(box[4]+box[1])/2#-(max(E[1])+min(E[1]))/2
	trZ1=(box[5]+box[2])/2#-(max(E[2])+min(E[2]))/2

	trX=-(max(E[0])+min(E[0]))/2
	trY=-(max(E[1])+min(E[1]))/2
	trZ=-(max(E[2])+min(E[2]))/2
	#print(trX,trY,trZ)
	#print(skX,skY,skZ)

	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x+trX,y+trY,z+trZ]
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x*skX,y*skY,z*skZ]
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x+trX1,y+trY1,z+trZ1]
		#mesh.draw()



def bindPose1(bindSkeleton,poseSkeleton,meshObject):
		#print('BINDPOSE')
		mesh=meshObject.getData(mesh=1)
		poseBones=poseSkeleton.getData().bones
		bindBones=bindSkeleton.getData().bones
		for vert in mesh.verts:
			index=vert.index
			skinList=mesh.getVertexInfluences(index)
			vco=vert.co.copy()*meshObject.matrixWorld
			vector=Vector()
			sum=0
			for skin in skinList:
				bone=skin[0]
				weight=skin[1]
				if bone in bindBones.keys() and bone in poseBones.keys():
					matA=bindBones[bone].matrix['ARMATURESPACE']#*bindSkeleton.matrixWorld
					matB=poseBones[bone].matrix['ARMATURESPACE']#*poseSkeleton.matrixWorld
					vector+=vco*matA.invert()*matB*weight
					sum+=weight
				else:
					vector=vco
					break
			vert.co=vector
		mesh.update()
		Blender.Window.RedrawAll()

def bindPose(bindSkeleton,poseSkeleton,meshObject):
		#print('BINDPOSE')
		mesh=meshObject.getData(mesh=1)
		poseBones=poseSkeleton.getData().bones
		bindBones=bindSkeleton.getData().bones
		for vert in mesh.verts:
			index=vert.index
			skinList=mesh.getVertexInfluences(index)
			vco=vert.co.copy()*meshObject.matrixWorld
			vector=Vector()
			sum=0
			for skin in skinList:
				bone=skin[0]
				weight=skin[1]
				if bone in bindBones.keys() and bone in poseBones.keys():
					matA=bindBones[bone].matrix['ARMATURESPACE']*bindSkeleton.matrixWorld
					matB=poseBones[bone].matrix['ARMATURESPACE']*poseSkeleton.matrixWorld
					vector+=vco*matA.invert()*matB*weight
					sum+=weight
				else:
					vector=vco
					break
			vert.co=vector
		mesh.update()
		Blender.Window.RedrawAll()



class Model:
	def __init__(self,input):
		self.meshList=[]
		self.filename=input
		self.dirname=None
		self.basename=None
		self.matPath=None
		self.matPath=self.filename+'.mat'


	def getMat(self):#
		if self.filename is not None and self.meshList>0:
			self.basename=os.path.basename(self.filename)
			self.dirname=os.path.dirname(self.filename)
			if os.path.exists(self.matPath)==False:
				print('--opening', self.matPath)
				matFile=open(self.matPath,'w')
				for i,mesh in enumerate(self.meshList):
					for j,mat in enumerate(mesh.matList):
						matFile.write(str(i)+'|'+str(j)+'|'+str(None)+'|'+str(None)+'|'+str(None)+'|'+str(None)+'|'+str(None)+'\n')#meshID+matID+diff+norm+spec
				matFile.close()


			#print(self.matPath)
			if os.path.exists(self.matPath)==True:
				print('--opening', self.matPath)
				matFile=open(self.matPath,'r')
				lines=matFile.readlines()
				lineID=0
				for i,mesh in enumerate(self.meshList):
					for j,mat in enumerate(mesh.matList):
						#for line in lines:
							line=lines[lineID]
							lineID+=1
							#print(i,j,line)
							values=line.strip().split('|')
							#print(values,self.filename)
							if len(values)>3:
								if not mat.diffuse:
									if os.path.exists(values[2])==True:
										mat.diffuse=values[2]
									else:
										if os.path.exists(self.filename)==True:
											path=os.path.dirname(self.filename)+os.sep+os.path.basename(values[2])
											mat.diffuse=path
								if not mat.diffuse2:
									if os.path.exists(values[2])==True:
										mat.diffuse2=values[2]
									else:
										if os.path.exists(self.filename)==True:
											path=os.path.dirname(self.filename)+os.sep+os.path.basename(values[2])
											mat.diffuse2=path
								if not mat.normal:
									if os.path.exists(values[3])==True:
										mat.normal=values[3]
									else:
										if os.path.exists(self.filename)==True:
											path=os.path.dirname(self.filename)+os.sep+os.path.basename(values[3])
											mat.normal=path
								if not mat.specular:
									if os.path.exists(values[4])==True:
										mat.specular=values[4]
									else:
										if os.path.exists(self.filename)==True:
											path=os.path.dirname(self.filename)+os.sep+os.path.basename(values[4])
											mat.specular=path
								if not mat.ao:
									if os.path.exists(values[5])==True:
										mat.ao=values[5]
									else:
										if os.path.exists(self.filename)==True:
											path=os.path.dirname(self.filename)+os.sep+os.path.basename(values[5])
											mat.ao=path
								if not mat.trans:
									if os.path.exists(values[6])==True:
										mat.trans=values[6]
									else:
										if os.path.exists(self.filename)==True:
											path=os.path.dirname(self.filename)+os.sep+os.path.basename(values[6])
											mat.trans=path
				matFile.close()

	def setMat(self):
		pass


	def set(self):
		fn = os.path.join(os.path.dirname(self.filename), "sesja.txt")
		if os.path.exists(fn)==False:
			file=open(fn,'w')
		file=open(fn,'r')
		copylines=file.readlines()
		file=open(fn,'w')
		for line in copylines:
			file.write(line)
		file.write('file|'+self.filename+'|'+str(len(self.meshList))+'\n')
		for i,mesh in enumerate(self.meshList):
			if len(mesh.vertPosList)>0:
				if mesh.SPLIT==False:
					if mesh.object:
						mesh.object.name = mesh.object.name+'-'+str(i)
				file.write('matCount'+'|'+str(len(mesh.matList))+'\n')
				for j,mat in enumerate(mesh.matList):
					if mesh.SPLIT==False:
						file.write(mat.name+'|'+mesh.object.name+'\n')
					if mesh.SPLIT==True:
						if mat.object:
							mat.object.name = mat.object.name+'-'+str(i)
							file.write(mat.name+'|'+mat.object.name+'\n')
		file.close()


	def draw(self):
		fn = os.path.join(os.path.dirname(self.filename), "sesja.txt")
		#self.getMat()
		if os.path.exists(fn)==False:
			file=open(fn,'w')
		file=open(fn,'r')
		copylines=file.readlines()
		file=open(fn,'w')
		for line in copylines:
			file.write(line)
		file.write('file|'+self.filename+'|'+str(len(self.meshList))+'\n')
		print('mesh count:',len(self.meshList))
		for i,mesh in enumerate(self.meshList):
			Blender.Window.DrawProgressBar(i/(float(len(self.meshList))),'wczytuje siatki')
			if len(mesh.vertPosList)>0:
				print(i,'vert:',len(mesh.vertPosList),'col:',len(mesh.vertColList),'uv:',len(mesh.vertUVList),'indice:',len(mesh.indiceList),'mat:',len(mesh.matList),'skin:',len(mesh.skinList))

				"""
				for j,mat in enumerate(mesh.matList):
					print(' '*4,'mat:',j,)
					if mat.diffuse:print('d:',1,)
					else:print('d:',0,)
					if mat.normal:print('n:',1,)
					else:print('n:',0,)
					if mat.specular:print('s:',1,)
					else:print('s:',0,)
					if mat.ao:print('ao:',1,)
					else:print('ao:',0,)
					if mat.trans:print('t:',1,)
					else:print('t:',0,)
				print
				"""

				mesh.draw()
				if mesh.SPLIT==False:
					if mesh.object:
						mesh.object.setName(mesh.object.name+'-'+str(i))
				file.write('matCount'+'|'+str(len(mesh.matList))+'\n')
				if mesh.BINDSKELETON is not None and mesh.BINDBONE is not None:
					mesh.setBoneMatrix(mesh.BINDSKELETON,mesh.BINDBONE)
				for j,mat in enumerate(mesh.matList):
					if mesh.SPLIT==False:
						file.write(mat.name+'|'+mesh.object.name+'\n')
					if mesh.SPLIT==True:
						if mat.object:
							mat.object.setName(mat.object.name+'-'+str(i))
							file.write(mat.name+'|'+mat.object.name+'\n')
		file.close()




class Mesh():

	def __init__(self):
		self.vertPosList=[]
		self.vertNormList=[]

		self.indiceList=[]
		self.faceList=[]
		self.triangleList=[]

		self.matList=[]
		self.matIDList=[]
		self.vertUVList=[]
		self.vertUVSList=[[],[],[],[],[],[],[],[]]
		self.faceUVList=[]
		self.faceColList=[]
		self.vertColList=[]

		self.skinList=[]
		self.skinWeightList=[]
		self.skinIndiceList=[]
		self.skinGroupList=[]
		self.skinIDList=[]
		self.bindPoseMatrixList=[]
		self.boneNameList=[]
		self.BINDBONE=None

		self.name=None
		self.mesh=None
		self.object=None
		self.TRIANGLE=False
		self.QUAD=False
		self.TRISTRIP=False
		self.BINDSKELETON=None
		self.BINDPOSESKELETON=None
		self.matrix=None
		self.SPLIT=False
		self.WARNING=False
		self.DRAW=False
		self.BINDPOSE=False
		self.UVFLIP=False
		self.sceneIDList=None

		self.vertModList=[]
		self.mod=False
		self.filename=None
		self.BUFFER=0

		self.RAW=0


	def setSkin(self,boneName):
		skin=Skin()
		self.skinList.append(skin)
		for m in range(len(self.vertPosList)):
			self.skinWeightList.append([1.0])
			self.skinGroupList.append([boneName])



	def addMat(self,mat,mesh,matID):
		mat.name=mesh.name.split('-')[0]+'-'+str(matID)+'-'+str(self.sceneIDList.objectID)
		return
		blendMat=Blender.Material.New(mat.name)
		blendMat.setRms(0.04)
		blendMat.shadeMode=Blender.Material.ShadeModes.CUBIC
		if mat.rgbCol is None:
			#blendMat.rgbCol=mat.rgba[:3]
			#blendMat.alpha = mat.rgba[3]
			pass
		else:
			blendMat.rgbCol=mat.rgbCol[:3]
			blendMat.alpha = mat.rgba[3]
		if mat.rgbSpec is not None:
			blendMat.specCol=mat.rgbSpec[:3]
		if mat.ZTRANS==True:
			blendMat.mode |= Blender.Material.Modes.ZTRANSP
			blendMat.mode |= Blender.Material.Modes.TRANSPSHADOW
			blendMat.alpha = 0.0
		if mat.diffuse:mat.setDiffuse(blendMat)
		if mat.diffuse2:mat.setDiffuse2(blendMat)
		if mat.specular:mat.setSpecular(blendMat)
		if mat.normal:mat.setNormal(blendMat)
		if mat.ao:mat.setAo(blendMat)
		if mat.trans:mat.setTransparent(blendMat)
		mesh.materials+=[blendMat]


	def addvertexUV(self,blenderMesh,mesh):
		pass # DEPRECADO "stiky UV"
		# blenderMesh.vertexUV = 1
		#for m in range(len(blenderMesh.vertices)):
		#	if self.UVFLIP==False:
		#		blenderMesh.verts[m].uvco = Vector(mesh.vertUVList[m][0], 1-mesh.vertUVList[m][1])
		#	else:
		#		blenderMesh.verts[m].uvco = Vector(mesh.vertUVList[m])


	def addfaceUV(self,blenderMesh,mesh):
		if len(blenderMesh.polygons)>0:
			blenderMesh.uv_layers.new()
			if len(mesh.vertUVList)>0 and False:
				for poly in(blenderMesh.polygons):
					###
					if self.UVFLIP==True:
						blenderMesh.verts[m].uvco = Vector(mesh.vertUVList[m])
					else:
						blenderMesh.verts[m].uvco = Vector(mesh.vertUVList[m][0], 1-mesh.vertUVList[m][1])



					face.uv = [v.uvco for v in poly.vertices]
					face.smooth = 1
					if len(mesh.matIDList)>0:
						if ID<len(mesh.matIDList):
							face.mat=mesh.matIDList[ID]
			if len(mesh.matIDList)>0:
				for ID in range(len(blenderMesh.polygons)):
					face=blenderMesh.polygons[ID]
					#face.smooth = 1
					#print(ID,len(mesh.matIDList))
					if ID<len(mesh.matIDList):
						pass
						#face.mat=mesh.matIDList[ID]
			if len(mesh.faceUVList)>0:
				for ID in range(len(blenderMesh.polygons)):
					face=blenderMesh.polygons[ID]
					if mesh.faceUVList[ID] is not None:
						pass
						#face.uv=mesh.faceUVList[ID]
			if len(self.vertNormList)==0:
				pass
				#blenderMesh.calcNormals()
			#blenderMesh.update()

	def addSkinIDList(self):
		if len(self.skinIDList)==0:
			for m in range(len(self.vertPosList)):
				self.skinIDList.append([])
				for n in range(len(self.skinList)):
					self.skinIDList[m].append(0)
			for skinID in range(len(self.skinList)):
				skin=self.skinList[skinID]
				if skin.IDStart==None:
					skin.IDStart=0
				if skin.IDCount==None:
					skin.IDCount=len(self.vertPosList)
				for vertID in range(skin.IDStart,skin.IDStart+skin.IDCount):
					self.skinIDList[vertID][skinID]=1


	def addSkinWithIndiceList(self,blendMesh,mesh):
		for vertID in range(len(mesh.skinIDList)):
			indices=mesh.skinIndiceList[vertID]
			weights=mesh.skinWeightList[vertID]
			for skinID,ID in enumerate(mesh.skinIDList[vertID]):
				if ID==1:
					if len(weights)<len(indices):count=len(weights)
					else:count=len(indices)
					for n in range(count):
						w  = weights[n]
						if type(w)==int:w=w/255.0
						if w!=0.0:
							grID = indices[n]
							if len(self.boneNameList)==0:
								if len(self.skinList[skinID].boneMap)>0:grName = str(self.skinList[skinID].boneMap[grID])
								else:grName = str(grID)
							else:
								if len(self.skinList[skinID].boneMap)>0:
									grNameID = self.skinList[skinID].boneMap[grID]
									grName=self.boneNameList[grNameID]
								else:
									grName=self.boneNameList[grID]
							if grName not in blendMesh.getVertGroupNames():
								blendMesh.addVertGroup(grName)
							add = Blender.Mesh.AssignModes.ADD
							blendMesh.assignVertsToGroup(grName,[vertID],w,add)
		blendMesh.update()


	def addSkinWithGroupList(self,blendMesh,mesh):
		for vertID in range(len(mesh.skinIDList)):
			groups=mesh.skinGroupList[vertID]
			weights=mesh.skinWeightList[vertID]
			for skinID,ID in enumerate(mesh.skinIDList[vertID]):
				if ID==1:
					if len(weights)<len(groups):count=len(weights)
					else:count=len(groups)
					for n in range(count):
						w  = weights[n]
						if type(w)==int:w=w/255.0
						if w!=0.0:
							grName=groups[n]
							if grName not in blendMesh.getVertGroupNames():
								blendMesh.addVertGroup(grName)
							add = Blender.Mesh.AssignModes.ADD
							blendMesh.assignVertsToGroup(grName,[vertID],w,add)
		blendMesh.update()


	def addSkin(self,blendMesh,mesh):
		#print('addskin')
		for vertID in range(len(mesh.skinIDList)):
			indices=mesh.skinIndiceList[vertID]
			weights=mesh.skinWeightList[vertID]
			#print(mesh.skinIDList[vertID])
			for skinID,ID in enumerate(mesh.skinIDList[vertID]):
				if ID==1:
					if len(weights)<len(indices):count=len(weights)
					else:count=len(indices)
					#print(indices,weights)
					for n in range(count):
						w  = weights[n]
						if type(w)==int:w=w/255.0
						if w!=0.0:
							grID = indices[n]
							if len(self.boneNameList)==0:
								if len(self.skinList[skinID].boneMap)>0:grName = str(self.skinList[skinID].boneMap[grID])
								else:grName = str(grID)
							else:
								if len(self.skinList[skinID].boneMap)>0:
									grNameID = self.skinList[skinID].boneMap[grID]
									grName=self.boneNameList[grNameID]
								else:
									grName=self.boneNameList[grID]
							if grName not in blendMesh.getVertGroupNames():
								blendMesh.addVertGroup(grName)
							add = Blender.Mesh.AssignModes.ADD
							blendMesh.assignVertsToGroup(grName,[vertID],w,add)
		blendMesh.update()



	def addFaces(self):
		if len(self.matList)==0:
			if len(self.faceList)!=0:
				self.triangleList=self.faceList
			if len(self.indiceList)!=0:
				if self.TRIANGLE==True:
					self.indicesToTriangles(self.indiceList,0)
				elif self.QUAD==True:
					self.indicesToQuads(self.indiceList,0)
				elif self.TRISTRIP==True:
					self.indicesToTriangleStrips(self.indiceList,0)
				else:
					if self.WARNING==True:
						print('WARNING: class<Mesh>.TRIANGLE:',self.TRIANGLE)
						print('WARNING: class<Mesh>.TRISTRIP:',self.TRISTRIP)


		else:
			if len(self.faceList)>0:
				if len(self.matIDList)==0:
					for matID in range(len(self.matList)):
						mat=self.matList[matID]
						if mat.IDStart is not None and mat.IDCount is not None:
							for faceID in range(mat.IDCount):
								self.triangleList.append(self.faceList[mat.IDStart+faceID])
								self.matIDList.append(matID)
						else:
							if mat.IDStart==None:
								mat.IDStart=0
							if mat.IDCount==None:
								mat.IDCount=len(self.faceList)
							for faceID in range(mat.IDCount):
								self.triangleList.append(self.faceList[mat.IDStart+faceID])
								self.matIDList.append(matID)
					#self.triangleList=self.faceList


				else:
					self.triangleList=self.faceList
					#for ID in range(len(self.matIDList)):
					#	mat=self.matList[matID]
						#if self.matIDList[ID]==matID:
					#	self.triangleList.append(self.faceList[ID])

			if len(self.indiceList)>0:
				if len(self.matIDList)==0:
					for matID in range(len(self.matList)):
						mat=self.matList[matID]
						if mat.IDStart==None:
							mat.IDStart=0
						if mat.IDCount==None:
							mat.IDCount=len(self.indiceList)
						indiceList=self.indiceList[mat.IDStart:mat.IDStart+mat.IDCount]
						if mat.TRIANGLE==True:
							self.indicesToTriangles(indiceList,matID)
						elif mat.QUAD==True:
							self.indicesToQuads(indiceList,matID)
						elif mat.TRISTRIP==True:
							self.indicesToTriangleStrips(indiceList,matID)
				"""else:

						if mat.TRIANGLE==True:
							self.indicesToTriangles2(indiceList)
						elif mat.QUAD==True:
							self.indicesToQuads2(indiceList)
						elif mat.TRISTRIP==True:
							self.indicesToTriangleStrips2(indiceList)"""




	def buildMesh(self,mesh,mat,meshID):
		if len(mesh.vertPosList)>0:
			blendMesh = bpy.data.meshes.new(mesh.name)
			blendMesh.verts.extend(mesh.vertPosList)
			triangleFlag=False
			for triangle in mesh.triangleList:
				if len(triangle)>4 or len(triangle)<3:
					print('not a triangle:',triangle)
					triangleFlag=True
			if triangleFlag==False:
				blendMesh.faces.extend(mesh.triangleList,ignoreDups=True)
				self.addMat(mat,blendMesh,meshID)
			if len(mesh.triangleList)>0:
				if len(mesh.vertUVList)>0:
					self.addvertexUV(blendMesh,mesh)
					self.addfaceUV(blendMesh,mesh)
				if len(mesh.faceUVList)>0:
					self.addfaceUV(blendMesh,mesh)
			if len(mesh.vertNormList)>0:
				for i,vert in enumerate(blendMesh.verts):
					vert.no=Vector(self.vertNormList[i])

			scene = bpy.context.scene
			if self.BUFFER==0:
				meshobject = scene.objects.new(blendMesh,mesh.name)
				try:
					self.addSkinWithIndiceList(blendMesh,mesh)
				except:
					print('WARNING:self.addSkinWithIndiceList:',mesh.name)


				mat.object=meshobject

			if self.BUFFER==1:
				mat.object=blendMesh
				mat.mesh=mesh
			Blender.Window.RedrawAll()

	def addMesh(self):
		self.mesh = bpy.data.meshes.new(self.name)
		#print('---addMesh...')
		#print('----self.vertPosList', self.vertPosList)
		#print('----self.triangleList', self.triangleList)
		#self.mesh.verts.extend(self.vertPosList)
		if len(self.vertNormList)>0:
			for i,vert in enumerate(self.mesh.verts):
				vert.no=Vector(self.vertNormList[i])
		self.mesh.from_pydata(self.vertPosList, [], self.triangleList)
		scene = bpy.context.scene
		self.object = bpy.data.objects.new(self.name, self.mesh)
		scene.collection.objects.link(self.object)


	def setSkeletonParent(self,skeletonName):
		if skeletonName is not None:
			scene = bpy.context.scene
			for object in scene.objects:
				if object.name==skeletonName:
					skeletonMatrix=self.object.getMatrix()*object.mat
					self.object.setMatrix(skeletonMatrix)
					object.makeParentDeform([self.object],1,0)


	def draw(self,id=None):
		#print('---draw...')
		self.sceneIDList=SceneIDList()
		if not self.name:
			self.name=str(self.sceneIDList.meshID).zfill(3)+'-0-'+str(self.sceneIDList.objectID)
		self.addFaces()
		if self.SPLIT==False:
			self.addMesh()
			if self.mod==True:
				print('--opening', self.name)
				modFile=open(self.name+'.txt','w')
				if self.filename is not None:
					modFile.write(self.filename+'\n')
				else:
					modFile.write('None'+'\n')
				for m in range(len(self.vertModList)):
					a,b,c=self.vertModList[m]
					modFile.write(str(a)+' '+str(b)+' '+str(c)+'\n')
				modFile.close()
			if len(self.triangleList)>0:
				if len(self.vertUVList)>0:
					self.addvertexUV(self.mesh,self)
			self.addfaceUV(self.mesh,self)
			for matID in range(len(self.matList)):
				mat=self.matList[matID]
				self.addMat(mat,self.mesh,matID)

			if self.BINDSKELETON is not None:
				scene = bpy.context.scene
				object = scene.objects.get(self.BINDSKELETON)
				if object:
					skeletonMatrix=self.object.matrix_world @ object.matrix_world
					#self.object.setMatrix(skeletonMatrix)
					#object.makeParentDeform([self.object],1,0)
			if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0 and False:
				if len(self.skinIndiceList)==len(self.skinWeightList)>0:
					try:
						self.addSkinIDList()
						self.addSkinWithIndiceList(self.mesh,self)
					except:
						print('WARNING:self.addSkinWithIndiceList:',self.mesh.name)
			if len(self.skinGroupList)>0 and len(self.skinWeightList)>0 and False:
				if len(self.skinGroupList)==len(self.skinWeightList)>0:
					#print('addSkinWithGroupList')
					try:
						self.addSkinIDList()
						self.addSkinWithGroupList(self.mesh,self)
					except:
						print('WARNING:self.addSkinWithGroupList:',self.mesh.name)

			if len(self.vertColList)==len(self.vertPosList) and False:
				if len(self.triangleList)>0:
					self.mesh.vertexColors = 1
					for face in self.mesh.faces:
						for i,v in enumerate(face):
							col=face.col[i]
							col.r=self.vertColList[v.index][0]
							col.g=self.vertColList[v.index][1]
							col.b=self.vertColList[v.index][2]
							#write(log,self.vertColList[v.index],0)
					print('MESH UZYWA VERTEX COLOR')
				else:
					print('MESH NIE UZYWA VERTEX COLOR:',self.mesh.name,len(self.triangleList))
			#Blender.Window.RedrawAll()



		if self.SPLIT==True:
			#print('Dzielenie siatek:',len(self.matList))
			#print('self.name:',self.name)
			meshList=[]
			for matID in range(len(self.matList)):
				mesh=Mesh()
				mesh.IDList={}
				mesh.IDCounter=0
				#if self.matList[matID].name is not None:
				#	mesh.name=self.matList[matID].name
				#else:
				#	mesh.name=self.name+'-'+str(matID)
				mesh.name=self.name.split('-')[0]+'-'+str(matID).zfill(3)+'-'+str(self.sceneIDList.objectID).zfill(3)
				#print(' '*4,'siatka:',matID,mesh.name)
				meshList.append(mesh)

			for faceID in range(len(self.matIDList)):
				matID=self.matIDList[faceID]
				mesh=meshList[matID]
				for vID in self.triangleList[faceID]:
					mesh.IDList[vID]=None

			for faceID in range(len(self.matIDList)):
				matID=self.matIDList[faceID]
				mesh=meshList[matID]
				for vID in self.triangleList[faceID]:
					if mesh.IDList[vID] is None:
						mesh.IDList[vID]=mesh.IDCounter
						mesh.IDCounter+=1


			for faceID in range(len(self.matIDList)):
				matID=self.matIDList[faceID]
				mesh=meshList[matID]
				face=[]
				for vID in self.triangleList[faceID]:
					face.append(mesh.IDList[vID])
				#mesh.faceList.append(face)
				mesh.triangleList.append(face)
				mesh.matIDList.append(0)
				if len(self.faceUVList)>0:
					mesh.faceUVList.append(self.faceUVList[faceID])
			for mesh in meshList:
				for m in range(len(mesh.IDList)):
					mesh.vertPosList.append(None)
				if len(self.vertUVList)>0:
					for m in range(len(mesh.IDList)):
						mesh.vertUVList.append(None)
				if len(self.skinList)>0:
					if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:
						for m in range(len(mesh.IDList)):
							mesh.skinWeightList.append([])
							mesh.skinIndiceList.append([])
							mesh.skinIDList.append(None)
			if len(self.skinList)>0:
				if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:
					if len(self.skinIDList)==0:
						try:
							self.addSkinIDList()
						except:
							print('WARNING:self.addSkinIDList:',self.name)
			for i,mesh in enumerate(meshList):
				#print(mesh.IDList.keys())
				for vID in mesh.IDList.keys():
					mesh.vertPosList[mesh.IDList[vID]]=self.vertPosList[vID]
				if len(self.vertUVList)>0:
					for vID in mesh.IDList.keys():
						mesh.vertUVList[mesh.IDList[vID]]=self.vertUVList[vID]
				if len(self.skinList)>0:
					if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:
						if len(self.skinIDList)>0:
							for vID in mesh.IDList.keys():
								mesh.skinWeightList[mesh.IDList[vID]]=self.skinWeightList[vID]
								mesh.skinIndiceList[mesh.IDList[vID]]=self.skinIndiceList[vID]
								mesh.skinIDList[mesh.IDList[vID]]=self.skinIDList[vID]
						else:
							#mat=self.matList[i]]
							#if mat.IDStart is not None and mat.IDCount is not None:
							#	for
							print('self.skinIDList is missing')

			if self.RAW==True:
				return meshList
			else:
				for meshID in range(len(meshList)):
					mesh=meshList[meshID]
					mat=self.matList[meshID]
					if id:
						if id==meshID:
							self.buildMesh(mesh,mat,meshID)
					else:
						self.buildMesh(mesh,mat,meshID)

				Blender.Window.RedrawAll()




	def indicesToQuads(self,indicesList,matID):
		for m in range(0, len(indicesList), 4):
			self.triangleList.append(indicesList[m:m+4] )
			self.matIDList.append(matID)

	def indicesToTriangles(self,indicesList,matID):
		for m in range(0, len(indicesList), 3):
			self.triangleList.append(indicesList[m:m+3] )
			self.matIDList.append(matID)


	def indicesToTriangleStrips(self,indicesList,matID):
		StartDirection = -1
		id=0
		f1 = indicesList[id]
		id+=1
		f2 = indicesList[id]
		FaceDirection = StartDirection
		while(True):
		#for m in range(len(indicesList)-2):
			id+=1
			f3 = indicesList[id]
			#print(f3)
			if (f3==0xFFFF):
				if id==len(indicesList)-1:break
				id+=1
				f1 = indicesList[id]
				id+=1
				f2 = indicesList[id]
				FaceDirection = StartDirection
			else:
				#f3 += 1
				FaceDirection *= -1
				if (f1!=f2) and (f2!=f3) and (f3!=f1):
					if FaceDirection > 0:
						self.triangleList.append([(f1),(f2),(f3)])
						self.matIDList.append(matID)
					else:
						self.triangleList.append([(f1),(f3),(f2)])
						self.matIDList.append(matID)
					if self.DRAW==True:
						f1,f2,f3
				f1 = f2
				f2 = f3
			if id==len(indicesList)-1:break


	def indicesToQuads2(self,indicesList):
		for m in range(0, len(indicesList), 4):
			self.triangleList.append(indicesList[m:m+4] )
			#self.matIDList.append(matID)

	def indicesToTriangles2(self,indicesList):
		for m in range(0, len(indicesList), 3):
			self.triangleList.append(indicesList[m:m+3] )
			#self.matIDList.append(matID)


	def indicesToTriangleStrips2(self,indicesList):
		StartDirection = -1
		id=0
		f1 = indicesList[id]
		id+=1
		f2 = indicesList[id]
		FaceDirection = StartDirection
		while(True):
		#for m in range(len(indicesList)-2):
			id+=1
			f3 = indicesList[id]
			#print(f3)
			if (f3==0xFFFF):
				if id==len(indicesList)-1:break
				id+=1
				f1 = indicesList[id]
				id+=1
				f2 = indicesList[id]
				FaceDirection = StartDirection
			else:
				#f3 += 1
				FaceDirection *= -1
				if (f1!=f2) and (f2!=f3) and (f3!=f1):
					if FaceDirection > 0:
						self.triangleList.append([(f1),(f2),(f3)])
						#self.matIDList.append(matID)
					else:
						self.triangleList.append([(f1),(f3),(f2)])
						#self.matIDList.append(matID)
					if self.DRAW==True:
						f1,f2,f3
				f1 = f2
				f2 = f3
			if id==len(indicesList)-1:break


class Skin:
	def __init__(self):
		self.boneMap=[]
		self.IDStart=None
		self.IDCount=None
		self.skeleton=None
		self.skeletonFile=None


def getImageFromBlender(path):
	img=None
	if os.path.exists(path)==True:
		for image in Blender.Image.Get():
			if image.getFilename()==path:
				img=image
		if not img:img=Blender.Image.Load(path)
	return img

class Mat:
	def __init__(self):
		self.name=None
		self.object=None

		self.diffuse=None#1
		self.normal=None#2
		self.specular=None#3
		self.ao=None#4
		self.trans=None#5
		self.ZTRANS=False
		self.diffuse2=None#6


		self.TRIANGLE=False
		self.TRISTRIP=False
		self.QUAD=False
		self.IDStart=None
		self.IDCount=None
		self.rgbCol=None
		self.rgbSpec=None

		r=random.randint(0,255)
		g=random.randint(0,255)
		b=random.randint(0,255)
		self.rgba=[r/255.0,g/255.0,b/255.0,1.0]

		self.TexCoUV=None
		self.MapToCOL=None
		self.MapToALPHA=None
		self.MapToNOR=None
		self.MapToCSP=None
		self.MapToSPEC=None

	def setDiffuse(self,blendMat):
		img=getImageFromBlender(self.diffuse)
		if img and False:
			imgName=blendMat.name+'-d'
			img.setName(imgName)
			texname=blendMat.name+'-d'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img
			blendMat.setTexture(0,tex,self.TexCoUV,self.MapToCOL|self.MapToALPHA)

	def setDiffuse2(self,blendMat):
		img=getImageFromBlender(self.diffuse2)
		if img and False:
			imgName=blendMat.name+'-d2'
			img.setName(imgName)
			texname=blendMat.name+'-d2'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img
			blendMat.setTexture(6,tex,self.TexCoUV,self.MapToCOL|self.MapToALPHA)
			mtextures = blendMat.getTextures()
			mtex=mtextures[6]
			#mtex.neg=True
			mtex.blendmode=Blender.Texture.BlendModes.ADD

	def setNormal(self,blendMat):
		img=getImageFromBlender(self.normal)
		if img and False:
			imgName=blendMat.name+'-n'
			img.setName(imgName)
			texname=blendMat.name+'-n'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img
			tex.setImageFlags('NormalMap')
			blendMat.setTexture(1,tex,self.TexCoUV,self.MapToNOR)

	def setSpecular(self,blendMat):
		img=getImageFromBlender(self.specular)
		if img and False:
			imgName=blendMat.name+'-s'
			img.setName(imgName)
			texname=blendMat.name+'-s'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img
			blendMat.setTexture(2,tex,self.TexCoUV,self.MapToCSP|self.MapToSPEC)
			mtextures = blendMat.getTextures()
			mtex=mtextures[2]
			mtex.neg=True
			mtex.blendmode=Blender.Texture.BlendModes.SUBTRACT

	def setAo(self,blendMat):
		img=getImageFromBlender(self.ao)
		if img and False:
			imgName=blendMat.name+'-ao'
			img.setName(imgName)
			texname=blendMat.name+'-ao'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img
			blendMat.setTexture(3,tex,self.TexCoUV,self.MapToCOL)
			mtex=blendMat.getTextures()[3]
			mtex.blendmode=Blender.Texture.BlendModes.MULTIPLY

	def setTransparent(self,blendMat):
		img=getImageFromBlender(self.trans)
		if img and False:
			imgName=blendMat.name+'-a'
			img.setName(imgName)
			texname=blendMat.name+'-a'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.setImageFlags('CalcAlpha')
			tex.image = img
			blendMat.setTexture(4,tex,self.TexCoUV,self.MapToALPHA)
			if blendMat.getTextures()[0] is not None:blendMat.getTextures()[0].mtAlpha=0

