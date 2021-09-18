import bpy
from mathutils import *

"""
			euler = mathutils.Euler()
			RotateEuler(euler,z,'z')
			RotateEuler(euler,x,'x')
			RotateEuler(euler,y,'y')
"""



class ActionBone:
	def	__init__(self):
		self.name=None
		self.posFrameList=[]
		self.rotFrameList=[]
		self.sizeFrameList=[]
		self.posKeyList=[]
		self.rotKeyList=[]
		self.sizeKeyList=[]
		self.matrixFrameList=[]
		self.matrixKeyList=[]
		self.shapeKeyList=[]
		self.shapeFrameList=[]


class Action:
	def __init__(self):
		self.frameCount=None
		self.name='action'
		self.skeleton='armature'
		self.boneList=[]
		self.ARMATURESPACE=False
		self.BONESPACE=False
		self.MIXSPACE=False
		self.FRAMESORT=False
		self.BONESORT=False
		self.UPDATE=True
		self.MS3DSPACE=False
		self.MESHSPACE=False
		self.shapeFrameList=[]
		self.shapeKeyList=[]

	def boneNameList(self):
		if self.skeleton is not None:
			scene = bpy.context.scene
			for object in scene.objects:
				if object.name==self.skeleton:
					self.boneNameList=object.getData().bones.keys()


	def setContext(self,fps=30):
		scn = Blender.Scene.GetCurrent()
		context = scn.getRenderingContext()
		if self.frameCount is not None:
			context.eFrame = self.frameCount
			context.fps = fps


	def shapeAnim(self,mesh,frameCount):
		key=mesh.key
		if not key:
			mesh.insertKey(0, 'relative')
			key= mesh.key

		key.ipo = Blender.Ipo.New('Key',mesh.name)
		ipo = key.ipo
		all_keys = ipo.curveConsts
		for m in range(1,frameCount+2):
			curve = ipo.getCurve(m)
			if curve == None:
				curve = ipo.addCurve(all_keys[m-1])
			curve.append((m-1,1))
			curve.append((m-2,0))
			curve.append((m,0))
			curve.setInterpolation('Linear')
			curve.recalc()


	def draw(self):
		scene = bpy.context.scene
		skeleton=None
		if self.skeleton is not None:
			for object in scene.objects:
				if object.getType()=='Armature':
					if object.name==self.skeleton:
						skeleton = object
		else:
			print('WARNING: no armature')

		if self.MESHSPACE==True:

			try:shapeObject=Blender.Object.Get(self.name)
			except:shapeObject=None
			if shapeObject:
				#try:
					if shapeObject.getType()=='Mesh':
						mesh=shapeObject.getData(mesh=1)
						if mesh:
							print('shape animation'	)
							Blender.Set("curframe",1)
							shapeObject.insertShapeKey()
							for n in range(len(self.shapeFrameList)):
								frame=self.shapeFrameList[n]
								shape=self.shapeKeyList[n]
								Blender.Set("curframe",frame)
								for id in range(len(mesh.verts)):
									mesh.verts[id].co = Vector(shape[id])
								mesh.update()
								#Blender.Window.RedrawAll()
								shapeObject.insertShapeKey()
							#self.shapeAnim(mesh,len(self.shapeFrameList))
							Blender.Set("curframe",1)
						self.frameCount=len(self.shapeFrameList)
				#except:pass




		if skeleton is None:
			scene = bpy.context.scene
			for object in scene.objects.selected:
				if object.type=='Armature':
					skeleton = object
		if skeleton is not None:
			armature=skeleton.getData()
			pose = skeleton.getPose()
			action = Blender.Armature.NLA.NewAction(self.name)
			action.setActive(skeleton)
			scn = Blender.Scene.GetCurrent()
			timeList=[]

			if self.FRAMESORT is True:
				frameList=[]
				for m in range(len(self.boneList)):
					actionbone=self.boneList[m]
					for n in range(len(actionbone.posFrameList)):
						frame=actionbone.posFrameList[n]
						if frame not in frameList:
							frameList.append(frame)
					for n in range(len(actionbone.rotFrameList)):
						frame=actionbone.rotFrameList[n]
						if frame not in frameList:
							frameList.append(frame)
					for n in range(len(actionbone.matrixFrameList)):
						frame=actionbone.matrixFrameList[n]
						if frame not in frameList:
							frameList.append(frame)

				for m in range(len(self.boneList)):
					actionbone=self.boneList[m]
					name=actionbone.name
					pbone=pose.bones[name]
					Blender.Window.RedrawAll()
					if pbone is not None:
						pbone.insertKey(skeleton,1,[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
						pose.update()

				for k in range(len(frameList)):
					frame=sorted(frameList)[k]
					for m in range(len(self.boneList)):
						actionbone=self.boneList[m]
						name=actionbone.name
						pbone=pose.bones[name]
						Blender.Window.RedrawAll()
						if pbone is not None:
							for n in range(len(actionbone.posFrameList)):
								if frame==actionbone.posFrameList[n]:
									timeList.append(frame)
									poskey=actionbone.posKeyList[n]
									bonematrix=poskey#TranslationMatrix(Vector(poskey))#.resize4x4()
									if self.ARMATURESPACE is True:
										pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
									if self.BONESPACE is True:
										if pbone.parent:
											pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
										else:
											pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.LOC],True)
										#if self.UPDATE==True:pose.update()



							for n in range(len(actionbone.rotFrameList)):
								if frame==actionbone.rotFrameList[n]:
									timeList.append(frame)
									rotkey=actionbone.rotKeyList[n]
									bonematrix=rotkey
									if self.ARMATURESPACE is True:
										pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT],True)
										if self.UPDATE==True:pose.update()
									if self.BONESPACE is True:
										if pbone.parent:
											pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
										else:
											pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, frame,\
											[Blender.Object.Pose.ROT],True)
										if self.UPDATE==True:pose.update()

							for n in range(len(actionbone.sizeFrameList)):
								frame=actionbone.sizeFrameList[n]
								timeList.append(frame)
								key=actionbone.sizeKeyList[n]
								if self.ARMATURESPACE is True:
									pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.SIZE],True)
									if self.UPDATE==True:pose.update()
								if self.BONESPACE is True:
									if pbone.parent:pbone.poseMatrix=key*pbone.parent.poseMatrix
									else:pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.SIZE],True)
									if self.UPDATE==True:pose.update()

							for n in range(len(actionbone.matrixFrameList)):
								if frame==actionbone.matrixFrameList[n]:
									timeList.append(frame)
									matrix=actionbone.matrixKeyList[n]
									if self.ARMATURESPACE is True:
										pbone.poseMatrix=matrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
											#[Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
									if self.BONESPACE is True:
										if pbone.parent:
											pbone.poseMatrix=matrix*pbone.parent.poseMatrix
										else:
											pbone.poseMatrix=skeleton.matrixWorld*matrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()

									if self.MIXSPACE is True:
										if pbone.parent:
											pbone.poseMatrix=matrix*pbone.parent.poseMatrix
											pbone.quat=matrix.rotationPart().toQuat()
										else:
											pbone.poseMatrix=skeleton.matrixWorld*matrix
											pbone.quat=matrix.rotationPart().toQuat()
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
											#[Blender.Object.Pose.ROT],True)
										if self.UPDATE==True:pose.update()
					#pose.update()

			elif self.BONESORT is True:



				if self.MS3DSPACE is True:
					boneList=[]
					def boneChildren(parent):
						for child in parent.children:
							boneList.append(child.name)
							boneChildren(child)


					for bone in armature.bones.values():
						if bone.parent is None:
							boneList.append(bone.name)
							boneChildren(bone)

					def getBone(name):
						bone=None
						for actionbone in self.boneList:
							if actionbone.name==name:
								bone=actionbone
								break
						return bone
					for m in range(len(self.boneList)):
					#for name in boneList[::-1]:
					#for name in boneList:
						#actionbone=getBone(name)
						actionbone=self.boneList[m]
						name=actionbone.name
						if actionbone:
							pbone=pose.bones[name]
							#Blender.Window.RedrawAll()
							#print(name)
							if pbone is not None:
								#matrix=armature.bones[name].matrix['ARMATURESPACE']
								#pbone.insertKey(skeleton,0,[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
								#pose.update()

								for n in range(len(actionbone.rotFrameList)):
									frame=actionbone.rotFrameList[n]
									timeList.append(frame)
									rotkey=actionbone.rotKeyList[n]
									quat=rotkey
									pbone.quat=quat
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.ROT],True)
									#pose.update()

								for n in range(len(actionbone.posFrameList)):
									frame=actionbone.posFrameList[n]
									timeList.append(frame)
									poskey=actionbone.posKeyList[n]
									loc=Vector(poskey)
									pbone.loc=loc
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.LOC],True)
					pose.update()


				else:

					for m in range(len(self.boneList)):

						#Blender.Window.DrawProgressBar(i/(float(len(self.boneList))),'wczytuje kosci')
						actionbone=self.boneList[m]
						name=actionbone.name
						Blender.Window.DrawProgressBar(m/(float(len(self.boneList))),name)
						#print(name)
						pbone=pose.bones[name]
						Blender.Window.RedrawAll()
						if pbone is not None:
							pbone.insertKey(skeleton,0,[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC,Blender.Object.Pose.SIZE],True)
							pose.update()
							#update pos
							for n in range(len(actionbone.posFrameList)):
								frame=actionbone.posFrameList[n]
								timeList.append(frame)
								key=actionbone.posKeyList[n]
								if self.ARMATURESPACE is True:
									pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.LOC],True)
									if self.UPDATE==True:pose.update()
								if self.BONESPACE is True:
									if pbone.parent:pbone.poseMatrix=key*pbone.parent.poseMatrix
									else:pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.LOC],True)
									if self.UPDATE==True:pose.update()
							#update rot
							for n in range(len(actionbone.rotFrameList)):
								frame=actionbone.rotFrameList[n]
								timeList.append(frame)
								key=actionbone.rotKeyList[n]
								if self.ARMATURESPACE is True:
									pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.ROT],True)
									if self.UPDATE==True:pose.update()
								if self.BONESPACE is True:
									if pbone.parent:pbone.poseMatrix=key*pbone.parent.poseMatrix
									else:pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.ROT],True)
									if self.UPDATE==True:pose.update()
							#update size
							for n in range(len(actionbone.sizeFrameList)):
								frame=actionbone.sizeFrameList[n]
								timeList.append(frame)
								key=actionbone.sizeKeyList[n]
								if self.ARMATURESPACE is True:
									pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.SIZE],True)
									if self.UPDATE==True:pose.update()
								if self.BONESPACE is True:
									if pbone.parent:pbone.poseMatrix=key#*pbone.parent.poseMatrix
									else:pbone.poseMatrix=key
									pbone.insertKey(skeleton, 1+frame,[Blender.Object.Pose.SIZE],True)
									if self.UPDATE==True:pose.update()


							for n in range(len(actionbone.matrixFrameList)):
								frame=actionbone.matrixFrameList[n]
								timeList.append(frame)
								matrixkey=actionbone.matrixKeyList[n]
								bonematrix=matrixkey
								if self.ARMATURESPACE is True:
									pbone.poseMatrix=bonematrix
									#pbone.poseMatrix=bonematrix
									pbone.insertKey(skeleton, 1+frame,\
										[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
										#[Blender.Object.Pose.ROT],True)
									if self.UPDATE==True:pose.update()
								if self.BONESPACE is True:
									if pbone.parent:
										pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
									else:
										pbone.poseMatrix=bonematrix
									pbone.insertKey(skeleton, frame,\
										[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
									if self.UPDATE==True:pose.update()

								if self.MIXSPACE is True:
									if pbone.parent:
										pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
										pbone.quat=bonematrix.rotationPart().toQuat()
									else:
										pbone.poseMatrix=skeleton.matrixWorld*bonematrix
										pbone.quat=bonematrix.rotationPart().toQuat()
									pbone.insertKey(skeleton, 1+frame,\
										[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
										#[Blender.Object.Pose.ROT],True)
									if self.UPDATE==True:pose.update()



			else:
				print('WARNING: missing BONESORT or FRAMESORT')
			#print(timeList	)
			if len(timeList)>0:
				#print(max(map(int,timeList))	)
				self.frameCount=max(map(int,timeList))
