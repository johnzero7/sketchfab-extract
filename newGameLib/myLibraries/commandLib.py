import bpy
import os
import zipfile

"""

def bf_parser(filename,g):
	cmd=Cmd()
	cmd.inputFile=filename
	cmd.outputFolder='x:\\tintin'
	quickbms.bms='D:\\all\\T\\Tintin\\tintin.bms.txt'
	cmd.command=quickbms
	cmd.run()
"""

blendDir=os.path.dirname(bpy.context.blend_data.filepath)
toolsDir=blendDir+os.sep+"tools"
bmsDir=toolsDir+os.sep+'quickbms'+os.sep+'scripts'

class Command():
	def __init__(self):
		self.input=None
		self.output=None
		self.option=None
		self.exe=None
		self.start=str(0)
		self.bms=None
		self.bmsDir=toolsDir+os.sep+"quickbms"+os.sep+"bms"

offzip=Command()
offzip.option=' -a -z -15'#-1
offzip.exe=toolsDir+os.sep+"Offzip"+os.sep+"offzip.exe"
offzip.start='0'

PNG=Command()
PNG.option=' -out png '
PNG.exe=toolsDir+os.sep+"Nconvert/nconvert.exe"

JPG=Command()
JPG.option=' -out jpeg '
JPG.exe=toolsDir+os.sep+"Nconvert/nconvert.exe"

DDS=Command()
DDS.option=' -out dds '
DDS.exe=toolsDir+os.sep+"Nconvert/nconvert.exe"

zip=Command()
zip.option='x'
zip.exe=toolsDir+os.sep+"7z"+os.sep+"7z.exe"

quickbms=Command()
quickbms.exe=toolsDir+os.sep+"quickbms"+os.sep+"quickbms.exe"

gr2=Command()
gr2.option='-a'
gr2.exe=toolsDir+os.sep+'"Gr2/grnreader98.exe"'

noesis=Command()
noesis.option="?cmode"
noesis.exe=toolsDir+os.sep+"noesis"+os.sep+"noesis.exe"

cd=Command()
cd.exe=blendDir+os.sep+'"tools/CDisplay/CDisplay.exe"'

pdf=Command()
pdf.exe=blendDir+os.sep+'"tools/PdfReader/reader.exe"'

UMODEL=Command()
UMODEL.exe=toolsDir+os.sep+'umodel'+os.sep+'umodel.exe'
UMODEL.option='"-export" "-meshes" "-nostat"'



class Cmd():
	def __init__(self):
		self.input=None
		self.output=None
		self.option=''
		self.exe=''
		self.gr2=False
		self.cd=False
		self.pdf=False
		self.PNG=False
		self.DDS=False
		self.JPG=False
		self.UMODEL=False
		self.QUICKBMS=False
		self.OFFZIP=False
		self.ZIP=False

	def run(self):
		#print('offzip')
		#if self.output is not None:
		#	try:os.mkdir(self.output)
		#	except:pass

		commandline=None
		if self.gr2==True:commandline = gr2.exe+' "'+ self.input +'" '+ gr2.option
		if self.cd==True:commandline = cd.exe+' "'+ self.input+'"'
		if self.pdf==True:commandline = pdf.exe+' "'+ self.input+'"'
		if self.PNG==True:commandline = PNG.exe+PNG.option+' "'+ self.input+'"'
		if self.JPG==True:commandline = JPG.exe+JPG.option+' "'+ self.input+'"'
		if self.DDS==True:commandline = DDS.exe+DDS.option+' "'+ self.input+'"'
		if self.QUICKBMS==True:
			if len(self.bms.split(os.sep))>1:
				commandline = quickbms.exe+' "'+self.bms+'"  "'+self.input+'" "'+self.output+'"'
			else:
				commandline = quickbms.exe+' "'+bmsDir+os.sep+self.bms+'"  "'+self.input+'" "'+self.output+'"'
			print(commandline)

		if self.OFFZIP==True:commandline = offzip.exe+' '+offzip.option+'  "'+self.input+'" "'+self.output+'" "'+offzip.start+'"'
		if self.UMODEL==True:commandline = UMODEL.exe+' '+UMODEL.option+' '+ '-out="'+os.path.dirname(self.input)+'" "'+self.input+'"'
		#if self.ZIP==True:commandline = zip.exe+' '+zip.option+' "'+ self.input+'" -o"'+self.output+'"'
		#if self.ZIP==True:commandline=zip.exe+' '+zip.option+' "'+self.input+'" -o"'+os.path.dirname(self.input)+'"'
		if self.ZIP==True:commandline=zip.exe+' '+zip.option+' "'+self.input+'" -y -o"'+os.path.dirname(self.input)+'"'
		if commandline is not None:os.system(commandline)













