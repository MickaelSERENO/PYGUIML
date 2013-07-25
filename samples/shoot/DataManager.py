import xml.etree.ElementTree as ET

class UserData():
	def __init__(self, name, score, classement):
		self.name = name
		self.score = score
		self.classement = classement

class DataManager:
	def __init__(self):
		self._difficult = None
		self._nbLive= 0
		self._continueNb = 0
		self._soundLvl = 0
		self._tree = ET.parse("data.xml")
		self._root = self._tree.getroot()

		self.sortClassement()
		self.updateData()

	def updateData(self):
		self._difficult = self._root[0].find("difficult").attrib['difficult']
		self._soundLvl = int(self._root[0].find("sound").attrib['volume'])
		self._nbLive = int(self._root[0].find("live").attrib['number'])
		self._continueNb = int(self._root[0].find("live").attrib['continue'])

	def addClassement(self, name, score):
		if len(self._root[1]) < 5:
			user = ET.SubElement(root[1], 'user',\
					{'name':name, 'score':str(score)})
			self.sortClassement()
		else:
			classementScore = 0
			i=0
			user = None
			while score <= classementScore or i==0:
				user = root[1][i]
				score = int(user.attrib['score'])
				i+=1
			if score > classementScore:
				user.set('score', str('score'))
				user.set('name', name)
			self._tree.write('dataCopy.xml')

	def getClassement(self):
		classement = list()
		for i, data in enumerate(self._root[1]):
			classement.append(UserData(\
					data.attrib['name'], int(data.attrib['score']), i+1))
		return classement

	def sortClassement(self):
		nameList = list()
		scoreList = list()

		for child in self._root[1]:
			index = len(scoreList)
			for i, score in enumerate(scoreList):
				if int(child.attrib['score']) > int(score):
					index = i
					break
			scoreList.insert(index, int(child.attrib['score']))
			nameList.insert(index, child.attrib['name'])

		for i, child in enumerate(self._root[1]):
			child.set('name', nameList[i])
			child.set('score', str(scoreList[i]))

		self._tree.write('dataCopy.xml')

	def setOption(self, name, attrib, value):
		option = self._root[0].find(name)
		option.set(attrib, str(value))
		self._tree.write("dataCopy.xml")
		self.updateData()
