
class Node:
	def __init__(self, nam):
		self.name = nam;
		self.neighbors = [];

	def addNeighbor(self, other, num):
		self.neighbors.append([other, num]);

	def removeNeighbor(self, other):
		for i in self.neighbors:
			if i.name == other[0].name:
				self.neighbors.pop(i);
				return;

	def hasNeighbor(self, other):
		for i in self.neighbors:
			if i[0].name == other.name:
				return True;
		return False;

	def __repr__(self):
		return self.name + " : " + str([i[0].name for i in self.neighbors]);