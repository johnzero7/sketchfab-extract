
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
		global offset, string, txt
		if(self.filename is not None):
			file=open(self.filename, 'r')
			self.input=file.read().replace('\x20', '').replace('\x0A', '').replace('&#34;', '"')
			line=self.input
			if(self.log==True):
				txt=open(self.filename+'.ys', 'w')

			if(line is not None and len(line)>0):
				offset=0
				n=0
				string=[]
				if(self.input[offset]=='{'):
					if(self.log==True):
						txt.write('\n')
						txt.write(' '*n+'header:'+str(None))
						txt.write(' { '+str(offset))
						txt.write(' '*(n+4))
				if(self.input[offset]=='['):
					if(self.log==True):
						txt.write('\n')
						txt.write(' '*n+'header:'+str(None))
						txt.write(' [ '+str(offset))
						txt.write(' '*(n+4))
				self.tree(self.root, n)
				if(self.log==True):
					txt.write(' '*n)

			file.close()

		if(self.log==True):
			txt.close()

	def getTree1(self, parent, list, key):
		for child in parent.children:
			if(key in child.header):
				list.append(child)
			self.getTree(child, list, key)


	def getTree(self, parent, list, key):
		if(key in parent.header or key in parent.data):
			list.append(parent)
		for child in parent.children:
			self.getTree(child, list, key)

	def values(self, data: bytes, type_flg: str):
		val_list={}
		#print(f'(\'---===data:\', \'{data}\', \' type_flg:\', \'{type_flg}\')')
		A=data.split(',')
		if(type_flg==':'):
			for a in A:
				if(':' in a):
					c=0
					alist=[]
					string=''
					for b in a:
						if(b=='"' and c==0):
							if(len(string)>0):
								alist.append(string)
							string=''
							string+=b
							c=1
						elif(b=='"' and c==1):
							string+=b
							if(len(string)>0):
								alist.append(string)
							string=''
							c=0
						elif(b==':'):
							pass
						else:
							string+=b
					if(len(string)>0):
						alist.append(string)
					if(len(alist)==2):
						val_list[alist[0]]=alist[1]
					if(len(alist)==1):
						val_list[alist[0]]='None'

					#if(a.count(':')>1):
		if(type_flg=='f'):
			val_list=list(map(float, A))
		if(type_flg=='i'):
			val_list=list(map(int, A))
		if(type_flg=='s'):
			val_list=A
		return val_list

	def getValue(self, values, name:bytes, type:str=None):
		if(name in values):
			if(type=='"f"'):
				return float(values[name].split('"')[1])
			elif(type=='"i"'):
				return int(values[name].split('"')[1])
			elif(type=='i'):
				#print(name, values[name])
				if(values[name]!='None'):
					return int(values[name])
				else:
					return None
			elif(type=='""'):
				return values[name].split('"')[1]
			else:
				return values[name]
		else:
			return None

	def get(self, node, key:str):
		val_list=[]
		self.getTree(node, val_list, key)
		if(len(val_list)>0):
			return val_list
		else:
			return None

	def tree(self, parentNode, n):
		global offset, string
		n+=4
		offset+=1
		while(True):
			if(offset>=len(self.input)):
				break
			value=self.input[offset]
			if(value=='}'):
				if(self.log==True):
					txt.write('\n')
					if(len(string)>0):
						txt.write(' '*n+'data:'+self.input[string[0]:offset])
					else:
						txt.write(' '*n+'data:None')
					txt.write('\n'+' '*n+' } '+str(offset))
				if(len(string)>0):
					parentNode.data=self.input[string[0]:offset]
				string=[]
				offset+=1
				break

			elif(value=='{'):
				if(self.log==True):
					txt.write('\n')
					if(len(string)>0):
						txt.write(' '*n+'header:'+self.input[string[0]:offset])
					else:
						txt.write(' '*n+'header:None')
					txt.write(' { '+str(offset))
					txt.write(' '*(n+4))
				#print(round(100*offset/float(len(self.input)), 3), 'procent')
				node=Node()
				node.parent=parentNode
				parentNode.children.append(node)
				node.offset=offset
				if(len(string)>0):
					node.header=self.input[string[0]:offset]
				string=[]
				self.tree(node, n)
				if(self.log==True):
					txt.write(' '*n)

			elif(value==']'):
				if(len(string)>0):
					parentNode.data=self.input[string[0]:offset]

				if(self.log==True):
					txt.write('\n')
					if(len(string)>0):
						txt.write(' '*n+'data:'+self.input[string[0]:offset]+'\n')
					else:
						txt.write(' '*n+'data:None')
					txt.write(' '*n+' ] '+str(offset))

				offset+=1
				string=[]
				break

			elif(value=='['):
				if(self.log==True):
					txt.write('\n')
					if(len(string)>0):
						txt.write(' '*n+'header:'+self.input[string[0]:offset])
					else:
						txt.write(' '*n+'header:None')
					txt.write(' [ '+str(offset))
					txt.write(' '*(n+4))
				#print(round(100*offset/float(len(self.input)), 3), 'procent')
				node=Node()
				node.parent=parentNode
				parentNode.children.append(node)
				node.offset=offset
				node.name=string
				if(len(string)>0):
					node.header=self.input[string[0]:offset]
				else:
					node.header=''
				string=[]
				self.tree(node, n)
				if(self.log==True):
					txt.write(' '*n)
			else:
				#string+=value
				if(len(string)==0):
					string.append(offset)
				offset+=1
