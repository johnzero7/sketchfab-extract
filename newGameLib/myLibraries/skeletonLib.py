#import Blender
from .myFunction import *
from mathutils import *
import bpy

#Strife Online nowy euler


def odlegloscmiedzykosciami(head1,head2):

	x=head2[0]-head1[0]
	y=head2[1]-head1[1]
	z=head2[2]-head1[2]
	e=1/2.0
	d=(x**2+y**2+z**2)**e
	return d,x,y,z

class Bone:
	def __init__(self):
		self.ID=None
		self.name=None
		self.parentID=None
		self.parentName=None
		self.quat=None
		self.pos=None
		self.matrix=None
		self.posMatrix=Matrix()
		self.rotMatrix=Matrix()
		self.scaleMatrix=Matrix()
		self.children=[]
		self.edit=None
		self.tail=None
		self.type=None
		self.transform=None#spine



class Skeleton:
	def __init__(self):
		self.name=None
		self.boneList=[]
		self.armature=None
		self.object=None
		self.boneNameList=[]
		self.ARMATURESPACE=False
		self.BONESPACE=True
		self.INVERTSPACE=False
		self.DEL=True
		self.NICE=False
		self.IK=False
		self.BINDMESH=False
		self.WARNING=False
		self.debug=None
		self.debugFile=None
		self.SORT=False
		self.matrix=None
		self.parentTestFlag=False
		self.nameTestFlag=False
		self.parentProblemList=[]
		self.nameProblemList=[]
		self.param=0.01
		self.JOIN=False

	def testParent(self):
		#self.parentTestFlag=False
		for bone in self.boneList:
			bone.parentList=[]
			if bone.name is not None:
			#print(bone.name,bone.parentName)
				for parent in self.boneList:
					if parent.name!=bone.name:
						if bone.parentName==parent.name:
							bone.parentList.append(parent)
		for bone in self.boneList:
			if len(bone.parentList)>1:
				self.parentTestFlag=True
				self.parentProblemList.append(bone)

	def testLongName(self):
		for bone in self.boneList:
			if bone.name is not None:
				if len(bone.name)>25:
					self.nameTestFlag=True
					self.nameProblemList.append(bone)
					#print('Problem: name too long for bone',bone.name)


	def boneChildren(self,parentBlenderBone,parentBone):
		for child in parentBlenderBone.children:
			for bone in self.boneList:
				if bone.name == child.name:
					blenderBone = self.armature.bones[bone.name]
					###bone.matrix @= parentBone.matrix
					self.boneChildren(blenderBone,bone)

	def createChildList(self):
		for boneID in range(len(self.boneList)):
			bone=self.boneList[boneID]
			name=bone.name
			blenderBone=self.armature.bones[name]
			if blenderBone.parent is None:
				self.boneChildren(blenderBone,bone)

	def draw(self):
		if self.ARMATURESPACE==True:
			self.BONESPACE=False
			self.INVERTSPACE=False
		if self.INVERTSPACE==True:
			self.BONESPACE=False
			self.ARMATURESPACE=False
		if self.BONESPACE==True:
			self.ARMATURESPACE=False
			self.INVERTSPACE=False
		objectID=SceneIDList().armatureID
		if not self.name:self.name='armature-'+str(objectID)
		if self.WARNING==True:
			print('INPUT:')
			print('class<Skeleton>.name:',self.name)
			print('class<Skeleton>.boneList:',len(self.boneList))
			print('class<Skeleton>.ARMATURESPACE:',self.ARMATURESPACE)
			print('class<Skeleton>.BONESPACE:',self.BONESPACE)

		if self.debug is not None:
			self.debugFile=open(self.debug+'.skeleton','w')

		#self.create_bones()
		self.testLongName()
		self.testParent()
		if self.parentTestFlag==False and self.nameTestFlag==False:
			self.check()
			if len(self.boneList)>0:
				self.create_bones()
				self.create_bone_connection()
				if self.SORT==True:
					self.createChildList()
				self.create_bone_position()
			if self.BINDMESH is True:
				scene = bpy.context.scene
				for object in scene.objects:
					if object.type=='Mesh':
						self.object.makeParentDeform([object],1,0)
			if self.IK==True:
				self.armature.data.display_type = 'OCTAHEDRAL'
				for key in self.armature.bones.keys():
					bone=self.armature.bones[key]
					#print(bone)
					children=bone.children
					if len(children)==1:
						self.armature.makeEditable()
						ebone=self.armature.bones[bone.name]
						#self.armature.bones[children[0].name].options=Blender.Armature.CONNECTED
						if ebone.tail!=children[0].head['ARMATURESPACE']:
							ebone.tail=children[0].head['ARMATURESPACE']
						self.armature.update()
				for key in self.armature.bones.keys():
					bone=self.armature.bones[key]
					#print(bone)
					children=bone.children
					if len(children)==1:
						self.armature.makeEditable()
						self.armature.bones[children[0].name].options=Blender.Armature.CONNECTED
						self.armature.update()
				if self.IK==True:
					self.armature.autoIK=True
			for bone in self.boneList:
				if bone.tail:
					self.armature.makeEditable()
					bonetail=self.boneList[bone.tail]
					ebone=self.armature.bones[bone.name]
					ebonetail=self.armature.bones[bonetail.name]
					if bone.type not in [6,7]:
						if ebone.head!=ebonetail.head:
							ebone.tail=ebonetail.head
							ebonetail.options=Blender.Armature.CONNECTED

					self.armature.update()
			return 1
		else:
			print
			print('=======PROBLEMY===========')
			if self.parentTestFlag is True:
				print('WARNING: Bones found with more than one parent')
				for bone in self.parentProblemList:
					print(bone.name,len(bone.parentList),'rodzic')
					for parent in bone.parentList:
						print(' '*4,parent.name)
			if self.nameTestFlag is True:
				print('WARNING: Found bones with too long names')
				for bone in self.nameProblemList:
					print(bone.name,len(bone.name),'liter')
			print
			return 0

		if self.debug is not None:
			self.debugFile.close()



	def create_bones(self):
		bpy.context.view_layer.objects.active = self.object
		bpy.ops.object.mode_set(mode='EDIT')
		boneList=[]
		for bone in self.armature.bones.values():
			if bone.name not in boneList:
				boneList.append(bone.name)
		for boneID in range(len(self.boneList)):
			name=self.boneList[boneID].name
			if self.debug is not None:
				self.debugFile.write(name+'\n')
			if name is None:
				name=str(boneID).encode()
				self.boneList[boneID].name=name
			self.boneNameList.append(name)
			if name not in boneList:
				eb = self.armature.edit_bones.new(name.decode())
				eb.length = 1
		bpy.ops.object.mode_set(mode='OBJECT')

	def create_bone_connection(self):
		bpy.context.view_layer.objects.active = self.object
		bpy.ops.object.mode_set(mode='EDIT')
		for boneID in range(len(self.boneList)):
			name=self.boneList[boneID].name
			if name is None:
				name=str(boneID).encode()
			bone=self.armature.edit_bones[name.decode()]
			parentID=None
			parentName=None
			if self.boneList[boneID].parentID is not None:
				parentID=self.boneList[boneID].parentID
				if parentID!=-1:
					parentName=self.boneList[parentID].name
			if self.boneList[boneID].parentName is not None:
				parentName=self.boneList[boneID].parentName
			if parentName is not None:
				parent=self.armature.edit_bones[parentName.decode()]
				if parentID is not None:
					if parentID!=-1:
						bone.parent=parent
				else:
					bone.parent=parent

			else:
				if self.WARNING==True:
					print('WARNING: no parent for bone',name)
		bpy.ops.object.mode_set(mode='OBJECT')



	def create_bone_position(self):
		bpy.context.view_layer.objects.active = self.object
		bpy.ops.object.mode_set(mode='EDIT')
		for m in range(len(self.boneList)):
			name=self.boneList[m].name
			rotMatrix=self.boneList[m].rotMatrix
			posMatrix=self.boneList[m].posMatrix
			scaleMatrix=self.boneList[m].scaleMatrix
			matrix=self.boneList[m].matrix
			bone = self.armature.edit_bones[name.decode()]
			if matrix:
				if self.ARMATURESPACE==True:
					bone.matrix = matrix.transposed()
					if self.NICE==True:
    						bone.length = self.param
				elif self.BONESPACE==True:
					rotMatrix=matrix.rotationPart()
					posMatrix=matrix.translationPart()
					scalePart=matrix.scalePart()
					if bone.parent:
						bone.head = posMatrix @ bone.parent.matrix + bone.parent.head
						if self.boneList[m].transform not in ["noRotationOrReflection","onlyTranslation"]:
							tempM = rotMatrix @ bone.parent.matrix
							###bone.matrix = tempM
						else:
							tempM = rotMatrix # * bone.parent.matrix
							###bone.matrix = tempM
					else:
						bone.head = posMatrix
						###bone.matrix = rotMatrix
					if self.NICE==True:
						bone.length = self.param
				elif self.INVERTSPACE==True:
					rotMatrix=matrix.rotationPart()
					posMatrix=matrix.translationPart()
					posMatrix=posMatrix @ rotMatrix.invert()
					posMatrix.negate()
					if bone.parent:
						bone.head = posMatrix
						tempM = bone.parent.matrix @ rotMatrix
						###bone.matrix = tempM
					else:
						bone.head = posMatrix
						###bone.matrix = rotMatrix
					if self.NICE==True:
						bone.length = self.param

				else:
					if self.WARNING==True:
						print('ARMATUREPACE or BONESPACE ?')
			elif posMatrix is not None:
				if self.ARMATURESPACE==True:
					if rotMatrix:
						rotMatrix=roundMatrix(rotMatrix,4)
					posMatrix=roundMatrix(posMatrix,4)
					if rotMatrix:
						pass
						###bone.matrix=rotMatrix @ posMatrix
					else:
						pass
						###bone.matrix=posMatrix

					if self.NICE==True:
						bone.length = self.param

				elif self.BONESPACE==True:
					rotMatrix=roundMatrix(rotMatrix,4).rotationPart()
					posMatrix=roundMatrix(posMatrix,4).translationPart()
					if bone.parent:
						bone.head = posMatrix @ bone.parent.matrix + bone.parent.head
						if self.boneList[m].transform not in ["noRotationOrReflection","onlyTranslation"]:
							tempM = rotMatrix @ bone.parent.matrix
							###bone.matrix = tempM
						else:
							tempM = rotMatrix# * bone.parent.matrix
							###bone.matrix = tempM
					else:
						bone.head = posMatrix
						###bone.matrix = rotMatrix
					if self.NICE==True:
						bone.length = self.param
				else:
					if self.WARNING==True:
						print('ARMATUREPACE or BONESPACE ?')
			else:
				if self.WARNING==True:
					print('WARNINIG: rotMatrix or posMatrix or matrix is None')

		bpy.ops.object.mode_set(mode='OBJECT')
		#Blender.Window.RedrawAll()



	def check(self):
		#scn = Blender.Scene.GetCurrent()
		scene = bpy.context.scene
		for object in (obj for obj in scene.objects if (obj.name == self.name and obj.type=='Armature')):
			#if object.type=='Armature':
				#if object.name == self.name:
					scene.objects.unlink(object)
		for object in (obj for obj in scene.objects if (obj.name == self.name and obj.type=='Armature')):
			#if object.type=='Armature':
				#if object.name == self.name:
					self.object = Blender.Object.Get(self.name)
					self.armature = self.object.data
					if self.DEL==True:
						self.armature.makeEditable()
						for bone in self.armature.bones.values():
							del self.armature.bones[bone.name]
						self.armature.update()
		if self.armature==None:
			self.armature = bpy.data.armatures.new(name=self.name)
			#self.object.link(self.armature)
		if self.object==None:
			self.object = bpy.data.objects.new(name=self.name, object_data=self.armature)
		#scn.link(self.object)
		scene.collection.objects.link(self.object)
		self.armature.display_type = 'OCTAHEDRAL'
		self.object.show_in_front = True
		self.object.display_type = 'WIRE'
		self.matrix = self.object.matrix_world


	def check1(self):
		#scn = Blender.Scene.GetCurrent()
		scene = bpy.context.scene
		self.armature = bpy.data.armatures.new(name=self.name)
		self.object = bpy.data.objects.new(name=self.name, object_data=self.armature)
		#scn.link(self.object)
		#self.object.link(self.armature)
		scene.collection.objects.link(self.object)
		self.armature.display_type = 'STICK'
		self.object.show_in_front = True
		self.object.display_type = 'WIRE'




class Node():
	def __init__(self):
		self.name=None
		self.offset=None
		self.children=[]
		self.dataL=''
		self.dataU=''
	def values(self,data):
		lines=data.split('\x0a')
		list={}
		for line in lines:
			lineStrip=line.strip().replace(',',' ')

			if len(lineStrip)>0:
				if ':' in lineStrip:
					lineSplit=line.split(':')
					if '"' in lineSplit[0]:
						key=lineSplit[0].split('"')[1]
						print('key',key)
					if '"' in lineSplit[1]:
						data=lineSplit[1].split('"')[1]
						print('data',data)


